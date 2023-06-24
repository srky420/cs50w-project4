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
        li.innerHTML = `<li id="comment${data.comment_id}">
                            <div class="row">
                                <div class="col-1 me-sm-2 mt-1">
                                    <img class="profile-pic profile-pic-sm" src="${data.profile_pic_url}" alt="profile-pic">
                                </div>
                                <div class="col-10 position-relative">
                                    <a href="/profile/${data.user_id}" class="h6 link-dark link-underline-opacity-0 link-underline-opacity-100-hover">${data.username}</a>
                                    <small class="text-muted ms-2">${data.created_on} ago</small>
                                    <p>${data.comment}</p>
                                    <button class="btn btn-outline-danger btn-sm border-0 p-2 py-1 position-absolute" 
                                        data-id="${data.comment_id}" data-postid="${post_id}" style="top: 0; right: 0;" onclick="delete_comment(this)">
                                        <i class="fa fa-trash-o"></i>
                                    </button>
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

function delete_comment(delete_btn) {
    // Get elements
    const comment_id = delete_btn.dataset.id;
    const post_id = delete_btn.dataset.postid;

    // Disable button
    delete_btn.disabled = true;

    fetch(`/comment/delete/${comment_id}`)
    .then(res => res.json())
    .then(data => {
        console.log(data);

        // Remove deleted comment
        document.querySelector(`#comment${comment_id}`).remove();

        // Update comments count
        document.querySelector(`#post${post_id}`).querySelector('.comments-count').innerHTML = data.comments_count;
    })
    .catch(error => {
        console.log(error);
        delete_btn.disabled = false;
    })

}