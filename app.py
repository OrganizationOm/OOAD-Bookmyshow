from flask import Flask,render_template,url_for,redirect,request,session
import json

app=Flask(__name__)
app.secret_key="abc"


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

"""
Things to be added:-
    User class with:-
        check_login() #should be done at home() after clicking view button
        check_register() #should be done at home() after clicking view button
        add_user() #should be done if both of the above fail
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
    get_movies=Movie_class()
    movie_list=get_movies.movie_object_list()
    return render_template("movie_display.html", content = movie_list)

@app.route("/about_movie.html",methods=["POST","GET"])
def about_movie():
    movie_data={}
    if request.method == "POST":
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

@app.route("/ticket_booking.html",methods=["POST","GET"])
def ticket_booking():
    movie_data=""
    theatre_name=""
    movie_time=""
    message=""
    if request.method == "POST":
        movie_name=request.form['movie']
        theatre_name=request.form['theatre_name']
        movie_time=request.form['movie_time']
        quantity=request.form['quantity']
        movie_info=Movie_class()
        movie_data=movie_info.get_movie_info(movie_name)
        if(quantity=="0"):
            message=""
        else:
            message="You have successfully booked "+quantity+" seats for the movie "+movie_data["name"]+" at "+movie_time+", "+theatre_name
    return render_template("ticket_booking.html", content=movie_data, theatre_name=theatre_name, movie_time=movie_time, msg=message)


@app.route("/login.html",methods=["POST","GET"])
def login():
    return render_template("login.html")


@app.route("/register.html",methods=["POST","GET"])
def register():
    return render_template("register.html")

if __name__=="__main__":
	app.run(debug = True)