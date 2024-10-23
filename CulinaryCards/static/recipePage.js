var leftSide;
var rightSide;

// function to match the height of left and right side on recipe page
function matchHeight() {
    if(leftSide)
        console.log(leftSide.offsetHeight);
    else
        console.log("leftSide is null");
    if(rightSide)
        console.log(rightSide.style.height);
    else
        console.log("rightSide is null");
    rightSide.style.height = `${leftSide.offsetHeight - 250}px`;
}

function addComment() {
    const comment = document.getElementById('comment-box').value;
    const recipeid = document.getElementById('hidden-recipe-id').textContent;
    const currentTime = new Date().toISOString();

    const data = {
        recipeid: recipeid,
        comment: comment,
        comment_time: currentTime
    };

    fetch(`/api/addcomment/${recipeid}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            console.log(response)
            comment.value =""
            return response.json();
        } else {
            console.error("Failed to submit comment");
            console.log(response);
        }
    })
    .then(data => {
        if (data) {
            console.log(data)
            console.log("Comment ID:", data.commentid);
            const commentContainer = document.getElementById('comment-container');

            const newCommentDiv = document.createElement('div');
            newCommentDiv.classList.add('pure-g', 'pure-u-1', 'comment');
            newCommentDiv.id = 'comment-with-button';
            newCommentDiv.setAttribute('commentid', data.commentid);

            const profileLink = document.createElement("a")
            profileLink.href = `/profile?profile=${data.userid}`
            profileLink.textContent = data.username
            profileLink.classList.add('username-link')
            profileLink.classList.add("profileTag")
            profileLink.setAttribute('userid', data.userid)

            const commentTextDiv = document.createElement('div');
            commentTextDiv.classList.add('pure-u-22-24');
            commentTextDiv.appendChild(profileLink)
            let profileLinkText = document.createTextNode(`: ${comment}`)
            commentTextDiv.appendChild(profileLinkText)

            const deleteButton = document.createElement('button');
            deleteButton.classList.add('pure-u-1-24', 'delete-btn');
            deleteButton.id = 'delete-button';
            deleteButton.type = 'button';
            deleteButton.setAttribute('commentid', data.commentid);
            deleteButton.setAttribute('commentuserid', data.userid);
            deleteButton.setAttribute('onClick', 'deleteComment()');
            deleteButton.textContent = 'x';

            newCommentDiv.appendChild(commentTextDiv);
            newCommentDiv.appendChild(deleteButton);

            commentContainer.insertBefore(newCommentDiv, commentContainer.firstChild);
            document.getElementById('comment-box').value = "";
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

function deleteComment(commentId, commentUserId) {
    console.log(commentId)
    const recipeid = document.getElementById('hidden-recipe-id').innerText;

    const commentDiv = document.querySelector(`div[commentid="${commentId}"]`);
    if (commentDiv) {
        commentDiv.remove();
    }

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
        if (!response.ok) {
            console.error("Failed to submit comment");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}


async function updateSaved(recipeid) {
    let response = await fetch(`/api/setusersave/${recipeid}`, {
        method: 'GET'
    })
    if (response.ok){
        let status = await response.json()
        status = status.status
        console.log(status)
        const savedButton = document.getElementById("savedICON")
        if (status === "saved"){
            savedButton.style.filter = "brightness(0) saturate(100%) invert(43%) sepia(100%) saturate(746%) hue-rotate(356deg) brightness(100%) contrast(111%)"
        }
        else if (status === "unsaved"){
            savedButton.style.filter = "invert(97%) sepia(2%) saturate(2146%) hue-rotate(326deg) brightness(85%) contrast(97%)"
        }
        else{
            console.log("Error saving")
        }
    }
    else{
        console.log("Error saving")
    }
}


async function updateLiked(recipeid) {
    let response = await fetch(`/api/setuserlike/${recipeid}`, {
        method: 'GET'
    })
    if (response.ok){
        let status = await response.json()
        status = status.status
        console.log(status)
        const likedButton = document.getElementById("likedICON")
        const likecountDoc = document.getElementById("likes-count")
        let likecount = likecountDoc.innerText
        if (status === "liked"){
            likecount = parseInt(likecount) + 1
            likecountDoc.innerText = likecount
            likedButton.style.filter = "brightness(0) saturate(100%) invert(43%) sepia(100%) saturate(746%) hue-rotate(356deg) brightness(100%) contrast(111%)"
        }
        else if (status === "unliked"){
            likecount = parseInt(likecount) - 1
            likecountDoc.innerText = likecount
            likedButton.style.filter = "invert(97%) sepia(2%) saturate(2146%) hue-rotate(326deg) brightness(85%) contrast(97%)"
        }
        else{
            console.log("Error liking")
        }
    }
    else{
        console.log("Error liking")
    }
}

window.onload = function() {
    leftSide = document.getElementById('left-side');
    rightSide = document.getElementById('comment-container');
    matchHeight();
    window.addEventListener('resize', matchHeight);

    document.addEventListener('click', function(event) {
        if (event.target && event.target.classList.contains('delete-btn')) {
            var commentId = event.target.getAttribute('commentid');
            var commentUserId = event.target.getAttribute('commentuserid');
            deleteComment(commentId, commentUserId);
        }
    });
}