console.log("connected");

/* =================================
// Autocomplete & wine_id checker //
================================= */

//--------------
// DOM variables
//--------------

const datalistBrands = document.querySelector("#datalist-brands");
const brandInput = document.querySelector("#brand");
const datalistVariety = document.querySelector("#datalist-varieties");
const varietyInput = document.querySelector("#variety");
const datalistYear = document.querySelector("#datalist-years");
const yearInput = document.querySelector("#year");
const wineId = document.querySelector("#wine_id");

//---------
// on load
//---------

// get the wines values from DB
let wines;
$.get("/api/wines", data => {
  // array of wine objects
  wines = data.wines;
  // array of brand names
  let brands = new Set(data.wines.map(wine => wine.brand));
  brands = [...brands];

  // initial load to brands (when data arrives)
  loadDropdown(brands, datalistBrands);
});

//------------
// page events
//------------

// if brands not null, populate varieties
brandInput.addEventListener("keyup", () => {
  // create varieties unique sub array
  let varieties = wines.reduce((arr, wine) => {
    if (brandInput.value == wine.brand && !arr.includes(wine.variety)) {
      arr.push(wine.variety);
    }
    return arr;
  }, []);
  // call helper functions
  wineIdUpdate();
  loadDropdown(varieties, datalistVariety);
});

// if varieties not null, populate year and store wine_id
varietyInput.addEventListener("keyup", () => {
  // create year sub array
  const years = wines.reduce((arr, wine) => {
    if (varietyInput.value == wine.variety && brandInput.value == wine.brand) {
      arr.push(wine.year);
    }
    return arr;
  }, []);
  // call helper functions
  wineIdUpdate();
  loadDropdown(years, datalistYear);
});

// check for wine_id if year is inputted
yearInput.addEventListener("keyup", () => {
  wineIdUpdate();
});

//-----------------
// helper functions
//-----------------

// load data into dropdown list. args = arr, dom datalist. e.g. brand, datalistBrands
// updates wine_id
function loadDropdown(arr, datalist) {
  let domlist = arr.map(item => {
    return `<option value="${item}">${item}</option>`;
  });
  domlist = domlist.join("");
  datalist.innerHTML = domlist;
}

// checks all the input values against the wine object array and sets the wine_id form value if found
function wineIdUpdate() {
  const wine = wines.find(wine => {
    return (
      brandInput.value == wine.brand &&
      varietyInput.value == wine.variety &&
      parseInt(yearInput.value) == parseInt(wine.year)
    );
  });
  wineId.value = wine ? wine.id : "";
}

/* =================
// Form interface //
==================*/

//--------------------------
// star rating click & input
//--------------------------

const stars = document.querySelectorAll(".star-scale span");
const rating = document.querySelector("#rating");

// On load
// data loads with page, via FLASK template, to rating input value
starUpdate();

// Update event

stars.forEach(star => {
  star.addEventListener("click", e => {
    // get the rating value of the star clicked
    const ratingInput = e.currentTarget.dataset.rating;
    // update the hidden form input
    rating.value = ratingInput;
    // update the star UI
    starUpdate();
  });
});

// helper

function starUpdate() {
  stars.forEach(star => {
    if (star.dataset.rating <= rating.value) {
      star.classList.add("checked");
    } else {
      star.classList.remove("checked");
    }
  });
}

//------------------------
// Preview image for form
//------------------------

const imgInput = document.querySelector("#image");
const imgInputHidden = document.querySelector("#hiddenimage");
const imgPreview = document.querySelector("#imgpreview");
const imgClose = document.querySelector(".close-img");

// (for edit page) show the remove img btn if an image is available
if (imgPreview.getAttribute("src")) {
  imgClose.classList.remove("hidden");
}

// update preview when img is changed
imgInput.addEventListener("change", previewImg);

function previewImg() {
  // read image and update imgPreview src
  const reader = new FileReader();
  reader.readAsDataURL(imgInput.files[0]);
  reader.onload = () => (imgPreview.src = reader.result);
  // add imageClose icon
  imgClose.classList.remove("hidden");
}

// remove image preview, input value & hide close icon
imgClose.addEventListener("click", () => {
  imgPreview.src = "";
  imgInput.value = "";
  imgInputHidden.value = "";
  imgClose.classList.add("hidden");
});

//------------------------
// Preview image for form
//------------------------
