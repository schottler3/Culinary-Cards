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

function setPfp(input) {
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(stream) {
            const pfpPreview = document.getElementById('pfpPreview');
            pfpPreview.src = stream.target.result;
        }
        reader.readAsDataURL(file);
    } 
    uploadImage(file).then(() => {
        setProfile();
    });
}

function uploadImage(image){
    //send the image to the backend sql
}

function showImage(img) {
    img.style.display = 'block';
}

//This will change once we have a way to set the user's profile
function setProfile() {
    user = sessionStorage.getItem('user');

    pfp = document.getElementById('pfp');
    pfp.setAttribute('src', '../static/test.png');

    username = document.getElementById('username');
    //username.innerHTML = 'schottler3';

    bio = document.getElementById('bio');
    //bio.innerHTML = 'I like to cook and bake!';

    let numRecipes = document.getElementById('numberOfRecipes');
    //numRecipes.innerHTML = '0';

    let numLikes = document.getElementById('numberOfLikes');
    //numLikes.innerHTML = '0';
}

function submitPfp() {
    const pfpPreview = document.getElementById('pfpPreview');
    const imageSrc = pfpPreview.src;

    pfpToggle();

    // This will change once we have a way to submit the user's profile picture
}

function sortRecipes() {
    let sort = document.getElementById('sortProfileRecipes').value;
    console.log('Sorting recipes: ' + sort);
    // This will change once we have a way to sort the user's recipes
}

let changeToMy = function() {
    console.log('Changing to my recipes');
    // Change the view of recipes shown to the user's recipes
}

let changeToLiked = function() {
    console.log('Changing to liked recipes');
    // Change the view of recipes shown to the user's liked recipes
}

let changeToSaved = function() {
    console.log('Changing to saved recipes');
    // Change the view of recipes shown to the user's saved recipes
}

window.onload = function() {
    setProfile();

    document.getElementById('sortProfileRecipes').addEventListener('change', sortRecipes);

    setRecipes();
}
