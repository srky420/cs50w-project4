function like(post_id, like_btn) {
 
    post_id = parseInt(post_id);

    // Disable like btn
    like_btn.classList.add('disabled');

    // Toggle like
    fetch(`/like/${post_id}`)
        .then(res => res.json())
        .then(data => {
            console.log(data.msg);
            like_btn.classList.remove('disabled');

            let likes_count = parseInt(document.querySelector(`#post${post_id}`).innerHTML);
            console.log(likes_count);

            // Increase/Decrease likes count
            if (data.liked) {
                like_btn.innerHTML = `<i class="fa fa-thumbs-up"></i>`;
                likes_count++;
                document.querySelector(`#post${post_id}`).innerHTML = likes_count;
            }
            else {
                like_btn.innerHTML = `<i class="fa fa-thumbs-o-up"></i>`;
                likes_count--;
                document.querySelector(`#post${post_id}`).innerHTML = likes_count;
            }
        })
        .catch(error => {
            console.log(error);
            like_btn.classList.remove('disabled');
        })

}
