document.getElementById("postComment").onsubmit = function () {
    console.log("analyzing")
    var messageBox = document.getElementById("messageBox");
    messageBox.style.display = "block";
    messageBox.textContent = "Processing your comment. Please wait...";
};