# wine.io

Web app for reviewing wine!

Final project for CS50x.

Using Flask for MVC & API, JS on the frontend and SQL for DB.

Initial design: https://www.figma.com/file/egP37kjleuM8chMPDmQ2Bz/figma-test?node-id=2%3A2

Current project: https://trello.com/b/8E4GEEEp/wineio

Deployed preview: https://wine-io.herokuapp.com/
NOTE: This is using a free account and a file db, so loading is a bit slow and images/reviews/users are all cleared between deploys.

## Features:

Track wines via reviews

- Reviews support star rating, user loaded images, written review & 'drink again'.
- Add wine reviews, view and sort/filter reviews, edit & delete review.

User auth & personal accounts.

- Reivews are only available to the user who created it.

Responsive web interface

- Interface has been built responsively, suitable for mobile & desktop useage.

Dynamic reviews page

- Reviews page is built dynamically to enable user interaction with their review history
- Scroll through and expand reviews for more information & editing
- Sorting & filtering of data dynamically on the page, without reloading.

Wine database is a user-shared generated db.

- Instead of pre-populating a list of brand, variety, year etc for the interface the users will submit these to the DB and create a new row in the wine DB if it doesn't exist. This table is shared for all users for the autocomete.

Adding data autocomplete

- The frontend 'add' route has an 'autocomplete' look-up as the user types, this is getting JSON data from the server via an API. It's used to populate the autocompletes, and if a match is found (i.e. brand, variety & year) the wine_id is populated and submitted to the server where it will not need to create a new wine_id.
