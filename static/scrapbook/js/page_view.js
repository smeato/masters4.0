const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

let add_button = document.getElementById("add");
add_button.addEventListener("click", function (e) {
    let text = document.getElementById("add_note").value;
    let title = document.getElementById("title_input").value;

    fetch('page/add-note/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({ 'note': text, 'title': title, 'page_pk': page_pk })
    })
        .then(response => {

            return response.json();
        })
        .catch(err => console.log(err))
        .then(data => {
            document.getElementById("add_note").value = "";
            document.getElementById("title_input").value = "";
            document.getElementById("add").innerHTML = "added";
            document.getElementById("add").style = "background-color: green";

            setTimeout(() => {
                document.getElementById("add").innerHTML = "Add Note";
                document.getElementById("add").style = "background-color: #4C651A";

            }, 2000);



        })
})