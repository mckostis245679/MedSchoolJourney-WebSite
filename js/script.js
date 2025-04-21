// script.js

document.addEventListener("DOMContentLoaded", function() {
  // 1. Load the header (if you have header-placeholder in your HTML)
  fetch('header.html')
    .then(response => response.text())
    .then(data => {
      const headerPlaceholder = document.getElementById('header-placeholder');
      if (headerPlaceholder) {
        headerPlaceholder.innerHTML = data;
      }
    })
    .catch(error => console.error('Error loading header:', error));

  // 2. Load the footer (if you have footer-placeholder in your HTML)
  fetch('footer.html')
    .then(response => response.text())
    .then(data => {
      const footerPlaceholder = document.getElementById('footer-placeholder');
      if (footerPlaceholder) {
        footerPlaceholder.innerHTML = data;
      }
      // After the footer is inserted, update the year
      const yearElements = document.querySelectorAll("#year");
      const currentYear = new Date().getFullYear();
      yearElements.forEach(el => {
        // This replaces <span id="year"></span> with the actual year
        el.textContent = currentYear;
      });
    })
    .catch(error => console.error('Error loading footer:', error));


});
