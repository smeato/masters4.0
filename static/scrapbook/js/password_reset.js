document.getElementById("unknown_email").addEventListener("click", showUsername, false)
document.getElementById("username_button").addEventListener("click", getHint, false)
document.getElementById("unknown_username").addEventListener("click", showSorry, false)

const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

function showUsername() {
    document.getElementById("username_section").style = "display: block;";
    document.getElementById("unknown_email").style = "display:none;";
}

function getHint() {
    username = document.getElementById("username").value
    console.log(username)
    fetch('check-username/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({ 'username': username })
    })
        .then(response => {
            return response.json();
        })
        .catch(err => console.log(err))
        .then(data => {

            if (data['relationship'] == 'none') {
                document.getElementById("errors").value = 'There is no account with that username registered.'
            }
            else {
                document.getElementById("username_section").style = "display:none;";
                document.getElementById("username_hint").style = "display:block;"
            }

            if (data['relationship'] == 'own') {
                document.getElementById("recovery_relationship").innerHTML = 'you';
            }
            else if (data['relationship'] == 'partner/spouse') {
                document.getElementById("recovery_relationship").innerHTML = 'your partner or spouse';
            }
            else if (data['relationship'] == 'child') {
                document.getElementById("recovery_relationship").innerHTML = 'your child';
            }
            else if (data['relationship'] == 'friend') {
                document.getElementById("recovery_relationship").innerHTML = 'a friend';
            }
            else if (data['relationship'] == 'carer') {
                document.getElementById("recovery_relationship").innerHTML = 'a carer or assistant';
            }




        })


}

function showSorry() {
    document.getElementById("username_section").style = "display: none;";
    document.getElementById("email").style = "display: none;";
    document.getElementById("sorry").style = "display:block;";
}