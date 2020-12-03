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






volumeSlider.oninput = function() {
  volumeDisplay.innerHTML = this.value
}

window.onSpotifyWebPlaybackSDKReady = () => {
    const token = authCode;
    console.log(authCode)
    const player = new Spotify.Player({
      name: 'Concert Discovery',
      getOAuthToken: cb => { cb(token); },
    });
  
    // Error handling
    player.addListener('initialization_error', ({ message }) => { console.error(message); });
    player.addListener('authentication_error', ({ message }) => { console.error(message); });
    player.addListener('account_error', ({ message }) => { console.error(message); });
    player.addListener('playback_error', ({ message }) => { console.error(message); });
  
    // Playback status updates
    player.addListener('player_state_changed', state => { console.log(state); });
  
    // Ready
    player.addListener('ready', ({ device_id }) => {
      console.log('Ready with Device ID', device_id);
    });
  
    // Not Ready
    player.addListener('not_ready', ({ device_id }) => {
      console.log('Device ID has gone offline', device_id);
    });

    player.setVolume(0.5).then(() => {
      console.log('Volume updated!');
    });

    player.getVolume().then(volume => {
      let volume_percentage = volume * 100;
      console.log(`The volume of the player is ${volume_percentage}%`);
    });
    
    playButton.addEventListener("click", function(){
      player.togglePlay().then(() => {
        console.log('Toggled playback!');
      });
    })

    volumeSlider.addEventListener("mousemove", function() {
      player.setVolume(this.value/100).then(() => {
        console.log('Volume updated!');
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
      console.log('Currently Playing', current_track);
      console.log('Position in Song', position);
      console.log('Duration of Song', duration);
    });

    lastSong.addEventListener("click", function () {
      player.previousTrack().then(() => {
        console.log('Set to previous track!');
      });
    })

    nextSong.addEventListener("click", function () {
      player.nextTrack().then(() => {
        console.log('Skipped to next track!');
      });
    })

    player.connect();

  };


// function pause(){
//   player.pause().then(() => {
//     console.log('Paused!');
//   });
// }