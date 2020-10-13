console.log("connected");

/* =================================
// Autocomplete & wine_id checker //
================================= */

const datalistBrands = document.querySelector("#datalist-brands");
const brandInput = document.querySelector("#brand");
const datalistVariety = document.querySelector("#datalist-varieties");
const varietyInput = document.querySelector("#variety");
const datalistYear = document.querySelector("#datalist-year");

// get the current values from DB
let wines;
let brands;
$.get("/wines", data => {
  // array of wine objects
  wines = data.wines;
  // array of brand names
  brands = data.wines.map(x => x.brand);

  // initial load to brands (when data arrives)
  loadDropdown(brands, datalistBrands);
});

// hacky way of getting the data into console
document.addEventListener("click", () => {
  console.log(wines);
  console.log(brands);
});

// if brands not null, populate varieties
// create varieties sub array

// if varieties not null, populate year
// create year sub array

// (helper function)
// load data into dropdown list. args = arr, dom datalist. e.g. brand, datalistBrands
function loadDropdown(arr, datalist) {
  let domlist = arr.map(x => {
    return `<option value="${x}">${x}</option>`;
  });
  domlist = domlist.join("");
  datalist.innerHTML = domlist;
}

/* =================
// Form interface //
==================*/

// star rating click & input
const stars = document.querySelectorAll(".star-scale span");
const rating = document.querySelector("#rating");

stars.forEach(star => {
  star.addEventListener("click", e => {
    // get the rating value of the star clicked
    const ratingInput = e.currentTarget.dataset.rating;
    // update the hidden form input
    rating.value = ratingInput;
    // update the star UI
    stars.forEach(star => {
      if (star.dataset.rating <= ratingInput) {
        star.classList.add("checked");
      } else {
        star.classList.remove("checked");
      }
    });
  });
});

// Render preview image for loaded image

const imgInput = document.querySelector("#image");
const imgPreview = document.querySelector("#imgpreview");
const imgClose = document.querySelector(".close-img");

imgInput.addEventListener("change", () => {
  // read image and update imgPreview src
  const reader = new FileReader();
  reader.readAsDataURL(imgInput.files[0]);
  reader.onload = () => (imgPreview.src = reader.result);
  // add imageClose icon
  imgClose.classList.remove("hidden");
  // if (imgPreview.src != "") {
  // }
});

// remove image preview, input value & hide close icon
imgClose.addEventListener("click", () => {
  imgPreview.src = "";
  imgInput.value = "";
  imgClose.classList.add("hidden");
});
