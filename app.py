from flask import Flask,render_template,url_for,redirect,request,session
from werkzeug.utils import secure_filename
import json
import os
UPLOAD_FOLDER = 'static/imgs'

app=Flask(__name__)
app.secret_key="abc"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Movie_class:
    def __init__(self, name="", rating="",description="",image=""):
        self.name=name
        self.rating=rating
        self.image=image
        self.description=description

    def movie_object_list(self):
        f = open('movie_file.json')
        data=json.load(f)
        movie_list=[]
        for movie in data:
            movie_list.append(Movie_class(data[movie]["name"],data[movie]["rating"],data[movie]["description"],data[movie]["image"]))
        return movie_list

    def get_movie_info(self,movie_name):
        f = open('movie_file.json')
        data=json.load(f)
        movie_data=data[movie_name]
        return movie_data
    


class Theatre_class:
    def __init__(self, name="", timings="",movie_name=""):
        self.name=name
        self.timings=timings
        self.movie_name=movie_name

    def theatre_object_list(self,movie_name):
        f = open('theatre_file.json')
        theatre_data=json.load(f)
        theatre_list=[]
        for theatre in theatre_data:
            theatre_list.append(Theatre_class(theatre,theatre_data[theatre],movie_name))
        return theatre_list


class User_class:
    def __init__(self,user_name="",password="",email=""):
        self.user_name=user_name
        self.password=password
        self.email=email
    
    def check_login(self):
        if "username" in session:
            return True
        else:
            return False
    
    def validate_login(self,username,password):
        f = open('user_file.json')
        user_data=json.load(f)
        if(username not in user_data):
            return False
        if(user_data[username]["password"]==password):
            return True
        else:
            return False

    def register_user(self,username,password,email,phone_no):
        f = open('user_file.json')
        user_data=json.load(f)
        if(username in user_data):
            return False
        user_data[username]={"username":username,"password":password,"email":email,"phone_no":phone_no}   
        with open("user_file.json", "w") as write_file:
            json.dump(user_data, write_file)
        return True


    def logout_user(self):
        session.pop('username',None)

    
    def book_movie(self, movie_name,movie_time,theatre_name,number_tickets,price,seats_no):
        self.movie_name=movie_name
        self.theatre_name=theatre_name
        self.movie_time=movie_time
        self.number_tickets=number_tickets
        self.price=price
        self.seats_no=seats_no
        f = open('user_history_file.json')
        user_data_history=json.load(f)
        if session["username"] in user_data_history:
            user_data_history[session["username"]].append(movie_name)
        else:
            user_data_history[session["username"]]=[]
            user_data_history[session["username"]].append(movie_name)
        with open("user_history_file.json","w") as write_file:
            json.dump(user_data_history,write_file)
        




class Admin_Class:

    def __init__(self, username="", password=""):
        self.username=username
        self.password=password
    
    def add_admin_user(self, username,password,email,phone):
        f = open('admin_file.json')
        admin_data=json.load(f)
        if(username in admin_data):
            return False
        admin_data[username]={"username":username,"password":password,"email":email,"phone_no":phone}   
        with open("admin_file.json", "w") as write_file:
            json.dump(admin_data, write_file)
        return True

    def validate_login_admin(self, username, password):
        f = open('admin_file.json')
        admin_data=json.load(f)
        if(username not in admin_data):
            return False
        if(admin_data[username]["password"]==password):
            return True
        else :
            return False

    def check_admin_login(self): 
        if "username" in session:
            return True
        else:
            return False


    def logout_admin_user(self):
        session.pop('username',None)

    
    def add_movie(self,movie_name,rating,description,file):
        f=open("movie_file.json")
        movie_data=json.load(f)
        if movie_name in movie_data:
            return False
        movie_data[movie_name]={"name":movie_name,"rating":rating,"description":description,"image":file.filename}
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        with open("movie_file.json", "w") as write_file:
            json.dump(movie_data, write_file)
        return True


    def delete_movie(self,movie_name):
        f=open("movie_file.json")
        movie_data=json.load(f)
        if movie_name not in movie_data:
            return False
        movie_data.pop(movie_name, None)
        with open("movie_file.json", "w") as write_file:
            json.dump(movie_data, write_file)
        return True

    def add_theatre(self,theatre_name,timings):
        f=open("theatre_file.json")
        theatre_data=json.load(f)
        if theatre_name in theatre_data:
            return False
        theatre_data[theatre_name]=timings
        # filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        with open("theatre_file.json", "w") as write_file:
            json.dump(theatre_data, write_file)
        return True

    def delete_theatre(self,theatre_name):
        f=open("theatre_file.json")
        theatre_data=json.load(f)
        if theatre_name not in theatre_data:
            return False
        theatre_data.pop(theatre_name, None)
        with open("theatre_file.json", "w") as write_file:
            json.dump(theatre_data, write_file)
        return True
        
        
        



        

    


"""
Things to be added:-
    User class with:-
        display_info() #never really displaying info but still
        update_booked_movie() #to be done in the ticket_booking() to update chosen movie with number of seats

    Admin Class with:-
        add_movie()
        remove_movie()
        add_theatre()
        remove_theatre()
        will have separate html file so separate app.routes
"""

    



@app.route("/",methods=["POST","GET"])
def home():
    user_obj=User_class()
    user_obj.logout_user()
    admin_obj=Admin_Class()
    admin_obj.logout_admin_user()
    get_movies=Movie_class()
    movie_list=get_movies.movie_object_list()
    return render_template("movie_display.html", content = movie_list)

@app.route("/movie_display_logged_in.html",methods=["POST","GET"])
def movie_display_logged_in():
    get_movies=Movie_class()
    movie_list=get_movies.movie_object_list()
    return render_template("movie_display_logged_in.html", content = movie_list)


@app.route("/movie_display_admin_logged_in.html",methods=["POST","GET"])
def movie_display_admin_logged_in():
    get_movies=Movie_class()
    movie_list=get_movies.movie_object_list()
    return render_template("movie_display_admin_logged_in.html", content = movie_list)


@app.route("/about_movie.html",methods=["POST","GET"])
def about_movie():
    movie_data={}
    if request.method == "POST":
        user_obj=User_class()
        admin_obj=Admin_Class()
        if(user_obj.check_login()==False):
            return redirect(url_for("home"))
        elif(admin_obj.check_admin_login()==False):
            return redirect(url_for("home"))
        movie_name=request.form['movie']
        movie_info=Movie_class()
        movie_data=movie_info.get_movie_info(movie_name)
        movie_data = Movie_class(movie_data["name"],movie_data["rating"],movie_data["description"],movie_data["image"])
    return render_template("about_movie.html", content = movie_data)



@app.route("/theatre.html",methods=["POST","GET"])
def theatre():
    theatre_list=[]
    if request.method == "POST":
        movie_name=request.form['movie']
        theate_obj = Theatre_class()
        theatre_list=theate_obj.theatre_object_list(movie_name)
    return render_template("theatre.html", theatres=theatre_list)

@app.route("/seating.html",methods=["POST","GET"])
def seating():
    if request.method == "POST":
        movie_name=request.form['movie']
        theatre_name=request.form['theatre_name']
        movie_time=request.form['movie_time']
    return render_template("seating.html", movie_name=movie_name, theatre_name=theatre_name, movie_time=movie_time)

@app.route("/ticket_booking.html",methods=["POST","GET"])
def ticket_booking():
    movie_data=""
    theatre_name=""
    movie_time=""
    if request.method == "POST":
        number = request.form["number"]
        cost = request.form["cost"]
        movie_name = request.form["movie_name"]
        movie_time = request.form["movie_time"]
        theatre_name = request.form["theatre_name"]
        seatsselected = request.form["seatsselected"]
        movie_info=Movie_class()
        movie_data=movie_info.get_movie_info(movie_name)
        user=User_class()
        user.book_movie(movie_name,movie_time,theatre_name,number,cost,seatsselected)
        return render_template("ticket_booking.html", content=movie_data, theatre_name=theatre_name, movie_time=movie_time, seatsselected=seatsselected, cost=cost, number=number)


@app.route("/login.html",methods=["POST","GET"])
def login():
    message=""
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        user_obj=User_class()
        admin_obj=Admin_Class()
        check=user_obj.validate_login(username,password)
        check_admin=admin_obj.validate_login_admin(username,password)
        if(check):
            session["username"]=username
            return redirect(url_for("movie_display_logged_in"))
        elif(check_admin):
            session["username"]=username
            return redirect(url_for('movie_display_admin_logged_in'))
        else:
            message="Invalid"

    return render_template("login.html",msg=message)


@app.route("/register.html",methods=["POST","GET"])
def register():
    message=""
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        email=request.form["email"]
        phone_no=request.form["phNo"]
        user_obj=User_class()
        check=user_obj.register_user(username,password,email,phone_no)
        if(check):
            session["username"]=username
            return redirect(url_for("movie_display_logged_in"))
        else:
            message="Already registered"

    return render_template("register.html",msg=message)

@app.route("/delete_movie",methods=["POST","GET"])
def delete_movie():
    movie_name=request.form["movie"]
    #print(movie_name)
    admin_obj=Admin_Class()
    admin_obj.delete_movie(movie_name)
    return redirect(url_for('movie_display_admin_logged_in'))

@app.route("/add_movie.html",methods=["POST","GET"])
def add_movie():
    if request.method!="POST":
        return render_template("add_movie.html")
    movie_name=request.form["movie_name"]
    rating=request.form["rating"]
    description=request.form["description"]
    # image=request.form["image"]
    file = request.files['file']
    print(file.filename)
    admin_obj=Admin_Class()
    check=admin_obj.add_movie(movie_name,rating,description,file)
    if(check):
        return redirect(url_for('movie_display_admin_logged_in'))
    else:
        return render_template("add_movie.html",msg="Movie already added")

@app.route("/add_theatre.html",methods=["POST","GET"])
def add_theatre():
    if request.method!="POST":
        return render_template("add_theatre.html")
    theatre_name=request.form["theatre_name"]
    timings=request.form["timings"]
    timings=timings.split(', ')
    admin_obj=Admin_Class()
    check=admin_obj.add_theatre(theatre_name,timings)
    if(check):
        return redirect(url_for('movie_display_admin_logged_in'))
    else:
        return render_template("add_theatre.html",msg="Movie already added")

@app.route("/delete_theatre",methods=["POST","GET"])
def delete_theatre():
    if request.method!="POST":
        return render_template("delete_theatre.html")
    theatre_name=request.form["theatre_name"]
    admin_obj=Admin_Class()
    check=admin_obj.delete_theatre(theatre_name)
    if(check):
        return redirect(url_for('movie_display_admin_logged_in'))
    else:
        return render_template("delete_theatre.html",msg="No such theatre exists")

if __name__=="__main__":
	app.run(debug = True)