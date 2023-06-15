document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#allposts-btn').addEventListener('click', () => load_posts('all'));
    document.querySelector('#followings-btn').addEventListener('click', () => load_posts('followings'));

    load_posts("all", 1);
});