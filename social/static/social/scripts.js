function send_like(postPk, userPk, postId, csrf) {
    const aHrefLike = $('#' + postId);
    const isLiked = aHrefLike.hasClass('liked');
    const smallTextLikesCount = $('#' + postId).find("#post-likes-count");
    aHrefLike.toggleClass("liked");
    aHrefLike.toggleClass("heart");
    $.ajax({
        url: '/like/',
        type: 'POST',
        data: {
            'postId': postPk,
            'userId': userPk,
            csrfmiddlewaretoken: csrf,
        },
        success: function (data) {
            let likesCount = parseInt(data);
            smallTextLikesCount.text(likesCount);
        },
        error: function (data) {
            console.log(data);
        },
    });
}