import datetime
from db import execute, fetchone, fetchall, _is_postgres


def create_analytics_tables():
    """Create analytics tables for tracking user activity and content metrics.
    DDL adapts to Postgres when DATABASE_URL is set, otherwise uses sqlite syntax."""
    if _is_postgres():
        # Postgres DDL
        execute('''
            CREATE TABLE IF NOT EXISTS UserAnalytics (
                analytics_id SERIAL PRIMARY KEY,
                user_id INTEGER,
                total_posts INTEGER DEFAULT 0,
                total_comments INTEGER DEFAULT 0,
                total_likes_given INTEGER DEFAULT 0,
                total_likes_received INTEGER DEFAULT 0,
                total_shares_given INTEGER DEFAULT 0,
                total_shares_received INTEGER DEFAULT 0,
                login_count INTEGER DEFAULT 0,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                account_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                profile_views INTEGER DEFAULT 0
            );
        ''')

        execute('''
            CREATE TABLE IF NOT EXISTS PostAnalytics (
                post_analytics_id SERIAL PRIMARY KEY,
                post_id INTEGER,
                views INTEGER DEFAULT 0,
                unique_views INTEGER DEFAULT 0,
                engagement_rate REAL DEFAULT 0.0,
                reach INTEGER DEFAULT 0,
                impressions INTEGER DEFAULT 0,
                click_through_rate REAL DEFAULT 0.0,
                avg_time_spent REAL DEFAULT 0.0,
                bounce_rate REAL DEFAULT 0.0
            );
        ''')

        execute('''
            CREATE TABLE IF NOT EXISTS DailyAnalytics (
                daily_id SERIAL PRIMARY KEY,
                date DATE DEFAULT CURRENT_DATE,
                total_users INTEGER DEFAULT 0,
                new_users INTEGER DEFAULT 0,
                active_users INTEGER DEFAULT 0,
                total_posts INTEGER DEFAULT 0,
                total_comments INTEGER DEFAULT 0,
                total_likes INTEGER DEFAULT 0,
                total_shares INTEGER DEFAULT 0,
                page_views INTEGER DEFAULT 0,
                unique_visitors INTEGER DEFAULT 0,
                avg_session_duration REAL DEFAULT 0.0
            );
        ''')

        execute('''
            CREATE TABLE IF NOT EXISTS ContentAnalytics (
                content_id SERIAL PRIMARY KEY,
                category TEXT,
                total_posts INTEGER DEFAULT 0,
                total_engagement INTEGER DEFAULT 0,
                avg_likes_per_post REAL DEFAULT 0.0,
                avg_comments_per_post REAL DEFAULT 0.0,
                avg_shares_per_post REAL DEFAULT 0.0,
                top_performing_post_id INTEGER,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        execute('''
            CREATE TABLE IF NOT EXISTS ActivityLog (
                activity_id SERIAL PRIMARY KEY,
                user_id INTEGER,
                activity_type TEXT,
                target_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT,
                ip_address TEXT,
                user_agent TEXT
            );
        ''')

        execute('''
            CREATE TABLE IF NOT EXISTS AdminUsers (
                admin_id SERIAL PRIMARY KEY,
                user_id INTEGER UNIQUE,
                admin_level INTEGER DEFAULT 1,
                granted_by INTEGER,
                granted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_admin_action TIMESTAMP
            );
        ''')

    else:
        # SQLite DDL (legacy)
        execute('''
            CREATE TABLE IF NOT EXISTS UserAnalytics (
                analytics_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                total_posts INTEGER DEFAULT 0,
                total_comments INTEGER DEFAULT 0,
                total_likes_given INTEGER DEFAULT 0,
                total_likes_received INTEGER DEFAULT 0,
                total_shares_given INTEGER DEFAULT 0,
                total_shares_received INTEGER DEFAULT 0,
                login_count INTEGER DEFAULT 0,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                account_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                profile_views INTEGER DEFAULT 0
            );
        ''')

        execute('''
            CREATE TABLE IF NOT EXISTS PostAnalytics (
                post_analytics_id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER,
                views INTEGER DEFAULT 0,
                unique_views INTEGER DEFAULT 0,
                engagement_rate REAL DEFAULT 0.0,
                reach INTEGER DEFAULT 0,
                impressions INTEGER DEFAULT 0,
                click_through_rate REAL DEFAULT 0.0,
                avg_time_spent REAL DEFAULT 0.0,
                bounce_rate REAL DEFAULT 0.0
            );
        ''')

        execute('''
            CREATE TABLE IF NOT EXISTS DailyAnalytics (
                daily_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE DEFAULT CURRENT_DATE,
                total_users INTEGER DEFAULT 0,
                new_users INTEGER DEFAULT 0,
                active_users INTEGER DEFAULT 0,
                total_posts INTEGER DEFAULT 0,
                total_comments INTEGER DEFAULT 0,
                total_likes INTEGER DEFAULT 0,
                total_shares INTEGER DEFAULT 0,
                page_views INTEGER DEFAULT 0,
                unique_visitors INTEGER DEFAULT 0,
                avg_session_duration REAL DEFAULT 0.0
            );
        ''')

        execute('''
            CREATE TABLE IF NOT EXISTS ContentAnalytics (
                content_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                total_posts INTEGER DEFAULT 0,
                total_engagement INTEGER DEFAULT 0,
                avg_likes_per_post REAL DEFAULT 0.0,
                avg_comments_per_post REAL DEFAULT 0.0,
                avg_shares_per_post REAL DEFAULT 0.0,
                top_performing_post_id INTEGER,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        execute('''
            CREATE TABLE IF NOT EXISTS ActivityLog (
                activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                activity_type TEXT,
                target_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT,
                ip_address TEXT,
                user_agent TEXT
            );
        ''')

        execute('''
            CREATE TABLE IF NOT EXISTS AdminUsers (
                admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                admin_level INTEGER DEFAULT 1,
                granted_by INTEGER,
                granted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_admin_action TIMESTAMP
            );
        ''')

    print("Analytics tables created successfully!")


if __name__ == "__main__":
    create_analytics_tables()
    # Tables created. Do not insert sample data — use real production data.