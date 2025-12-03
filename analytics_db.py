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


def insert_sample_analytics_data():
    """Insert sample data for demonstration"""
    sample_daily_data = [
        ('2024-10-25', 150, 12, 89, 45, 123, 567, 234, 1250, 890, 285.5),
        ('2024-10-26', 155, 8, 95, 52, 145, 634, 267, 1356, 945, 312.2),
        ('2024-10-27', 162, 15, 102, 48, 139, 612, 289, 1423, 978, 298.7),
        ('2024-10-28', 168, 11, 98, 61, 167, 698, 312, 1567, 1023, 325.4),
        ('2024-10-29', 175, 9, 105, 55, 154, 665, 298, 1489, 1067, 318.9)
    ]

    for data in sample_daily_data:
        try:
            execute('''
                INSERT INTO DailyAnalytics 
                (date, total_users, new_users, active_users, total_posts, total_comments, 
                 total_likes, total_shares, page_views, unique_visitors, avg_session_duration)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)
        except Exception:
            # try Postgres param style
            execute('''
                INSERT INTO DailyAnalytics 
                (date, total_users, new_users, active_users, total_posts, total_comments, 
                 total_likes, total_shares, page_views, unique_visitors, avg_session_duration)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', data)

    content_categories = [
        ('Technology', 89, 2340, 26.3, 12.4, 8.7),
        ('Lifestyle', 67, 1890, 28.2, 14.1, 6.3),
        ('Education', 45, 1456, 32.4, 18.7, 9.1),
        ('Business', 78, 2156, 27.6, 11.8, 7.9),
        ('Entertainment', 92, 2678, 29.1, 16.3, 12.4)
    ]

    for category, posts, engagement, likes, comments, shares in content_categories:
        try:
            execute('''
                INSERT INTO ContentAnalytics 
                (category, total_posts, total_engagement, avg_likes_per_post, 
                 avg_comments_per_post, avg_shares_per_post)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (category, posts, engagement, likes, comments, shares))
        except Exception:
            execute('''
                INSERT INTO ContentAnalytics 
                (category, total_posts, total_engagement, avg_likes_per_post, 
                 avg_comments_per_post, avg_shares_per_post)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (category, posts, engagement, likes, comments, shares))

    print("Sample analytics data inserted!")


if __name__ == "__main__":
    create_analytics_tables()
    insert_sample_analytics_data()