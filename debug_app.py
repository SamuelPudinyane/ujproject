#!/usr/bin/env python3

from flask import Flask
import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the original app but with better error handling
try:
    from application import app
    
    @app.errorhandler(500)
    def internal_error(error):
        print(f"Internal Server Error: {error}")
        import traceback
        traceback.print_exc()
        return f"Internal Server Error: {str(error)}", 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        print(f"Unhandled Exception: {e}")
        import traceback
        traceback.print_exc()
        return f"Exception: {str(e)}", 500
    
    if __name__ == "__main__":
        print("Starting Flask app with enhanced error handling...")
        app.run(host='localhost', port=9000, debug=True)
        
except Exception as e:
    print(f"Error importing application: {e}")
    import traceback
    traceback.print_exc()