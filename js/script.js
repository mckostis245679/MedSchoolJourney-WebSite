// script.js

document.addEventListener("DOMContentLoaded", function() {
  // 1. Load the header
  fetch('header.html')
    .then(response => response.text())
    .then(data => {
      const headerPlaceholder = document.getElementById('header-placeholder');
      if (headerPlaceholder) {
        headerPlaceholder.innerHTML = data;
        initMobileMenu();   // ← αρχικοποίηση hamburger menu
      }
    })
    .catch(error => console.error('Error loading header:', error));

  // 2. Load the footer
  fetch('footer.html')
    .then(response => response.text())
    .then(data => {
      const footerPlaceholder = document.getElementById('footer-placeholder');
      if (footerPlaceholder) {
        footerPlaceholder.innerHTML = data;
      }
      updateFooterYear();
    })
    .catch(error => console.error('Error loading footer:', error));
});

// ---------------------------
// Mobile menu (hamburger) logic
// ---------------------------
function initMobileMenu() {
  const hamburger = document.getElementById('hamburger');
  const navMenu   = document.querySelector('.main-nav');

  if (!hamburger || !navMenu) return;

  // Άνοιγμα/Κλείσιμο με toggle κλάσης .open
  hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('open');
  });

  // Κλείσε όταν κάνεις κλικ σε οποιοδήποτε link
  navMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('open');
    });
  });

  // (προαιρετικό) Κλείσε αν κλικάρεις έξω από το menu
  document.addEventListener('click', e => {
    if (!navMenu.contains(e.target) && e.target !== hamburger) {
      navMenu.classList.remove('open');
    }
  });
}

// ---------------------------
// Footer Year update
// ---------------------------
function updateFooterYear() {
  const yearElements = document.querySelectorAll("#year");
  const currentYear = new Date().getFullYear();
  yearElements.forEach(el => el.textContent = currentYear);
}

// ---------------------------
// EmailJS contact form logic
// ---------------------------
function sendMail() {
  const btn = document.getElementById('sendBtn');
  if (btn.disabled) return;  // αποφυγή double-send

  const params = {
    email:   document.getElementById("email").value,
    message: document.getElementById("message").value
  };

  btn.textContent = 'Sending…';
  btn.disabled   = true;

  const serviceID  = "service_hecci3k";
  const templateID = "template_kfos0wa";

  emailjs.send(serviceID, templateID, params)
    .then(res => {
      document.getElementById("email").value   = "";
      document.getElementById("message").value = "";
      btn.textContent = 'Email sent';
    })
    .catch(err => {
      console.error(err);
      btn.textContent = 'Error — try again';
      btn.disabled   = false;
    });
}
