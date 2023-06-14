function get_posts(filter, page_num) {
    fetch(`/posts/${filter}?page=${page_num}`)
    .then(res => res.json())
    .then(posts => console.log(posts))
    .catch(error => console.log(error))
}