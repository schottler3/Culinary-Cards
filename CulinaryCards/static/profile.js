var recipes;

function toggleEdit(location) {
    let editProfileContainer = document.getElementById('editProfileContainer');
    
    let editUsername = document.getElementById('editUsername');
    let editBio = document.getElementById('editBio');
    editUsername.value = username;
    editBio.value = bio;

    if(editProfileContainer.style.display === 'flex') {
        if(location.getAttribute('id') === 'editProfile') {
            pfpToggle();
        }
        editProfileContainer.style.display = 'none';
    } 
    else {
        editProfileContainer.style.display = 'flex';
        let preview = document.getElementById('pfpPreview');
        preview.setAttribute('src', document.getElementById('pfp').getAttribute('src'));
    }
}

async function submitEdit(event) {
    let newUsername = document.getElementById('editUsername').value;
    let newBio = document.getElementById('editBio').value;

    let isUser = false;
    await fetch("/api/isuser?username=" + newUsername)
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            isUser = true;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        return false;
    });

    if(newUsername == username) {
        isUser = false;
    }

    if(newUsername.length > 20 || newUsername.length < 3 || isUser ) {
        usernameError.style.display = 'block';
        return;
    }
    else {
        usernameError.style.display = 'none';
    }

    if(newUsername.length < 3) {
        alert('Username must be at least 3 characters long');
        return;
    }
    else if(newBio.length > 200) {
        alert('Bio must be less than 200 characters long');
        return;
    }
    else if(newUsername === username && newBio === bio) {
        toggleEdit(event.target);
        return;
    }

    // This will change once we have a way to submit the user's new profile information

    let changes = {username : newUsername, bio : newBio}

    setProfileResponse = await fetch("/api/editprofile",{method : "PUT", headers : {"Content-Type" : "application/json"}, body: JSON.stringify(changes)});
    console.log(setProfileResponse.ok)
    if(setProfileResponse.ok){
        username = newUsername;
        bio = newBio;
        document.getElementById('username').innerText = newUsername;
        document.getElementById('bio').innerText = newBio;
        toggleEdit(event.target);
    }
    
}

function pfpToggle() {
    let pfpSelect = document.getElementById('pfpSelect');
    let pfpGrayBackground = document.getElementById('pfpGrayBackground');
    if(pfpGrayBackground.style.display === 'block') {
        pfpGrayBackground.style.display = 'none';
        pfpSelect.style.display = 'none';
    } else {
        pfpGrayBackground.style.display = 'block';
        pfpSelect.style.display = 'grid';
    }
}

function setPfpPreview(input) {
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(stream) {
            const pfpPreview = document.getElementById('pfpPreview');
            pfpPreview.src = stream.target.result;
        }
        reader.readAsDataURL(file);
    } 
}

async function setPfp(){
    let image = document.getElementById('pfpInput').files[0]

    let binary = new FormData()
    binary.append("newpfp",image)
    let response = await fetch("/api/editprofilepicture",{method : "PUT", body: binary})
    if (response.ok){
        window.location.reload()
    }
}

function submitPfp() {
    const pfpPreview = document.getElementById('pfpPreview');
    const imageSrc = pfpPreview.src;
    pfpToggle();
}

function sortRecipes() {
    let sort = document.getElementById('sortProfileRecipes').value;
    console.log('Sorting recipes: ' + sort);
    // This will change once we have a way to sort the user's recipes
}

let changeToMy = function() {
    console.log('Changing to my recipes');
    console.log(userId)
    window.location.href = `/profile?profile=${userId}`
}

let changeToLiked = function() {
    console.log('Changing to liked recipes');
    window.location.href = `/profile/likes?profile=${userId}`
}

let changeToSaved = function() {
    console.log('Changing to saved recipes');
    window.location.href = "/profile/saved"
}

let toggleSettings = function() {
    let profileContainerAll = document.getElementById('profileContainerAll');
    let accountSettings = document.getElementById('accountSettings');
    let accountDeletionConfirmation = document.getElementById('accountDeletionConfirmation');
    if(profileContainerAll.style.display === 'none') {
        profileContainerAll.style.display = 'block';
        accountSettings.style.display = 'none';
        if(accountDeletionConfirmation.style.display === 'block') {
            accountDeletionConfirmation.style.display = 'none';
            pfpGrayBackground.style.display = 'none';
        }
    }
    else{
        profileContainerAll.style.display = 'none';
        accountSettings.style.display = 'block';
    }
}

let toggleDeletion = function() {
    let accountDeletionConfirmation = document.getElementById('accountDeletionConfirmation');
    let pfpGrayBackground = document.getElementById('pfpGrayBackground');
    if(accountDeletionConfirmation.style.display === 'none') {
        accountDeletionConfirmation.style.display = 'block';
        pfpGrayBackground.style.display = 'block';
    }
    else{
        accountDeletionConfirmation.style.display = 'none';
        pfpGrayBackground.style.display = 'none';
    }
}

async function deleteAccount(){
    let call = await fetch("/api/deleteaccount",{method : "DELETE"})
    if(call.ok){
        alert("Account Deleted")
        window.location.href = "/"
    }
}

window.onload = function() {
    var accountGear = document.getElementById('accountGear');
    if (accountGear != null){
    accountGear.addEventListener('click', function() {
        if(accountGear.classList.contains('spin')) {
            accountGear.classList.remove('spin');
            accountGear.classList.add('spinBack');
        }
        else {
            if(accountGear.classList.contains('spinBack')) {
                accountGear.classList.remove('spinBack');
            }
            accountGear.classList.add('spin');
        }
        toggleSettings();
    });}

    let href = window.location.href;
    if(href.includes('profile/likes')) {
        document.getElementById('liked').style.fontWeight = 'bold';
    }
    else if(href.includes('profile/saved')) {
        document.getElementById('saved').style.fontWeight = 'bold';
    }
    else {
        document.getElementById('my').style.fontWeight = 'bold';
    }
}
