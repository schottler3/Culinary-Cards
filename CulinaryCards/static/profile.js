
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
    let pfp = document.getElementById('pfp');
    pfp.setAttribute('src', '../static/test.png');

    let username = document.getElementById('username');
    username.innerHTML = 'schottler3';

    let numRecipes = document.getElementById('numberOfRecipes');
    numRecipes.innerHTML = '0';

    let numLikes = document.getElementById('numberOfLikes');
    numLikes.innerHTML = '0';

    document.getElementById('sortProfileRecipes').addEventListener('change', sortRecipes);

    setRecipes();
}
