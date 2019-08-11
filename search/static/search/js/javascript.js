function saveFavorite(entry) {
    event.preventDefault();
    let form = new FormData(entry);
    let req = new XMLHttpRequest();
    let id = entry.getAttribute("id");
    req.open("POST", "/accounts/favorites/new/");
    req.addEventListener("load", function () {
        if (req.status >= 200 && req.status < 400) {
            checkResponse(req.responseText, id);
        } else if (req.status === 403) {
            document.getElementsByTagName('html')[0].innerHTML = req.responseText;
        } else {
            console.error(req.status + " " + req.statusText);
        }
    });
    req.addEventListener("error", function () {
        console.error("Network error");
    });
    req.send(form);
}

function checkResponse(body, id) {
    let response = JSON.parse(body);
    let button_id = "save-" + id;
    if (response.error === "favorite already exists") {
        document.getElementById(button_id).className = "btn btn-outline-info";
        document.getElementById(button_id).innerText = "Sauvegarde";
        let newMessage = document.createElement("div");
        newMessage.className = "text-info";
        newMessage.innerText = "Ce produit est deja sauvegarder";
        document.getElementById(id).appendChild(newMessage);
    } else {
        document.getElementById(button_id).className = "btn btn-outline-success";
        document.getElementById(button_id).innerText = "Sauvegarde";
    }
}