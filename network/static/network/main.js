document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#allposts-btn').addEventListener('click', () => load_posts('all'));
    document.querySelector('#following-btn').addEventListener('click', () => load_posts('followings'));
    document.querySelector('#create-post-btn').addEventListener('click', () => create_post());

    
});