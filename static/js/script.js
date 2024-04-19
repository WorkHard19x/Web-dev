let slideIndex; // Declare slideIndex variable
let slideInterval; // Declare slideInterval variable for automatic slideshow
// Ensure the slideshow is initialized after the functions are defined
showSlides(1);

// Start automatic slideshow when the page loads
startSlideShow();
// Rest of the code


// Import MongoClient from the MongoDB package


function toggleUserDropdown() {
  var dropdown = document.getElementById("userDropdown");
  if (dropdown.style.display === "block") {
      dropdown.style.display = "none";
  } else {
      dropdown.style.display = "block";
  }
}



document.addEventListener("DOMContentLoaded", function() {
    updateTimeAgo();
    setInterval(updateTimeAgo, 60000); // Update every minute
  });
  
  function updateTimeAgo() {
    const timeElements = document.getElementsByClassName("time-ago");
    for (let i = 0; i < timeElements.length; i++) {
      const timestamp = new Date(timeElements[i].getAttribute("data-timestamp"));
      const timeAgo = timeSince(timestamp);
      timeElements[i].textContent = timeAgo;
    }
  }
  
  function timeSince(date) {
    // Adjust for CDT timezone (UTC -5 hours)
    const offsetHours = 5;
    date.setHours(date.getHours() + offsetHours);
  
    const seconds = Math.floor((new Date() - date) / 1000);
    let interval = Math.floor(seconds / 31536000);
  
    if (interval > 1) {
      return interval + " years ago";
    }
    interval = Math.floor(seconds / 2592000);
    if (interval > 1) {
      return interval + " months ago";
    }
    interval = Math.floor(seconds / 86400);
    if (interval > 1) {
      return interval + " days ago";
    }
    interval = Math.floor(seconds / 3600);
    if (interval > 1) {
      return interval + " hours ago";
    }
    interval = Math.floor(seconds / 60);
    if (interval > 1) {
      return interval + " minutes ago";
    }
    return Math.floor(seconds) + " seconds ago";
  }



function toggleDropdown() {
    var dropdownContent = document.getElementById("aboutDropdown");
    dropdownContent.classList.toggle("show");
}

window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

function plusSlides(n) {
    // Initialize slideIndex to 1 if it's currently undefined
    slideIndex = slideIndex === undefined ? 1 : slideIndex;
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("demo");
    let captionText = document.getElementById("caption");

    // Initialize slideIndex to 1 if it's currently undefined
    slideIndex = slideIndex === undefined ? 1 : slideIndex;

    if (n > slides.length) { slideIndex = 1; }
    if (n < 1) { slideIndex = slides.length; }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    if (slides.length > 0) {
        slides[slideIndex - 1].style.display = "block";
        dots[slideIndex - 1].className += " active";
        captionText.innerHTML = dots[slideIndex - 1].alt;
    }
}

// Function to start automatic slideshow
function startSlideShow() {
    slideInterval = setInterval(function() {
        plusSlides(1); // Advance to the next slide
    }, 5000); // Change slide every 2 seconds (adjust as needed)
}

// Function to stop automatic slideshow
function stopSlideShow() {
    clearInterval(slideInterval);
}



