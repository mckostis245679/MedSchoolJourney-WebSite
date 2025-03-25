import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

BOOKS_JSON = "books.json"
EDKOSEIS_HTML = "ekdoseis.html"
books = []  # in-memory

def load_books():
    global books
    if os.path.exists(BOOKS_JSON):
        with open(BOOKS_JSON, "r", encoding="utf-8") as f:
            books = json.load(f)
    else:
        books = []

def save_changes():
    with open(BOOKS_JSON, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)
    generate_html()
    messagebox.showinfo("Αποθηκεύτηκε", "Όλες οι αλλαγές αποθηκεύτηκαν με επιτυχία.")

def generate_html():
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

def refresh_book_list():
    book_listbox.delete(0, tk.END)
    for book in books:
        book_listbox.insert(tk.END, f"{book['id']} - {book['title']}")

def on_book_select(event):
    selected = book_listbox.curselection()
    if not selected:
        return
    index = selected[0]
    book = books[index]

    entry_id.delete(0, tk.END)
    entry_id.insert(0, book["id"])
    entry_title.delete(0, tk.END)
    entry_title.insert(0, book["title"])
    entry_subtitle.delete(0, tk.END)
    entry_subtitle.insert(0, book["subtitle"])
    image_path_label.config(text=book.get("image", "No file selected"))

    syllabus_text.delete("1.0", "end")
    syllabus_text.insert("1.0", ", ".join(book.get("syllabus", [])))

    contents_text.delete("1.0", "end")
    contents_text.insert("1.0", ", ".join(book.get("contents", [])))

def clear_form():
    entry_id.delete(0, tk.END)
    entry_title.delete(0, tk.END)
    entry_subtitle.delete(0, tk.END)
    image_path_label.config(text="No file selected")
    syllabus_text.delete("1.0", "end")
    contents_text.delete("1.0", "end")

def add_book():
    book_id = entry_id.get().strip()
    title = entry_title.get().strip()
    subtitle = entry_subtitle.get().strip()
    image_path = image_path_label.cget("text")
    if image_path == "No file selected":
        image_path = ""

    syllabus_str = syllabus_text.get("1.0", "end").strip()
    contents_str = contents_text.get("1.0", "end").strip()

    if not book_id or not title:
        messagebox.showerror("Σφάλμα", "Το ID και ο Τίτλος είναι υποχρεωτικά πεδία.")
        return

    if any(b["id"] == book_id for b in books):
        messagebox.showerror("Σφάλμα", "Υπάρχει ήδη βιβλίο με αυτό το ID!")
        return

    new_book = {
        "id": book_id,
        "title": title,
        "subtitle": subtitle,
        "image": image_path,
        "syllabus": [s.strip() for s in syllabus_str.split(",") if s.strip()],
        "contents": [c.strip() for c in contents_str.split(",") if c.strip()]
    }

    books.append(new_book)
    refresh_book_list()
    messagebox.showinfo("Επιτυχία", "Το βιβλίο προστέθηκε!")
    clear_form()

def edit_book():
    book_id = entry_id.get().strip()
    for i, book in enumerate(books):
        if book["id"] == book_id:
            books[i] = {
                "id": book_id,
                "title": entry_title.get().strip(),
                "subtitle": entry_subtitle.get().strip(),
                "image": image_path_label.cget("text"),
                "syllabus": [s.strip() for s in syllabus_text.get("1.0", "end").split(",") if s.strip()],
                "contents": [c.strip() for c in contents_text.get("1.0", "end").split(",") if c.strip()]
            }
            refresh_book_list()
            messagebox.showinfo("Επιτυχία", "Το βιβλίο ενημερώθηκε!")
            return
    messagebox.showerror("Σφάλμα", "Δεν βρέθηκε βιβλίο με αυτό το ID.")

def delete_book():
    selected = book_listbox.curselection()
    if not selected:
        messagebox.showerror("Σφάλμα", "Δεν επιλέξατε βιβλίο για διαγραφή.")
        return
    index = selected[0]
    confirm = messagebox.askyesno("Επιβεβαίωση", f"Διαγραφή του βιβλίου: {books[index]['title']}?")
    if confirm:
        del books[index]
        refresh_book_list()
        clear_form()
        messagebox.showinfo("Επιτυχία", "Το βιβλίο διαγράφηκε.")

def move_book_up():
    selected = book_listbox.curselection()
    if not selected or selected[0] == 0:
        return
    index = selected[0]
    books[index - 1], books[index] = books[index], books[index - 1]
    refresh_book_list()
    book_listbox.select_set(index - 1)

def move_book_down():
    selected = book_listbox.curselection()
    if not selected or selected[0] == len(books) - 1:
        return
    index = selected[0]
    books[index + 1], books[index] = books[index], books[index + 1]
    refresh_book_list()
    book_listbox.select_set(index + 1)

def select_image():
    path = filedialog.askopenfilename(
        title="Select Image",
        initialdir=os.path.join(os.getcwd(), "images/books"),
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif"), ("All Files", "*.*")]
    )
    if path:
        relative_path = os.path.relpath(path, os.getcwd())
        image_path_label.config(text=relative_path)

# --- GUI ---
root = tk.Tk()
root.title("Διαχειριστής Εκδόσεων - Προσθήκη Βιβλίου")
root.configure(padx=20, pady=20)
root.geometry("1000x700")
root.resizable(False, False)

tk.Label(root, text="Διαχειριστής Εκδόσεων", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 20))

tk.Label(root, text="Book ID:").grid(row=1, column=0, sticky="e")
entry_id = tk.Entry(root, width=30)
entry_id.grid(row=1, column=1)

tk.Label(root, text="Title:").grid(row=2, column=0, sticky="e")
entry_title = tk.Entry(root, width=30)
entry_title.grid(row=2, column=1)

tk.Label(root, text="Subtitle:").grid(row=3, column=0, sticky="e")
entry_subtitle = tk.Entry(root, width=30)
entry_subtitle.grid(row=3, column=1)

tk.Label(root, text="Image:").grid(row=4, column=0, sticky="e")
image_path_label = tk.Label(root, text="No file selected", fg="gray", anchor="w", width=40, relief="sunken")
image_path_label.grid(row=4, column=1, columnspan=2, sticky="w", padx=5, pady=5)

tk.Button(root, text="Browse...", command=select_image).grid(row=5, column=1, sticky="w", padx=5, pady=5)

tk.Label(root, text="Syllabus (comma-separated):").grid(row=6, column=0, sticky="ne")
syllabus_text = tk.Text(root, width=40, height=3)
syllabus_text.grid(row=6, column=1, columnspan=2, sticky="w", padx=5)

tk.Label(root, text="Contents (comma-separated):").grid(row=7, column=0, sticky="ne")
contents_text = tk.Text(root, width=40, height=5)
contents_text.grid(row=7, column=1, columnspan=2, sticky="w", padx=5)

tk.Button(root, text="Add Book", command=add_book).grid(row=8, column=1, pady=10)
tk.Button(root, text="Edit Selected", command=edit_book).grid(row=9, column=1)
tk.Button(root, text="Delete Selected", command=delete_book).grid(row=10, column=1, pady=10)

book_listbox = tk.Listbox(root, width=40, height=20)
book_listbox.grid(row=1, column=3, rowspan=10, padx=(20, 0))
book_listbox.bind("<<ListboxSelect>>", on_book_select)

btn_up = tk.Button(root, text="↑ Move Up", command=move_book_up)
btn_up.grid(row=11, column=3, sticky="ew", padx=(20, 0))

btn_down = tk.Button(root, text="↓ Move Down", command=move_book_down)
btn_down.grid(row=12, column=3, sticky="ew", padx=(20, 0))

tk.Button(root, text="💾 Save Changes", command=save_changes, bg="#4CAF50", fg="white").grid(row=13, column=1, pady=20)

load_books()
refresh_book_list()
root.mainloop()
