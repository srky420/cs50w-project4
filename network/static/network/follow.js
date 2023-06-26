function follow(follow_btn) {

    follow_btn.disabled = true;
    const user_id = follow_btn.dataset.id;

    fetch(`/profile/${user_id}/follow`)
        .then(res => res.json())
        .then(data => {
            console.log(data.msg);

            if (data.follow) {
                follow_btn.innerHTML = `<i class="fa fa-close"></i> Unfollow`;
            }
            else {
                follow_btn.innerHTML = `<i class="fa fa-check"></i> Follow`;
            }

            document.querySelector('#follower-count').innerHTML = data.followers_count;
            document.querySelector('#followings-count').innerHTML = data.followings_count;

            follow_btn.disabled = false;
        })
        .catch(error => {
            console.log(error);
            follow_btn.disabled = false;
        })
}