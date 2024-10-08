var username;
var bio;
var pfp;

function setRecipes() {
    let profileRecipesContainer = document.getElementById('profileRecipesContainer');
    
    // This will change once we have a way to get the user's recipes from db
    let numRecipes = 10;

    let createRecipeTile = document.createElement('div');
    createRecipeTile.setAttribute('class', 'pure-u-1 pure-u-sm-1-3 pure-u-md-1-4 pure-u-lg-1-5 pure-u-xl-1-6 createRecipeTile ');
    createRecipeTile.innerHTML = '+';
    createRecipeTile.addEventListener('click', function() {
        window.location.href = '/createRecipe';
    });
    profileRecipesContainer.appendChild(createRecipeTile);

    for (let i = 0; i < numRecipes; i++) {
        let recipe = document.createElement('div');
        recipe.setAttribute('class', 'pure-u-1 pure-u-sm-1-3 pure-u-md-1-4 pure-u-lg-1-5 pure-u-xl-1-6 profileRecipe');
        profileRecipesContainer.appendChild(recipe);
    }
}

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

function checkUsername() {
    let newUsername = document.getElementById('editUsername').value;
    let usernameError = document.getElementById('usernameError');

    //This will need a sql call to check if the username is already taken
    let existingUsernames = ['schottler3', 'testUser', 'user123'];
    if(newUsername.length > 20 || existingUsernames.includes(newUsername)) {
        usernameError.style.display = 'block';
    }
    else {
        usernameError.style.display = 'none';
    }
}

async function submitEdit(event) {
    let newUsername = document.getElementById('editUsername').value;
    let newBio = document.getElementById('editBio').value;

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
        username.value = newUsername
        bio = document.getElementById('bio');
        bio.value = newBio
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
