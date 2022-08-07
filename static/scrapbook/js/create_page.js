document.getElementById("title_button").addEventListener("click", function () { saveInput("title_input") }, false);
document.getElementById("title_button").addEventListener("click", function () { showNext("song_section") }, false);
document.getElementById("song_button").addEventListener("click", function () { saveInput("song_input") }, false);
document.getElementById("song_button").addEventListener("click", function () { saveInput("artist_input") }, false);
document.getElementById("song_button").addEventListener("click", function () { showNext("picture_section") }, false);
document.getElementById("picture_button").addEventListener("click", function () { saveInput("picture_input") }, false);
document.getElementById("picture_button").addEventListener("click", function () { showNext("video_section") }, false);
document.getElementById("video_button").addEventListener("click", function () { saveInput("video_input") }, false);
document.getElementById("video_button").addEventListener("click", function () { saveInput("youtube_input") }, false);
document.getElementById("video_button").addEventListener("click", function () { showNext("finish") }, false);


var url = 'create-page/' + '{{username}}'
const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value

function showNext(section) {
    document.querySelectorAll('div').forEach(div => {
        div.style.display = 'none';
    })

    // Show the div provided in the argument
    document.querySelector(`#${section}`).style.display = 'block';
}


async function saveInput(inputName) {

    var input = document.getElementById(inputName).value;

    if (input == null) {
        return;
    }

    fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({ 'post_data': input })
    })
        .then(response => {
            return response.json()
        })
}
