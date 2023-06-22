function edit(edit_btn) {

    post_id = edit_btn.dataset.id;

    const post = document.querySelector(`#post${post_id}`);
    const postContent = post.querySelector('.post-content').innerHTML;
    console.log(postContent);
    post.querySelector('.edit-textarea').value = postContent;
}