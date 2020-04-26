from flask import Flask, render_template,request,send_from_directory,session,flash
import re
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["firas_db"]
users = db["users"]
users.create_index("username")

app = Flask(__name__)

#secret key for the session
app.secret_key = "super secret key"

def add_user_to_db(username,password):
      users.insert({
            "username": username,
            "password": password
        })
    
def check_user_in_db(username):
    # user = users.find({"username":username})
    user = users.find_one({"username":username})
    if user :        
       
        return True

def check_pass_in_db(username,password):
        user=users.find_one({"username":username})
        if user["password"] == password:
            return True

@app.route('/', methods=['Get','POST'])
@app.route('/cabinet', methods=['Get','POST'])
def index():
    
    #check if the user logged in, if not go back to login html
      if not session.get('logged_in'):
          return render_template('login.html')
      
      else:
        msg=''
        
        
        if request.method == 'POST':
              getdata=''
             
            # if the post doesn't include new_message it means that it redirected from login page and no need to process data
              if "new_message" not in request.form :
                  return render_template('cabinet.html')
                    
@app.route('/login', methods=['GET','POST'])
def do_admin_login():
    
    #if  method='GET' it comes from log out
    if request.method=='GET':
        session['logged_in'] = False
        return index()  
    
    else:
       #if email not exist it is from login page, else from register page
        username = request.form.get('username')
        password = request.form.get('password')
        if "email" not in request.form :
                if check_user_in_db(username):
                    if check_pass_in_db(username, password):
                        session['logged_in'] = True
                    else :
                        flash('Wrong Password!')
                else:
                    flash('User not exsit!')
                return index()    
            
        else:
       
             if check_user_in_db(username) :
                     flash('Username existed')
                     print(username+"   "+password)
                     session['logged_in'] = False
                     return do_reg()
             else:
                 add_user_to_db(username, password)
                 session['logged_in'] = False
                 return index()
                    
#execute index function after set the session value
#return index()
 
@app.route('/register')
def do_reg():
    return render_template('register.html')    

     
@app.route('/static/<image_name>')
def index2(image_name):
       return send_from_directory('static/img',image_name)
       

@app.route('/static/<path:path>')
def index3(path):
     return app.send_static_file(path)

  
if __name__ == '__main__':

    app.run( port='5000',threaded=True)