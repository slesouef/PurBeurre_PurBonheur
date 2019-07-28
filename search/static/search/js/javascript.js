function save_favorite(entry) {
    event.preventDefault();
    let form = new FormData(entry);
    let req = new XMLHttpRequest();
    req.open("POST", "/accounts/favorite/new/");
    req.addEventListener("load", function () {
        if (req.status >= 200 && req.status < 400) {
            console.log(req.responseText)
        } else {
            console.error(req.status + " " + req.statusText);
            // displayFatalErrorMessage();
        }
    });
    req.addEventListener("error", function () {
        console.error("Network error");
        // displayFatalErrorMessage();
    });
    req.send(form);
}