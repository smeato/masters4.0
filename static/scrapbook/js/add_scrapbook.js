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
            if (data['user'] != 'none') {
                document.getElementById("add_button").innerHTML = 'added';
                document.getElementById("message").innerText = "Added successfully! Click 'Home'to view your available scrapbooks.";
                console.log(index);
                window.location.replace(index);
            }
            else {
                document.getElementById("message").innerText = "This code does not match any scrapbooks."
            }
            document.getElementById("code_input").value = " ";
        })
}

