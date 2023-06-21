document.addEventListener('DOMContentLoaded', () => {
    // Get all like buttons
    const likeBtns = document.querySelectorAll('.like-btn');

    // Add event listener to each like button
    likeBtns.forEach(btn => {
        btn.addEventListener('click', (e) => like(e.currentTarget));
    });

    // Add event listener to follow button
    document.querySelector('#follow-btn').addEventListener('click', (e) => follow(e.currentTarget));

});