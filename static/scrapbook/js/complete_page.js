document.getElementById("search_button").addEventListener("click", getSpotifyResults, false);
document.getElementById("yt_button").addEventListener("click", updateSrc, false);
document.getElementById("add_vid").addEventListener("click", saveYtEmbed, false);

const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
var vid_id = "{{ page.vid_id }}"

window.onload = function () {
    //document.getElementById("yt_vid").src = "https://www.youtube.com/embed/" + vid_id;
}

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
            document.getElementById("embed1").setAttribute("src", data['result 1']);
            if (document.getElementById("embed1").src != "") {
                document.getElementById("button1").style = "display: block";
                document.getElementById("button1").addEventListener('click', getSong, false);
                document.getElementById("button1").addEventListener('click', nextSection, false);

            }
            document.getElementById("embed2").setAttribute("src", data['result 2']);
            if (document.getElementById("embed2").src != "") {
                document.getElementById("button2").style = "display: block";
                document.getElementById("button2").addEventListener('click', getSong, false);
            }
            document.getElementById("embed3").setAttribute("src", data['result 3']);
            if (document.getElementById("embed3").src != "") {
                document.getElementById("button3").style = "display: block";
                document.getElementById("button3").addEventListener('click', getSong, false);
            }
            document.getElementById("embed4").setAttribute("src", data['result 4']);
            if (document.getElementById("embed4").src != "") {
                document.getElementById("button4").style = "display: block";
                document.getElementById("button4").addEventListener('click', getSong, false);
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
        embed = document.getElementById("embed1").src;
    }
    else if (clicked == 'button3') {
        embed = document.getElementById("embed1").src;
    }
    else if (clicked == 'button4') {
        embed = document.getElementById("embed1").src;
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

            if (data['vid_required']) {
                document.getElementById("video_selection").style = "display: block";
            }

        })
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