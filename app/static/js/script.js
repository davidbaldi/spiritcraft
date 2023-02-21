function toggleCardLike(cardId) {
    var cardURL = "/cards/toggle_card_like";
    var heartButtonStatus = document.getElementById('heartButton' + cardId);
    var heartImage = document.getElementById("heartImage" + cardId);
    console.log("HEARTIMAGESRC? " + heartImage.src)
    var cardIdObject = {
        cardId: cardId,
        heartButtonStatus: heartButtonStatus.ariaPressed
        };
    var cardIdJSON = JSON.stringify(cardIdObject);

    // console.log("aria-pressed: " + heartButtonStatus.ariaPressed);
    // console.log("heartImage.src: " + heartImage.src);
    // console.log("cardIdObject: " + cardIdObject);
    // console.log("cardIdJSON: " + cardIdJSON);

    // if (heartButtonStatus.ariaPressed === true) {
    //     heartButton.src = "/static/img-liked.png";
    // } else if (heartButtonStatus.ariaPressed === false) {
    //     heartButton.src = "/static/img-unliked.png";
    // };

    fetch(cardURL, {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(cardIdJSON)
        })
    .then(response => response.json())
    .then(response => {
        console.log(JSON.stringify(response));
        if (response.heartButtonStatus == "true") {
            console.log("TRUE " + heartImage.src);
            heartImage.src = "http://localhost:5000/static/img-liked.png";
            heartButtonStatus.ariaPressed = false;
        } else if (response.heartButtonStatus == "false") {
            console.log("FALSE " + heartImage.src);
            heartImage.src = "http://localhost:5000/static/img-unliked.png";
            heartButtonStatus.ariaPressed = true;
        };
    });
};