import sqlite3


conn = sqlite3.connect('blog.db')

cursor = conn.cursor()
#cursor.execute(''' drop table pOST''')
#cursor.execute(''' drop table Comment''')
# cursor.execute(''' drop table Messages''')

# Create replies table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS replies (
        reply_id INTEGER PRIMARY KEY,
        comment_id INTEGER,
        reply_text TEXT,
        post_id INTEGER,
        post_date DATE DEFAULT CURRENT_DATE,
        post_time TIME DEFAULT CURRENT_TIME,
        FOREIGN KEY (post_id) REFERENCES Post(postId)
        FOREIGN KEY (comment_id) REFERENCES comments(comment_id)
    )
''')


cursor.execute('''  CREATE TABLE IF NOT EXISTS User (
        userId INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        date_of_birth DATE,
        gender TEXT,
        email TEXT UNIQUE NOT NULL,
        occupation TEXT,
        bio TEXT,
        contact_details TEXT,
        home_address TEXT,
        postal_code TEXT,
        password TEXT NOT NULL,
        images TEXT
    )
        ''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS Post (
        postId INTEGER PRIMARY KEY,
        user_id INTEGER,
        author TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        media TEXT,
        likes INTEGER DEFAULT 0,
        comments INTEGER DEFAULT 0,
        shares INTEGER DEFAULT 0,
        post_date DATE DEFAULT CURRENT_DATE,
        post_time TIME DEFAULT CURRENT_TIME,
        FOREIGN KEY (user_id) REFERENCES User(userId)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Comment (
        commentId INTEGER PRIMARY KEY,
        user_id INTEGER,
        post_id INTEGER,
        text TEXT,
        post_date DATE DEFAULT CURRENT_DATE,
        post_time TIME DEFAULT CURRENT_TIME,
        FOREIGN KEY (user_id) REFERENCES User(userId),
        FOREIGN KEY (post_id) REFERENCES Post(postId)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS fundings (
        id INTEGER PRIMARY KEY,
        public_private TEXT,
        type_of_source TEXT,
        name_of_source TEXT,
        type_of_disbursement_channel TEXT,
        name_of_disbursement_channel TEXT,
        name_of_funding_opportunity TEXT,
        financial_instrument TEXT,
        size_of_investment TEXT,
        investment_opportunity_info TEXT,
        direct_use TEXT,
        sectors TEXT,
        fund_contact_name TEXT,
        fund_contact_email TEXT,
        fund_contact_number TEXT,
        fund_contact_website TEXT
    )
''')



cursor.execute('''
    CREATE TABLE IF NOT EXISTS Likes (
        likeId INTEGER PRIMARY KEY,
        user_id INTEGER,
        post_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES User(userId),
        FOREIGN KEY (post_id) REFERENCES Post(postId)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Shares (
        shareId INTEGER PRIMARY KEY,
        user_id INTEGER,
        post_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES User(userId),
        FOREIGN KEY (post_id) REFERENCES Post(postId)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Messages (
    messageId INTEGER PRIMARY KEY,
    senderId INTEGER NOT NULL,
    receiverId INTEGER NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    replyTo INTEGER, -- This column is used to store the messageId of the message this is a reply to
    FOREIGN KEY (senderId) REFERENCES User(userId),
    FOREIGN KEY (receiverId) REFERENCES User(userId)
)
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reply (
    replyId INTEGER PRIMARY KEY,
    senderId INTEGER NOT NULL,
    receiverId INTEGER NOT NULL,
    reply TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (senderId) REFERENCES User(userId),
    FOREIGN KEY (receiverId) REFERENCES Messages(receiverId),
    FOREIGN KEY (senderId) REFERENCES Messages(senderId)
)
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS SurveyQuestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        question_type TEXT CHECK(question_type IN ('single', 'multiple', 'custom')) NOT NULL,
        choices TEXT
)
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS customSurveys(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surveyName TEXT NOT NULL,
        questions TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS customSurveysAnswers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        survey_name TEXT NOT NULL,
        user_name TEXT NOT NULL,
        answer TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        
)
''')














# Close the connection
conn.close()
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)


class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    occupation = db.Column(db.String(100), nullable=True)
    contact_details = db.Column(db.String(100), nullable=True)
    home_address = db.Column(db.String(200), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    interests = db.Column(db.String(200), nullable=True)
    posts = db.relationship('Post', backref='author', lazy=True)  # Relationship to the Post table

    def __repr__(self):
        return '<User %r>' % self.email

class Post(db.Model):
    postId = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)  # Foreign key relationship to User table
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    images = db.Column(db.BLOB, nullable=True)  # Assuming storing images as BLOB data
    videos = db.Column(db.BLOB, nullable=True)  # Assuming storing videos as BLOB data
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Post %r>' % self.title

# Create the tables
with app.app_context():
    db.create_all()
    
    '''