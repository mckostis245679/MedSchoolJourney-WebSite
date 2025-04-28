// js/book.js

document.addEventListener("DOMContentLoaded", function() {
  // 1. Παίρνουμε το 'id' από το query parameter
  const urlParams = new URLSearchParams(window.location.search);
  const bookId = urlParams.get('id');

  // 2. Επιλεγμένα στοιχεία στο DOM
  const breadcrumbCurrent     = document.getElementById('breadcrumbCurrent');
  const bookTitleEl           = document.getElementById('bookTitle');
  const bookSubtitleEl        = document.getElementById('bookSubtitle');
  const bookImageEl           = document.getElementById('bookImage');
  const syllabusListEl        = document.getElementById('syllabusList');
  const contentsListEl        = document.getElementById('contentsList');
  const breadcrumbCategoryEl  = document.getElementById('breadcrumbCategory');
  const msgField              = document.getElementById('message');

  // 3. Χαρτογράφηση για μετάφραση κατηγορίας
  const categoryMap = {
    academic:    "1ο - 7ο εξάμηνο",
    clinical:    "8ο - 12ο εξάμηνο",
    kataktiries: "Κατατακτήριες"
  };
  // 4. Χαρτογράφηση για τα αντίστοιχα URL των κατηγοριών
  const categoryLinks = {
    academic:    "academic.html",
    clinical:    "clinical.html",
    kataktiries: "kataktiries.html"
  };

  // 5. Πρώτος έλεγχος: έλλειψη ID
  if (!bookId) {
    bookTitleEl.textContent = 'Δεν βρέθηκε βιβλίο';
    return;
  }

  // 6. Φόρτωση του books.json (τρέχει σε local server)
  fetch('books.json')
    .then(response => response.json())
    .then(data => {
      // 7. Εντοπίζουμε το βιβλίο με το id
      const book = data.find(item => item.id === bookId);
      if (!book) {
        bookTitleEl.textContent = 'Το βιβλίο δεν υπάρχει στη λίστα.';
        return;
      }

      // 8. Ενημερώνουμε το breadcrumb, τον τίτλο, τον υπότιτλο και την εικόνα
      breadcrumbCurrent.textContent = book.title;
      bookTitleEl.textContent       = book.title;
      bookSubtitleEl.textContent    = book.subtitle || '';
      bookImageEl.src               = book.image || 'images/placeholder.jpg';
      bookImageEl.alt               = book.title;

      // 9. Ορίζουμε την κατηγορία στο breadcrumb
      const categoryKey  = book.category;
      const categoryText = categoryMap[categoryKey] || book.category;
      breadcrumbCategoryEl.textContent = categoryText;
      breadcrumbCategoryEl.href        = categoryLinks[categoryKey] || "#";

      // 10. Γεμίζουμε τη λίστα “Ύλη που Καλύπτεται”
      if (Array.isArray(book.syllabus)) {
        syllabusListEl.innerHTML = '';
        book.syllabus.forEach(item => {
          const li = document.createElement('li');
          li.textContent = item;
          syllabusListEl.appendChild(li);
        });
      }

      // 11. Γεμίζουμε τη λίστα “Περιεχόμενα Συγγράμματος”
      if (Array.isArray(book.contents)) {
        contentsListEl.innerHTML = '';
        book.contents.forEach(item => {
          const li = document.createElement('li');
          li.textContent = item;
          contentsListEl.appendChild(li);
        });
      }

      // 12. Ορισμός του preset μηνύματος στο textarea
      if (msgField) {
        msgField.value =
          `Θα ήθελα να αποκτήσω πρόσβαση στο e-book με τίτλο "${book.title}". ` +
          `Παρακαλώ επικοινωνήστε μαζί μου για περισσότερες πληροφορίες και ενημερώστε με ` +
          `για τη διαδικασία απόκτησης του e-book.`;

        // Προαιρετικά: καθαρίζει το default όταν ο χρήστης κάνει focus
      
      }
    })
    .catch(error => {
      console.error('Σφάλμα στη φόρτωση των βιβλίων:', error);
      bookTitleEl.textContent = 'Σφάλμα κατά τη φόρτωση.';
    });
});
