# wine.io

Web app for reviewing wine!

Final project for CS50x.

Using Flask for MVC & API, JS on the frontend and SQL for DB.

Initial design: https://www.figma.com/file/egP37kjleuM8chMPDmQ2Bz/figma-test?node-id=2%3A2

Current project: https://trello.com/b/8E4GEEEp/wineio

Deployed preview: TODO

Features:
----------
User auth & accounts

Reivews are only available to the user who created it. Reviews support star rating, user loaded images, written review & 'drink again'.

Wine database is a user-shared generated db.
* Instead of pre-populating a list of brand, variety, year etc for the interface the users will submit these to the DB and create a new row in the wine DB if it doesn't exist. This table is shared for all users for the autocomete.

Adding data autocomplete
* The frontend 'add' route has an 'autocomplete' look-up as the user types, this is getting JSON data from the server via an API. It's used to populate the autocompletes, and if a match is found (i.e. brand, variety & year) the wine_id is populated and submitted to the server where it will not need to create a new wine_id.


