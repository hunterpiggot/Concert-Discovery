from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """ Connects to the Database """
    db.app = app
    db.init_app(app)


class UserInformation(db.Model):
    """ This is to store basic information on the such as login info and search options"""

    __tablename__ = "users"

    ########## user informaion ############
    email = db.Column(db.Unicode(length=50), primary_key=True)
    first_name = db.Column(db.Unicode(length=50), nullable=False)
    last_name = db.Column(db.Unicode(length=50), nullable=False)
    password = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    search_radius = db.Column(db.Integer, default=100)
    ######## relationships ########
    recent = db.relationship(
        "RecentSongs", cascade="all,delete", backref="users", passive_deletes=True
    )
    liked = db.relationship(
        "LikedSongs", cascade="all,delete", backref="users", passive_deletes=True
    )

    ############ Register User ############
    @classmethod
    def register(cls, email, first, last, pwd, city, state, search):
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        return cls(
            email=email,
            password=hashed_utf8,
            first_name=first,
            last_name=last,
            city=city,
            state=state,
            search_radius=search,
        )

    ############# Authenticate User ############
    @classmethod
    def authenticate(cls, email, pwd):
        """Validates if user exists and if the password is correct
        Returns user if valid, flase if its not"""

        u = UserInformation.query.filter_by(email=email).first()
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False

    ############### DUNDER METHOD ########################
    def __repr__(self):
        return f"<UserInformation {self.email} fist_name={self.first_name} last_name={self.last_name} >"


class RecentSongs(db.Model):
    """ This is all the recent songs that will have the user, artist, and song"""

    __tablename__ = "recent"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(
        db.Unicode(length=50), db.ForeignKey("users.email", ondelete="CASCADE")
    )
    song_name = db.Column(db.Text, nullable=False)
    artist_name = db.Column(db.Text, nullable=False)

    ############### DUNDER METHOD ########################
    def __repr__(self):
        return f"<RecentSongs {self.email} song_name={self.song_name} artist_name={self.artist_name} >"


class LikedSongs(db.Model):
    """ This will have the user and the songs they likes, disliked or did neither with """

    __tablename__ = "liked"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(
        db.Unicode(length=50), db.ForeignKey("users.email", ondelete="CASCADE")
    )
    song_name = db.Column(db.Text, nullable=False)
    artist_name = db.Column(db.Text, nullable=False)
    liked = db.Column(db.Boolean)
    shown_concert = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<LikedSongs {self.email} song_name={self.song_name} artist_name={self.artist_name} liked={self.liked} artist_name={self.shown_concert} >"
