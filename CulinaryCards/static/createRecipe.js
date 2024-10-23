var selectedCategories = [];
var title = "Chicken Alfredo";
var currentStep = 1;
var description;
var ingredients = [];
var instructions = [];
var photo;
var url;
var unitSystem = '';

var lastEdit = '';

//Units for ingredients to have in dropdown
const units = {
    imperial: ['count','tsp', 'tbsp', 'floz', 'cup', 'pint', 'quart', 'gallon', 'oz', 'lb','pinch'],
    metric: ['count','ml', 'l', 'g', 'kg', 'mg','pinch']
};

//Starting ID for ingredients
var ingredientID = 0;

function nextStep() {
    switch(currentStep) {
        case 1:
            if(submitTitle()){
                if(!recipeid && unitSystem == '')
                    showUnits();
                else{
                    showStepTwo();
                }
                currentStep++;
            }
            break;
        case 2:
            if(submitIngredients()){
                showStepThree();
                currentStep++;
            }
            break;
        case 3:
            if(submitInstructions()){
                toggleNext();
                showStepFour();
                currentStep++;
            }
            break;
    }
}

let previousStep = function() {
    switch(currentStep) {
        case 2:
            let form = document.getElementById('createRecipeOne');
            form.style.display = 'flex';
            let Two = document.getElementById('createRecipeTwo');
            Two.style.display = 'none';
            currentStep--;
            toggleBack();
            break;
        case 3:
            let formTwo = document.getElementById('createRecipeTwo');
            formTwo.style.display = 'block';
            let Three = document.getElementById('createRecipeThree');
            Three.style.display = 'none';
            currentStep--;
            break;
        case 4:
            let formThree = document.getElementById('createRecipeThree');
            formThree.style.display = 'block';
            let formFour = document.getElementById('createRecipeFour');
            formFour.style.display = 'none';
            toggleNext();
            currentStep--;
            break;
    }
}

let toggleBack = function() {
    let back = document.getElementById('backStep');
    if(back.style.display === 'none' || back.style.display === '') {
        back.style.display = 'flex';
    }
    else {
        back.style.display = 'none';
    }
}

let toggleNext = function() {
    let next = document.getElementById('submitStep');
    if(next.style.display === 'none' || next.style.display === '') {
        next.style.display = 'flex';
    }
    else {
        next.style.display = 'none';
    }
}

//====================================================================================================
//Title, Categories, and Description
//====================================================================================================

//Backend call to get the current categories
function getCategories() {
    //backend integration later
    return ['Breakfast', 'Lunch', 'Dinner', 'Dessert', 'Snack', 'Drink'];
}

//Categories dropdown populations as well as functionality defining what happens when a category is selected
function populateCategories(){
    let categoriesList = getCategories();
    let dropdown = document.getElementById('dropdown');
    //Create a dropdown option for each category
    for(let category of categoriesList) {
        //Create a div for the category
        let option = document.createElement('div');
        option.setAttribute('class', 'option');

        //Add category to selected categories
        option.addEventListener('click', function() {
            let selected = option.textContent;
            if(selectedCategories.includes(selected)) {
                return;
            } 
            else {
                selectedCategories.push(selected);
            }

            //Get the selected categories list and create a new list item for the selected category
            let selectedCategoriesList = document.querySelector('#selectedCategories .pure-menu-list');
            let selectedCategory = document.createElement('li');
            selectedCategory.setAttribute('class', 'pure-menu-item');
            let category = document.createElement('a');
            category.setAttribute('class', 'pure-menu-item');

            //Remove category from selected categories
            category.addEventListener('click', function() {
                let index = selectedCategories.indexOf(selected);
                if (index > -1) {
                    selectedCategories.splice(index, 1);
                }
                selectedCategoriesList.removeChild(selectedCategory);
            });

            //Add category to selected categories
            category.textContent = selected;
            selectedCategory.appendChild(category);
            selectedCategoriesList.appendChild(selectedCategory);
        });
        //Add category to dropdown
        option.textContent = category;
        dropdown.appendChild(option);
    }
}

let categoryFlag = false;

//Function to toggle the dropdown visibility
function toggleDropdown() {
    let dropdown = document.getElementById('dropdown');
    if(dropdown.style.display === 'none' || dropdown.style.display === '') {
        dropdown.style.display = 'flex';
        categoryFlag = true;
    } 
    else {
        dropdown.style.display = 'none';
        categoryFlag = false;
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

//Function to submit the title and description of the recipe
//Also hides the title and description form and shows the units form
function submitTitle() {
    const form = document.getElementById('createRecipeOne');
    title = form.querySelector('#recipeTitle').value;
    if(title === '') {
        alert('Title is required!');
        return false;
    }
    description = form.querySelector('#recipeDescription').value;
    if(description === '') {
        alert('Description is required!');
        return false;
    }

    if(selectedCategories.length === 0) {
        alert('At least one category is required!');
        console.log(selectedCategories)
        return false;
    }

    form.style.display = 'none';

    return true
}

//Function to show the units form
function showUnits() {
    let submitStep = document.getElementById('submitStep');
    submitStep.style.display = 'none';
    let showUnits = document.getElementById('showUnits');
    showUnits.style.display = 'block';
}

//Function to set the units to imperial from the UnitsForm
//Also hides the units form and shows the ingredients form
function setUnitsImperial() {
    unitSystem = 'imperial';
    const unitsDropdown = document.getElementById('ingredientUnit');

    unitsDropdown.innerHTML = '<option value="">Select Unit</option>';

    units["imperial"].forEach(unit => {
        const option = document.createElement('option');
        option.value = unit;
        option.textContent = unit;
        unitsDropdown.appendChild(option);
    });
    
    if(!recipeid)
        showStepTwo();
}

//Function to set the units to metric from the UnitsForm
//Also hides the units form and shows the ingredients form
function setUnitsMetric() {
    unitSystem = 'metric';
    const unitsDropdown = document.getElementById('ingredientUnit');

    unitsDropdown.innerHTML = '<option value="">Select Unit</option>';

    units["metric"].forEach(unit => {
        const option = document.createElement('option');
        option.value = unit;
        option.textContent = unit;
        unitsDropdown.appendChild(option);
    });

    if(!recipeid)
        showStepTwo();
}

//====================================================================================================
//Ingredients
//====================================================================================================

//Function to show the ingredients form
function showStepTwo() {
    toggleBack();
    let submitStep = document.getElementById('submitStep');
    submitStep.style.display = 'flex';
    let showUnits = document.getElementById('showUnits');
    let formTwo = document.getElementById('createRecipeTwo');
    showUnits.style.display = 'none';
    formTwo.style.display = 'block';
}

//Function to add an ingredient to the ingredients list
function addIngredient() {
    let baseIngredient = document.getElementById('baseIngredient');
    let ingredientName = baseIngredient.querySelector('#ingredientName');
    let ingredientAmount = baseIngredient.querySelector('#ingredientAmount');
    let ingredientFraction = baseIngredient.querySelector('#ingredientFraction');
    let ingredientUnit = baseIngredient.querySelector('#ingredientUnit');

    let ingredientNameValue = ingredientName.value;
    let ingredientAmountValue = ingredientAmount.value;
    let ingredientFractionValue = ingredientFraction.value;
    let ingredientUnitValue = ingredientUnit.value;

    //Check if all fields are filled out correctly
    if(ingredientNameValue === '') {
        alert('Ingredient name is required!');
        return false;
    }
    else if(ingredientNameValue.includes(',')){
        alert('Ingredient name cannot contain a comma');
        return false;
    }
    else if(ingredientAmountValue === '' && ingredientFractionValue === '') {
        alert('Ingredient amount or fraction is required!');
        return false;
    }
    else if(!/^\d+$/.test(ingredientAmountValue) && ingredientFractionValue === ''){
        alert('Invalid Ingredient Amount');
        return false;
    }
    if (ingredientFractionValue !== '' && !/^([1-9][0-9]*)\/([1-9][0-9]*)$/.test(ingredientFractionValue)) {
        alert('Invalid Fractional Amount');
        return false;
    }
    else if(ingredientUnitValue === '') {
        alert('Ingredient unit is required!');
        return false;
    }

    //Create a new ingredient object and add it to the ingredients list
    ID = ingredientID++;

    let ingredient = {
        ID: ID,
        name: ingredientNameValue,
        amount: ingredientAmountValue,
        fraction: ingredientFractionValue,
        unit: ingredientUnitValue,
    };

    let newIngredient = baseIngredient.cloneNode(true);
    newIngredient.querySelector('#ingredientName').id=`ingredientName${ID}`;
    newIngredient.querySelector('#ingredientAmount').id=`ingredientAmount${ID}`;
    newIngredient.querySelector('#ingredientFraction').id=`ingredientFraction${ID}`;
    newIngredient.querySelector('#ingredientUnit').value = ingredientUnitValue;
    newIngredient.querySelector('#ingredientUnit').id=`ingredientUnit${ID}`;
    newIngredient.id = `ingredient${ID}`;

    //Add an event listener for changing the already created ingredient
    newIngredient.addEventListener('change', function(event) {
        adjustIngredient(event.target);
    });

    let ingredientsDiv = document.getElementById('ingredients');

    //Add a remove button to the ingredient
    let removeButton = document.createElement('img');
    removeButton.src = '/static/resources/remove.png';
    removeButton.setAttribute('class', 'pure-u-1-3 pure-u-md-1-4 removeButton');
    removeButton.setAttribute('id', `removeButton${ID}`);
    removeButton.addEventListener('click', function(event) {
        removeIngredient(event.target);
    });
    newIngredient.appendChild(removeButton);

    ingredientsDiv.appendChild(newIngredient);

    //Clear the fields for the base ingredient (input)
    ingredientName.value = '';
    ingredientAmount.value = '';
    ingredientFraction.value = '';
    ingredientUnit.value = '';

    ingredients.push(ingredient);

    //Show the added ingredients title now that there is an ingredient
    let addedIngredientsTitle = document.getElementById('addedIngredientsTitle');
    addedIngredientsTitle.style.display = 'block';

    console.log(ingredients);
    return true
}

//Function to adjust an ingredient in the ingredients list (HTML & JS)
function adjustIngredient(changed) {
    let fieldChanged = changed.id.replace(/\d+/g, '');
    let ID = changed.id.replace(fieldChanged, '');
    var value = changed.value;

    //Check if the ingredient is in the ingredients list
    //If it is, adjust the field that was changed
    for(let curIngredient of ingredients) {
        if(curIngredient.ID == ID) {
            switch(fieldChanged) {
                case 'ingredientName':
                    if(value === '') {
                        alert('Ingredient name is required. \nRemove the ingredient using the "X" button if you want to delete this ingredient.');
                        changed.value = curIngredient.name;
                        return false;
                    }
                    else{
                        curIngredient.name = value;
                        break; 
                    }
                case 'ingredientAmount':
                    if(value === '' || !/^\d+$/.test(value)) {
                        alert('Ingredient amount is required. \nRemove the ingredient using the "X" button if you want to delete this ingredient.');
                        changed.value = curIngredient.amount;
                        return false;
                    }
                    else {
                        curIngredient.amount = value;
                        break;
                    }
                case 'ingredientFraction':
                    if (value !== '' && !/^\d+\/\d+$/.test(value)) {
                        alert('Invalid Fractional Amount');
                        changed.value = curIngredient.fraction;
                        return false;
                    }
                    else {
                        curIngredient.fraction = value;
                        break;
                    }
                case 'ingredientUnit':
                    if(value === '') {
                        alert('Ingredient unit is required. \nRemove the ingredient using the "X" button if you want to delete this ingredient.');
                        changed.value = curIngredient.unit;
                        return false;
                    }
                    else {
                        curIngredient.unit = value;
                        break;
                    }
            }
        }
    }

    console.log(ingredients);
}

//Function to remove an ingredient from the ingredients list
function removeIngredient(button) {
    let ID = button.id.replace('removeButton', '');
    console.log(ID);
    let ingredientsListDiv = document.getElementById('ingredients');
    let ingredientDiv = ingredientsListDiv.querySelector(`#ingredient${ID}`);
    ingredientsListDiv.removeChild(ingredientDiv);
    
    for(let curIngredient of ingredients) {
        if(curIngredient.ID == ID) {
            let index = ingredients.indexOf(curIngredient);
            if (index > -1) {
                ingredients.splice(index, 1);
            }
        }
    }

    //Hide the added ingredients title if there are no ingredients
    if(ingredients.length === 0) {
        let addedIngredientsTitle = document.getElementById('addedIngredientsTitle');
        addedIngredientsTitle.style.display = 'none';
    }

    console.log(ingredients);
}

//Function to submit the ingredients and show the instructions form
function submitIngredients() {
    if(ingredients.length === 0) {
        alert('At least one ingredient is required!');
        return false;
    }

    let formTwo = document.getElementById('createRecipeTwo');
    formTwo.style.display = 'none';

    return true;
}

//====================================================================================================
//Instructions
//====================================================================================================

//Function to show the instructions form
function showStepThree() {
    let formThree = document.getElementById('createRecipeThree');
    formThree.style.display = 'block';

    populateIngredients();
}

//Show the previously given ingredients in the left menu
function populateIngredients() {
    let ingredientsList = document.getElementById('ingredientsList');
    for(let item of ingredients){
        let ingredient = document.createElement('li');
        ingredient.setAttribute('class', 'pure-menu-item ingredient');
        let button = document.createElement('button');
        button.setAttribute('class', 'pure-button ingredientButton');
        button.setAttribute('type', 'button');
        button.textContent = `${item.amount} ${item.fraction} ${item.unit} ${item.name}`;
        button.addEventListener('click', function() {
            let instructionEntry = document.getElementById('instruction');
            let trimmedText = button.textContent.replace(/\s\s+/g, ' ');
            instructionEntry.value = instructionEntry.value + trimmedText;
        });
        ingredient.appendChild(button);
        ingredientsList.appendChild(ingredient);
    }
}

//Adds typed instruction to the instructions list
function addInstruction() {
    let instructionText = document.getElementById('instruction');
    let instructionValue = instructionText.value;
    if(instructionValue === '') {
        alert('Instruction is required!');
        return false;
    }

    let instruction = {
        ID: instructions.length,
        instruction: instructionValue
    };

    instructions.push(instruction);

    let instructionsDiv = document.getElementById('instructions');

    let newInstruction = document.createElement('li');
    newInstruction.setAttribute('class', 'pure-menu-item instruction');
    newInstruction.setAttribute('id', `instruction${instruction.ID}`);
    newInstruction.textContent = `${instruction.ID+1}. ${instruction.instruction}`;

    newInstruction.addEventListener('click', function(event) {
        spawnEditDeletePopup(event);
    });

    instructionsDiv.appendChild(newInstruction);

    instructionText.value = '';

    instructionsDiv.scrollTop = instructionsDiv.scrollHeight;
}

//Flag to know if we are editing an instruction
let editFlag = false;

//Function to save the edited instruction
function saveEditInstruction() {
    let instructionEntryGrid = document.getElementById('instructionEntryGrid');

    let ID = lastEdit[0];

    let instruction = document.getElementById(`instruction${ID}`);
    let instructionEntry = document.getElementById('instruction');


    if(instructionEntry.value === '') {
        alert('Instruction is required!');
        return false;
    }
    else if(instructionEntry.value === lastEdit[1]) {
        return false;
    }
    else if(!/^[0-9]+\./.test(instructionEntry.value) || !instructionEntry.value.startsWith(`${parseInt(ID) + 1}.`)) {
        let listNum = parseInt(ID) + 1;
        instruction.textContent = `${listNum}. ${instructionEntry.value}`;
    }
    else{
        instruction.textContent = `${instructionEntry.value}`;
    }
    
    if(lastEdit[1] === '') {
        instructionEntry.value = '';
    }
    else {
        instructionEntry.value = lastEdit[1];
    }
    
    editFlag = false;
    let editTitle = document.getElementById('editTitle');
    editTitle.style.display = 'none';
    instructionEntryGrid.querySelector('#submitInstruction').style.display = 'block';
    instructionEntryGrid.querySelector('#saveInstruction').style.display = 'none';
    return true
}

//variable to save the current instruction being edited or deleted
let currentInstruction;

//Flag to know if the popup is present
let popupFlag = false;

//Function to spawn the edit/delete popup
function spawnEditDeletePopup(event) {
    let mouseX = event.clientX;
    let mouseY = event.clientY + 32;

    popupFlag = true;

    let editButton = document.getElementById('editInstruction');
    if(editFlag){
        editButton.style.display = 'none';
    }
    else{
        editButton.style.display = 'block';
    }

    let popup = document.getElementById('editDeletePopup');
    popup.style.display = 'block';
    popup.style.left = mouseX + 'px';
    popup.style.top = mouseY + 'px';

    currentInstruction = event.target;
}

//Function to close the edit/delete popup
function closeEditDeletePopup() {
    popupFlag = false;
    let popup = document.getElementById('editDeletePopup');
    popup.style.display = 'none';
}

//Function to set the edit area to the chosen edit instruction
function editInstruction() {
    if(editFlag)
        return;
    editFlag = true;
    let editTitle = document.getElementById('editTitle');
    editTitle.style.display = 'block';
    let instructionEntryGrid = document.getElementById('instructionEntryGrid');
    let instructionEntry = instructionEntryGrid.querySelector('#instruction');
    instructionEntryGrid.querySelector('#submitInstruction').style.display = 'none';
    instructionEntryGrid.querySelector('#saveInstruction').style.display = 'block';
    let currentID = currentInstruction.id.replace('instruction', '');
    lastEdit = [currentID,instructionEntry.value];
    instructionEntry.value = currentInstruction.textContent;
    closeEditDeletePopup();
}

//Function to delete the chosen instruction
function deleteInstruction() {
    currentInstruction.remove();
    instructions.splice(currentInstruction.id.replace('instruction', ''), 1);

    let instructionsList = document.getElementsByClassName('instruction');
    for (let i = 0; i < instructionsList.length; i++) {
        instructionsList[i].setAttribute('id', `instruction${i}`);
        instructionsList[i].textContent = `${i+1}. ${instructionsList[i].textContent.replace(/^[0-9]+\./, '')}`;
    }

    closeEditDeletePopup();
}

function submitInstructions() {
    if(instructions.length === 0) {
        alert('At least one instruction is required!');
        return false;
    }

    let formThree = document.getElementById('createRecipeThree');
    formThree.style.display = 'none';

    return true
}

//====================================================================================================
//Photo and submit recipe
//====================================================================================================

function showStepFour() {
    let formFour = document.getElementById('createRecipeFour');
    formFour.style.display = 'flex';

    showPreviewPhoto();
}

function showPreviewPhoto(){
    
    fetch(`/api/getrecipepreviewimage?title=${encodeURIComponent(title)}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                let photoPreview = document.getElementById('photoPreview');
                if(data.imgurl === ""){
                    photoPreview.src = '/static/resources/Logo.png';
                    url = '/static/resources/Logo.png';
                }
                else{   
                    photoPreview.src = data.imgurl;
                    url = data.imgurl;
                }
            } 
            else {
                alert('Fetch for image URL failed');
            }
        });
        
    let photoPreview = document.getElementById('photoPreview');
    photoPreview.src = '/static/resources/Logo.png';
}

function setPhoto(){
    let imgSelect = document.getElementById('imgSelect');
    let file = document.getElementById('photoInput').files[0];
    if (file) {
        imgSelect.src = URL.createObjectURL(file);
    }
}

let selected = '';

function setSelected(div) {
    let upload = document.getElementById('upload');
    let generated = document.getElementById('generated');

    if(upload === div) {
        upload.style.backgroundColor = '#cffacf';
        generated.style.backgroundColor = 'white';
        selected = 'upload';
    }
    else {
        upload.style.backgroundColor = 'white';
        generated.style.backgroundColor = '#cffacf';
        selected = 'generated';
    }
}

submitRecipe = async () => {
    let input = document.getElementById('photoInput');
    if(selected === 'upload' && input.files.length > 0){
        photo = input.files[0];
    }

    let finalIngredients = [];
    ingredients.forEach(ingredient => {
        finalIngredients.push((`${ingredient.amount} ${ingredient.fraction} ${ingredient.unit},${ingredient.name}`).replace(/\s\s+/g, ' '));
    });

    let finalInstructions = [];
    instructions.forEach(instruction => {
        finalInstructions.push(instruction.instruction);
    });

    let url = 'None';
    if(selected === 'generated' || (selected === '' && recipeid)){
        url = document.getElementById('photoPreview').src;
    }

    let recipeData = {
        title: title,
        description: description,
        categories: selectedCategories,
        ingredients: finalIngredients,
        instructions: finalInstructions,
        photoUrl: url
    };

    try {
        let response = await fetch('/api/addrecipe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(recipeData),
        });

        if (!response.ok) {
            let errorText = await response.text();
            console.error('Error response:', errorText);
            alert('Failed to create recipe: ' + errorText);
            return;
        }

        let data = await response.json();

        if (data.status === 'success') {
            //window.location.href = `/recipe/${data.recipeID}`;
            if(selected === 'upload'){
                let imageForm = new FormData();
                imageForm.append('image', photo);
                imageForm.append('recipeid', data.recipeID);
                let imageResponse = await fetch('/api/setRecipeImage', {
                    method: 'POST',
                    body: imageForm,
                });
                if (!imageResponse.ok) {
                    let errorText = await imageResponse.text();
                    console.error('Error response:', errorText);
                    alert('Failed to upload recipe image: ' + errorText);
                    return;
                }
            }
            console.log(data.recipeID);
            window.location.href = `/recipe/${data.recipeID}`;
        } 
        else {
            alert('Failed to create recipe: ' + data.message);
        }
    } 
    catch (error) {
        console.error('Error:', error);
        alert('An error occurred while creating the recipe');
    }
}
//====================================================================================================
//Edit Recipe Start
//====================================================================================================

let fillStepOne = function() {
    document.getElementById('recipeTitle').value = title;
    document.getElementById('recipeDescription').value = description;

    let selectedCategoriesList = document.querySelector('#selectedCategories .pure-menu-list');
    for(let category of selectedCategories) {
        let selectedCategory = document.createElement('li');
        selectedCategory.setAttribute('class', 'pure-menu-item');
        let categoryElement = document.createElement('a');
        categoryElement.setAttribute('class', 'pure-menu-item');
        categoryElement.textContent = category;
        selectedCategory.appendChild(categoryElement);
        selectedCategoriesList.appendChild(selectedCategory);
        selectedCategory.addEventListener('click', function() {
            let index = selectedCategories.indexOf(category);
            if (index > -1) {
                selectedCategories.splice(index, 1);
            }
            selectedCategoriesList.removeChild(selectedCategory);
        });
    }

    if(units.imperial.includes(ingredients[0].unit))
        setUnitsImperial();
    else
        setUnitsMetric();
}

let fillStepTwo = function() {
    for(let ingredient of ingredients) {

        let baseIngredient = document.getElementById('baseIngredient');
        if (!baseIngredient) {
            console.log('baseIngredient not found');
        }

        id = ingredient.ID;

        let newIngredient = baseIngredient.cloneNode(true);
        newIngredient.id = `ingredient${id}`;

        newIngredient.querySelector('#ingredientName').id=`ingredientName${id}`;
        newIngredient.querySelector('#ingredientAmount').id=`ingredientAmount${id}`;
        newIngredient.querySelector('#ingredientFraction').id=`ingredientFraction${id}`;
        newIngredient.querySelector('#ingredientUnit').id=`ingredientUnit${id}`;

        newIngredient.querySelector(`#ingredientName${id}`).value = ingredient.name;
        newIngredient.querySelector(`#ingredientAmount${id}`).value = ingredient.amount;
        newIngredient.querySelector(`#ingredientFraction${id}`).value = ingredient.fraction;
        newIngredient.querySelector(`#ingredientUnit${id}`).value = ingredient.unit;
        newIngredient.querySelector(`#ingredientUnit${id}`).selected = ingredient.unit;

        //Add an event listener for changing the already created ingredient
        newIngredient.addEventListener('change', function(event) {
            adjustIngredient(event.target);
        });

        let ingredientsDiv = document.getElementById('ingredients');

        //Add a remove button to the ingredient
        let removeButton = document.createElement('img');
        removeButton.src = '/static/resources/remove.png';
        removeButton.setAttribute('class', 'pure-u-1-3 pure-u-md-1-4 removeButton');
        removeButton.setAttribute('id', `removeButton${ingredient.ID}`);
        removeButton.addEventListener('click', function(event) {
            removeIngredient(event.target);
        });
        newIngredient.appendChild(removeButton);

        ingredientsDiv.appendChild(newIngredient);
    }

    //Show the added ingredients title now that there is an ingredient
    let addedIngredientsTitle = document.getElementById('addedIngredientsTitle');
    addedIngredientsTitle.style.display = 'block';
}

let fillStepThree = function() {
    for(let instruction of instructions) {
        let instructionsDiv = document.getElementById('instructions');

        let newInstruction = document.createElement('li');
        newInstruction.setAttribute('class', 'pure-menu-item instruction');
        newInstruction.setAttribute('id', `instruction${instruction.ID}`);
        newInstruction.textContent = `${instruction.ID+1}. ${instruction.instruction}`;

        newInstruction.addEventListener('click', function(event) {
            spawnEditDeletePopup(event);
        });

        instructionsDiv.appendChild(newInstruction);

        instructionsDiv.scrollTop = instructionsDiv.scrollHeight;
    }
}

let normalizeIngredients = function(ing) {
    for (let t of ing) {
        console.log(t);
        let parts = t.split(','); 
        let quantityFractionUnit = parts[0].split(' '); 
        let ingredient;
        if(quantityFractionUnit.length == 3){
            ingredient = {
                ID: ingredientID++,
                name: parts[1], 
                amount: quantityFractionUnit[0], 
                fraction: quantityFractionUnit[1],
                unit: quantityFractionUnit[2] 
            };
        }
        else{
            ingredient = {
                ID: ingredientID++,
                name: parts[1], 
                amount: quantityFractionUnit[0], 
                fraction: '',
                unit: quantityFractionUnit[1] 
            };
        }
        ingredients.push(ingredient);
    }
}

let normalizeInstructions = function(ins) {
    let instructionID = 0;
    for(let x of ins){
        let instruction = {
            ID: instructionID++,
            instruction: x
        };
        instructions.push(instruction);
    }
}

async function getRecipe(recipeid) {
    try {
        const response = await fetch(`/api/getrecipe/${recipeid}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        if (data.status === "success") {
            return data.recipe;
        } 
        else {
            console.error('Failed to retrieve recipe:', data.message);
            return null;
        }
    } 
    catch (error) {
        console.error('Fetch error:', error);
        return null;
    }
}

let setRecipe = function(recipe) {
    console.log(recipe);
    title = recipe[1];
    description = recipe[2];
    selectedCategories = recipe[8];

    normalizeIngredients(recipe[3]);

    normalizeInstructions(recipe[4]);

    console.log(ingredients);

    console.log(selectedCategories)
    fillStepOne();
    fillStepTwo();
    fillStepThree();
}

let toggleDelete = function() {
    let deletePrompt = document.getElementById('deletePrompt');
    let grayBackground = document.getElementById('grayBackground');
    if(deletePrompt.style.display === 'none' || deletePrompt.style.display === '') {
        deletePrompt.style.display = 'block';
        grayBackground.style.display = 'block';
    }
    else {
        deletePrompt.style.display = 'none';
        grayBackground.style.display = 'none';
    }
}

let deleteRecipe = async function() {
    try {
        let response = await fetch('/api/deleterecipe', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ recipeid: recipeid })
        });

        if (!response.ok) {
            let errorText = await response.text();
            console.error('Error response:', errorText);
            alert('Failed to delete recipe: ' + errorText);
            return;
        }

        let data = await response.json();

        if (data.status === 'success') {
            window.location.href = '/profile';
        } else {
            alert('Failed to delete recipe: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while deleting the recipe');
    }
}

let updateRecipe = async function() {
    let input = document.getElementById('photoInput');
    if(selected === 'upload'){
        photo = input.files[0];
    }
    let url = 'None';
    if(selected === 'generated'){
        url = document.getElementById('photoPreview').src;
    }

    let finalIngredients = [];
    ingredients.forEach(ingredient => {
        finalIngredients.push((`${ingredient.amount} ${ingredient.fraction} ${ingredient.unit},${ingredient.name}`).replace(/\s\s+/g, ' '));
    });

    let finalInstructions = [];
    instructions.forEach(instruction => {
        finalInstructions.push(instruction.instruction);
    });

    let recipeData = {
        title: title,
        description: description,
        categories: selectedCategories,
        ingredients: finalIngredients,
        instructions: finalInstructions,
        photoUrl: url
    };

    try {
        let response = await fetch ('/api/updaterecipe', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({recipeid: recipeid, recipeData: recipeData})
        });

        if (!response.ok) {
            let errorText = await response.text();
            console.error('Error response:', errorText);
            alert('Failed to edit recipe: ' + errorText);
            return;
        }

        let data = await response.json();

        console.log(data);

        if (data.status === 'success') {
            if(selected === 'upload' && input.files.length > 0){
                photo = input.files[0];
                let imageForm = new FormData();
                imageForm.append('image', photo);
                imageForm.append('recipeid', recipeid);
                let imageResponse = await fetch('/api/updaterecipeimage', {
                    method: 'POST',
                    body: imageForm,
                });
                if (!imageResponse.ok) {
                    let errorText = await imageResponse.text();
                    console.error('Error response:', errorText);
                    alert('Failed to upload recipe image: ' + errorText);
                    return;
                }
            }
            window.location.href = `/recipe/${recipeid}`;
        } 
        else {
            alert('Failed to edit recipe: ' + data.message);
        }
    } 
    catch (error) {
        console.error('Error:', error);
        alert('An error occurred while editing the recipe');
    }
}

//====================================================================================================
//Edit Recipe End
//====================================================================================================

//Loads categories and popup exit functions
window.onload = async function() {
    populateCategories();
    if(recipeid){
        let recipe = await getRecipe(recipeid);
        setRecipe(recipe[0])
    }

    window.addEventListener('click', function(event) {
        if(categoryFlag){
            let x = event.clientX;
            let y = event.clientY;

            let dropdown = document.getElementById('dropdown');
            let selectCategories = document.getElementById('selectCategories');
            let rect = dropdown.getBoundingClientRect();
            let rect2 = selectCategories.getBoundingClientRect();
            let dropdownX = rect.left;
            let dropdownY = rect2.top;
            let dropdownWidth = rect.width;
            let dropdownHeight = rect.height + rect2.height;

            if(x < dropdownX || x > dropdownX + dropdownWidth || y < dropdownY || y > dropdownY + dropdownHeight) {
                dropdown.style.display = 'none';
                categoryFlag = false;
            }
        }
        if(popupFlag){
            let x = event.clientX;
            let y = event.clientY;

            let popup = document.getElementById('editDeletePopup');
            let rect = popup.getBoundingClientRect();
            let popupX = rect.left;
            let popupY = rect.top;
            let popupWidth = rect.width;
            let popupHeight = rect.height;

            if(x < popupX || x > popupX + popupWidth || y < popupY || y > popupY + popupHeight) {
                closeEditDeletePopup();
            }
        }
        
    });
}


