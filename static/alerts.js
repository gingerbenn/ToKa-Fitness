var milliseconds = 2000;

setTimeout(function () {
  var element = document.getElementById("my-app");
  element.style.opacity = "0"; // Set opacity to 0 for fading effect
  setTimeout(function () {
    element.remove(); // Remove the element after the fade
  }, 1000); // Wait for 1 second (1000 milliseconds) for the fade to complete
}, milliseconds);
