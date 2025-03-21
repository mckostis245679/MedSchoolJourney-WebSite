document.addEventListener("DOMContentLoaded", function() {
  // 1. Παίρνουμε το 'id' από το query parameter
  const urlParams = new URLSearchParams(window.location.search);
  const bookId = urlParams.get('id');

  // 2. Επιλεγμένα στοιχεία στο DOM
  const breadcrumbCurrent = document.getElementById('breadcrumbCurrent');
  const bookTitleEl = document.getElementById('bookTitle');
  const bookSubtitleEl = document.getElementById('bookSubtitle');
  const bookImageEl = document.getElementById('bookImage');
  const syllabusListEl = document.getElementById('syllabusList');
  const contentsListEl = document.getElementById('contentsList');

  // 3. Αν δεν έχουμε ID, βγάζουμε μήνυμα
  if (!bookId) {
    bookTitleEl.textContent = 'Δεν βρέθηκε βιβλίο';
    return;
  }

  // 4. Φόρτωση του books.json (χρειάζεται να τρέχεις σε local server)
  fetch('books.json')
    .then(response => response.json())
    .then(data => {
      // 5. Εντοπίζουμε το βιβλίο με το id
      const book = data.find(item => item.id === bookId);
      if (!book) {
        bookTitleEl.textContent = 'Το βιβλίο δεν υπάρχει στη λίστα.';
        return;
      }

      // 6. Ενημερώνουμε το breadcrumb, τον τίτλο, υπότιτλο, εικόνα
      breadcrumbCurrent.textContent = book.title || 'Λεπτομέρειες Βιβλίου';
      bookTitleEl.textContent = book.title || 'Άγνωστος Τίτλος';
      bookSubtitleEl.textContent = book.subtitle || '';
      bookImageEl.src = book.image || 'images/placeholder.jpg';
      bookImageEl.alt = book.title || 'Εικόνα Βιβλίου';

      // 7. Γεμίζουμε τη λίστα “Ύλη που Καλύπτεται”
      if (Array.isArray(book.syllabus)) {
        syllabusListEl.innerHTML = '';
        book.syllabus.forEach(item => {
          const li = document.createElement('li');
          li.textContent = item;
          syllabusListEl.appendChild(li);
        });
      }

      // 8. Γεμίζουμε τη λίστα “Περιεχόμενα Συγγράμματος”
      if (Array.isArray(book.contents)) {
        contentsListEl.innerHTML = '';
        book.contents.forEach(item => {
          const li = document.createElement('li');
          li.textContent = item;
          contentsListEl.appendChild(li);
        });
      }
    })
    .catch(error => {
      console.error('Σφάλμα στη φόρτωση των βιβλίων:', error);
      bookTitleEl.textContent = 'Σφάλμα κατά τη φόρτωση.';
    });
});
