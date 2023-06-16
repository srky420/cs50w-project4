function load_posts(filter, page_num) {
    
    fetch(`/posts/${filter}?page=${page_num}`)
    .then(res => res.json())
    .then(data => {
        console.log(data)
        
        posts = data.posts;

        document.querySelector('#posts').innerHTML = `<h2 class="my-3">${filter} posts</h2>`;
        // For each post
        posts.forEach(post => {
            let html = `<div class="card my-3 w-100">
                            <div class="card-body">
                            <h5 class="card-title"><a href="#">${post.posted_by.username}</a></h5>
                            <small class="card-subtitle mb-2 text-body-secondary">${post.posted_on}</small>
                            <p class="card-text my-3">${post.content}</p>
                            <a href="#" class="card-link">Like</a>
                            <a href="#" class="card-link">Comment</a>
                            </div>
                        </div>`;
            document.querySelector('#posts').innerHTML += html;
        })



        if (data.next) {
            document.querySelector('#next-page-btn').classList.toggle('disabled'); 
        }

        if (data.previous) {
            document.querySelector('#prev-page-btn').classList.toggle('disabled');
        }

    })
    .catch(error => {
        console.log(error)
        
    })
}