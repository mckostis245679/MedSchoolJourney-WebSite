import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

# Paths to your JSON and HTML files
BOOKS_JSON = "books.json"
EDKOSEIS_HTML = "ekdoseis.html"

def load_books():
    """Read existing books from books.json."""
    if not os.path.exists(BOOKS_JSON):
        return []
    with open(BOOKS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def save_books(books):
    """Save the list of books to books.json."""
    with open(BOOKS_JSON, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

def generate_html(books):
    html_header = """<!DOCTYPE html>
<html lang="el">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Εκδόσεις</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <div id="header-placeholder"></div>
  <section class="ekdoseis-section">
    <div class="container">
      <h1>Εκδόσεις</h1>
      <p>Δείτε τις τελευταίες εκδόσεις μας σε πανεπιστημιακά συγγράμματα.</p>
      <div class="ekdoseis-grid">
    """
    html_footer = """
      </div>
    </div>
  </section>
  <div id="footer-placeholder"></div>
  <script src="js/script.js"></script>
</body>
</html>"""

    cards_html = ""
    for book in books:
        card = f"""
        <div class="publication-card">
          <a href="book.html?id={book.get('id')}" class="card-link">
            <img src="{book.get('image')}" alt="{book.get('title', 'Βιβλίο')}">
            <h3>{book.get('title')}</h3>
            <p>{book.get('subtitle')}</p>
          </a>
          <a href="book.html?id={book.get('id')}" class="btn-sm">Περισσότερα</a>
        </div>
        """
        cards_html += card

    full_html = html_header + cards_html + html_footer
    with open(EDKOSEIS_HTML, "w", encoding="utf-8") as f:
        f.write(full_html)

def add_book():
    """
    Called when the user clicks 'Add Book'.
    Gathers form data, updates books.json, regenerates ekdoseis.html.
    """
    book_id = entry_id.get().strip()
    title = entry_title.get().strip()
    subtitle = entry_subtitle.get().strip()
    # Get image path from the label text (if file selected, otherwise empty)
    image_path = image_path_label.cget("text")
    # If no file selected, set image_path to empty string
    if image_path == "No file selected":
        image_path = ""
    syllabus_str = entry_syllabus.get().strip()
    contents_str = entry_contents.get().strip()

    if not book_id or not title:
        messagebox.showerror("Σφάλμα", "Το ID και ο Τίτλος είναι υποχρεωτικά πεδία.")
        return

    # Convert comma-separated strings to lists
    syllabus = [s.strip() for s in syllabus_str.split(",")] if syllabus_str else []
    contents = [c.strip() for c in contents_str.split(",")] if contents_str else []

    new_book = {
        "id": book_id,
        "title": title,
        "subtitle": subtitle,
        "image": image_path,
        "syllabus": syllabus,
        "contents": contents
    }

    books = load_books()
    # Check for duplicate ID
    for b in books:
        if b.get("id") == book_id:
            messagebox.showerror("Σφάλμα", "Υπάρχει ήδη βιβλίο με αυτό το ID!")
            return

    books.append(new_book)
    save_books(books)
    generate_html(books)
    messagebox.showinfo("Επιτυχία", "Το βιβλίο προστέθηκε και η σελίδα ενημερώθηκε!")

    # Clear fields
    entry_id.delete(0, tk.END)
    entry_title.delete(0, tk.END)
    entry_subtitle.delete(0, tk.END)
    image_path_label.config(text="No file selected")
    entry_syllabus.delete(0, tk.END)
    entry_contents.delete(0, tk.END)

def select_image():
    """
    Open a file dialog for the user to select an image path.
    Updates the image_path_label with the chosen path.
    """
    path = filedialog.askopenfilename(
        title="Select Image",
        initialdir="images/books",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif"), ("All Files", "*.*")]
    )
    if path:
        image_path_label.config(text=path)

# Create the main Tkinter window
root = tk.Tk()
root.title("Διαχειριστής Εκδόσεων - Προσθήκη Βιβλίου")
root.configure(padx=20, pady=20)  # Add some padding around the window

# Title label for the application
title_label = tk.Label(root, text="Διαχειριστής Εκδόσεων", font=("Helvetica", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Book ID
lbl_id = tk.Label(root, text="Book ID:")
lbl_id.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_id = tk.Entry(root, width=30)
entry_id.grid(row=1, column=1, padx=5, pady=5)

# Title
lbl_title = tk.Label(root, text="Title:")
lbl_title.grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_title = tk.Entry(root, width=30)
entry_title.grid(row=2, column=1, padx=5, pady=5)

# Subtitle
lbl_subtitle = tk.Label(root, text="Subtitle:")
lbl_subtitle.grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_subtitle = tk.Entry(root, width=30)
entry_subtitle.grid(row=3, column=1, padx=5, pady=5)

# Image Path: Only a Browse button and a label showing the selected file
lbl_image = tk.Label(root, text="Image:")
lbl_image.grid(row=4, column=0, padx=5, pady=5, sticky="e")
btn_select_image = tk.Button(root, text="Browse...", command=select_image)
btn_select_image.grid(row=4, column=1, padx=5, pady=5, sticky="w")
image_path_label = tk.Label(root, text="No file selected", fg="gray")
image_path_label.grid(row=4, column=1, padx=80, pady=5, sticky="w")

# Syllabus (comma-separated)
lbl_syllabus = tk.Label(root, text="Syllabus (comma-separated):")
lbl_syllabus.grid(row=5, column=0, padx=5, pady=5, sticky="e")
entry_syllabus = tk.Entry(root, width=30)
entry_syllabus.grid(row=5, column=1, padx=5, pady=5)

# Contents (comma-separated)
lbl_contents = tk.Label(root, text="Contents (comma-separated):")
lbl_contents.grid(row=6, column=0, padx=5, pady=5, sticky="e")
entry_contents = tk.Entry(root, width=30)
entry_contents.grid(row=6, column=1, padx=5, pady=5)

# Button: Add Book
btn_add = tk.Button(root, text="Add Book", font=("Helvetica", 12), command=add_book)
btn_add.grid(row=7, column=0, columnspan=2, padx=5, pady=20)

root.mainloop()
