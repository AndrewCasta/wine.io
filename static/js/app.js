console.log("connected");

// console.log("{{ name|tojson }}"); Data needs to come from an API not via template

// Form interface

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

// Display rating input from slider
/*
// Initial attempt, adds rating from slider to span
const rating = document.querySelector("#rating");
const ratingNumber = document.querySelector("#rating-number");

rating.addEventListener("change", e => {
  ratingNumber.textContent = e.currentTarget.value;
});
*/

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
