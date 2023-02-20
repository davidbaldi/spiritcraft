function toggleCardLike(cardId) {
    var cardURL = "/cards/like_or_unlike_card";
    var heartImage = document.getElementById("heartImage" + cardId).src;
    var cardIdJSON = {"cardId": cardId};
    console.log(heartImage);

    fetch(cardURL) {

    }
};