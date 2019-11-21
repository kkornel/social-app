function send_like(postId, userId, id, csrf) {
    // const aHrefLike = $('#' + id);
    // const isLiked = aHrefLike.hasClass('liked');
    const smallTextLikesCount = $('#' + id).find("#post-likes-count");
    // const likesCountText = smallTextLikesCount.text();
    // let likesCount = parseInt(likesCountText);

    // if (isLiked) {
    //     likesCount -= 1;
    // } else {
    //     likesCount += 1;
    // }
    // smallTextLikesCount.text(likesCount);

    // aHrefLike.toggleClass("liked");
    // aHrefLike.toggleClass("heart");
    console.log(postId);
    console.log(userId);
    console.log(id);
    $.ajax({
        url: '/like/',
        type: 'POST',
        data: {
            'postId': postId,
            'userId': userId,
            csrfmiddlewaretoken: csrf,
        },
        success: function (data) {
            console.log('Liked!');
            console.log(data);
            let likesCount = parseInt(data);
            smallTextLikesCount.text(likesCount);
        },
        error: function (data) {
            console.log(data);
        },
    });
}