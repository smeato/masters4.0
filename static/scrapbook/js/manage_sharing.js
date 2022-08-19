const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
// document.getElementById("add_button").addEventListener('click', addCollab, false);
document.getElementById("code_button").addEventListener('click', copyCode, false);


window.onload = function () {
    addListeners();
}

function addListeners() {
    let buttons = document.getElementsByClassName('remove');
    for (let button of buttons) {
        let id = button.getAttribute('id');
        console.log(id)

        document.getElementById(id).addEventListener('click', function (e) {

            fetch('update/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrf_token,
                },
                body: JSON.stringify({ 'removed_collab': id })
            })
                .then(response => {
                    document.getElementById(id).innerHTML = "REMOVED";
                }, false)
        });

    }
}

function copyCode() {
    var code = document.getElementById("code");
    code.select();
    code.setSelectionRange(0, 99999);
    navigatornavigator.clipboard.writeText(copyText.value);
    alert("Code Copied");
}

// function addCollab() {
//     username = document.getElementById("user_add").value;
//     if (username) {
//         fetch('add/', {
//             method: 'POST',
//             credentials: 'same-origin',
//             headers: {
//                 'Accept': 'application/json',
//                 'X-Requested-With': 'XMLHttpRequest',
//                 'X-CSRFToken': csrf_token,
//             },
//             body: JSON.stringify({ 'add_collab': username })
//         })
//             .catch(err => console.log(err))
//             .then(data => {
//                 document.getElementById("user_add").value = "";
//                 document.getElementById("add_button").innerHTML = "added";
//                 document.getElementById("add_button").style = "background-color: green;";

//                 setTimeout(() => {
//                     document.getElementById("add_button").innerHTML = "Add";
//                     document.getElementById("add_button").style = "background-color: #4C651A;";

//                 }, 2000);



//             })
//     }
// }

