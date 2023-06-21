function follow(follow_btn) {
    follow_btn.disabled = true;
    user_id = follow_btn.dataset.id;

    fetch(`/profile/${user_id}/follow`)
        .then(res => res.json())
        .then(data => {
            console.log(data.msg);
            
            let follower_count = parseInt(document.querySelector('#follower-count').innerHTML);

            if (data.follow) {
                follow_btn.innerHTML = `<i class="fa fa-close"></i> Unfollow`;
                follower_count++;
                document.querySelector('#follower-count').innerHTML = follower_count;
            }
            else {
                follow_btn.innerHTML = `<i class="fa fa-check"></i> Follow`;
                follower_count--;
                document.querySelector('#follower-count').innerHTML = follower_count;
            }

            follow_btn.disabled = false;
        })
        .catch(error => {
            console.log(error);
            follow_btn.disabled = false;
        })
}