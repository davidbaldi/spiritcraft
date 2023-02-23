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
            heartImage.src = "static/img-liked.png";
            heartButton.ariaPressed = true;
        } else if (response.isCardLiked == "false") {
            heartImage.src = "static/img-unliked.png";
            heartButton.ariaPressed = false;
        };
    });
};

function toggleGenusOrOrder(value) {
    var genusField = document.getElementById("card_genus");
    var orderField = document.getElementById("card_order");

    switch(value) {
        case "Entity":
            genusField.disabled = false;
            orderField.disabled = true;
            break;
        case "Helper":
        case "Item":
            genusField.disabled = true;
            orderField.disabled = false;
            break;
        default:
            genusField.disabled = true;
            orderField.disabled = true;
    }
};

function togglePriceField(value) {
    var priceField = document.getElementById("price");
    var quantityField = document.getElementById("quantity");

    if (value == "Out of stock") {
        priceField.disabled = true;
        quantityField.disabled = true;
    } else if (value != "Out of stock") {
        priceField.disabled = false;
        quantityField.disabled = false;
    }
}

function toggleCardIssueField(value) {
    var TypeField = document.getElementById("card_type");
    var genusField = document.getElementById("card_genus");
    var orderField = document.getElementById("card_order");

    if (value == "collectable") {
        TypeField.disabled = true;
        genusField.disabled = true;
        orderField.disabled = true;
    } else if (value == "playable") {
        TypeField.disabled = false;
        genusField.disabled = false;
        orderField.disabled = false;
    }
}