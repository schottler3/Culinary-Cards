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

    let isUser = await fetch("/api/isUser",{method : "GET", headers : {"Content-Type" : "application/json"}, body: JSON.stringify(newUsername)});

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

window.onload = function() {
    var accountGear = document.getElementById('accountGear');
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
    });
    document.getElementById('sortProfileRecipes').addEventListener('change', sortRecipes);
}
