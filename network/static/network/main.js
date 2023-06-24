document.addEventListener('DOMContentLoaded', () => {
    // Add event listener to each like button
    const likeBtns = document.querySelectorAll('.like-btn');
    likeBtns.forEach(btn => {
        btn.addEventListener('click', (e) => like(e.currentTarget));
    });

    // Add event listener to comment button
    const commentBtns = document.querySelectorAll('.comment-btn');
    commentBtns.forEach(btn => {
        btn.addEventListener('click', (e) => comment(e.currentTarget));
    });

    // Add event listener to edit button
    const editBtns = document.querySelectorAll('.edit-btn');
    editBtns.forEach(btn => {
        btn.addEventListener('click', (e) => edit(e.currentTarget));
    });

    // Add event listener to follow button
    document.querySelector('#follow-btn').addEventListener('click', (e) => follow(e.currentTarget));

});