document.addEventListener('click', function(event) {
    if (event.target && event.target.classList.contains('delete-btn')) {
        var commentId = event.target.getAttribute('commentid');
        var commentUserId = event.target.getAttribute('commentuserid');
        deleteComment(commentId, commentUserId);
    }
});

const leftSide = document.getElementById('left-side');
const rightSide = document.getElementById('comment-container');

console.log(leftSide);
console.log(rightSide);

// function to match the height of left and right side on recipe page
function matchHeight() {
    rightSide.style.height = `${leftSide.offsetHeight - 250}px`;
}

function addComment() {
    const comment = document.getElementById('comment-box').value;
    const recipeid = document.getElementById('hidden-recipe-id').innerText;
    const currentTime = new Date().toISOString();

    const data = {
        recipeid: recipeid,
        comment: comment,
        comment_time: currentTime
    };

    fetch(`/recipe/${recipeid}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            console.error("Failed to submit comment");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

function deleteComment(commentId, commentUserId) {
    console.log(commentId)
    const recipeid = document.getElementById('hidden-recipe-id').innerText;

    const data = {
        commentid: commentId,
        recipeid: recipeid,
        commentuserid: commentUserId
    };

    fetch(`/recipe/${recipeid}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            console.error("Failed to submit comment");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}


matchHeight();
window.addEventListener('resize', matchHeight);