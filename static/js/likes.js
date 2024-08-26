document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-button');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.dataset.postId;
            const userId = this.dataset.userId;
            const likeCount = this.querySelector('.like-count');

            fetch(`/like/${userId}/${postId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                likeCount.textContent = data.likes;
                if (data.action === 'liked') {
                    this.classList.add('text-blue-500');
                } else {
                    this.classList.remove('text-blue-500');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});