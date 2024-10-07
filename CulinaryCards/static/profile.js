var username;
var bio;
var pfp;

let setRecipes = function() {
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

let toggleEdit = function() {
    let editProfileContainer = document.getElementById('editProfileContainer');
    if(editProfileContainer.style.display === 'block') {
        pfpToggle();
    } else {
        editProfileContainer.style.display = 'block';
        let preview = document.getElementById('pfpPreview');
        preview.setAttribute('src', pfp.getAttribute('src'));
    }
}

let pfpToggle = function() {
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
}

//This will change once we have a way to set the user's profile
let setProfile = function() {
    user = sessionStorage.getItem('user');

    pfp = document.getElementById('pfp');
    pfp.setAttribute('src', '../static/test.png');

    username = document.getElementById('username');
    username.innerHTML = 'schottler3';

    bio = document.getElementById('bio');
    bio.innerHTML = 'I like to cook and bake!';

    let numRecipes = document.getElementById('numberOfRecipes');
    numRecipes.innerHTML = '0';

    let numLikes = document.getElementById('numberOfLikes');
    numLikes.innerHTML = '0';
}

let submitPfp = function() {
    const pfpPreview = document.getElementById('pfpPreview');
    const imageSrc = pfpPreview.src;

    pfpToggle();

    // This will change once we have a way to submit the user's profile picture
}

let sortRecipes = function() {
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
