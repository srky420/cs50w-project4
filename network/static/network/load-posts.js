function load_posts(filter, page_num) {
    fetch(`/posts/${filter}?page=${page_num}`)
    .then(res => res.json())
    .then(posts => {
        console.log(posts)
        posts.forEach(post => {
            let div = document.createElement('div');
            div.innerHTML = `${post.posted_by.username}<br>${post.content}`;
            document.querySelector('#posts').append(div);
        })
        return true;
    })
    .catch(error => {
        console.log(error)
        return false;
    })
}