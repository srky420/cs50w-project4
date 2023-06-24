function comment(comment_btn) {
    // Get post id and comment
    const post_id = comment_btn.dataset.id;
    const comment = document.querySelector(`#comment${post_id}`).value;
    const post = document.querySelector(`#post${post_id}`);

    // Disabled comment button
    comment_btn.disabled = true;

    // Get csrf token from Cookies
    const csrf_token = Cookies.get('csrftoken');

    fetch(`/comment/${post_id}`, {
        method: 'POST',
        headers: {'X-CSRFToken': csrf_token},
        mode: 'same-origin',
        body: JSON.stringify({
            comment: comment
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data.profile_pic_url);
        console.log(data.comment);

        // Create new comment item
        let li = document.createElement('li');
        li.innerHTML = `<li>
                            <div class="row">
                                <div class="col-1 me-sm-2 mt-1">
                                    <img class="profile-pic profile-pic-sm" src="${data.profile_pic_url}" alt="profile-pic">
                                </div>
                                <div class="col-10">
                                    <a href="#" class="h6 link-dark link-underline-opacity-0 link-underline-opacity-100-hover">${data.username}</a>
                                    <p>${data.comment}</p>
                                </div>
                            </div>
                        </li>`;
        
        // Append li to comment list
        post.querySelector('.comment-list').append(li);
        post.querySelector('.comments-count').innerHTML = data.comments_count;

        // Empty comment field and enable comment button
        document.querySelector(`#comment${post_id}`).value = '';
        comment_btn.disabled = false;
    })
    .catch(error => {
        console.log(error);

        // Empty comment field and enable comment button
        document.querySelector(`#comment${post_id}`).value = '';
        comment_btn.disabled = false;
    })
}