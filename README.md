# Module 1 Group Assignment

CSCI 5117, Fall 2024, [assignment description](https://canvas.umn.edu/courses/460699/pages/project-1)

## App Info:

* Team Name: Peanut Butter Pickles
* App Name: CullinaryCards
* App Link: <https://culinarycards.onrender.com/>

### Students

* Adam Kvant, kvant003
* Minh Tong, tong0154
* Rock Zgutowicz, zguto005
* Lucas Schottler, schot147


## Key Features

**Describe the most challenging features you implemented
(one sentence per bullet, maximum 4 bullets):**

* Recipe Create and Edit Page, due to complexity and multiple "pages" and function on one template.
* Finding adequate documentation online for Postgres full-text search, it was not well documented and required digging in materialized views.
* Finding a good api that works, we had to pivot to Unsplash, as the original recipe apis were either expensive, nonfunctional, limited.
* Figuring an alternative way to setup recipe of the day, without using a cron job, persistent storage, etc.

## Testing Notes

**Is there anything special we need to know in order to effectively test your app? (optional):**

* THE SERVER FILE IS IN `__init__.py`, I did it this way as it's the way the server was setup in the Flask tutorial.
* Unsplash has a limit of 50 images per hour.
* Recipes can be searched by name, words from description, category, ingredients, username, and are sorted by likes descending.
* Firefox might be glitchy when clicking the Categories button. However, this should be fixed!


## Screenshots of Site

**[Add a screenshot of each key page (around 4)](https://stackoverflow.com/questions/10189356/how-to-add-screenshot-to-readmes-in-github-repository)
along with a very brief caption:**

![](https://media.giphy.com/media/o0vwzuFwCGAFO/giphy.gif)

![](https://github.com/csci5117f24/project-1-peanut-butter-pickles/blob/main/images/home.png)
Culinary Cards Home Page, with Search bar

![](https://github.com/csci5117f24/project-1-peanut-butter-pickles/blob/main/images/recipeoftheday.png)
Culinary Cards Recipe of the day

![](https://github.com/csci5117f24/project-1-peanut-butter-pickles/blob/main/images/results.png)
Culinary Cards search results for Chicken Alfredo

![](https://github.com/csci5117f24/project-1-peanut-butter-pickles/blob/main/images/recipecard.png)
Culinary Card for Chicken Alfredo Recipe

![](https://github.com/csci5117f24/project-1-peanut-butter-pickles/blob/main/images/profile.png)
Culinary Cards Profile Page

![](https://github.com/csci5117f24/project-1-peanut-butter-pickles/blob/main/images/recipeedit-create.png)
Culinary Cards Recipe create/edit view



## Mock-up 

There are a few tools for mock-ups. Paper prototypes (low-tech, but effective and cheap), Digital picture edition software (gimp / photoshop / etc.), or dedicated tools like moqups.com (I'm calling out moqups here in particular since it seems to strike the best balance between "easy-to-use" and "wants your money" -- the free teir isn't perfect, but it should be sufficient for our needs with a little "creative layout" to get around the page-limit)

In this space please either provide images (around 4) showing your prototypes, OR, a link to an online hosted mock-up tool like moqups.com



<a href="https://github.com/csci5117f24/project-1-peanut-butter-pickles/blob/main/REVISED-MOCKUP-PeanutButterPickles.pdf">PDF OF REVISED LO-FI MOCKUP FOUND HERE</a>
<a href="https://github.com/csci5117f24/project-1-peanut-butter-pickles/blob/main/REVISED-MOCKUP-PeanutButterPickles.pdf">PDF OF REVISED LO-FI MOCKUP FOUND HERE</a>
<a href="https://github.com/csci5117f24/project-1-peanut-butter-pickles/blob/main/REVISED-MOCKUP-PeanutButterPickles.pdf">PDF OF REVISED LO-FI MOCKUP FOUND HERE</a>
<a href="https://github.com/csci5117f24/project-1-peanut-butter-pickles/blob/main/REVISED-MOCKUP-PeanutButterPickles.pdf">PDF OF REVISED LO-FI MOCKUP FOUND HERE</a>
<a href="https://github.com/csci5117f24/project-1-peanut-butter-pickles/blob/main/REVISED-MOCKUP-PeanutButterPickles.pdf">PDF OF REVISED LO-FI MOCKUP FOUND HERE</a>
<a href="https://github.com/csci5117f24/project-1-peanut-butter-pickles/blob/main/REVISED-MOCKUP-PeanutButterPickles.pdf">PDF OF REVISED LO-FI MOCKUP FOUND HERE</a>
<a href="https://github.com/csci5117f24/project-1-peanut-butter-pickles/blob/main/REVISED-MOCKUP-PeanutButterPickles.pdf">PDF OF REVISED LO-FI MOCKUP FOUND HERE</a>

**The function of each page in the pdf is found on the yellow sticky note in a top corner, or printed as text at the top of the page.**


## External Dependencies

**Document integrations with 3rd Party code or services here.
Please do not document required libraries. or libraries that are mentioned in the product requirements**

* Pandas - Date conversion
* Unsplash API - Generated images for recipes: NOTE if we were on the paid plan for this API, we would have significantly more accurate images for our recipes.
* uuid - nonce generation
* cdn-icons-png.flaticon.com - for some website icons

**If there's anything else you would like to disclose about how your project
relied on external code, expertise, or anything else, please disclose that
here: Sometimes images can take a second to load. Recipes can be edited on the recipe card page.
In the recipe edit view, you can choose to delete your recipe.
...
