function toggleCardLike(cardId) {
    var cardURL = "/cards/toggle_card_like";
    var heartButton = document.getElementById('heartButton' + cardId);
    var heartImage = document.getElementById("heartImage" + cardId);
    var cardIdObject = {
        cardId: cardId,
        isCardLiked: heartButton.ariaPressed
        };
    var cardIdJSON = JSON.stringify(cardIdObject);

    fetch(cardURL, {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(cardIdJSON)
        })
    .then(response => response.json())
    .then(response => {
        if (response.isCardLiked == "true") {
            heartImage.src = "http://localhost:5000/static/img-liked.png";
            heartButton.ariaPressed = true;
        } else if (response.isCardLiked == "false") {
            heartImage.src = "http://localhost:5000/static/img-unliked.png";
            heartButton.ariaPressed = false;
        };
    });
};