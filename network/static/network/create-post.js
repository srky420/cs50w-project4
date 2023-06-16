function create_post() {

    // Get csrf token from cookie
    const csrf_token = Cookies.get('csrftoken');
    console.log(csrf_token);

    // Get input data
    const content = document.querySelector('#post-content').value;

    // Send post request to server with csrf token
    fetch('/create-post', {
        method: 'POST',
        headers: {'X-CSRFToken': csrf_token},
        mode: 'same-origin',
        body: JSON.stringify({
            content: content
        })
    })
    .then(res => res.json())
    .then(msg => {
        console.log(msg);
        document.querySelector('#post-content').value = '';
        load_posts('all');
    })
    .catch(error => console.log(error));
}