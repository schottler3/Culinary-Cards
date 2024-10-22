document.addEventListener('DOMContentLoaded', function() {
    var circleTop = document.getElementById('scroll-to-top');
    // var categoryContainer = document.querySelector('.card-container'); 

    function Scroll() {
        // var div = circleTop.getBoundingClientRect();
        window.scrollTo(0, window.top);
    }

    document.addEventListener("scroll", (event) => {
        if (circleTop != null){
        if (window.scrollY >= 200) {
            circleTop.style.bottom = "50px";
            circleTop.style.right = "50px";
            circleTop.style.width = "70px";
            circleTop.style.height = "70px";
        }
        else {
            circleTop.style.bottom = "-100px";
            circleTop.style.right = "-100px";
            circleTop.style.width = "0px";
            circleTop.style.height = "0px";
        }
    }
    });

    if (circleTop != null){
    circleTop.addEventListener('click', function() { 
        Scroll();
    });}



});