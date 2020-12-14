from flask import (
    Flask,
    request,
    session,
    redirect,
    render_template,
    flash,
    url_for,
    Response,
    jsonify,
)
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, UserInformation, RecentSongs, LikedSongs
from create_user_form import create_user
from forms import UserForm, LoginForm

import requests

from config import *


app = Flask(__name__)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///concertdiscovery"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "12345"
toolbar = DebugToolbarExtension(app)
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)


connect_db(app)


@app.route("/")
def home_page():
    if "email" not in session:
        flash("Please Log in", "danger")
        return redirect("/register")
    else:
        return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = UserForm()
    if form.validate_on_submit():
        new_user = create_user(form)
        email = new_user.email
        db.session.add(new_user)
        db.session.commit()
        # try:
        #     db.session.commit()
        # except IntegrityError:
        #     form.email.errors.append("Email is taken, please provide another")
        #     return render_template("register.html", form=form)
        session["email"] = new_user.email
        return redirect(url_for("get_lat_long", email=email))
    return render_template("register.html", form=form)


def remove_space(city):
    return city.replace(" ", "%20")


@app.route("/get_lat_long/<email>")
def get_lat_long(email):
    user = UserInformation.query.filter_by(email=email).first()
    city = user.city
    state = user.state
    url = (
        "http://open.mapquestapi.com/geocoding/v1/address?key=TjM9QJlI2AYMCCkqtzSTVmVW73ZzYwaL&location="
        + remove_space(city)
        + ","
        + state
    )
    response = requests.get(url)
    lat = response.json()["results"][0]["locations"][0]["latLng"]["lat"]
    lng = response.json()["results"][0]["locations"][0]["latLng"]["lng"]
    user.latitude = lat
    user.longitude = lng
    db.session.add(user)
    db.session.commit()
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = UserInformation.authenticate(email, password)
        if user:
            flash(f"Welcome Back! {user.first_name}!", "primary")
            session["email"] = user.email
            return redirect("/")
        else:
            form.email.errors = ["Invalid email/password"]
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/music/<auth_code>")
def music_page(auth_code):
    user = UserInformation.query.filter_by(email=session["email"]).first()
    lat = user.latitude
    lng = user.longitude
    searchRadius = user.search_radius
    return render_template(
        "testMusicPage.html",
        auth_code=auth_code,
        lat=lat,
        lng=lng,
        searchRadius=searchRadius,
    )


@app.route("/authorize", methods=["GET", "POST"])
def authorize():
    code = request.args.get("code")
    if request.method == "GET":
        headers = {
            "Authorization": "Basic ODlmZmQ1MTQ1NWZhNDExM2IxYzNhYjU4NDk2YzA5NzA6MmI1ZDYzYmY4YjhiNDVkN2JmN2Y1OTk4OGIzYTlkMWI=",
        }

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://127.0.0.1:5000/authorize",
        }

        response = requests.post(
            "https://accounts.spotify.com/api/token", headers=headers, data=data
        )
        auth_code = response.json()["access_token"]
        session["refreshToken"] = response.json()["refresh_token"]
        if auth_code:
            return redirect(url_for("music_page", auth_code=auth_code))


@app.route("/likeSong", methods=["GET", "POST"])
def like_song():
    data = request.json
    user = LikedSongs.query.filter_by(email=session["email"]).all()

    duplicate = False
    for song in user:
        if data["song"] == song.song_name and data["artist"] == song.artist_name:
            duplicate = True

    if not duplicate:
        song = LikedSongs(
            email=session["email"],
            song_name=data["song"],
            artist_name=data["artist"],
            liked=True,
            shown_concert=False,
        )
        db.session.add(song)
        db.session.commit()
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": Authorization,
        }

        params = (
            (
                "ids",
                data["songId"],
            ),
        )

        response = requests.put(
            "https://api.spotify.com/v1/me/tracks", headers=headers, params=params
        )
        data = {"success": True}
        return data
    data = {"success": False}
    return data


@app.route("/dislikeSong", methods=["GET", "POST"])
def dislike_song():
    data = request.json
    user = LikedSongs.query.filter_by(email=session["email"]).all()
    duplicate = False
    for song in user:
        if data["song"] == song.song_name and data["artist"] == song.artist_name:
            song.liked = False
            db.session.commit()
            duplicate = True
    if not duplicate:
        song = LikedSongs(
            email=session["email"],
            song_name=data["song"],
            artist_name=data["artist"],
            liked=False,
            shown_concert=False,
        )
        db.session.add(song)
        db.session.commit()
        data = {"success": True}
        return data
    data = {"success": True}
    return data


@app.route("/likedSongs")
def users_liked_songs():
    user = LikedSongs.query.filter_by(email=session["email"]).all()
    return render_template("users_liked_songs.html", user=user)


def update_concert_to_liked(user, data):
    for song in user:
        if data["artist"].lower() == song.artist_name.lower():
            song.shown_concert = True
            db.session.commit()


@app.route("/checkLikedSongs", methods=["GET"])
def check_liked_songs():
    data = request.args
    user = LikedSongs.query.filter_by(email=session["email"]).all()
    for song in user:
        if (
            data["songName"].lower() == song.song_name.lower()
            and data["artist"].lower() == song.artist_name.lower()
            and song.liked == True
            and song.shown_concert == False
        ):
            update_concert_to_liked(user, data)
            song.shown_concert = True
            db.session.commit()
            data = {"ShowConcert": True}
            return data
    return {"ShowConcert": False}
