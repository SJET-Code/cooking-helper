# [Cooking-Helper](https://cooking--helper.herokuapp.com/)
A tool to store, rate, and easily list out recipes and ingredients used in cooking!

This application allows users to create recipes, browse and like other users recipes and create a list of recipes that includes a combined list of all the ingredients used in those recipes. This is a very useful tool for people who like to plan out their cooking a week ahead, while still having a nice amount of variety with their food.

### Cooking-Helper features:

- [x] See  the 20 latest and the 20 most liked recipes in the frontpage
- [x] Open a recipe and see the step-by-step instructions and a list of ingredients for that recipe
- [x] Register an account and login
- [x] Once logged in:
  - [x] Create a recipe with different ingredients and step-by-step instructions, 
  - [x] Like recipes
  - [x] Create a Cooking Plan (a list of recipes) from your liked recipes, and form a shopping list (a list of all the ingredients in Cooking Plan recipes)
  - [x] Edit / delete your own recipes and Cooking Plans
  - [x] Hide / unhide ingredients from a shopping list (to filter out ingredients you already have in the pantry)
  - [x] See all your Cooking Plans and recipes in the "My Page" - page

### Testing
Testing can be done in [Heroku](https://cooking--helper.herokuapp.com/), you need to register and log in to create and like recipes, make Cooking Plans and to see your "My Page" view!

### Database Diagram

![dbdiagram](https://user-images.githubusercontent.com/90755361/167111401-b4c17803-da61-4762-84d9-a9c0f49d422f.png)

### Security

- All password are stored in the database as hash values and decrypted using a secret key.
- There is code to prevent a csrf vulnerability when submitting a form.
- There are no SQL or XSS injection vulnerabilities, due to the way the code is structured.
- Users cannot access parts of the website that they have no access to, editing or deleting other users recipes, for example.
