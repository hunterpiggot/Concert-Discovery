const playButton = document.getElementById("playButton")
const volumeSlider = document.getElementById("volume-slider")
const volumeDisplay = document.getElementById("volume-display")
volumeDisplay.innerHTML = volumeSlider.value

const currentTrack = document.getElementById("current-track")
const currentAlbumCover = document.getElementById("album-cover")
const currentArtist = document.getElementById("current-artist")
const lastSong = document.getElementById("previous-track")
const nextSong = document.getElementById("next-track")

const authCode = document.getElementById("auth-code").innerText

const lat = document.getElementById('latitude').innerText
const lng = document.getElementById('longitude').innerText
const searchRadius = document.getElementById("serachRadius").innerText

const likeBtn = document.getElementById("likeSong")
const dislikeBtn = document.getElementById("dislikeSong")
const songId = document.getElementById("song-id")

const notification = document.getElementById("concert-notification")
const artistNotification = document.getElementById("artist-notification")


const stubhubURL = 'https://api.stubhub.com/sellers/search/events/v3?performerName='

// when artist changes, check if the user has like them and the concert has not been show, if true, check if the artist has a concert coming up, if they do, show them the concert

setInterval( function() { 
  fetch(`/checkLikedSongs?songName=${currentTrack.innerText}&artist=${currentArtist.innerText.substring(4)}`, {
        method: 'GET'
      }).then(results => results.json()).then((data) => {
        if (data["ShowConcert"] == true){
          let url = stubhubURL + removeSpaces(currentArtist.innerText)
          console.log(url)
          console.log("HERE")
          fetch(url, {
          headers: {
          Accept: "application/json",
          Authorization: "Bearer rbSWVTH2iRdcTn5zIe8ifEfGlwCg"
            }
          }).then(response => response.json()).then(data => data['events'].map(x => distance(lat,lng,x['venue']['latitude'],x['venue']['longitude'])))
          // artistNotification.innerText = `${currentArtist.innerText} has a concert coming up in your area`
          // document.body.classList.add('active')
        }
      })
}, 20000)



likeBtn.addEventListener("click", function () {
  {
    // check stubhub API
    let url = stubhubURL + removeSpaces(currentArtist.innerText)
    console.log(url)
    console.log("HERE")
    fetch(url, {
    headers: {
      Accept: "application/json",
      Authorization: "Bearer rbSWVTH2iRdcTn5zIe8ifEfGlwCg"
      }
    }).then(response => response.json()).then(data => data['events'].map(x => distance(lat,lng,x['venue']['latitude'],x['venue']['longitude'])))
    // like the song in DB
    fetch('/likeSong', {
      method :"POST",
      headers: {
        'Content-Type': 'application/json',
        "Accept" :"application/json"
      },
      body: JSON.stringify({
        song: currentTrack.innerText,
        artist: currentArtist.innerText.substring(4),
        show: true,
        songId: songId.innerText
      })
    }).then(results => results.json()).then(data => console.log(data))
  }
})

dislikeBtn.addEventListener("click", function () {
  fetch('/dislikeSong', {
    method :"POST",
    headers: {
      'Content-Type': 'application/json',
      "Accept" :"application/json"
    },
    body: JSON.stringify({
      song: currentTrack.innerText,
      artist: currentArtist.innerText.substring(4),
      show: true,
      songId: songId.innerText
    })
  }).then(results => results.json()).then(data => console.log(data))
}
)


volumeSlider.oninput = function() {
  volumeDisplay.innerHTML = this.value
}

function removeSpaces (word) {
  return word.toString().substring(4).replace(/\s/g,"%20")
}



// Calculate distance from Location
function distance(lat1, lon1, lat2, lon2, unit) {
	if ((lat1 == lat2) && (lon1 == lon2)) {
		return 0;
	}
	else {
		var radlat1 = Math.PI * lat1/180;
		var radlat2 = Math.PI * lat2/180;
		var theta = lon1-lon2;
		var radtheta = Math.PI * theta/180;
		var dist = Math.sin(radlat1) * Math.sin(radlat2) + Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta);
		if (dist > 1) {
			dist = 1;
		}
		dist = Math.acos(dist);
		dist = dist * 180/Math.PI;
		dist = dist * 60 * 1.1515;
		if (unit=="K") { dist = dist * 1.609344 }
    if (unit=="N") { dist = dist * 0.8684 }
    console.log("CHEKING LIKED SONGS")
    // check_liked_song()
    if (dist < searchRadius) {
      artistNotification.innerText = `${currentArtist.innerText} has a concert coming up in your area`
      document.body.classList.add('active')
    }
		return dist;
	}
}




window.onSpotifyWebPlaybackSDKReady = () => {
    const token = authCode;
    const player = new Spotify.Player({
      name: 'Concert Discovery',
      getOAuthToken: cb => { cb(token); },
    });
  
    // Error handling
    // player.addListener('initialization_error', ({ message }) => { console.error(message); });
    // player.addListener('authentication_error', ({ message }) => { console.error(message); });
    // player.addListener('account_error', ({ message }) => { console.error(message); });
    // player.addListener('playback_error', ({ message }) => { console.error(message); });
  
    // // Playback status updates
    // player.addListener('player_state_changed', state => { console.log(state); });
  
    // Ready
    player.addListener('ready', ({ device_id }) => {
      // console.log('Ready with Device ID', device_id);
    });
  
    // Not Ready
    player.addListener('not_ready', ({ device_id }) => {
      // console.log('Device ID has gone offline', device_id);
    });

    player.setVolume(0.5).then(() => {
      // console.log('Volume updated!');
    });

    player.getVolume().then(volume => {
      let volume_percentage = volume * 100;
      // console.log(`The volume of the player is ${volume_percentage}%`);
    });
    
    playButton.addEventListener("click", function(){
      player.togglePlay().then(() => {
        // console.log('Toggled playback!');
      });
    })

    volumeSlider.addEventListener("mousemove", function() {
      player.setVolume(this.value/100).then(() => {
        // console.log('Volume updated!');
      });
    })

    player.addListener('player_state_changed', ({
      position,
      duration,
      track_window: { current_track }
    }) => {
      currentTrack.innerText = current_track["name"]
      currentAlbumCover.src = current_track["album"]["images"][0]["url"]
      currentArtist.innerText = "By: " + current_track["artists"][0]["name"]
      songId.innerText = current_track["id"]
      localStorage.setItem("currentArtist", current_track["artists"][0]["name"])

      // stubhubApiRequest(current_track["artists"][0]["name"])
      // console.log('Currently Playing', current_track);
      // console.log('Position in Song', position);
      // console.log('Duration of Song', duration);
    });

    lastSong.addEventListener("click", function () {
      player.previousTrack().then(() => {
        // console.log('Set to previous track!');
      });
    })

    nextSong.addEventListener("click", function () {
      player.nextTrack().then(() => {
        // console.log('Skipped to next track!');
      });
    })

    player.connect();

  };

