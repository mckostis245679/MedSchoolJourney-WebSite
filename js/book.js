document.addEventListener("DOMContentLoaded", function() {
    // Λήψη του query parameter "id" από το URL
    const urlParams = new URLSearchParams(window.location.search);
    const bookId = urlParams.get('id');
  
    const bookContent = document.getElementById('book-content');
  
    if (!bookId) {
      bookContent.innerHTML = '<p>Δεν επιλέχθηκε βιβλίο.</p>';
      return;
    }
  
    // Φόρτωση του αρχείου books.json (αν δεν χρησιμοποιείς server, χρησιμοποίησε έναν τοπικό server)
    fetch('books.json')
      .then(response => response.json())
      .then(data => {
        // Εύρεση του βιβλίου με το συγκεκριμένο id
        const book = data.find(b => b.id === bookId);
        if (!book) {
          bookContent.innerHTML = '<p>Δεν βρέθηκε το βιβλίο.</p>';
          return;
        }
        
        // Δημιουργία HTML για την εμφάνιση των λεπτομερειών
        let html = `<h1>${book.title}</h1>`;
        
        // Δημιουργία carousel με dots για τις εικόνες
        if (book.images && book.images.length > 0) {
          html += `<div class="carousel">`;
          book.images.forEach((img, index) => {
            html += `<img src="${img}" alt="${book.title} Εικόνα ${index + 1}" class="carousel-image ${index === 0 ? 'active' : ''}">`;
          });
          html += `<div class="carousel-dots">`;
          book.images.forEach((_, index) => {
            html += `<span class="dot ${index === 0 ? 'active' : ''}" data-index="${index}"></span>`;
          });
          html += `</div></div>`;
        }
        
        // Εμφάνιση της περιγραφής του βιβλίου
        html += `<div class="book-description"><p>${book.description}</p></div>`;
        
        bookContent.innerHTML = html;
  
        // Ενεργοποίηση του carousel (όπως στο προηγούμενο παράδειγμα με dots)
        const carousel = document.querySelector('.carousel');
        if (carousel) {
          const images = carousel.querySelectorAll('.carousel-image');
          const dots = carousel.querySelectorAll('.carousel-dots .dot');
          let currentIndex = 0;
          function showImage(index) {
            images.forEach((img, i) => {
              img.classList.toggle('active', i === index);
            });
            dots.forEach((dot, i) => {
              dot.classList.toggle('active', i === index);
            });
          }
          dots.forEach(dot => {
            dot.addEventListener('click', function() {
              const index = parseInt(dot.getAttribute('data-index'));
              currentIndex = index;
              showImage(currentIndex);
            });
          });
        }
      })
      .catch(error => {
        console.error('Σφάλμα στη φόρτωση των δεδομένων:', error);
        bookContent.innerHTML = '<p>Σφάλμα στη φόρτωση των λεπτομερειών του βιβλίου.</p>';
      });
  });
  