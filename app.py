"""
Compatibility shim for platforms that call `gunicorn app:application`.
This file exposes the Flask app as the symbol `application` so both
`gunicorn application:app` and `gunicorn app:application` work.
"""
try:
    # Import the app object from the main module
    from application import app as application
except Exception:
    # Fallback for relative import layouts
    from .application import app as application

# Export both names so either `app:application` or `app:app` work
app = application

# Exported name is `application` to match some deploy configs
