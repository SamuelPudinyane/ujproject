from flask import Flask,redirect,url_for,render_template,request,jsonify,session,flash
# Robust imports for local modules when running via Flask CLI or direct python
try:
    from user_validation import matchPassword,encryptdata
except ModuleNotFoundError:
    from .user_validation import matchPassword,encryptdata

try:
    from user import (
        updatePassword,sharing,likes_update_table_row,increase_like_count,update_likes_delete,decrease_like_count,user_has_liked_post,loadCommentsandUser,
        loadComments,insert_comment,updateMedia,updateDescription,updateTitle,get_one_post,deletelikes,deletereplies,deletecomments,deleteshare,
        deletepost,get_post,retrieve_media,activeusers,loadPosts,insertUserIntodb,loginCredentials,selectAllfromUser_with_Id,emailExists,
        selectAllfromUser,insertBio,insertOccupation,insertContact,insertAddress,insertPostal,insertInterests,insertImage,insertPost,user_has_liked_post,
        retrievesurvey,survey,get_full_post_content,get_suggestions,load_Posts,delete_profile_picture,insert_share,countPosts,decrease_like_count,insertreplyMessages,
        All_Surveys,insert_customSurvey_answer,scheduled_task,loadfundings,updateFunding,popup_custom_Surveys,deleteCustomSurveyQuestion,custom_Surveys,customSurveys,insert_survey_name,customSurveys,retrieveCustomizedsurvey,deleteSurveyQuestion,increase_like_count,selectAllmessages,insertMessages,selectAllmessages,countPosts,loadPosts
    )
except ModuleNotFoundError:
    from .user import (
        updatePassword,sharing,likes_update_table_row,increase_like_count,update_likes_delete,decrease_like_count,user_has_liked_post,loadCommentsandUser,
        loadComments,insert_comment,updateMedia,updateDescription,updateTitle,get_one_post,deletelikes,deletereplies,deletecomments,deleteshare,
        deletepost,get_post,retrieve_media,activeusers,loadPosts,insertUserIntodb,loginCredentials,selectAllfromUser_with_Id,emailExists,
        selectAllfromUser,insertBio,insertOccupation,insertContact,insertAddress,insertPostal,insertInterests,insertImage,insertPost,user_has_liked_post,
        retrievesurvey,survey,get_full_post_content,get_suggestions,load_Posts,delete_profile_picture,insert_share,countPosts,decrease_like_count,insertreplyMessages,
        All_Surveys,insert_customSurvey_answer,scheduled_task,loadfundings,updateFunding,popup_custom_Surveys,deleteCustomSurveyQuestion,custom_Surveys,customSurveys,insert_survey_name,customSurveys,retrieveCustomizedsurvey,deleteSurveyQuestion,increase_like_count,selectAllmessages,insertMessages,selectAllmessages,countPosts,loadPosts
    )

try:
    from .analytics_functions import (
        get_analytics_overview, get_daily_analytics, get_top_posts,
        get_user_analytics, get_content_analytics, is_admin_user,
        add_admin_user, get_growth_metrics
    )
except ModuleNotFoundError:
    from .analytics_functions import (
        get_analytics_overview, get_daily_analytics, get_top_posts,
        get_user_analytics, get_content_analytics, is_admin_user,
        add_admin_user, get_growth_metrics
    )

# from webscrapping import fetch_and_parse
import base64
import io
try:
    from datafile import data
except ModuleNotFoundError:
    from .datafile import data
from PIL import Image
import cv2
import os
from dotenv import load_dotenv
import datetime
import json
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators
from configparser import ConfigParser
import hashlib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import schedule
from datetime import datetime, timedelta
import threading
from werkzeug.serving import run_simple
import requests
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app=Flask(__name__)
    
app.secret_key="session"

# Configure Flask for proper URL generation
app.config['APPLICATION_ROOT'] = '/'
app.config['PREFERRED_URL_SCHEME'] = 'http'

# Context processor to make admin status available to all templates
@app.context_processor
def inject_admin_status():
    """Make admin status available to all templates"""
    # Check external API role first
    if session.get("data_source") == "external_api":
        admin_status = session.get('role', '').lower() == 'admin'
    else:
        # Fall back to database admin check
        user_id = session.get('user_id')
        if user_id:
            admin_status = is_admin_user(user_id)
        else:
            admin_status = False
    return dict(is_admin=admin_status)

# Function to set user session from master application
def set_user_from_master_app(user_id, email, first_name=None, last_name=None, **kwargs):
    """
    Set user session data from master application
    This function should be called by the master app when user accesses this sub-app
    """
    session["user_id"] = user_id
    session["email"] = email
    if first_name:
        session["first_name"] = first_name
    if last_name:
        session["last_name"] = last_name
    
    # Store additional user data passed from master app
    for key, value in kwargs.items():
        session[f"master_app_{key}"] = value

# Route for master application to set user session
@app.route('/set_user_session', methods=['POST'])
def set_user_session():
    """
    Endpoint for master application to set user session
    Expected JSON: {
        "user_id": int,
        "email": string,
        "first_name": string,
        "last_name": string,
        ...other user data
    }
    """
    try:
        data = request.get_json()
        if not data or 'user_id' not in data:
            return jsonify({"error": "Invalid user data"}), 400
        
        set_user_from_master_app(**data)
        return jsonify({"success": True, "message": "User session set successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# External API Configuration
EXTERNAL_API_BASE_URL = "http://localhost:5000"  # Replace with your actual external API URL

def fetch_user_from_external_api(user_id):
    """
    Fetch user data from external API
    """
    try:
        # Make request to your external API
        response = requests.get(
            f"{EXTERNAL_API_BASE_URL}/stem-app-route/{user_id}",
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"Successfully fetched user data from external API for user_id: {user_id}")
            return user_data
        else:
            print(f"External API error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user from external API: {e}")
        return None

def store_external_user_in_session(user_data):
    """
    Store external user data in Flask session
    """
    try:
        # Store core user information in session
        session["user_id"] = user_data.get("user_id", 1)
        session["email"] = user_data.get("email", "")
        session["first_name"] = user_data.get("first_name", "")
        session["last_name"] = user_data.get("last_name", "")
        session["bio"] = user_data.get("bio", "")
        session["avatar"] = user_data.get("avatar", "")
        session["role"] = user_data.get("role", "user")
        session["address"] = user_data.get("address", "")
        session["occupation"] = user_data.get("occupation", "")
        session["contact_number"] = user_data.get("contact_number", "")
        session["date_of_birth"] = user_data.get("date_of_birth", "")
        session["gender"] = user_data.get("gender", "")
        session["postal_code"] = user_data.get("postal_code", "")
        session["active"] = user_data.get("active", True)
        session["verified"] = user_data.get("verified", False)
        
        # Store any additional fields
        session["external_user_data"] = user_data
        session["data_source"] = "external_api"
        
        print(f"Stored external user data in session for user_id: {session['user_id']}")
        return True
        
    except Exception as e:
        print(f"Error storing external user data in session: {e}")
        return False

def get_user_profile_from_session():
    """
    Get formatted user profile data from session for templates
    """
    if session.get("data_source") == "external_api":
        return {
            'userId': session.get('user_id', 1),
            'user_id': session.get('user_id', 1),
            'first_name': session.get('first_name', 'Guest'),
            'last_name': session.get('last_name', 'User'),
            'email': session.get('email', 'guest@example.com'),
            'bio': session.get('bio', 'Welcome to the app'),
            'images': session.get('avatar', None),  # Use avatar as profile image
            'avatar': session.get('avatar', None),
            'role': session.get('role', 'user'),
            'address': session.get('address', ''),
            'occupation': session.get('occupation', 'User'),  # Use actual occupation field
            'gender': session.get('gender', 'Other'),
            'contact_number': session.get('contact_number', ''),
            'date_of_birth': session.get('date_of_birth', ''),
            'postal_code': session.get('postal_code', ''),
            'active': session.get('active', True),
            'verified': session.get('verified', False)
        }
    else:
        # Return default/fallback user data
        return {
            'userId': session.get('user_id', 1),
            'user_id': session.get('user_id', 1),
            'first_name': 'Guest',
            'last_name': 'User',
            'email': 'guest@example.com',
            'bio': 'Welcome to the app',
            'images': None,
            'occupation': 'Guest User',
            'gender': 'Other'
        }

@app.route('/fetch_external_user/<string:user_id>')
def fetch_external_user(user_id):
    """
    Endpoint to fetch user data from external API and store in session
    """
    try:
        # Fetch user data from external API
        user_data = fetch_user_from_external_api(user_id)
        
        if not user_data:
            return jsonify({
                "error": "Failed to fetch user data from external API",
                "fallback": True
            }), 404
        
        # Store user data in session
        if store_external_user_in_session(user_data):
            return jsonify({
                "success": True,
                "message": "User data fetched and stored successfully",
                "user_data": get_user_profile_from_session()
            }), 200
        else:
            return jsonify({
                "error": "Failed to store user data in session"
            }), 500
            
    except Exception as e:
        print(f"Error in fetch_external_user endpoint: {e}")
        return jsonify({
            "error": str(e),
            "fallback": True
        }), 500

# Route to handle encrypted user token from master application
@app.route('/auth_user/<path:encrypted_token>')
def auth_user(encrypted_token):
    """
    Endpoint to handle encrypted user tokens from master application
    This receives the encrypted token and sets up the user session
    """
    try:
        # Store the encrypted token in session
        session['master_user_token'] = encrypted_token
        
        
        print(f"Authenticated user with token: {encrypted_token[:50]}...")  # Log first 50 chars for security
        
        # Redirect to posts page
        return redirect(url_for("post"))
        
    except Exception as e:
        print(f"Authentication error: {e}")
        return jsonify({"error": "Authentication failed"}), 400

# CSRF protection disabled for sub-application
# Security is handled by the master application
# csrf = CSRFProtect(app)
load_dotenv()
# Load email configuration from config.cfg
config = ConfigParser()
config.read('config.cfg')

# Configure Flask-Mail
app.config['MAIL_SERVER'] = config['EMAIL']['MAIL_SERVER']
app.config['MAIL_PORT'] = config['EMAIL']['MAIL_PORT']
app.config['MAIL_USE_TLS'] = config.getboolean('EMAIL', 'MAIL_USE_TLS')
app.config['MAIL_USE_SSL'] = config.getboolean('EMAIL', 'MAIL_USE_SSL')

app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') 
mail = Mail(app)

comment_list=[]
comments={}
# import socket
# socket.getaddrinfo('127.0.0.1', 8000)
# port = int(os.environ.get('FLASK_RUN_PORT', 8000))

@app.route("/",methods=["POST","GET"])
def homePage():
    # Run updateFunding in the background to avoid blocking the redirect
    def background_update():
        try:
            updateFunding(data)
        except Exception as e:
            print(f"Background funding update error: {e}")
    
    # Start the background thread
    thread = threading.Thread(target=background_update)
    thread.daemon = True  # Thread will close when main program closes
    thread.start()
    
    # Handle user parameter from master application
    user_param = request.args.get('user')
    session['user_id'] = user_param
    if user_param:
        # Try to fetch user data from external API
        user_data = fetch_user_from_external_api(user_param)
       
        if user_data:
            # Store external user data in session
            store_external_user_in_session(user_data)
            print(f"Fetched and stored external user data for user_id: {user_param}")
        else:
            # Fallback to basic session data
            session['master_user_token'] = user_param
            session['user_id'] = user_param
            print(f"External API unavailable, using fallback session for user_id: {user_param}")
    
    # Since this is a sub-application, redirect directly to posts
    return redirect(url_for("post")) 

   
@app.route("/deleteProfile_picture",methods=["POST","GET"])
def deleteProfile_picture():
    userId=session["user_id"]
    
    image=delete_profile_picture(userId)
    delete_profile_picture_from_file(image)
    return redirect(url_for("post"))
    
@app.route("/funds",methods=["POST","GET"])
def funds():
    # Handle user parameter from master application
    user_param = request.args.get('user')
    if user_param:
        # Try to fetch fresh user data from external API if not already in session
        if session.get('user_id') != user_param or session.get('data_source') != 'external_api':
            user_data = fetch_user_from_external_api(user_param)
            if user_data:
                store_external_user_in_session(user_data)
            else:
                session['user_id'] = user_param
    
    # Ensure user session exists
    if 'user_id' not in session:
        session["user_id"] = 1  # Fallback user ID
    
  
    funds = loadfundings()
    return render_template("funds.html", funds=funds)


@app.route('/save_data', methods=['GET','POST'])
def api_save_data():
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    try:
        
        updateFunding(data)
        print(data)
        return jsonify({"message": "Data saved successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
  
    
@app.route("/post")
def post():

    # Handle user parameter from master application
    user_param = request.args.get('user')

    
    if user_param:
        session['user_id'] = user_param
        # Try to fetch fresh user data from external API if not already in session
        if session.get('user_id') != user_param or session.get('data_source') != 'external_api':
            user_data = fetch_user_from_external_api(user_param)
            
            if user_data:
                store_external_user_in_session(user_data)
                print(f"Refreshed external user data for user_id: {user_param}")
            else:
                # Fallback to basic session data
                session['user_id'] = user_param
                session['master_user_token'] = user_param
                print(f"External API unavailable, using fallback session for user_id: {user_param}")
    
    # For sub-application: Create a default user session if not exists
    if 'user_id' not in session:
        session["user_id"] = 1  # Fallback user ID
        session["email"] = "default@example.com"  # Default email
    
    counts=countPosts()
    
    # Get pagination parameters
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit
    
    post=load_Posts(offset=offset, limit=limit)
    if "message" not in post:
        for item in post:
            if "media" in item and item['media']:
                try:
                    # Parse the media string from database
                    media_string = item['media']
                    if media_string.startswith('[') and media_string.endswith(']'):
                        # Remove brackets and split by comma
                        media_list = media_string[1:-1].split(', ')
                        # Clean up quotes and escape characters
                        cleaned_media = []
                        for media_item in media_list:
                            # Remove quotes and fix path separators
                            clean_item = media_item.strip('"').replace('\\\\', '/')
                            # Ensure the path starts with static/
                            if not clean_item.startswith('static/'):
                                clean_item = clean_item
                            cleaned_media.append(clean_item)
                        item['media'] = cleaned_media
                    else:
                        item['media'] = []
                except Exception as e:
                    print(f"Error processing media for post {item.get('postId', 'unknown')}: {e}")
                    item['media'] = []
            else:
                item['media'] = []
    
   
    
    userId=session["user_id"]
    
    # Get user data from session (external API or fallback)
    userdata = get_user_profile_from_session()
    
    # If external API data is available, use it; otherwise try database fallback
    if session.get('data_source') != 'external_api':
        try:
            db_userdata = selectAllfromUser_with_Id(userId)
            if db_userdata:
                # Use database data if available
                userdata = db_userdata
            # If no database user exists, the fallback userdata from get_user_profile_from_session is used
        except Exception as e:
            print(f"Error getting user data from database: {e}")
            # Continue with fallback userdata from session
    
    # Safely get profile image
    if isinstance(userdata, dict):
        profileimage = userdata.get('images', None)
    else:
        profileimage = getattr(userdata, 'images', None) if userdata else None
    # If the client requests JSON (for infinite scroll), return paginated data
    wants_json = request.args.get('format') == 'json' or 'application/json' in request.headers.get('Accept', '')
    if wants_json:
        return jsonify({
            "page": page,
            "limit": limit,
            "hasMore": len(post) == limit,
            "posts": post,
            "user": userdata if isinstance(userdata, dict) else getattr(userdata, '__dict__', {})
        })

    return render_template("post.html",post=post,counts=counts,user=userdata,profileimage=profileimage)

    
@app.route("/loadposts/<string:name>",methods=["GET"])
def loadposts(name):
    posts=loadPosts(name)
    userId=session["user_id"]
    userdata=selectAllfromUser_with_Id(userId)
    profileimage = userdata['images']
    media=[]
    
    if "message" not in posts:
        for item in posts:
            if "media" in item and item['media']:
                try:
                    # Parse the media string from database
                    media_string = item['media']
                    if media_string.startswith('[') and media_string.endswith(']'):
                        # Remove brackets and split by comma
                        media_list = media_string[1:-1].split(', ')
                        # Clean up quotes and escape characters
                        cleaned_media = []
                        for media_item in media_list:
                            # Remove quotes and fix path separators
                            clean_item = media_item.strip('"').replace('\\\\', '/')
                            cleaned_media.append(clean_item)
                        item['media'] = cleaned_media
                    else:
                        item['media'] = []
                except Exception as e:
                    print(f"Error processing media for post {item.get('postId', 'unknown')}: {e}")
                    item['media'] = []
            else:
                item['media'] = []
                    
        return render_template("postcontent.html",post=posts,user=userdata,profileimage=profileimage)
    else:
        return redirect(url_for("post"))


@app.route('/get_full_post', methods=['GET'])
def get_full_post():
    column = request.args.get('column')
    value = request.args.get('value')
    post_content = get_full_post_content(column, value)
    return jsonify(post_content)



@app.route("/loadmessages")
def loadmessages():
    # Handle user parameter from master application
    user_param = request.args.get('user')
    if user_param:
        session['user_id'] = user_param
    
    # For sub-application: Ensure user session exists
    if 'user_id' not in session:
        session["user_id"] = 1  # Fallback user ID from master app
        session["email"] = "guest@example.com"
    
    try:
        userId = session["user_id"]
        messages = selectAllmessages(userId)
        
        # Provide sender_id for the template
        sender_id = userId
        
        return render_template("inbox.html", messages=messages, sender_id=sender_id)
    except Exception as e:
        print(f"Error loading messages: {e}")
        # Return to post page if there's an error
        flash(f"Error loading messages: {str(e)}")
        return redirect(url_for("post"))
    

# Ensure analytics tables exist at startup (real data storage)
try:
    from analytics_db import create_analytics_tables
    create_analytics_tables()
    print("Analytics tables verified/created.")
except Exception as e:
    print(f"Failed to initialize analytics tables: {e}")

# Admin route removed - not functional in this sub-application
# @app.route("/admin")
# def admin():
#     return render_template("admin.html")

@app.route('/analytics')
def analytics():
    """Analytics dashboard - admin access only"""
    
    user_id = session.get('user_id')
    print(f"Analytics access attempt by user_id: {user_id}")
    
    # Check if user has admin privileges (prioritize external API role)
    if session.get("data_source") == "external_api":
        admin_status = session.get('role', '').lower() == 'admin'
        print(f"External API admin status for user {user_id}: {admin_status}")
    else:
        admin_status = is_admin_user(user_id)
        print(f"Database admin status for user {user_id}: {admin_status}")
    
    if not admin_status:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('post'))
    
    try:
        # Get real analytics data from database
        print("DEBUG: Fetching real analytics data from database...")

        analytics_overview = {}
        daily_analytics = []
        top_posts = []
        top_users = []
        content_analytics = []

        # Fetch each dataset with isolated error handling
        try:
            analytics_overview = get_analytics_overview() or {}
            print(f"DEBUG: Got analytics overview: {analytics_overview}")
        except Exception as e:
            print(f"ERROR fetching analytics overview: {e}")

        try:
            daily_analytics = get_daily_analytics() or []
            print(f"DEBUG: Got daily analytics: {daily_analytics}")
        except Exception as e:
            print(f"ERROR fetching daily analytics: {e}")

        try:
            top_posts = get_top_posts() or []
            print(f"DEBUG: Got top posts: {top_posts}")
        except Exception as e:
            print(f"ERROR fetching top posts: {e}")

        try:
            top_users = get_user_analytics() or []
            print(f"DEBUG: Got top users: {top_users}")
        except Exception as e:
            print(f"ERROR fetching top users: {e}")

        try:
            content_analytics = get_content_analytics() or []
            print(f"DEBUG: Got content analytics: {content_analytics}")
        except Exception as e:
            print(f"ERROR fetching content analytics: {e}")

        print("DEBUG: Real database data fetched successfully")

    except Exception as e:
        print(f"Unexpected error fetching analytics data: {e}")
        flash('An error occurred while fetching analytics data.', 'error')
        return redirect(url_for('post'))


    # Helper to make objects JSON-safe without changing tuple/list string content
    def clean_for_json(obj):
        if obj is None:
            return None
        if isinstance(obj, dict):
            return {k: clean_for_json(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [clean_for_json(item) for item in obj]
        if isinstance(obj, (int, float, bool, str)):
            return obj
        try:
            return str(obj)
        except Exception:
            return None

    # Clean and serialize daily analytics for use in charts (JSON)
    try:
        cleaned_daily = clean_for_json(daily_analytics)
        daily_analytics_json = json.dumps(cleaned_daily)
    except Exception as e:
        print(f"ERROR cleaning/serializing daily_analytics: {e}")
        daily_analytics_json = "[]"

    # For template rendering, pass tuples/lists directly (they render fine in Jinja)
    return render_template(
        'analytics.html',
        analytics_overview=analytics_overview,
        daily_analytics=daily_analytics_json,
        top_posts=top_posts,
        top_users=top_users,
        content_analytics=content_analytics,
        user_analytics=top_users
    )

    
@app.route('/analytics/migrate', methods=['POST','GET'])
def analytics_migrate():
    """Run migration to create/update analytics database tables."""
    user_id = session.get('user_id')
    try:
        # Require admin privileges to run migration
        if session.get("data_source") == "external_api":
            admin_status = session.get('role', '').lower() == 'admin'
        else:
            admin_status = is_admin_user(user_id)
        if not admin_status:
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('post'))

        from analytics_db import create_analytics_tables
        create_analytics_tables()
        flash('Analytics tables migration completed successfully.', 'success')
        return redirect(url_for('analytics'))
    except Exception as e:
        print(f"Analytics migration failed: {e}")
        flash(f'Analytics migration failed: {e}', 'error')
        return redirect(url_for('analytics'))

@app.route('/home')
def home():
    survey=popup_custom_Surveys()
    print("survey ",survey)
    for item in survey:
        survey=item['questions']
        survey=json.loads(survey)
    return render_template('survey.html',customSurveys=survey)

@app.route('/api/create-question', methods=['POST'])
def create_question():
    # Get form data from POST request
    question = request.form.get('question')
    question_type = request.form.get('questionType')
    choices = request.form.get('choices')
    custom_answer = request.form.get('customAnswer')
    # Validate inputs
    if not question or not question_type:
        return jsonify({'error': 'Question and Question Type are required'}), 400

    # Handle choices based on question type
    if question_type == 'custom':
        survey(question,question_type,json.dumps(choices),custom_answer)
        choices = None
    elif question_type == 'single':
        if ',' not in custom_answer:
            if not choices:
                return jsonify({'error': 'Choices are required for single or multiple choice questions'}), 400
            choices=choices.split(',')
            if len(choices)==2:
                survey(question,question_type,json.dumps(choices),custom_answer)
                custom_answer = None
            
    elif question_type == 'multiple':
        if ',' not in custom_answer:
            if not choices:
                return jsonify({'error': 'Choices are required for single or multiple choice questions'}), 400
            choices=choices.split(',')
            survey(question,question_type,json.dumps(choices),custom_answer)
            custom_answer = None
    return redirect(url_for('admin'))

@app.route("/deletesurveyquestion/<int:id>")
def deletesurveyquestion(id):
    deleteSurveyQuestion(id)
    
    return redirect(url_for('surveyQuestions'))


@app.route("/answers/<int:id>")
def answers(id):
    answers=All_Surveys(id)
    print(answers)
    for item in answers:
        
        item['answer']=json.loads(item['answer'])
        print(type(item['answer']))
    print(answers)
    return render_template('answers.html',customSurveys=answers)
   

@app.route('/submit_survey/<int:id>', methods=['POST'])
def submit_survey(id):
    # Initialize responses dictionary to store form data
    responses = {}
    userId=session["user_id"]
    id=id
    # Process the form data
    for key, value in request.form.items():
        if key.startswith('choices_'):
            # For radio buttons (single choice questions)
            question_id = key.split('_')[1]
            responses[question_id] = value
        elif key.startswith('checkedbox_'):
            # For checkboxes (multiple choice questions)
            question_id = key.split('_')[1]
            if question_id not in responses:
                question_id = key.split('_')[1]
                responses[question_id] = request.form.getlist(key)
            else:
                responses[question_id].extend(request.form.getlist(key))
        elif key.startswith('opinion_'):
            # For text inputs (opinion questions)
            question_id = key.split('_')[1]
            responses[question_id] = value
    insert_customSurvey_answer(id,userId,json.dumps(responses))
    # Redirect to a 'Thank You' page or another route after processing
    return redirect('http://127.0.0.1:5000/home')


    
@app.route('/thank_you')
def thank_you():
    return "Thank you for submitting the survey!"



@app.route("/surveyQuestions")
def surveyQuestions():
    questions=retrievesurvey()
    if 'message' in questions:
        return redirect(url_for('admin'))
    else:
        survey=customSurveys()
        print(survey)
        return render_template('surveyquestions.html',questions=questions,survey=survey)
        
@app.route('/submit_customized_survey', methods=['POST'])
def submit_customized_survey():
    if request.method == 'POST':
        checked_ids = request.form.get('checked_ids')
        surveyName=request.form.get('surveyName')
        if checked_ids:
            
            checked_ids_list = checked_ids.split(',')
            checked_ids_list=retrieveCustomizedsurvey(checked_ids_list)
            choice_s=[]
            
            for item in checked_ids_list:
                if "choices" in item:
                    choice=item['choices'][1:-1].split(', ')
                    choice=[s.strip('"') for s in choice]
                    choice_s.append(choice)
                    for choice in choice_s:
                        item['choices']=choice
            # Redirect or render another template as needed
            insert_survey_name(surveyName,json.dumps(checked_ids_list))
            return redirect(url_for('surveyQuestions'))
        else:
            # Handle case where no checkboxes were checked
            print('No checkboxes were checked')
            # Redirect or render another template as needed
        
        # Example: Redirect back to the survey page
    return redirect(url_for('surveyQuestions'))


@app.route('/customized_survey/<string:surveyName>')
def customized_survey(surveyName):
    customSurveys=custom_Surveys(surveyName)
    questions_list = [item for item in customSurveys]

    print(type(questions_list))
    for item in questions_list:
        questions_list=item['questions']
        questions_list=json.loads(questions_list)
    return render_template('survey.html',customSurveys=questions_list)


@app.route('/delete_customized_survey/<int:id>')
def delete_customized_survey(id):
    deleteCustomSurveyQuestion(id)
    return redirect(url_for('surveyQuestions'))



@app.route("/selectedUserProfile/<int:user_id>", methods=["GET", "POST"])
def selectedUserProfile(user_id):
    try:
        # For sub-application: Ensure user session exists
        if 'user_id' not in session:
            session["user_id"] = 1  # Default user ID from master app
            session["email"] = "guest@example.com"
        
        # Get the target user data
        user = selectAllfromUser_with_Id(user_id)
        print("Selected user data: ", user)
        if not user:
            flash(f"User with ID {user_id} not found")
            return redirect(url_for("post"))
        
        # Get current user (sender) data
        sender_id = session.get("user_id")
        print(f"Sender ID from session: {sender_id}")
        
        # Always ensure we have a sender_id for the sub-application
        if not sender_id:
            sender_id = 1  # Default sender ID
            session["user_id"] = sender_id
            print("Set default sender_id to 1")
        
        # Get sender data, try external API first, then database, then default
        sender_data = None
        if session.get('data_source') == 'external_api':
            sender_data = get_user_profile_from_session()
        else:
            try:
                sender_data = selectAllfromUser_with_Id(sender_id)
            except Exception as e:
                print(f"Error getting sender data from database: {e}")
        
        if not sender_data:
            # Create default sender data if not found
            sender_data = {
                'userId': sender_id,
                'first_name': 'Guest',
                'last_name': 'User',
                'email': 'guest@example.com',
                'images': None
            }
        print(f"Final sender data: {sender_data}")
        
        reply_to = request.args.get("reply_to")
        print(f"About to render selectedUserProfile template for user_id: {user_id}")
        
        if request.method == "POST":
            message = request.form.get("message")
            
            if not message:
                flash("Message cannot be empty")
                return redirect(url_for("selectedUserProfile", user_id=user_id))
            
            try:
                if reply_to:  # Check if it's a reply
                    insertreplyMessages(sender_id, user_id, message, reply_to)
                else:
                    insertMessages(sender_id, user_id, message)
                flash("Message sent successfully")
            except Exception as e:
                print(f"Error sending message: {e}")
                flash(f"Error sending message: {str(e)}")
            
            return redirect(url_for("post"))
        
        return render_template("selectedUserProfile.html", sender_id=sender_id, user=user, sender_data=sender_data)
        
    except Exception as e:
        print(f"Error in selectedUserProfile: {e}")
        flash(f"Error loading user profile: {str(e)}")
        return redirect(url_for("post"))



# Note: Login/Logout routes removed since this is a sub-application
# Authentication is handled by the master application

@app.route("/clear_session")
def clear_session():
    """Route for master application to clear session when user logs out"""
    session.clear()
    return jsonify({"success": True, "message": "Session cleared"})

@app.route("/api/app_info")
def app_info():
    """Endpoint for master application to get sub-app information"""
    return jsonify({
        "app_name": "Social Media Sub-Application",
        "version": "1.0.0",
        "status": "active",
        "features": [
            "Post creation and viewing",
            "Social media sharing",
            "User messaging",
            "Funding information",
            "Survey system"
        ],
        "endpoints": {
            "set_user_session": "/set_user_session",
            "clear_session": "/clear_session",
            "main_app": "/post"
        }
    })

@app.route("/api/health")
def health_check():
    """Health check endpoint for master application"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "session_active": 'user_id' in session
    })

@app.route('/debug_session')
def debug_session():
    """Debug route to test user session handling"""
    try:
        # Check user parameter from request
        user_param = request.args.get('user')
        
        # Check current session
        session_user_id = session.get('user_id', 'None')
        master_token = session.get('master_user_token', 'None')
        
        debug_info = {
            'request_user_param': user_param,
            'session_user_id': session_user_id,
            'master_user_token': master_token,
            'all_session_keys': list(session.keys()),
            'session_data': dict(session)
        }
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({'error': str(e), 'type': type(e).__name__})


# Note: Account creation handled by master application
# This route is kept for potential internal user profile updates

@app.route("/updateUserProfile",methods=["POST",'GET'])
def updateUserProfile():
    """Route to update user profile information within the sub-application"""
    if 'user_id' not in session:
        session["user_id"] = 1  # Default user ID from master app
        session["email"] = "guest@example.com"
    
    if request.method=='POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        occupation = request.form.get('occupation')
        bio = request.form.get('bio')
        contact = request.form.get('contact')
        address = request.form.get('address')
        postalCode = request.form.get('postalCode')
        
        userId = session["user_id"]
        
        # Update user information (without password changes)
        if firstName:
            # Update first name (you'd need to implement this function)
            pass
        if lastName:
            # Update last name (you'd need to implement this function)
            pass
        if occupation:
            insertOccupation(userId, occupation)
        if bio:
            insertBio(userId, bio)
        if contact:
            insertContact(userId, contact)
        if address:
            insertAddress(userId, address)
        if postalCode:
            insertPostal(userId, postalCode)
            
        flash('Profile updated successfully!')
        return redirect(url_for('post'))
    else:
        return redirect(url_for('post'))  # Redirect to posts instead of showing create account form




@app.route('/createNewPost', methods=["POST", "GET"])
def createNewPost():
    # Handle user parameter from master application
    user_param = request.args.get('user')
    if user_param:
        session['user_id'] = user_param
    
    # For sub-application: Ensure user session exists
    if 'user_id' not in session:
        session["user_id"] = 1  # Default user ID from master app
        session["email"] = "guest@example.com"

    if request.method == "POST":
        userId = session['user_id']
        title = request.form.get('title')
        description = request.form.get('description')
        media = request.files.getlist('media[]')
        file_list= create_upload_folder(media)
        insertPost(userId, title, description, file_list)
        return redirect(url_for('post'))  # Redirect to the post page after creating the post
    
    return render_template('add_post.html')


@app.route('/userProfile',methods=["POST","GET"])
def userProfile():
    try:
        # For sub-application: Ensure user session exists
        if 'user_id' not in session:
            session["user_id"] = 1  # Default user ID from master app
            session["email"] = "guest@example.com"
        
        userId = session["user_id"]
        
        # Get user data from session (external API or fallback)
        userdata = get_user_profile_from_session()
      
        # If external API data is not available, try database fallback
        if session.get('data_source') != 'external_api':
            try:
                db_userdata = selectAllfromUser_with_Id(userId)
                if db_userdata:
                    userdata = db_userdata
            except Exception as e:
                print(f"Error getting user data from database in userProfile: {e}")
        
        # Use userdata as user for consistency
        user = userdata
        
        # Get user posts
        userPosts = get_post(userId)
        
        if request.method == 'POST':
            return render_template('post.html', user=user)
        else:
            media = []
            
            if userPosts is not None:
                for item in userPosts:
                    if 'media' in item and item['media']:
                        try:
                            # Parse the media string from database
                            media_string = item['media']
                            if media_string.startswith('[') and media_string.endswith(']'):
                                # Remove brackets and split by comma
                                media_list = media_string[1:-1].split(', ')
                                # Clean up quotes and escape characters
                                cleaned_media = []
                                for media_item in media_list:
                                    # Remove quotes and fix path separators
                                    clean_item = media_item.strip('"').replace('\\\\', '/')
                                    cleaned_media.append(clean_item)
                                item['media'] = cleaned_media
                            else:
                                item['media'] = []
                        except Exception as e:
                            print(f"Error processing media for post: {e}")
                            item['media'] = []
                    else:
                        item['media'] = []
            
        return render_template('userProfile.html', userPosts=userPosts, userdata=userdata, user=user)
        
    except Exception as e:
        print(f"Error in userProfile route: {e}")
        flash(f"Error loading user profile: {str(e)}")
        return redirect(url_for("post"))

@app.route('/updatePost/<int:postid>',methods=["POST","GET"])

def updatePost(postid):
    Post=get_one_post(postid)
    if request.method=='POST':
        media=[]
        for item in Post:
            images=item['media'][1:-1].split(', ')
            images=[s.strip('"') for s in images]
            media.append(images)
            for picture_list in media:
                item['media']=picture_list
    return render_template('editPost.html',Post=Post)


@app.route('/editOldPost/<int:postid>', methods=["POST", "GET"])
def editOldPost(postid):
    # For sub-application: Ensure user session exists
    if 'user_id' not in session:
        session["user_id"] = 1  # Default user ID from master app
        session["email"] = "guest@example.com"

    if request.method == "POST":
        userId = session['user_id']
        title = request.form.get('title')
        description = request.form.get('description')
        media = request.files.getlist('media[]')
        
        file= create_upload_folder(media)
        if title:
            updateTitle(postid,title)
        if description:
            updateDescription(postid,description)
        if file:
            updateMedia(postid,file)

        flash('Post updated successfully.')
        return redirect(url_for('post'))  # Redirect to the post page after creating the post
    
    return render_template('add_post.html')


@app.route('/deletePost/<int:postid>',methods=["POST","GET"])

def deletePost(postid):
    userId=session["user_id"]
    userPosts=get_post(userId)
    if request.method=='POST':
        deletepost(userId,postid)
        deleteshare(postid)
        deletecomments(postid)
        deletereplies(postid)
        deletelikes(postid)
        return redirect(url_for('post'))
    
    # Get user data for the template
    userdata = selectAllfromUser_with_Id(userId)
    user = selectAllfromUser_with_Id(userId)
    return render_template('add_post.html',userPosts=userPosts,data=data,userdata=userdata,user=user)


@app.route('/comments_list/<int:postid>',methods=["GET"])
def comments_list(postid):
    try:
        print(f"DEBUG: comments_list called with postid: {postid}")
        
        # For sub-application: Ensure user session exists
        if 'user_id' not in session:
            session["user_id"] = 1  # Default user ID from master app
            session["email"] = "guest@example.com"
            print("DEBUG: Created default session")
        
        userId = session["user_id"]
        print(f"DEBUG: userId from session: {userId}")
        
        userdata = selectAllfromUser_with_Id(userId)
        print(f"DEBUG: userdata: {userdata}")
        
        if not userdata:
            # Create default user data
            userdata = {
                'user_id': userId,
                'images': '',
                'firstname': 'Guest',
                'lastname': 'User'
            }
            print("DEBUG: Created default userdata")
        
        postid = int(postid)
        print(f"DEBUG: About to call loadCommentsandUser with postid: {postid}")
        
        comment_list = loadCommentsandUser(postid)
        print(f"DEBUG: comment_list result: {comment_list}")
        
        return jsonify(comment_list)
        
    except Exception as e:
        print(f"ERROR in comments_list route: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/share/<int:postid>', methods=["GET"])
def share(postid):
    # For sub-application: Ensure user session exists
    if 'user_id' not in session:
        session["user_id"] = 1  # Default user ID from master app
        session["email"] = "guest@example.com"
    
    post_content=sharing(postid)
    userId=session["user_id"]
    userdata=selectAllfromUser_with_Id(userId)
    insert_share(postid, userId)
    profileimage = userdata['images']

    return jsonify(post_content)
    




@app.route('/comments/<int:postid>', methods=["POST", "GET"])
def comments(postid):
    # For sub-application: Ensure user session exists
    if 'user_id' not in session:
        session["user_id"] = 1  # Default user ID from master app
        session["email"] = "guest@example.com"
    
    userId = session["user_id"]
    
    # Try to get user data, create default if not exists
    try:
        userdata = selectAllfromUser_with_Id(userId)
        if not userdata:
            # Create default user data
            userdata = {
                'user_id': userId,
                'firstname': 'Guest',
                'lastname': 'User',
                'email': session.get('email', 'guest@example.com')
            }
        
        surname = userdata.get('lastname', 'User')
        firstname = userdata.get('firstname', 'Guest')
       
        if request.method == "POST":
            comment = request.form.get('comment')
            if comment and comment.strip():  # Only insert if comment is not empty
                insert_comment(postid, userId, comment)
                # Redirect back to the post page after successful comment submission
                return redirect(url_for('post'))
        
        # For GET request, load comments and render appropriate page
        comment_list = loadCommentsandUser(postid)
        
        # Check if this is an AJAX request
        if request.headers.get('Content-Type') == 'application/json' or request.headers.get('Accept', '').find('application/json') != -1:
            return jsonify(comment_list)
        
        # For regular requests, redirect to post page
        return redirect(url_for('post'))
        
    except Exception as e:
        print(f"Error in comments route: {e}")
        # Redirect to post page on error
        return redirect(url_for('post'))



  
  

@app.route('/like/<int:postid>/<string:name>', methods=["GET","POST"])
def like(postid,name):
    # posts=loadPosts(name)
    userId=session["user_id"]
    # userdata=selectAllfromUser_with_Id(userId)
    # profileimage = userdata['images']
    # media=[]

    if request.method=="POST":
        post_id=postid
        results=user_has_liked_post(userId, post_id)
        count=0
        if results:
            decrease_like_count(post_id)
            update_likes_delete(userId,post_id)
            count=count-count
        else:
            increase_like_count(post_id)
            likes_update_table_row(userId,post_id)
            count=count+count
    # return count, to check if is one,button must be blue,
    # if count is zero the button color must be white
    return redirect(url_for('post',name=name))

    
@app.route('/updateUserInfo',methods=['POST'])

def updateUser():

    user_id=session['user_id']
    bio=request.form.get('bio')
    contact=request.form.get('contact')
    address=request.form.get('address')
    postal_code=request.form.get('postalCode')
    occupation=request.form.get('occupation')
    
    image=request.files['file']
    
    if bio:
        insertBio(user_id,bio)
        
    if contact:
        insertContact(user_id,contact)
    
    if occupation:
        insertOccupation(user_id,occupation)
    
    if address:
        insertAddress(user_id,address) 
        
    if postal_code:
        insertPostal(user_id,postal_code)
        
    if image.filename:
        image_=profile_image(image)
        insertImage(user_id,image_)
        # post=loadPosts()
    return redirect(url_for('post'))
        
@app.route('/createPost')
def createPostPage():
    return render_template('add_post.html')

@app.route('/userinfo')
def selectUserInfo():

    if "email" in session:
        userEmail=session["email"]
        user=selectAllfromUser(userEmail)
        return user


def create_upload_folder(files):
    config={'base_dir':'static\\'}
    # Get base directory from config
    base_dir = config['base_dir']
   
    # Construct path for the uploads folder
    uploads_dir = os.path.join(base_dir, 'uploads')

    # Create the uploads folder if it doesn't exist
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    # Construct path for the file within the uploads folder
    file_paths=[]
    for file_obj  in files:
        file_path = os.path.join(uploads_dir, file_obj.filename)
        file_obj.save(file_path)
        file_paths.append(file_path)
        
    return file_paths

def delete_media_content_from_file(file):
    try:
        base_dir = "static/uploads"
        # Construct the full file path
        file_path = os.path.join(base_dir, file)
        
        # Check if the file exists before attempting to delete
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file}' successfully deleted.")
        else:
            print(f"Error: File '{file}' does not exist.")
    except OSError as e:
        print(f"Error: Failed to delete file '{file}'. Reason: {str(e)}")



def delete_profile_picture_from_file(file):
    file=str(file).replace('\\','/')
    try:
        base_dir = "/static/images"
        # Construct the full file path
        file_path = os.path.join(base_dir,file)
        
        # Check if the file exists before attempting to delete
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file}' successfully deleted.")
        else:
            print(f"Error: File '{file}' does not exist.")
    except OSError as e:
        print(f"Error: Failed to delete file '{file}'. Reason: {str(e)}")



def delete_midea_picture_from_file(file):
    file=str(file).replace('\\','/')
    try:
        base_dir = "static/uploads"
        # Construct the full file path
        for images in file:
            file_path = os.path.join(base_dir,images)
                    
        # Check if the file exists before attempting to delete
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"File '{file}' successfully deleted.")
            else:
                 print(f"Error: File '{file}' does not exist.")
    except OSError as e:
        print(f"Error: Failed to delete file '{file}'. Reason: {str(e)}")



def media_file(files):
    # Create the 'uploads' directory if it doesn't exist
    os.makedirs('static/uploads', exist_ok=True)
    file_paths = []
    for file in files:
        # Save each file to the 'uploads' directory
        file_path = os.path.join('static/uploads', file.filename)
        file.save(file_path)
        file_paths.append(file_path)
        
        # Check if the file was saved successfully
        if not os.path.exists(file_path):
            print(f"Error: File '{file.filename}' not found.")
            return None
    
    return file_paths
    

def profile_image(files):
   
    
        # Save each file to the 'uploads' directory
    file_path = os.path.join('static/images', files.filename)
    files.save(file_path)
        
        # Check if the file was saved successfully
    if not os.path.exists(file_path):
        print(f"Error: File '{files.filename}' not found.")
        return None
    
    return file_path


class EmailForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    submit = SubmitField('Send Reset Email')

# Flask-WTF form for password reset
class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[validators.DataRequired(), validators.Length(min=8)])
    confirm_password = PasswordField('Confirm New Password', validators=[validators.DataRequired(), validators.EqualTo('password')])
    submit = SubmitField('Reset Password')

# Route to send reset email
@app.route('/reset_password_page', methods=['GET', 'POST'])
def reset_password_page():
        if request.method=="POST":
            email = request.form['email']
            user=selectAllfromUser(email)
            send_reset_email(user['email'])
            return render_template('login.html')

        return render_template('email.html')


# Function to send reset email
@app.route("/send_reset_email/<string:email>", methods=["POST",'GET'])
def send_reset_email(email):
    token = generate_token(email) 
    session['email']=email
    sender = app.config['MAIL_USERNAME']  # Replace with verified sender address if needed
    recipient = email
    try:
        message = Message(subject='Reset Your Password', sender=sender, recipients=[recipient])
        message.html ="""
    <div class="container">
        <h1>Password Reset</h1>
        <p>Hello,</p>
        <p>You requested a password reset. Click the button below to reset your password:</p>
        <a href=`http://127.0.0.1:9000/reset_password`>Reset Password</a>
        <p>If you did not request a password reset, please ignore this email.</p>
        <p>Thank you,</p>
        <p>The Team</p>
    </div>"""
        mail.send(message)
        return f"Reset email sent successfully to {email}"
    except Exception as e:
        print(f"Error sending email: {e}")
        return "Error sending reset email"    
    
# Dummy function to generate token
def generate_token(email):
    # Concatenate email and current timestamp
    data = email + str(time.time())
    
    # Hash the concatenated data using SHA256
    hashed_data = hashlib.sha256(data.encode()).hexdigest()
    
    # Return the hashed token
    return hashed_data

@app.route("/reset_password", methods=["POST","GET"])
def reset_password():
    if request.method=="POST":
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')
        email=session["email"]
        finalPassword = matchPassword(password.strip(), confirmPassword.strip())
            
        #check if password dont match
        if not finalPassword:
            return flash('Passwords do not match')
        password=encryptdata(password.strip())
        updatePassword(email,password)
        return redirect(url_for('post'))
    return render_template('reset_password.html')


@app.route('/search_suggestions')
def search_suggestions():
    query = request.args.get('q', '')
    if query:
        suggestions = get_suggestions(query)
        return jsonify(suggestions)
    return jsonify([])


@app.route('/search', methods=["POST","GET"])
def search():
    search = request.form.get('searchBox')
    funds=loadfundings()
    if request.method=="POST":
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        offset = (page - 1) * limit
        post = get_full_post_content(search,offset=offset, limit=limit)
      
       
        if "message" not in post:
            for item in post:
                if "media" in item and item['media']:
                    try:
                        # Parse the media string from database
                        media_string = item['media']
                        if media_string.startswith('[') and media_string.endswith(']'):
                            # Remove brackets and split by comma
                            media_list = media_string[1:-1].split(', ')
                            # Clean up quotes and escape characters
                            cleaned_media = []
                            for media_item in media_list:
                                # Remove quotes and fix path separators
                                clean_item = media_item.strip('"').replace('\\\\', '/')
                                cleaned_media.append(clean_item)
                            item['media'] = cleaned_media
                        else:
                            item['media'] = []
                    except Exception as e:
                        print(f"Error processing media for post {item.get('postId', 'unknown')}: {e}")
                        item['media'] = []
                else:
                    item['media'] = []
                        
        if 'user_id' not in session:
            return render_template("login.html")
    
        userId=session["user_id"]
        userdata=selectAllfromUser_with_Id(userId)
        profileimage = userdata['images']
        return render_template("post.html",funds=funds,post=post,user=userdata,profileimage=profileimage)

# Configuration and Debug Endpoints for External API Integration

@app.route('/config/external_api_url', methods=['GET', 'POST'])
def config_external_api_url():
    """
    Configure the external API URL
    GET: Returns current URL
    POST: Sets new URL (expects JSON: {"url": "http://localhost:5000"})
    """
    global EXTERNAL_API_BASE_URL
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            if data and 'url' in data:
                EXTERNAL_API_BASE_URL = data['url'].rstrip('/')  # Remove trailing slash
                return jsonify({
                    "success": True,
                    "message": "External API URL updated successfully",
                    "new_url": EXTERNAL_API_BASE_URL
                }), 200
            else:
                return jsonify({"error": "Missing 'url' in request data"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({
            "current_external_api_url": EXTERNAL_API_BASE_URL,
            "status": "active"
        }), 200

@app.route('/debug/external_user/<string:user_id>')
def debug_external_user(user_id):
    """
    Debug endpoint to test external API integration
    """
    try:
        # Test API connection
        user_data = fetch_user_from_external_api(user_id)
        
        return jsonify({
            "test_results": {
                "api_url": EXTERNAL_API_BASE_URL,
                "user_id_tested": user_id,
                "api_response": user_data,
                "api_available": user_data is not None
            },
            "current_session": {
                "user_id": session.get('user_id'),
                "data_source": session.get('data_source'),
                "has_external_data": 'external_user_data' in session,
                "session_keys": list(session.keys())
            },
            "processed_user_profile": get_user_profile_from_session()
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "api_url": EXTERNAL_API_BASE_URL,
            "user_id": user_id
        }), 500

@app.route('/debug/session_info')
def debug_session_info():
    """
    Debug endpoint to show current session information
    """
    return jsonify({
        "session_data": dict(session),
        "user_profile": get_user_profile_from_session(),
        "external_api_url": EXTERNAL_API_BASE_URL
    }), 200

@app.route('/external_api_config')
def external_api_config():
    """
    Configuration page for external API integration
    """
    return render_template('external_api_config.html')

@app.route('/test_profile')
def test_profile():
    """
    Test endpoint to view current user profile data
    """
    profile_data = get_user_profile_from_session()
    return jsonify({
        "profile_data": profile_data,
        "session_data": {
            "user_id": session.get('user_id'),
            "role": session.get('role'),
            "data_source": session.get('data_source'),
            "is_admin": session.get('role', '').lower() == 'admin'
        },
        "context_admin_status": inject_admin_status()
    })

@app.route('/debug_routes')
def debug_routes():
    """
    Debug endpoint to list all available routes
    """
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': str(rule)
        })
    return jsonify(routes)

@app.route('/test_userProfile_redirect')
def test_userProfile_redirect():
    """
    Test endpoint to check if userProfile route works
    """
    try:
        from flask import url_for
        profile_url = url_for('userProfile')
        return jsonify({
            "status": "success",
            "profile_url": profile_url,
            "message": "userProfile route is working",
            "session_user": session.get('user_id'),
            "user_data": get_user_profile_from_session()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "userProfile route has issues"
        }), 500

@app.route('/test_selectedUserProfile/<int:user_id>')
def test_selectedUserProfile(user_id):
    """
    Test endpoint to check selectedUserProfile route
    """
    try:
        from flask import url_for
        selected_url = url_for('selectedUserProfile', user_id=user_id)
        
        # Test if user exists
        user = selectAllfromUser_with_Id(user_id)
        
        return jsonify({
            "status": "success",
            "selected_url": selected_url,
            "user_id": user_id,
            "user_exists": user is not None,
            "user_data": user if user else None,
            "session_user": session.get('user_id'),
            "message": "selectedUserProfile route is working"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "selectedUserProfile route has issues"
        }), 500

@app.route('/test_analytics_access')
def test_analytics_access():
    """
    Test endpoint to check analytics access permissions
    """
    try:
        user_id = session.get('user_id')
        
        # Check admin status using same logic as analytics route
        if session.get("data_source") == "external_api":
            admin_status = session.get('role', '').lower() == 'admin'
            data_source = "external_api"
        else:
            admin_status = is_admin_user(user_id) if user_id else False
            data_source = "database"
        
        return jsonify({
            "user_id": user_id,
            "data_source": data_source,
            "role": session.get('role'),
            "admin_status": admin_status,
            "session_keys": list(session.keys()),
            "can_access_analytics": admin_status,
            "analytics_url": url_for('analytics') if admin_status else "Access denied"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Error checking analytics access"
        }), 500

if __name__ =="__main__":
    run_simple('localhost', 9000, app, use_reloader=True, processes=1)
