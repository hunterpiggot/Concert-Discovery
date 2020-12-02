from models import db, connect_db, UserInformation, RecentSongs, LikedSongs
from app import app

db.drop_all()
db.create_all()

u1 = UserInformation(
    email = "hunterpiggot@gmail.com",
    first_name= "Hunter",
    last_name= "Piggot",
    password = "Password",
    city = "Colorado Springs",
    state="CO",
    search_radius = 90
)
u2 = UserInformation(
    email = "piggothunter@gmail.com",
    first_name= "Apollo",
    last_name= "Piggot",
    password = "Password123",
    city = "Colorado Springs",
    state="CO",
    search_radius = 5
)
u3 = UserInformation(
    email = "hpiggot@gmail.com",
    first_name= "Anthony",
    last_name= "Coronado",
    password = "123456789",
    city = "Suprize",
    state="AZ"
)

rs1 = RecentSongs(
    email="hunterpiggot@gmail.com",
    song_name="Neighbors",
    artist_name="J. Cole"
)
rs2 = RecentSongs(
    email="piggothunter@gmail.com",
    song_name="Icon",
    artist_name="Jaden"
)
rs3 = RecentSongs(
    email="hpiggot@gmail.com",
    song_name="A.D.H.D",
    artist_name="Kendrick Lamar"
)
rs4 = RecentSongs(
    email="hunterpiggot@gmail.com",
    song_name="8701",
    artist_name="JID"
)
rs5 = RecentSongs(
    email="piggothunter@gmail.com",
    song_name="Caitlyn",
    artist_name="Jank"
)

ls1 = LikedSongs(
    email="hunterpiggot@gmail.com",
    song_name="Neighbors",
    artist_name="J. Cole",
    liked=True,
    shown_concert = False
)

ls2 = LikedSongs(
    email="piggothunter@gmail.com",
    song_name="Icon",
    artist_name="Jaden",
    shown_concert = False
)
ls3 = LikedSongs(
    email="hpiggot@gmail.com",
    song_name="A.D.H.D",
    artist_name="Kendrick Lamar",
    liked=False,
    shown_concert = False
)
ls4 = LikedSongs(
    email="hunterpiggot@gmail.com",
    song_name="8701",
    artist_name="JID",
    liked=True,
    shown_concert = True
)
ls5 = LikedSongs(
    email="piggothunter@gmail.com",
    song_name="Caitlyn",
    artist_name="Jank",
    liked=True,
    shown_concert = False
)

db.session.add(u1)
db.session.add(u2)
db.session.add(u3)
db.session.commit()
db.session.add(rs1)
db.session.add(rs2)
db.session.add(rs3)
db.session.add(rs4)
db.session.add(rs5)
db.session.commit()
db.session.add(ls1)
db.session.add(ls2)
db.session.add(ls3)
db.session.add(ls4)
db.session.add(ls5)
db.session.commit()