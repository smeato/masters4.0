document.getElementById("add_button").addEventListener('click', checkCode, false)

const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

function checkCode() {
    code = document.getElementById("code_input").value
    console.log("reached")
    if (code == "") {
        return
    }

    fetch('add-with-code/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({ 'code': code })
    })
        .then(response => {
            return response.json();
        })
        .catch(err => console.log(err))
        .then(data => {
            console.log(data['user'])

        })
}