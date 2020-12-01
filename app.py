from flask import Flask, request, session, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, UserInformation, RecentSongs, LikedSongs
from create_user_form import create_user
from forms import UserForm, LoginForm


if __name__ == "__main__":
    app.run(debug=True)

app = Flask(__name__)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///concertdiscovery"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "12345"
toolbar = DebugToolbarExtension(app)

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
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.email.errors.append("Email is taken, please provide another")
            return render_template("register.html", form=form)
        session["email"] = new_user.email
        flash("Thank you for joining!")
        return redirect("/")
    return render_template("register.html", form=form)


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