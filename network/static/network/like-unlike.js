function like(like_btn) {
 
    const post_id = like_btn.dataset.id;
    const post = document.querySelector(`#post${post_id}`);

    // Disable like btn
    like_btn.classList.add('disabled');

    // Toggle like
    fetch(`/like/${post_id}`)
        .then(res => res.json())
        .then(data => {
            console.log(data.msg);
            like_btn.classList.remove('disabled');

            // Increase/Decrease likes count
            if (data.liked) {
                like_btn.innerHTML = `<i class="fa fa-thumbs-up"></i>`;
            }
            else {
                like_btn.innerHTML = `<i class="fa fa-thumbs-o-up"></i>`;
            }

            // Set likes count
            post.querySelector('.likes-count').innerHTML = data.likes_count;
        })
        .catch(error => {
            console.log(error);
            like_btn.classList.remove('disabled');
        })

}
