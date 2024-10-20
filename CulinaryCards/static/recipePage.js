const leftSide = document.getElementById('left-side');
const rightSide = document.getElementById('comment-container');

console.log(leftSide);
console.log(rightSide);

// function to match the height of left and right side on recipe page
function matchHeight() {
    rightSide.style.height = `${leftSide.offsetHeight - 250}px`;
}

matchHeight();
window.addEventListener('resize', matchHeight);