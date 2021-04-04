from flask import Flask,render_template,url_for,redirect,request,session
import json

app=Flask(__name__)
app.secret_key="abc"

@app.route("/",methods=["POST","GET"])
def home():
    f = open('movie_file.json')
    data=json.load(f)
    movie_list=[]
    for movie in data:
        movie_list.append(data[movie])
    return render_template("movie_display.html", content = movie_list)

@app.route("/about_movie.html",methods=["POST","GET"])
def about_movie():
    return render_template("about_movie.html")

@app.route("/theatre.html",methods=["POST","GET"])
def theatre():
    return render_template("theatre.html")

@app.route("/ticket_booking.html",methods=["POST","GET"])
def ticket_booking():
    return render_template("ticket_booking.html")


if __name__=="__main__":
	app.run(debug = True)