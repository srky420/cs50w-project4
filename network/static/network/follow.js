function follow(follow_btn) {

    // Disable follow button
    follow_btn.disabled = true;
    const user_id = follow_btn.dataset.id;

    fetch(`/profile/${user_id}/follow`)
        .then(res => res.json())
        .then(data => {
            console.log(data);

            // Toggle follow button
            if (data.follow) {
                follow_btn.innerHTML = `<i class="fa fa-close"></i> Unfollow`;
            }
            else {
                follow_btn.innerHTML = `<i class="fa fa-check"></i> Follow`;
            }

            // Update followers and followings count
            document.querySelector('#follower-count').innerHTML = data.followers_count;
            document.querySelector('#followings-count').innerHTML = data.followings_count;

            // Enable follow button
            follow_btn.disabled = false;
        })
        .catch(error => {
            console.log(error);

            // Enable follow button
            follow_btn.disabled = false;
        })
}