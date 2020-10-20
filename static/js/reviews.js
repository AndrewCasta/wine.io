/* ================
// Sort & filter //
================ */

//--------------
// variables
//--------------

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
      // if review has no image, add the no-img class
      let reviewClass = "review";
      if (!review.image) {
        reviewClass = "review no-img";
      }
      // return each review HTML article
      return `<div class="card">
      <article class="${reviewClass}" id="review-${review.review_id}">
      <h4 class="brand">${review.brand}</h4>
      <div class="star-scale">
      ${starHTML}
      </div>
      ${
        review.image
          ? `<div class="review-img-container">
        <img src="${review.image}" alt="image of review" class="review-img" />
      </div>`
          : `<span class="review-img"></span>`
      }
      <p class="variety-year"><span class="variety">${review.variety}</span>, <span class="year">${
        review.year
      }</span></p>
      <p class="datetime">${review.date}</p>

      <div class="review-text">
          <h6>Review:</h6>
          <p>${review.review}</p>
        </div>
        <span class="drink-again">Drink again: 
        ${review.drink_again ? `<i class="fas fa-check">` : `<i class="fas fa-times"></i>`}</i></span>
        <span id="review-edit-btn">
          <form action="/edit">
            <button type="submit" class="btn btn-primary" name="review_id" value="${review.review_id}">Edit</button>
          </form>
        </span>

      </article>
      <div class="review-expand chevron-down" data-reviewId="review-${review.review_id}"></div>
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

reviewsHTML.addEventListener("click", e => {
  // select all the reviews
  let reviews = document.querySelectorAll(".review");
  // review id, of clicked element
  let reviewId = e.target.dataset.reviewid;
  // selector for the element to be opened/closed
  let reviewElement = reviewsHTML.querySelector(`#${reviewId}`);

  // if clicking review-expend button
  if (e.target.matches(".review-expand")) {
    // if target already has view-review, remove it & swap chevron icon
    if (reviewElement.classList.contains("view-review")) {
      reviewElement.classList.remove("view-review");
      e.target.classList.add("chevron-down");
      e.target.classList.remove("chevron-up");
    } else {
      // else remove review-expand from all & swap chevron icon
      reviews.forEach(review => {
        review.classList.remove("view-review");
        review.nextElementSibling.classList.remove("chevron-up");
        review.nextElementSibling.classList.add("chevron-down");
      });
      // expand the clicked review & swap chevron icon
      reviewElement.classList.add("view-review");
      e.target.classList.remove("chevron-down");
      e.target.classList.add("chevron-up");
    }
  }
});
