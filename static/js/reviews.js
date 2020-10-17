/* ================
// Sort & filter //
================ */

//--------------
// variables
//--------------

// Sort by: rating
// Sort by: date
// Filter: drink_again

// DOM elements
const sortBtns = document.querySelectorAll(".sort-btns");
const filterBtn = document.querySelector("#drink_again");
const reviewsHTML = document.querySelector("#reviews-html");

// variabtes to store the search logic. Defaults on load:
const sort = "datetime"; // rating | datetime
const order = "ASC"; // ASC | DESC
const drinkAgain = ""; // True | ''

//---------
// on load
//---------

// call load data function
loadReviews();

//------------
// page events
//------------

// filter
// check button (change drink_again)

// sort

// Select all btns
// Foreach, On click

// update btn
// remove .toggle
// currentTarget add .toggle

// update variable
// If dataset.sort == sort
// order = desc
// Helper
// Else
// order = asc
// sort = dataset.sort
// Helper

//-----------------
// helper functions
//-----------------

// Helper
// load reviews on page

function loadReviews() {
  // get data from API (sort, filter, order)
  $.get(`/api/reviews?sort=${sort}&drink_again=${drinkAgain}&order=${order}`, reviews => {
    // Build the HTML for each review
    let reviewHTML = reviews.map(review => {
      // Build star rating based on stored rating value
      let starHTML = "";
      for (let i = 0; i < 5; i++) {
        if (review.rating > i) {
          starHTML += '<span class="fa fa-star checked"></span>';
        } else {
          starHTML += '<span class="fa fa-star"></span>';
        }
      }
      // return each review HTML article
      return `<article class="review">
      <h4 class="brand">${review.brand}</h4>
      <div class="star-scale">
      ${starHTML}
      </div>
      <div class="review-img-container">
        <img src="${review.image ? review.image : ""}" alt="image of review" class="review-img" />
      </div>
      <p class="variety-year"><span class="variety">${review.variety}</span>, <span class="year">${
        review.year
      }</span></p>
      <p class="datetime">${review.datetime}</p>
      </article>`;
    });
    // join articles & insert data
    reviewsHTML.innerHTML = reviewHTML.join("");
  });
}

/* ================
// click review //
================ */
