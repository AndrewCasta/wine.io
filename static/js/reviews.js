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
const sortBtns = document.querySelectorAll(".sort-btn");
const orderBtn = document.querySelector(".order-btn");
const filterBtn = document.querySelector("#drink_again");
const reviewsHTML = document.querySelector("#reviews-html");

// variabtes to store the search logic. Defaults on load:
let sort = "datetime"; // rating | datetime
let order = "DESC"; // ASC | DESC (most recent first)
let drinkAgain = ""; // True | ''

//---------
// on load
//---------

// call load data function
loadReviews();

//------------
// page events
//------------

// filter button
filterBtn.addEventListener("click", e => {
  // toggle icon display
  e.currentTarget.querySelector("i").classList.toggle("hide-hidden");
  // update filter variable
  drinkAgain = drinkAgain == "True" ? "" : "True";
  // get & load data
  loadReviews();
});

// sort buttons
sortBtns.forEach(btn => {
  btn.addEventListener("click", e => {
    // remove active style from btns
    sortBtns.forEach(btn => {
      btn.classList.remove("active");
    });
    // add active style
    e.currentTarget.classList.add("active");
    // update sort variable
    sort = e.currentTarget.dataset.sort;
    // get & load data
    loadReviews();
  });
});

// order btn
orderBtn.addEventListener("click", e => {
  // swap between asc & desc icons
  orderBtn.classList.toggle("asc");
  orderBtn.classList.toggle("desc");
  // update order variable
  order = order == "ASC" ? "DESC" : "ASC";
  console.log(order);
  // get & load data
  loadReviews();
});

//-----------------
// helper functions
//-----------------

// loads reviews on page, using the sort/filter variables, which are maninupated by the events above

function loadReviews() {
  // get data from API (sort, filter, order)
  $.get(`/api/reviews?sort=${sort}&drink_again=${drinkAgain}&order=${order}`, reviews => {
    console.log(reviews);
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
