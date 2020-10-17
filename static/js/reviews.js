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
      return `<div class="card">
      <article class="review">
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
      </article>
      <div class="review-expand chevron-down"></div>
      </div>`;
    });
    // join articles & insert data
    reviewsHTML.innerHTML = reviewHTML.join("");
  });
}

/* ==============
// view review //
============== */

// reusing this var from above
// const reviewsHTML = document.querySelector("#reviews-html");

/*
Need to revisit this approach.
Challenge is these events need to be added after load happens
// Add query selector at the end of load function?
// or, target parent that exists at time of load, then add event handlers dynamically.
  // below is a first attempt, but doesn't fire when children clicked
  // maybe add event listener to children when clicked instead of the below messy traversal...
*/

// as DOM is generated after page is loaded, the events here are delcared from the parent
reviewsHTML.addEventListener("click", e => {
  let reviews = reviewsHTML.querySelectorAll(".review");
  // if a review expand is clicked, opens up review panel
  if (e.target.classList.contains("review")) {
    if (e.target.classList.contains("view-review")) {
      e.target.classList.remove("view-review");
    } else {
      reviews.forEach(review => {
        review.classList.remove("view-review");
      });
      e.target.classList.toggle("view-review");
    }
  }
  // if the chevron is lcicked
  if (e.target.classList.contains("review-expand")) {
    console.log(e.target);
    if (e.target.parentElement.firstChild.nextSibling.classList.contains("view-review")) {
      e.target.parentElement.firstChild.nextSibling.classList.remove("view-review");
    } else {
      reviews.forEach(review => {
        review.classList.remove("view-review");
      });
      e.target.parentElement.firstChild.nextSibling.classList.toggle("view-review");
    }
  }
});
