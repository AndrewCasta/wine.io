console.log("connected:home.js");

//--------------------------
// star rating click & input
//--------------------------

const stars = document.querySelectorAll(".star-scale span");
const rating = document.querySelector("#rating");

// On load
// data loads with page, via FLASK template, to rating input value
starUpdate();

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
