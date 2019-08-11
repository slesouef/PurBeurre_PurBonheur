function save_favorite(entry) {
    event.preventDefault();
    let form = new FormData(entry);
    let req = new XMLHttpRequest();
    req.open("POST", "/accounts/favorites/new/");
    req.addEventListener("load", function () {
        if (req.status >= 200 && req.status < 400) {
            console.log(req.responseText);
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