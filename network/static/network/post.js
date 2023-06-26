function edit(edit_btn) {
    post_id = edit_btn.dataset.id;

    // Get this post's elements
    const post = document.querySelector(`#post${post_id}`);
    const postContent = post.querySelector('.post-content').innerHTML;
    const textArea = post.querySelector('.edit-textarea');

    // Set text area to content
    textArea.value = postContent;

    // Add event listener to save changes button
    post.querySelector('.save-btn').addEventListener('click', (e) => save(textArea.value, post, post_id));
}

function save(content, post, post_id) {
    // Disable modal buttons
    post.querySelector('.save-btn').disabled = true;
    post.querySelector('.close-btn').disabled = true;
    post.querySelector('.btn-close').disabled = true;

    // Get csrf token from cookies
    const csrf_token = Cookies.get('csrftoken');

    // PUT content to server
    fetch(`/edit/${post_id}`, {
        method: "PUT",
        headers: {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/json'
        },
        mode: 'same-origin',
        body: JSON.stringify({
            content: content
        })
    })
    .then(() => {
        // Enable modal buttons
        post.querySelector('.save-btn').disabled = false;
        post.querySelector('.close-btn').disabled = false;
        post.querySelector('.btn-close').disabled = false;

        // Close modal and set post content to new content
        post.querySelector('.close-btn').click();
        post.querySelector('.post-content').innerHTML = content;
    })
    .catch(error => {
        console.log(error);
        post.querySelector('.save-btn').disabled = false;
        post.querySelector('.close-btn').disabled = false;
    })
}

function delete_post(delete_btn) {
    
    const post_id = delete_btn.dataset.id;
    const post = document.querySelector(`#post${post_id}`);

    // Create an overlay for loading
    const overlay = document.createElement('div');
    overlay.classList.add('overlay');
    overlay.innerHTML = `<div class="d-flex justify-content-center align-items-center h-100">
                            <div class="spinner-border" role="status">
                            <span class="visually-hidden">Loading...</span>
                            </div>
                        </div>`;
    post.append(overlay);

    fetch(`/delete/${post_id}`)
        .then(res => res.json())
        .then(data => {
            console.log(data);
            post.remove();
        })
        .catch(error => {
            console.log(error);
            overlay.remove();
        })
}