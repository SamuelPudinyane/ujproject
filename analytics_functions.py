import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import sqlite3
from datetime import datetime, timedelta
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
import json

# Use db helper which will choose Postgres when DATABASE_URL is set
from db import fetchall, fetchone, execute, get_connection


def get_analytics_overview():
    """Get overall platform analytics overview"""
    # Get total users
    row = fetchone("SELECT COUNT(*) FROM \"User\"")
    total_users = row[0] if row else 0

    # Get total posts
    row = fetchone("SELECT COUNT(*) FROM \"Post\"")
    total_posts = row[0] if row else 0

    # Get total comments
    row = fetchone("SELECT COUNT(*) FROM \"Comment\"")
    total_comments = row[0] if row else 0

    # Get total likes
    row = fetchone("SELECT COUNT(*) FROM \"Likes\"")
    total_likes = row[0] if row else 0

    # Get total shares
    row = fetchone("SELECT COUNT(*) FROM \"Shares\"")
    total_shares = row[0] if row else 0

    # Get new users this month (best-effort). If we can't determine, return 0.
    new_users_month = 0
    try:
        # try common column name used in DB schemas
        row = fetchone("SELECT COUNT(*) FROM \"User\" WHERE date(account_created) >= date('now','start of month')")
        if row:
            new_users_month = row[0]
        else:
            # try Postgres-style date_trunc if previous query fails or returns None
            row = fetchone("SELECT COUNT(*) FROM \"User\" WHERE account_created >= date_trunc('month', now())")
            if row:
                new_users_month = row[0]
    except Exception:
        try:
            row = fetchone("SELECT COUNT(*) FROM \"User\" WHERE created_at >= date_trunc('month', now())")
            if row:
                new_users_month = row[0]
        except Exception:
            new_users_month = 0

    # active users in last 7 days - best-effort
    try:
        row = fetchone(
            "SELECT COUNT(DISTINCT user_id) FROM (SELECT user_id FROM \"Post\" WHERE post_date >= date('now','-7 days') UNION SELECT user_id FROM \"Comment\" WHERE post_date >= date('now','-7 days'))"
        )
        active_users_week = row[0] if row else 0
    except Exception:
        active_users_week = 0

    engagement_rate = round((total_likes + total_comments + total_shares) / max(total_posts, 1) * 100, 2)

    return {
        'total_users': total_users,
        'total_posts': total_posts,
        'total_comments': total_comments,
        'total_likes': total_likes,
        'total_shares': total_shares,
        'new_users_month': new_users_month,
        'active_users_week': active_users_week,
        'engagement_rate': engagement_rate
    }


def get_daily_analytics(days=7):
    """Get daily analytics for the specified number of days"""
    try:
        daily_data = fetchall(
            """
            SELECT date, total_users, new_users, active_users, total_posts,
                   total_comments, total_likes, total_shares, page_views
            FROM DailyAnalytics
            ORDER BY date DESC
            LIMIT ?
            """,
            (days,)
        )
    except Exception:
        try:
            daily_data = fetchall(
                """
                SELECT date, total_users, new_users, active_users, total_posts,
                       total_comments, total_likes, total_shares, page_views
                FROM DailyAnalytics
                ORDER BY date DESC
                LIMIT %s
                """,
                (days,)
            )
        except Exception:
            daily_data = []

    if not daily_data:
        # No daily analytics rows found — return empty list so caller uses real data when available.
        return []

    return list(reversed(daily_data))


def get_top_posts(limit=5):
    """Get top performing posts by engagement"""
    try:
        return fetchall(
            """
                 SELECT p.title, p.author, p.likes, p.comments, p.shares,
                     (p.likes + p.comments + p.shares) as total_engagement,
                     p.post_date
                 FROM "Post" p
                 ORDER BY total_engagement DESC
                 LIMIT ?
            """,
            (limit,)
        )
    except Exception:
        return fetchall(
            """
                 SELECT p.title, p.author, p.likes, p.comments, p.shares,
                     (p.likes + p.comments + p.shares) as total_engagement,
                     p.post_date
                 FROM "Post" p
                 ORDER BY total_engagement DESC
                 LIMIT %s
            """,
            (limit,)
        )


def get_user_analytics(limit=10):
    """Get top users by activity"""
    try:
        return fetchall(
            """
                 SELECT u.first_name || ' ' || u.last_name as full_name,
                     COUNT(DISTINCT p.postId) as post_count,
                     COUNT(DISTINCT c.commentId) as comment_count,
                     COUNT(DISTINCT l.likeId) as likes_given,
                     u.email
                 FROM "User" u
                 LEFT JOIN "Post" p ON u.userId = p.user_id
                 LEFT JOIN "Comment" c ON u.userId = c.user_id
                 LEFT JOIN "Likes" l ON u.userId = l.user_id
                 GROUP BY u.userId
                 ORDER BY (post_count + comment_count + likes_given) DESC
                 LIMIT ?
            """,
            (limit,)
        )
    except Exception:
        return fetchall(
            """
                 SELECT u.first_name || ' ' || u.last_name as full_name,
                     COUNT(DISTINCT p.postId) as post_count,
                     COUNT(DISTINCT c.commentId) as comment_count,
                     COUNT(DISTINCT l.likeId) as likes_given,
                     u.email
                 FROM "User" u
                 LEFT JOIN "Post" p ON u.userId = p.user_id
                 LEFT JOIN "Comment" c ON u.userId = c.user_id
                 LEFT JOIN "Likes" l ON u.userId = l.user_id
                 GROUP BY u.userId
                 ORDER BY (post_count + comment_count + likes_given) DESC
                 LIMIT %s
            """,
            (limit,)
        )


def get_content_analytics():
    """Get content performance analytics"""
    row = fetchone("SELECT COUNT(*) FROM ContentAnalytics")
    if not row or row[0] == 0:
        return []

    return fetchall(
        """
        SELECT category, total_posts, total_engagement,
               avg_likes_per_post, avg_comments_per_post, avg_shares_per_post
        FROM ContentAnalytics
        ORDER BY total_engagement DESC
        """
    )


def is_admin_user(user_id):
    """Check if user has admin privileges"""
    row = fetchone("SELECT admin_level FROM AdminUsers WHERE user_id = ?", (user_id,))
    return row is not None and row[0] >= 1


def add_admin_user(user_id, admin_level=1, granted_by=None):
    """Add a user as admin"""
    # Try Postgres-style upsert, fallback to sqlite REPLACE
    try:
        execute(
            """
            INSERT INTO AdminUsers (user_id, admin_level, granted_by)
            VALUES (?, ?, ?)
            ON CONFLICT (user_id) DO UPDATE SET admin_level = EXCLUDED.admin_level, granted_by = EXCLUDED.granted_by
            """,
            (user_id, admin_level, granted_by),
        )
    except Exception:
        execute(
            """
            INSERT OR REPLACE INTO AdminUsers (user_id, admin_level, granted_by)
            VALUES (?, ?, ?)
            """,
            (user_id, admin_level, granted_by),
        )


def get_growth_metrics():
    """Get growth metrics for charts"""
    try:
        growth_data = fetchall(
            """
            SELECT date, new_users, total_users
            FROM DailyAnalytics
            ORDER BY date DESC
            LIMIT ?
            """,
            (30,),
        )
    except Exception:
        growth_data = fetchall(
            """
            SELECT date, new_users, total_users
            FROM DailyAnalytics
            ORDER BY date DESC
            LIMIT %s
            """,
            (30,),
        )

    if not growth_data:
        return []

    return list(reversed(growth_data))
