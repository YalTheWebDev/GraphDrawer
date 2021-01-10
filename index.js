let userHasScrolled = false;
let draw_button = document.querySelector("#draw-btn")
let graph_image = document.querySelector(".graph-image")
let invisible_text = document.querySelector(".invisible-text")

window.onscroll = function (e) {
    userHasScrolled = true;
}

if (userHasScrolled === true) {
    document.querySelector("h1").classList.add("on-scroll");
}

draw_button.addEventListener("click", function () {
    window.location.href = "draw.html";
});

condition = graph_image.addEventListener("mouseover", function () {
    invisible_text.classList.remove("invisible-text");
});