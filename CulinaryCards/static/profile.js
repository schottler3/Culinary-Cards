var username;
var bio;
var pfp;
var recipes;

function toggleEdit(location) {
    let editProfileContainer = document.getElementById('editProfileContainer');
    
    let editUsername = document.getElementById('editUsername');
    let editBio = document.getElementById('editBio');
    editUsername.value = username.innerHTML;
    editBio.value = bio.innerHTML;

    if(editProfileContainer.style.display === 'flex') {
        if(location.getAttribute('id') === 'editProfile') {
            pfpToggle();
        }
        editProfileContainer.style.display = 'none';
    } else {
        editProfileContainer.style.display = 'flex';
        let preview = document.getElementById('pfpPreview');
        preview.setAttribute('src', pfp.getAttribute('src'));
    }
}

async function submitEdit(event) {
    let newUsername = document.getElementById('editUsername').value;
    let newBio = document.getElementById('editBio').value;

    let isUser = await fetch("/api/isUser",{method : "PUT", headers : {"Content-Type" : "application/json"}, body: JSON.stringify(newUsername)});

    if(newUsername.length > 20 || newUsername.length < 3 || isUser.ok) {
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
    else if(newUsername === username.innerHTML && newBio === bio.innerHTML) {
        toggleEdit(event.target);
        return;
    }

    // This will change once we have a way to submit the user's new profile information

    let changes = {username : newUsername, bio : newBio}

    setProfileResponse = await fetch("/api/editprofile",{method : "PUT", headers : {"Content-Type" : "application/json"}, body: JSON.stringify(changes)});
    console.log(setProfileResponse.ok)
    if(setProfileResponse.ok){
        //setProfile();
        username = document.getElementById('username');
        username.innerText = newUsername
        bio = document.getElementById('bio');
        bio.innerText = newBio
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
    window.location.href = "/profile"
}

let changeToLiked = function() {
    console.log('Changing to liked recipes');
    window.location.href = "/profile/likes"
}

let changeToSaved = function() {
    console.log('Changing to saved recipes');
    window.location.href = "/profile/saved"
}

window.onload = function() {

    document.getElementById('sortProfileRecipes').addEventListener('change', sortRecipes);
}
