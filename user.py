import sqlite3
from flask import Flask,jsonify
import requests
import json
import asyncio
from datetime import datetime, timedelta
# Connect to SQLite database (creates if not exists)




def insertUserIntodb(first_name, last_name, date_of_birth, gender, email, occupation,bio, contact_details, home_address, postal_code, password):
    query="""INSERT INTO "User" (first_name, last_name, date_of_birth, gender, email, occupation,bio, contact_details, home_address, postal_code, password)VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, [ first_name, last_name, date_of_birth, gender, email, occupation,bio, contact_details, home_address, postal_code, password])
        conn.commit()        
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()



def loginCredentials(email, password):
    query="""SELECT * from User WHERE email=? and password=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (email,password))
        credentials=cursor.fetchone()
        if credentials:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
def updatePassword(email,password):
    query="""UPDATE User SET password=? where email=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(password,email))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()

        
def emailExists(email):
    query="""SELECT email from User WHERE email=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(email,))
        user = cursor.fetchone()
        if user:
            return True
        else:
            return False 
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
def selectAllfromUser(email):
    query="""SELECT * from "User" WHERE email=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(email,))
        user = cursor.fetchone()
        
        if user:
            column=[column[0] for column in cursor.description]
            user_dict=dict(zip(column,user))
            user=user_dict
            return user
        else:
            return {'message':'email dont exist'}
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
def selectAllmessages(senderId, receiverId):
    query="""SELECT * from "Messages" WHERE senderId=? AND receiverId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(senderId, receiverId))
        Messages = cursor.fetchall()
        
        if Messages:
            column=[column[0] for column in cursor.description]
            messages_dict=dict(zip(column,Messages))
            messages=messages_dict
            return messages
        else:
            return {'message':'no messages found'}
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
        
def selectAllfromUser_with_Id(id):
    query="""SELECT * from "User" WHERE userId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(id,))
        user = cursor.fetchone()
        
        if user:
            column=[column[0] for column in cursor.description]
            user_dict=dict(zip(column,user))
            user=user_dict
            return user
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()

        
def insertBio(user_id,bio):
    query="""UPDATE "User" SET bio=? WHERE userId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(bio,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        

def insertOccupation(user_id,occupation):
    query="""UPDATE "User" SET occupation=? where userId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(occupation,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()


def insertContact(user_id,contact):
    query="""UPDATE "User" SET contact_details=? WHERE userId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(contact,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
def insertAddress(user_id,address):
    query="""UPDATE "User" SET home_address=? WHERE userId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(address,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
        
def insertPostal(user_id,postal_code):
    query="""UPDATE "User" SET postal_code=? WHERE userId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(postal_code,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
        
def insertInterests(user_id,interests):
    query="""UPDATE "User" SET interests=? WHERE userId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(interests,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()

def insertImage(user_id,image):
    query="""UPDATE "User" SET images=? WHERE userId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(image,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
def insertPostimage(user_id,image):
    query="""UPDATE "Post" SET images=? WHERE user_Id=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(image,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
def insertPostvideo(user_id,video):
    query="""UPDATE "Post" SET video=? WHERE user_Id=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(video,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()

def insertPost(userId, title, description,media):
    user=selectAllfromUser_with_Id(userId)
    author=user['first_name']+' '+user['last_name']
    query = """INSERT INTO "Post" (user_id, author, title, description, media) VALUES (?, ?, ?, ?, ?)"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (userId, author, title, description, json.dumps(media)))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()


def updateTitle(post_id,title):
    query="""UPDATE "Post" SET title=? WHERE postId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(title,post_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
def updateDescription(post_id,description):
    query="""UPDATE "Post" SET description=? WHERE postId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(description,post_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()

def updateMedia(post_id,media):
    query="""UPDATE "Post" SET media=? WHERE postId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(media,post_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()

def updateOldPost(postId, userId, title, description,media):
    query = """UPDATE "Post" SET user_id=?, title=?, description=?, media=? WHERE postId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (userId, title, description, json.dumps(media), postId))
        conn.commit()
        print("message i am here")
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
    
    
def get_post(userId):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    query = "SELECT * FROM \"Post\" WHERE user_id = ?"
    cursor.execute(query, (userId,))
    posts = cursor.fetchall()
    if posts:
            column=[column[0] for column in cursor.description]
            post_list = []
            for post in posts:
                post_dict=dict(zip(column,post))
                post_list.append(post_dict)
    
            return post_list
    conn.close()


def get_one_post(post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    query = "SELECT * FROM \"Post\" WHERE postId = ?"
    cursor.execute(query, (post_id,))
    posts = cursor.fetchone()
    if posts:
            column=[column[0] for column in cursor.description]
            post_list = []
            post_dict=dict(zip(column,posts))
            post_list.append(post_dict)
    
            return post_list
    conn.close()



def deletepost(userId,post_id):
    query = """DELETE FROM "Post" WHERE user_id=? AND postId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (userId, post_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()

def deleteshare(post_id):
    query = """DELETE FROM "Shares" WHERE post_id=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (post_id,))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()

def deletecomments(post_id):
    query = """DELETE FROM Comment WHERE post_id=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (post_id,))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
        
def deletereplies(post_id):
    query = """DELETE FROM replies WHERE post_id=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (post_id,))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
        
def deletelikes(post_id):
    query = """DELETE FROM Likes WHERE post_id=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (post_id,))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
        

def retrieve_media(post_id):
    post = get_post(post_id)
    if post:  
        media = post[6]  
        media = json.loads(media)
        return media
    else:
        return None
    
    
    
def loadPosts(name):
    query="SELECT * ,COUNT(*) as total FROM Post where title=? ORDER BY post_date DESC, post_time DESC"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,[name,])
        posts = cursor.fetchall()
        
        if posts:
            columns = [column[0] for column in cursor.description]
            posts_list = []
            for post in posts:
                post_dict = dict(zip(columns, post))
                if post_dict['total']==0:
                    return {'message': 'No posts found'}
                else:
                    posts_list.append(post_dict)
                    return posts_list
        else:
            return {'message': 'No posts found'}
    except sqlite3.Error as e:
        print('Error:', e)
        return {'message': 'An error occurred while loading posts'}
    finally:
        conn.close()


def load_Posts(offset=0, limit=10):
    query="SELECT * FROM Post ORDER BY post_date DESC, post_time DESC LIMIT ? OFFSET ?"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(limit, offset))
        posts = cursor.fetchall()
        print("posts",posts)
        if posts:
            columns = [column[0] for column in cursor.description]
            posts_list = []
            for post in posts:
                post_dict = dict(zip(columns, post))
                posts_list.append(post_dict)
            return posts_list
        else:
            return {'message': 'No posts found'}
    except sqlite3.Error as e:
        print('Error:', e)
        return {'message': 'An error occurred while loading posts'}
    finally:
        conn.close()




def countPosts():
    query="SELECT title,COUNT(title) as total FROM Post GROUP BY title"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,)
        posts = cursor.fetchall()
        
        columns = [column[0] for column in cursor.description]
        post_list = []
        for post in posts:
                
            post_dict = dict(zip(columns, post))
            post_list.append(post_dict)
                
        return post_list 
        
    except sqlite3.Error as e:
        print('Error:', e)
        return {'message': 'An error occurred while loading posts'}
    finally:
        conn.close()


def loadComments(postid):
    query = "SELECT * FROM Comment WHERE post_id=? ORDER BY post_date DESC, post_time DESC"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, (postid,))
        comments = cursor.fetchall()
        
        if comments:
            
            columns = [column[0] for column in cursor.description]
            comment_list = []
            for comment in comments:
                
                comment_dict = dict(zip(columns, comment))
                comment_list.append(comment_dict)
                
            return json.dumps(comment_list)  # Return JSON data
        else:
            return json.dumps({'message': 'No comments found'})  # Return JSON data
    except sqlite3.Error as e:
        print('Error:', e)
        return json.dumps({'message': 'An error occurred while loading comments'})  # Return JSON data
    finally:
        conn.close()



def loadUsersIdViwComments(userId):
    query = "SELECT * FROM User WHERE userId=?"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, (userId,))
        userIds = cursor.fetchall()
        
        if userIds:
            
            columns = [column[0] for column in cursor.description]
            UserId_list = []
            for userId in userIds:
                
                UserId_dict = dict(zip(columns, userId))
                UserId_list.append(UserId_dict)
                
            return json.dumps(UserId_list)  # Return JSON data
        else:
            return json.dumps({'message': 'No User Id found'})  # Return JSON data
    except sqlite3.Error as e:
        print('Error:', e)
        return json.dumps({'message': 'An error occurred while loading user'})  # Return JSON data
    finally:
        conn.close()
        
 


def loadCommentsandUser(postid):
    query = """
    SELECT 
        u.first_name, 
        u.last_name, 
        c.post_id,
        c.text,
        c.post_date,
        c.post_time
    FROM Comment c
    INNER JOIN User u ON c.user_id = u.userId
    WHERE c.post_id=?
    """
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, (postid,))
        comments = cursor.fetchall()
        if comments:
            # Get column names
            column_names = [description[0] for description in cursor.description]
            
            comment_list = []
            for comment in comments:
                # Create a dictionary with column names as keys
                comment_dict = {column_names[i]: comment[i] for i in range(len(column_names))}
                comment_list.append(comment_dict)
                
            return json.dumps(comment_list)  # Return JSON data
        else:
            return json.dumps({'message': 'No comments found'})  # Return JSON data
    except sqlite3.Error as e:
        print('Error:', e)
        return json.dumps({'message': 'An error occurred while loading comments'})  # Return JSON data
    finally:
        conn.close()
        

        

def activeusers():
    query = "SELECT COUNT(active) AS countActive FROM User_session WHERE active=TRUE"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        countActive = cursor.fetchone()[0]  # Fetch one row and extract the count
        return {'message': 'Success', 'countActive': countActive}
    except sqlite3.OperationalError as e:
        return {'message': 'Database error: {}'.format(e)}
    except sqlite3.Error as e:
        return {'message': 'An error occurred: {}'.format(e)}
    finally:
        conn.close()


def count_likes():
    query = "SELECT SUM(likes) AS totalLikes FROM Posts"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        total_likes = cursor.fetchone()[0]  # Fetch one row and extract the total likes
        return total_likes
    except sqlite3.Error as e:
        print('An error occurred:', e)
        return None
    finally:
        conn.close()
        
def count_comments():
    query = "SELECT COUNT(*) AS totalComments FROM Comments"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        total_comments = cursor.fetchone()[0]  # Fetch one row and extract the total comments
        return total_comments
    except sqlite3.Error as e:
        print('An error occurred:', e)
        return None
    finally:
        conn.close()


def user_has_liked_post(user_id, post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM likes WHERE user_id = ? AND post_id = ?", (user_id, post_id))
    like_count = cursor.fetchone()[0] 
    
    conn.close()
    
    # If like_count is greater than 0, it means the user has liked the post
    return like_count > 0

def decrease_like_count(post_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE \"Post\" SET likes = likes - 1 WHERE postId = ?", (post_id,))
    
    conn.commit()
    
    conn.close()


def update_likes_delete(userId,post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM \"Likes\" WHERE user_id = ? AND post_id=?", (userId,post_id))
    
    conn.commit()
    
    conn.close()

def likes_update_table_row(userId,post_id):
    query = """INSERT INTO \"Likes\" (post_id, user_id) VALUES (?, ?)"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (post_id, userId))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
        
    
    
def increase_like_count(post_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE \"Post\" SET likes = likes + 1 WHERE postId = ?", (post_id,))
    
    conn.commit()
    
    conn.close()
 

def insert_comment(post_id, user_id, comment):
    query = """INSERT INTO Comment (post_id, user_id, text) VALUES (?, ?, ?)"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (post_id, user_id, comment))
        conn.commit()
        increase_comment_count(post_id)
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
 
def increase_comment_count(post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        # Fetch the current comment count for the post
        cursor.execute("SELECT comments FROM Post WHERE postId=?", (post_id,))
        current_count = cursor.fetchone()[0]

        # Increment the comment count by one
        new_count = current_count + 1

        # Update the comment count in the Post table
        cursor.execute("UPDATE Post SET comments=? WHERE postId=?", (new_count, post_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
        
        
        
def insert_share(post_id, user_id):
    query = """INSERT INTO Shares (post_id, user_id) VALUES (?, ?)"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (post_id, user_id))
        conn.commit()
        increment_share_count(post_id)
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()

def share_count(post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        # Fetch the current comment count for the post
        cursor.execute("SELECT count(share) FROM Post WHERE postId=?", (post_id,))
        current_count = cursor.fetchone()
        conn.commit()
        return current_count
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
    
    
def delete_profile_picture(userId):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    image = None  # Initialize image variable to store the deleted image

    try:
        # Fetch the user's current profile picture (images) from the database
        cursor.execute("SELECT images FROM User WHERE userId = ?", (userId,))
        profile = cursor.fetchone()
        
        if profile:
            image = profile[0]  # Assuming 'images' is a column in the User table
            print("Image from db:", image)
            
            # Update the User table to set the images column to NULL
            cursor.execute("UPDATE User SET images = NULL WHERE userId = ?", (userId,))
            conn.commit()
            print(f"Profile picture for user ID {userId} successfully deleted.")
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()
        return image  # Return the image URL or path that was deleted from the database

# Example usage:
if __name__ == "__main__":
    user_id_to_delete = 1  # Replace with the actual user ID
    deleted_image = delete_profile_picture(user_id_to_delete)
    if deleted_image:
        print(f"Deleted profile picture: {deleted_image}")
    else:
        print(f"No profile picture found for user ID {user_id_to_delete}")
    
 
def increment_share_count(post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        # Fetch the current comment count for the post
        cursor.execute("SELECT shares FROM Post WHERE postId=?", (post_id,))
        current_count = cursor.fetchone()[0]

        # Increment the comment count by one
        new_count = current_count + 1

        # Update the comment count in the Post table
        cursor.execute("UPDATE Post SET shares=? WHERE postId=?", (new_count, post_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
 
 
    
def update_comment(comment_id, comment, user_id):
    query = """UPDATE Comment SET text=? WHERE comment_id=? AND user_id=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (comment, comment_id, user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
    

def sharing(postid):
    query="SELECT author,title,description,media FROM Post WHERE postid=? ORDER BY post_date DESC, post_time DESC"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(postid,))
        posts = cursor.fetchall()
        
        if posts:
            columns = [column[0] for column in cursor.description]
            posts_list = []
            for post in posts:
                post_dict = dict(zip(columns, post))
                posts_list.append(post_dict)
            return posts_list
        else:
            return {'message': 'No posts found'}
    except sqlite3.Error as e:
        print('Error:', e)
        return {'message': 'An error occurred while loading posts'}
    finally:
        conn.close()

def insertreplyMessages(sender_id, receiverId, reply, replyTo):
    query="""INSERT INTO Reply (senderId, receiverId, reply,replyTo) VALUES (?, ?, ?,?)"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, [ sender_id, receiverId, reply,replyTo])
        conn.commit()        
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()



def insertMessages(senderId, receiverId, message):
    query="""INSERT INTO Messages(senderId, receiverId, message) VALUES ( ?, ?, ?)"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, [ senderId, receiverId, message])
        conn.commit()        
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()


def messagesFromSender(senderId, receiverId):
    query="SELECT User.first_name, User.last_name, Messages.message, Messages.timestamp FROM Messages INNER JOIN User ON Messages.senderId = User.userId WHERE senderId=? and receiverId=?"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(senderId, receiverId))
        Messages = cursor.fetchall()
        
        if Messages:
            columns = [column[0] for column in cursor.description]
            messages_list = []
            for message in Messages:
                message_dict = dict(zip(columns, message))
                messages_list.append(message_dict)
            return messages_list
        else:
            return {'message':'no messages found'}
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
def selectAllmessages(userId):
    query = """
    SELECT DISTINCT 
        M1.messageId AS message_id,
        Sender.userId AS sender_id, 
        Sender.first_name AS sender_first_name, 
        Sender.last_name AS sender_last_name, 
        Receiver.userId AS receiver_id,
        Receiver.first_name AS receiver_first_name, 
        Receiver.last_name AS receiver_last_name, 
        M1.message, 
        M1.timestamp AS message_timestamp,
        M2.message AS reply_message, 
        M2.timestamp AS reply_timestamp
    FROM 
        Messages AS M1
    INNER JOIN 
        User AS Sender ON M1.senderId = Sender.userId 
    INNER JOIN 
        User AS Receiver ON M1.receiverId = Receiver.userId 
    LEFT JOIN 
        Messages AS M2 ON M1.messageId = M2.replyTo
    WHERE 
        Receiver.userId = ? 
    ORDER BY 
        M1.timestamp DESC;
    """
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, [userId])
        rows = cursor.fetchall()
        if rows:
            columns = [column[0] for column in cursor.description]
            messages_list = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                messages_list.append(row_dict)
                print(messages_list)
            return messages_list
        else:
            return {'message': 'No messages found.'}
    except sqlite3.Error as e:
        print('Error:', e)
    finally:
        conn.close()


def update_campaign(subject, overview, funding_goal, duration, description):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Campaigns (subject, overview, funding_goal, duration, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (subject, overview, funding_goal, duration, description))
    conn.commit()
    conn.close()
    



def get_column_names():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(Post)")
    columns = cursor.fetchall()
    conn.close()
    # Extract column names from the result of PRAGMA table_info
    return [column[1] for column in columns]


def get_suggestions(query):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()

    columns = get_column_names()
    columns = [column for column in columns if column != 'media']
    # Create the SQL query dynamically
    sql_query = " UNION ".join([f"SELECT {column}, '{column}' as column_name FROM Post WHERE {column} LIKE ?" for column in columns])
    parameters = ['%' + query + '%'] * len(columns)
    
    cursor.execute(sql_query, parameters)
    results = cursor.fetchall()
    conn.close()

    # Remove duplicates and extract results
    unique_results = {(result[0], result[1]) for result in results}
    return list(unique_results)


def get_full_post_content(search, offset=0, limit=10):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    # Get column names except 'media'
    columns = get_column_names()
    columns = [column for column in columns if column != 'media']
    
    # Constructing the SQL query dynamically to search across all relevant columns
    sql_query = f"SELECT * FROM Post WHERE "
    sql_query += " OR ".join([f"{column} LIKE ?" for column in columns])
    sql_query += " ORDER BY post_date DESC, post_time DESC LIMIT ? OFFSET ?"
    
    # Execute the SQL query
    try:
        cursor.execute(sql_query, ['%' + search + '%' for _ in columns] + [limit, offset])
        post_content = cursor.fetchall()
        
        if post_content:
            columns = [column[0] for column in cursor.description]
            post_list = []
            for row in post_content:
                row_dict = dict(zip(columns, row))
                post_list.append(row_dict)
            return post_list
        else:
            print("No posts found matching the search criteria.")
            return []
    except sqlite3.Error as e:
        print(f"Error executing SQLite query: {e}")
        return []
    finally:
        conn.close()



def survey(question,question_type,choices,custom_answer):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO SurveyQuestions (question, question_type, choices, custom_answer)
        VALUES (?, ?, ?, ?)
    """, (question, question_type, choices, custom_answer))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Question created successfully'}), 200

def retrievesurvey():
    query="""SELECT * FROM SurveyQuestions"""
    conn=sqlite3.connect('blog.db')
    cursor=conn.cursor()
    
    try:
        cursor.execute(query,)
        questions = cursor.fetchall()
        
        if questions:
            columns = [column[0] for column in cursor.description]
            questions_list = []
            for question in questions:
                questions_dict = dict(zip(columns, question))
                questions_list.append(questions_dict)
            return questions_list
        else:
            return {'message':'no questions found'}
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()

def deleteSurveyQuestion(surveyId):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM SurveyQuestions  WHERE  id=?", (surveyId,))
        conn.commit() 
    except sqlite3.Error as e:
        print('Error: ',e)  
    finally:
        conn.close()
        
        

def retrieveCustomizedsurvey(list):
    query="""SELECT * FROM SurveyQuestions WHERE id=?"""
    conn=sqlite3.connect('blog.db')
    cursor=conn.cursor()
    
    questions_list = []
    try:
        for item_id in list:
            cursor.execute(query, (item_id,))
            question = cursor.fetchone()  # Fetch a single question (assuming ID is unique)

            if question:
                columns = [column[0] for column in cursor.description]
                question_dict = dict(zip(columns, question))
                questions_list.append(question_dict)
            else:
                # Handle case where no question is found for a specific ID
                questions_list.append({'message': f'No question found for ID {item_id}'})
        
        if questions_list:
            return questions_list
        else:
            return {'message': 'No questions found for the given IDs'}
    
    except sqlite3.Error as e:
        print('SQLite Error:', e)
        return {'message': 'Database error occurred'}



def customSurveys():
    query="""SELECT * FROM customSurveys"""
    conn=sqlite3.connect('blog.db')
    cursor=conn.cursor()
    cursor.execute(query, )
    custom = cursor.fetchall()
    customSurveys_list = []
    try:
        if custom:
            for item in custom:
                columns = [column[0] for column in cursor.description]
                customSurveys_dict = dict(zip(columns, item))
                customSurveys_list.append(customSurveys_dict)
          
        if customSurveys_list:
            return customSurveys_list
        
    except sqlite3.Error as e:
        print('SQLite Error:', e)
        return {'message': 'Database error occurred'}


def insert_survey_name(survey_name,questions):
    conn = sqlite3.connect('blog.db')
    cur = conn.cursor()

    try:
        # SQL query to insert surveyName into customSurveys table
        sql = """
        INSERT INTO customSurveys (surveyName,questions) 
        VALUES (?,?)
        """
        cur.execute(sql, (survey_name,questions))
        conn.commit()
        print("Survey name inserted successfully.")

    except sqlite3.Error as e:
        print(f"Error inserting survey name: {e}")

    finally:
        conn.close()
        
        
def custom_Surveys(surveyName):
    query="""SELECT * FROM customSurveys WHERE surveyName=?"""
    conn=sqlite3.connect('blog.db')
    cursor=conn.cursor()
    cursor.execute(query,(surveyName,) )
    custom = cursor.fetchall()
    customSurveys_list = []
    try:
        if custom:
            for item in custom:
                columns = [column[0] for column in cursor.description]
                customSurveys_dict = dict(zip(columns, item))
                customSurveys_list.append(customSurveys_dict)
        if customSurveys_list:
            return customSurveys_list
        
    except sqlite3.Error as e:
        print('SQLite Error:', e)
        return {'message': 'Database error occurred'}


def popup_custom_Surveys():
    query="""SELECT * FROM customSurveys ORDER BY timestamp DESC limit 1"""
    conn=sqlite3.connect('blog.db')
    cursor=conn.cursor()
    cursor.execute(query,)
    custom = cursor.fetchall()
    customSurveys_list = []
    try:
        if custom:
            
            for item in custom:
                
                columns = [column[0] for column in cursor.description]
                customSurveys_dict = dict(zip(columns, item))
                customSurveys_list.append(customSurveys_dict)
        if customSurveys_list:
            return customSurveys_list
        
    except sqlite3.Error as e:
        print('SQLite Error:', e)
        return {'message': 'Database error occurred'}



def deleteCustomSurveyQuestion(survey_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM customSurveys  WHERE  id=?", (survey_id,))
        conn.commit() 
    except sqlite3.Error as e:
        print('Error: ',e)  
    finally:
        conn.close()
        
        
        
def insert_customSurvey_answer(survey_id,user_id, answer):
      
    query = '''INSERT INTO customSurveysAnswers (survey_name, user_name, answer)
               VALUES (?, ?, ?)'''
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    user=selectAllfromUser_with_Id(user_id)
    
    name=custom_Surveys_name(survey_id)
    survey_name=name[0]['surveyName']
    print(survey_name)
    print(user)
    user_name=user['first_name']+" "+ user['last_name']
    
    try:
        cursor.execute(query, (survey_name, user_name, answer))
        conn.commit()
        return {'message': 'Answer added successfully', 'answer_id': cursor.lastrowid}
    
    except sqlite3.Error as e:
        print('SQLite Error:', e)
        return {'message': 'Database error occurred'}
    
    finally:
        cursor.close()
        conn.close()        
        

def custom_Surveys_name(survey_id):
    query="""SELECT surveyName FROM customSurveys WHERE id=?"""
    conn=sqlite3.connect('blog.db')
    cursor=conn.cursor()
    cursor.execute(query,(survey_id,))
    custom = cursor.fetchall()
    customSurveys_list = []
    try:
        if custom:
            
            for item in custom:
                
                columns = [column[0] for column in cursor.description]
                customSurveys_dict = dict(zip(columns, item))
                customSurveys_list.append(customSurveys_dict)
        if customSurveys_list:
            return customSurveys_list
        
    except sqlite3.Error as e:
        print('SQLite Error:', e)
        return {'message': 'Database error occurred'}




def All_Surveys(id):
    query="""SELECT * FROM customSurveysAnswers WHERE id=?"""
    conn=sqlite3.connect('blog.db')
    cursor=conn.cursor()
    cursor.execute(query,(id,))
    custom = cursor.fetchall()
   
    customSurveys_list = []
    try:
        if custom:
            
            for item in custom:
                
                columns = [column[0] for column in cursor.description]
                customSurveys_dict = dict(zip(columns, item))
                customSurveys_list.append(customSurveys_dict)
        if customSurveys_list:
          
            print(customSurveys_list)
            return customSurveys_list
        
    except sqlite3.Error as e:
        print('SQLite Error:', e)
        return {'message': 'Database error occurred'}







        
#fundings
def loadfundings():
    
    query="SELECT * FROM fundings"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,)
        funds = cursor.fetchall()
        
        if funds:
            columns = [column[0] for column in cursor.description]
            funds_list = []
            for fund in funds:
                fund_dict = dict(zip(columns, fund))
                funds_list.append(fund_dict)
            print(funds_list)
            return funds_list
        else:
            return {'message': 'No funds found'}
    except sqlite3.Error as e:
        print('Error:', e)
        return {'message': 'An error occurred while loading funds'}
    finally:
        conn.close()

       
def updateFunding(data):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    for item in data:
        cursor.execute('''
        INSERT INTO fundings (
            public_private,
            type_of_source,
            name_of_source,
            type_of_disbursement_channel,
            name_of_disbursement_channel,
            name_of_funding_opportunity,
            financial_instrument,
            size_of_investment,
            investment_opportunity_info,
            direct_use,
            sectors,
            fund_contact_name,
            fund_contact_email,
            fund_contact_number,
            fund_contact_website
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item["Public/ Private"],
            item["Type of source/ Intermediary of finance"],
            item["Name of  source/ Intermediary of finance"],
            item["Type of disbursement channel "],
            item["Name of  disbursment channel"],
            item["Name of funding opportunity"],
            item["Financial instrument"],
            item["Size of investment"],
            item["Investment opportunity information"],
            item["Direct Use"],
            item["Sector(s)"],
            item["Fund Contact Details / Contact Name"],
            item["Fund Contact E-mail"],
            item["Fund Contact Number"],
            item["Fund Contact Website"]
        ))

    conn.commit()
    conn.close()


def fetch_search_criteria():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()

   
    query = "SELECT * FROM fundings"
    cursor.execute(query,)
    rows = cursor.fetchall()

   
    criteria_list = []
    for row in rows:
        criteria = {
            "Type_of_organisation_seeking_funding": row[1],
            "financial_sector_type": row[2],
            "Type_of_Investment_Instrument": row[3],
            "type_of_financing_organisation": row[4],
           # "Type_of_EIP_initiatives_search": row[5],
          #  "Name_financing_organisation": row[6],
          #  "Fund_name": row[7],
          #  "Specific_focus_of_funding": row[8],
          #  "EIP_initiatives_result": row[9],
          #  "Finance_threshhold": row[10],
           # "Eligibility_criteria": row[11],
            "Weblink": row[12],
            "Contact_details": row[13],
            #"Investment_opportunity_information": row[14],
            #"Questionaire_with_financing_institution2": row[15]
        }
        criteria_list.append(criteria)

    conn.close()
    return criteria_list


def search_web(criteria):
    api_key = 'AIzaSyAqRhITpdaLI-osXVA3SvarQADy_ZX_0Xs' 
    search_engine_id = 'a3e8b272ad2b14296'  
    criteria = [value for value in criteria.values() if value is not None]
    query = ' '.join(criteria)

    url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}'

    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        scheduled_task()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return None


def update_database(data, criteria):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()

    if data is not None and 'items' in data:
        for result in data['items']:
            title = result.get('title', '')
            url = result.get('link', '')
            description = result.get('snippet', '')

            print(f"URL: {url}")
            print(f"Updated database for criteria: {criteria['Type_of_organisation_seeking_funding']}")
            print(f"Title: {title}")
            print(f"Description: {description}")
            print("\n")  # Add a separator between entries

        conn.commit()
        conn.close()

def run_task():
    search_criteria_list = fetch_search_criteria()
    for criteria in search_criteria_list:
        search_results = search_web(criteria)
        update_database(search_results, criteria)

def calculate_next_run_date():
    today = datetime.today()
    next_run_date = today + timedelta(days=90)  # Approximation for 3 months
    return next_run_date

next_run_date = calculate_next_run_date()

def scheduled_task():
    global next_run_date
    today = datetime.today().date()
    if today >= next_run_date.date():
        run_task()
        next_run_date = calculate_next_run_date()

