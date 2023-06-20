document.addEventListener('DOMContentLoaded', () => {
    
    const likeBtns = document.querySelectorAll('.like-btn');

    likeBtns.forEach(btn => {
        btn.addEventListener('click', (e) => like(e.currentTarget.dataset.post, e.currentTarget))
    });

});