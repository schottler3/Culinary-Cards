var selectedCategories = [];
var title;
var description;
var ingredients = [];
var instructions = [];

function getCategories() {
    //backend integration later
    return ['Breakfast', 'Lunch', 'Dinner', 'Dessert', 'Snack', 'Drink'];
}

function populateCategories(){
    let categoriesList = getCategories();
    let dropdown = document.getElementById('dropdown');
    for(let category of categoriesList) {
        let option = document.createElement('div');
        option.setAttribute('class', 'option');
        option.addEventListener('click', function() {
            let selected = option.textContent;
            if(selectedCategories.includes(selected)) {
                return;
            } else {
                selectedCategories.push(selected);
            }
            let selectedCategoriesList = document.querySelector('#selectedCategories .pure-menu-list');
            let selectedCategory = document.createElement('li');
            selectedCategory.setAttribute('class', 'pure-menu-item');
            let category = document.createElement('a');
            category.setAttribute('class', 'pure-menu-link');
            category.addEventListener('click', function() {
                let index = selectedCategories.indexOf(selected);
                if (index > -1) {
                    selectedCategories.splice(index, 1);
                }
                selectedCategoriesList.removeChild(selectedCategory);
            });
            category.textContent = selected;
            selectedCategory.appendChild(category);
            selectedCategoriesList.appendChild(selectedCategory);
        });
        option.textContent = category;
        dropdown.appendChild(option);
    }
}

function toggleDropdown() {
    let dropdown = document.getElementById('dropdown');
    if(dropdown.style.display === 'none' || dropdown.style.display === '') {
        dropdown.style.display = 'flex';
    } else {
        dropdown.style.display = 'none';
    }
}

//Credit to w3schools for this function:
//https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_js_dropdown_filter
function filterFunction() {
    const input = document.getElementById("search");
    const filter = input.value.toUpperCase();
    const div = document.getElementById("dropdown");
    const a = div.getElementsByTagName("div");
    for (let i = 0; i < a.length; i++) {
        txtValue = a[i].textContent || a[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
        a[i].style.display = "";
        } else {
        a[i].style.display = "none";
        }
    }
}

function submitTitle() {
    const form = document.getElementById('createRecipeOne');
    title = form.querySelector('#recipeTitle').value;
    if(title === '') {
        alert('Title is required, silly!');
        return;
    }
    description = form.querySelector('#recipeDescription').value;
    if(description === '') {
        alert('Description is required, silly!');
        return;
    }

    form.style.display = 'none';
    let formTwo = document.getElementById('createRecipeTwo');
    formTwo.style.display = 'block';
}

window.onload = function() {
    populateCategories();
    
}


