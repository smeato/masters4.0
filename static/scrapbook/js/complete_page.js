document.getElementById("search_button").addEventListener("click", getSpotifyResults, false);
// document.getElementById("yt_button").addEventListener("click", updateSrc, false);
document.getElementById("add_vid").addEventListener("click", saveYtEmbed, false);
document.getElementById("no_vid").addEventListener("click", gotoEnd, false);
document.getElementById("yt_search").addEventListener("click", getYtResults, false);

const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
var vid_id = "{{ page.vid_id }}"

window.onload = function () {
    //document.getElementById("yt_vid").src = "https://www.youtube.com/embed/" + vid_id;

}


async function getSpotifyResults() {
    var title = document.getElementById("song_title").value;
    var artist = document.getElementById("song_artist").value;

    // todo make error function
    if (title == null || title == "") {
        return;
    }


    fetch('song-search/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({ 'song_title': title, 'artist': artist })
    })
        .then(response => {
            return response.json();
        })
        .catch(err => console.log(err))
        .then(data => {

            if (data['resultsNum'] == 0) {
                document.getElementById("message").innerText = "No results. Check for typing errors, try searching without the artist/band or use fewer words. "
            }
            else {
                document.getElementById("message").innerText = ""
            }
            if (data['resultsNum'] > 0) {
                document.getElementById("embed1").setAttribute("src", data['result 1']);
                document.getElementById("button1").style = "display: block";
                document.getElementById("button1").addEventListener('click', getSong, false);
                document.getElementById("button1").addEventListener('click', nextSection, false);
            }
            if (data['resultsNum'] > 1) {
                document.getElementById("embed2").setAttribute("src", data['result 2']);
                document.getElementById("button2").style = "display: block";
                document.getElementById("button2").addEventListener('click', getSong, false);
                document.getElementById("button2").addEventListener('click', nextSection, false);
            }
            if (data['resultsNum'] > 2) {
                document.getElementById("embed3").setAttribute("src", data['result 3']);
                document.getElementById("button3").style = "display: block";
                document.getElementById("button3").addEventListener('click', getSong, false);
                document.getElementById("button3").addEventListener('click', nextSection, false);
            }
            if (data['resultsNum'] > 3) {
                document.getElementById("embed4").setAttribute("src", data['result 4']);
                document.getElementById("button4").style = "display: block";
                document.getElementById("button4").addEventListener('click', getSong, false);
                document.getElementById("button4").addEventListener('click', nextSection, false);
            }
        })

}

async function getSong(e) {
    let clicked = e.target.id;
    console.log(clicked);

    if (clicked == 'button1') {
        embed = document.getElementById("embed1").src;
    }
    else if ((clicked == 'button2')) {
        embed = document.getElementById("embed2").src;
    }
    else if (clicked == 'button3') {
        embed = document.getElementById("embed3").src;
    }
    else if (clicked == 'button4') {
        embed = document.getElementById("embed4").src;
    }


    fetch('song-save/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({ 'embed': embed, 'page_id': page_id })
    })
        .then(response => {
            return response.json();
        })
        .catch(err => console.log(err))
        .then(data => {
            document.getElementById("song_selection").style = "display: none";
            console.log(data['vid_required']);
            if (data['vid_required']) {
                document.getElementById("video_selection").style = "display: block";
                document.getElementById("add_vid").style = "display:none;"
                console.log("should be visible")
            }

        })
}


function getYtResults() {

    var q = document.getElementById("yt_q").value;
    if (q == '') {
        return;
    }

    authenticate().then(loadClient)
    execute(q);
}

// Make sure the client is loaded and sign-in is complete before calling this method.
function execute(query) {
    return gapi.client.youtube.search.list({
        "part": [
            "snippet"
        ],
        "maxResults": 5,
        "q": query,
        "type": [
            "video"
        ],
        "videoEmbeddable": "true"
    })
        .then(function (response) {
            // Handle the results here (response.result has the parsed body).
            console.log("Response", response);
        },
            function (err) { console.error("Execute error", err); });
}
gapi.load("client:auth2", function () {
    gapi.auth2.init({ client_id: yt_client_id });
});



function updateSrc() {
    link = document.getElementById("yt_link").value;
    if (link.includes('youtube')) {
        console.log(link.includes('youtube'));
        vid_id = link.split("watch?v=")[1];

    }
    else if (link.includes('youtu.be')) {
        console.log(link.includes('youtube'));
        vid_id = link.split("youtu.be/")[1];
    }
    document.getElementById("yt_vid").src = "https://www.youtube.com/embed/" + vid_id;
    document.getElementById("add_vid").style = "display: block;"
}



async function saveYtEmbed() {

    src = document.getElementById("yt_vid").src

    fetch('youtube-search/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({ 'src': src, 'page_id': page_id })
    })
        .then(response => {
            $("#yt_vid").load(window.location.href + " #yt_vid");
        })

    document.getElementById("video_selection").style = "display: none";
    document.getElementById("finished").style = "display: block";

}

function isValidYt(link) {
    return
}


function nextSection() {
    if (vid_required == true) {
        document.getElementById("video_selection").style = "display: block";
    }
    else {
        document.getElementById("finished").style = "display: block";
    }

    document.getElementById("song_selection").style = "display: none";
}


function gotoEnd() {
    document.getElementById("song_selection").style = "display: none";
    document.getElementById("video_selection").style = "display: none";
    document.getElementById("finished").style = "display: block";
}


// yt helper functions
function authenticate() {
    return gapi.auth2.getAuthInstance()
        .signIn({ scope: "https://www.googleapis.com/auth/youtube.force-ssl" })
        .then(function () { console.log("Sign-in successful"); },
            function (err) { console.error("Error signing in", err); });
}
function loadClient() {
    gapi.client.setApiKey(yt_key);
    return gapi.client.load("https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest")
        .then(function () { console.log("GAPI client loaded for API"); },
            function (err) { console.error("Error loading GAPI client for API", err); });
}