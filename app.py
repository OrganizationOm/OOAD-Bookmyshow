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
    movie_data={}
    if request.method == "POST":
        movie_data=request.form['movie']
        f = open('movie_file.json')
        data=json.load(f)
        movie_data=data[movie_data]
    return render_template("about_movie.html", content = movie_data)

@app.route("/theatre.html",methods=["POST","GET"])
def theatre():
    movie_data={}
    theatre_data={}
    if request.method == "POST":
        movie_data=request.form['movie']
        f = open('movie_file.json')
        data=json.load(f)
        movie_data=data[movie_data]
        f = open('theatre_file.json')
        theatre_data=json.load(f)
        # print(theatre_data["Inox Multiplex"])

    return render_template("theatre.html", content = movie_data['name'] , theatres=theatre_data)

@app.route("/ticket_booking.html",methods=["POST","GET"])
def ticket_booking():
    movie_data=""
    theatre_name=""
    movie_time=""
    message=""
    if request.method == "POST":
        movie_data=request.form['movie']
        theatre_name=request.form['theatre_name']
        movie_time=request.form['movie_time']
        quantity=request.form['quantity']
        f = open('movie_file.json')
        data=json.load(f)
        movie_data=data[movie_data]
        if(quantity=="0"):
            message=""
        else:
            message="You have successfully booked "+quantity+" seats for the movie "+movie_data["name"]+" at "+movie_time+", "+theatre_name
        print("this is the "+quantity)
        print(movie_data)
        print(theatre_name)
        print(movie_time)

    
    return render_template("ticket_booking.html", content=movie_data, theatre_name=theatre_name, movie_time=movie_time, msg=message)


if __name__=="__main__":
	app.run(debug = True)