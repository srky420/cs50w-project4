function get_profile(id) {
    fetch(`/profile/${id}`)
    .then(res => res.json())
    .then(info => console.log(info))
    .catch(error => console.log(error))
}