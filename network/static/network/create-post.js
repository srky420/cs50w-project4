function create_post(content) {
    fetch('/create-post', {
        method: 'POST',
        body: JSON.stringify({
            content: content
        })
    })
    .then(res => res.json())
    .then(msg => console.log(msg))
    .catch(error => console.log(error));
}