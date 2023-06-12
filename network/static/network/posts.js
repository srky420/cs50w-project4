function get_posts(filter) {
    fetch(`/posts/${filter}`)
    .then(res => res.json())
    .then(posts => console.log(posts))
}