
// $(document).ready(function() {
//     const URL = 'https://accounts.spotify.com/authorize?client_id=89ffd51455fa4113b1c3ab58496c0970&response_type=code&redirect_uri=http://127.0.0.1:5000/%2Fcallback&scope=user-read-private%20user-read-email&state=34fFs29kd09'
//     $('#apiTest').click(function () {
//         $.ajax({
//             url: URL,
//             type: "GET",
//             success: function (result) {
//                 console.log(result)
//             },
//             error: function(error) {
//                 console.log(`Error: ${error}`)
//             }
//         })
//     })
// })

// const Http = new XMLHttpRequest();
// const url='https://accounts.spotify.com/authorize?client_id=89ffd51455fa4113b1c3ab58496c0970&response_type=code&redirect_uri=http://127.0.0.1:5000/';

// $(document).ready(function(){
//     $("#apiTest").click(function(){
//       $.get(url, function(){
//         console.log("You made it")
//       });
//     });
//   });