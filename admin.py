import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json
import os

BOOKS_JSON = "books.json"
books = []  # In-memory list of books
last_selected_id = None

ACADEMIC_HTML = "academic.html"
CLINICAL_HTML = "clinical.html"
KATAKTIRIES_HTML = "kataktiries.html"

def load_books():
    global books
    if os.path.exists(BOOKS_JSON):
        try:
            with open(BOOKS_JSON, "r", encoding="utf-8") as f:
                books = json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Σφάλμα", "Αποτυχία φόρτωσης των βιβλίων λόγω σφάλματος στο JSON.")
            books = []
    else:
        books = []

def save_changes():
    """Αποθηκεύει το 'books' σε JSON και παράγει τα τρία αρχεία HTML για κάθε κατηγορία."""
    try:
        with open(BOOKS_JSON, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=4)
        generate_all_html()
        messagebox.showinfo("Αποθηκεύτηκε", "Όλες οι αλλαγές αποθηκεύτηκαν και οι σελίδες δημιουργήθηκαν με επιτυχία.")
    except Exception as e:
        messagebox.showerror("Σφάλμα", f"Αποτυχία αποθήκευσης: {e}")

def generate_all_html():
    """Δημιουργεί τα HTML αρχεία για τις κατηγορίες: academic, clinical και kataktiries."""
    generate_category_html("academic", ACADEMIC_HTML, "Ακαδημαϊκές Σημειώσεις")
    generate_category_html("clinical", CLINICAL_HTML, "Κλινικές Σημειώσεις")
    generate_category_html("kataktiries", KATAKTIRIES_HTML, "Κατατακτήριες")

def generate_category_html(category, filename, heading):
    filtered_books = [b for b in books if b.get("category", "") == category]

    html_header = f"""<!DOCTYPE html>
<html lang="el">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{heading}</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <div id="header-placeholder"></div>
  <section class="ekdoseis-section">
    <div class="container">
      <h1>{heading}</h1>
      <p>Δείτε τα διαθέσιμα βιβλία στην κατηγορία {heading}.</p>
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
    for book in filtered_books:
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
    with open(filename, "w", encoding="utf-8") as f:
        f.write(full_html)

def refresh_book_list():
    """Ανανέωση της λίστας βιβλίων βάσει της επιλεγμένης κατηγορίας."""
    book_listbox.delete(0, tk.END)
    selected_cat = category_var.get()
    filtered_books = [b for b in books if b.get("category", "") == selected_cat]
    for book in filtered_books:
        book_listbox.insert(tk.END, f"{book['id']} - {book['title']}")

def on_book_select(event):
    """Εμφάνιση των δεδομένων του επιλεγμένου βιβλίου στη φόρμα."""
    global last_selected_id
    selected = book_listbox.curselection()
    if not selected:
        return
    index = selected[0]
    selected_cat = category_var.get()
    filtered_books = [b for b in books if b.get("category", "") == selected_cat]
    if index >= len(filtered_books):
        return
    book = filtered_books[index]
    last_selected_id = book["id"]

    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_id.insert(0, book["id"])
    entry_id.config(state="disabled")
    
    entry_title.delete(0, tk.END)
    entry_title.insert(0, book["title"])
    entry_subtitle.delete(0, tk.END)
    entry_subtitle.insert(0, book["subtitle"])
    image_path_label.config(text=book.get("image", "No file selected"))

    # Εμφάνιση syllabus και contents σε πολλαπλές γραμμές
    syllabus_text.delete("1.0", tk.END)
    syllabus_text.insert("1.0", "\n".join(book.get("syllabus", [])))
    contents_text.delete("1.0", tk.END)
    contents_text.insert("1.0", "\n".join(book.get("contents", [])))

def clear_form():
    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_id.config(state="disabled")
    entry_title.delete(0, tk.END)
    entry_subtitle.delete(0, tk.END)
    image_path_label.config(text="No file selected")
    syllabus_text.delete("1.0", tk.END)
    contents_text.delete("1.0", tk.END)

def add_book():
    title = entry_title.get().strip()
    subtitle = entry_subtitle.get().strip()
    image_path = image_path_label.cget("text")
    if image_path == "No file selected":
        image_path = ""
    syllabus_str = syllabus_text.get("1.0", tk.END).strip()
    contents_str = contents_text.get("1.0", tk.END).strip()

    if not title:
        messagebox.showerror("Σφάλμα", "Ο Τίτλος είναι υποχρεωτικό πεδίο.")
        return

    # Auto-generate new ID as one more than the maximum existing ID
    if books:
        new_id = str(max(int(b["id"]) for b in books) + 1)
    else:
        new_id = "1"

    new_book = {
        "id": new_id,
        "title": title,
        "subtitle": subtitle,
        "image": image_path,
        "category": category_var.get(),
        "syllabus": [s.strip() for s in syllabus_str.splitlines() if s.strip()],
        "contents": [c.strip() for c in contents_str.splitlines() if c.strip()]
    }

    books.append(new_book)
    refresh_book_list()
    messagebox.showinfo("Επιτυχία", "Το βιβλίο προστέθηκε!")
    clear_form()

def edit_book():
    global last_selected_id
    selected_cat = category_var.get()
    filtered_books = [b for b in books if b.get("category", "") == selected_cat]
    selected = book_listbox.curselection()
    if not selected:
        # Χρήση του last_selected_id αν δεν υπάρχει τρέχουσα επιλογή
        if last_selected_id is not None:
            indices = [i for i, b in enumerate(filtered_books) if b["id"] == last_selected_id]
            if indices:
                selected_index = indices[0]
            else:
                messagebox.showerror("Σφάλμα", "Δεν βρέθηκε το βιβλίο προς επεξεργασία.")
                return
        else:
            messagebox.showerror("Σφάλμα", "Δεν επιλέξατε βιβλίο για επεξεργασία.")
            return
    else:
        selected_index = selected[0]

    if selected_index >= len(filtered_books):
        return

    old_book = filtered_books[selected_index]
    new_title = entry_title.get().strip()
    new_subtitle = entry_subtitle.get().strip()
    new_image = image_path_label.cget("text")
    new_category = category_var.get()
    new_syllabus = [s.strip() for s in syllabus_text.get("1.0", tk.END).splitlines() if s.strip()]
    new_contents = [c.strip() for c in contents_text.get("1.0", tk.END).splitlines() if c.strip()]

    if not new_title:
        messagebox.showerror("Σφάλμα", "Ο Τίτλος είναι υποχρεωτικό πεδίο.")
        return

    # Ενημέρωση του βιβλίου
    for i, b in enumerate(books):
        if b["id"] == old_book["id"]:
            books[i] = {
                "id": old_book["id"],
                "title": new_title,
                "subtitle": new_subtitle,
                "image": new_image,
                "category": new_category,
                "syllabus": new_syllabus,
                "contents": new_contents
            }
            refresh_book_list()
            updated_filtered = [b for b in books if b.get("category", "") == new_category]
            for idx, bk in enumerate(updated_filtered):
                if bk["id"] == old_book["id"]:
                    book_listbox.select_set(idx)
                    last_selected_id = bk["id"]
                    break
            messagebox.showinfo("Επιτυχία", "Το βιβλίο ενημερώθηκε!")
            return

    messagebox.showerror("Σφάλμα", "Δεν βρέθηκε το βιβλίο στη λίστα.")

def delete_book():
    global last_selected_id
    selected_cat = category_var.get()
    filtered_books = [b for b in books if b.get("category", "") == selected_cat]
    selected = book_listbox.curselection()
    if not selected:
        messagebox.showerror("Σφάλμα", "Δεν επιλέξατε βιβλίο για διαγραφή.")
        return
    index = selected[0]
    if index >= len(filtered_books):
        return

    confirm = messagebox.askyesno("Επιβεβαίωση", f"Διαγραφή του βιβλίου: {filtered_books[index]['title']}?")
    if confirm:
        to_delete_id = filtered_books[index]["id"]
        for i, b in enumerate(books):
            if b["id"] == to_delete_id:
                del books[i]
                break
        if last_selected_id == to_delete_id:
            last_selected_id = None
        refresh_book_list()
        clear_form()
        messagebox.showinfo("Επιτυχία", "Το βιβλίο διαγράφηκε.")

def move_book_up():
    selected_cat = category_var.get()
    indices = [i for i, b in enumerate(books) if b.get("category", "") == selected_cat]
    if not indices:
        return
    selected = book_listbox.curselection()
    if not selected or selected[0] == 0:
        return
    filtered_index = selected[0]
    main_index = indices[filtered_index]
    prev_main_index = indices[filtered_index - 1]
    books[prev_main_index], books[main_index] = books[main_index], books[prev_main_index]
    refresh_book_list()
    book_listbox.select_set(filtered_index - 1)

def move_book_down():
    selected_cat = category_var.get()
    indices = [i for i, b in enumerate(books) if b.get("category", "") == selected_cat]
    if not indices:
        return
    selected = book_listbox.curselection()
    if not selected:
        return
    filtered_index = selected[0]
    if filtered_index >= len(indices) - 1:
        return
    main_index = indices[filtered_index]
    next_main_index = indices[filtered_index + 1]
    books[next_main_index], books[main_index] = books[main_index], books[next_main_index]
    refresh_book_list()
    book_listbox.select_set(filtered_index + 1)

def select_image():
    path = filedialog.askopenfilename(
        title="Select Image",
        initialdir=os.path.join(os.getcwd(), "images/books"),
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif"), ("All Files", "*.*")]
    )
    if path:
        relative_path = os.path.relpath(path, os.getcwd())
        image_path_label.config(text=relative_path)

def on_category_change(*args):
    """Ανανέωση της λίστας όταν αλλάζει η κατηγορία."""
    refresh_book_list()

def main():
    global root, entry_id, entry_title, entry_subtitle, image_path_label
    global syllabus_text, contents_text, category_var, book_listbox, last_selected_id

    root = tk.Tk()
    root.title("Διαχειριστής Εκδόσεων - Φιλτράρισμα Κατηγορίας")
    root.configure(bg="#f0f0f0")  # Ελαφρύ background
    root.geometry("1100x700")     # Μεγαλύτερο παράθυρο
    root.resizable(False, False)

    # --- Στυλ / Γραμματοσειρές ---
    label_font = ("Helvetica", 11)
    entry_font = ("Helvetica", 10)

    # Μεγάλος τίτλος
    lbl_title = tk.Label(root, text="Διαχειριστής Εκδόσεων", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
    lbl_title.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

    # --- Frame για τη Φόρμα (Αριστερά) ---
    form_frame = tk.Frame(root, bg="#f0f0f0")
    form_frame.grid(row=1, column=0, padx=(10, 10), sticky="n")

    # ID
    lbl_id = tk.Label(form_frame, text="Book ID:", font=label_font, bg="#f0f0f0")
    lbl_id.grid(row=0, column=0, sticky="e", padx=5, pady=5)
    entry_id = tk.Entry(form_frame, width=30, state="disabled", font=entry_font)
    entry_id.grid(row=0, column=1, padx=5, pady=5)

    # Title
    lbl_title_form = tk.Label(form_frame, text="Title:", font=label_font, bg="#f0f0f0")
    lbl_title_form.grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_title = tk.Entry(form_frame, width=30, font=entry_font)
    entry_title.grid(row=1, column=1, padx=5, pady=5)

    # Subtitle
    lbl_subtitle = tk.Label(form_frame, text="Subtitle:", font=label_font, bg="#f0f0f0")
    lbl_subtitle.grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_subtitle = tk.Entry(form_frame, width=30, font=entry_font)
    entry_subtitle.grid(row=2, column=1, padx=5, pady=5)

    # Category
    lbl_category = tk.Label(form_frame, text="Category:", font=label_font, bg="#f0f0f0")
    lbl_category.grid(row=3, column=0, sticky="e", padx=5, pady=5)
    category_var = tk.StringVar(root)
    categories = ["academic", "clinical", "kataktiries"]
    category_var.set("academic")
    option_category = tk.OptionMenu(form_frame, category_var, *categories)
    option_category.config(width=28)
    option_category.grid(row=3, column=1, padx=5, pady=5, sticky="w")
    category_var.trace("w", on_category_change)

    # Image
    lbl_image = tk.Label(form_frame, text="Image:", font=label_font, bg="#f0f0f0")
    lbl_image.grid(row=4, column=0, sticky="e", padx=5, pady=5)
    image_path_label = tk.Label(form_frame, text="No file selected", fg="gray", anchor="w", width=30, relief="sunken", bg="#fff")
    image_path_label.grid(row=4, column=1, sticky="w", padx=5, pady=5)
    btn_browse = tk.Button(form_frame, text="Browse...", command=select_image, font=entry_font)
    btn_browse.grid(row=4, column=2, sticky="w", padx=5, pady=5)

    # Syllabus
    lbl_syllabus = tk.Label(form_frame, text="Syllabus (one/line):", font=label_font, bg="#f0f0f0")
    lbl_syllabus.grid(row=5, column=0, sticky="ne", padx=5, pady=5)
    syllabus_text = tk.Text(form_frame, width=40, height=5, font=entry_font, wrap="word")
    syllabus_text.grid(row=5, column=1, columnspan=2, sticky="w", padx=5, pady=5)

    # Contents
    lbl_contents = tk.Label(form_frame, text="Contents (one/line):", font=label_font, bg="#f0f0f0")
    lbl_contents.grid(row=6, column=0, sticky="ne", padx=5, pady=5)
    contents_text = tk.Text(form_frame, width=40, height=7, font=entry_font, wrap="word")
    contents_text.grid(row=6, column=1, columnspan=2, sticky="w", padx=5, pady=5)

    # Buttons κάτω από τη φόρμα
    btn_add = tk.Button(form_frame, text="Add Book", command=add_book, font=entry_font, bg="#e7e7e7")
    btn_add.grid(row=7, column=1, pady=10, sticky="w")
    btn_edit = tk.Button(form_frame, text="Edit Selected", command=edit_book, font=entry_font, bg="#e7e7e7")
    btn_edit.grid(row=8, column=1, pady=5, sticky="w")
    btn_delete = tk.Button(form_frame, text="Delete Selected", command=delete_book, font=entry_font, bg="#e7e7e7")
    btn_delete.grid(row=9, column=1, pady=10, sticky="w")

    # --- Frame για τη Λίστα (Δεξιά) ---
    list_frame = tk.Frame(root, bg="#f0f0f0")
    list_frame.grid(row=1, column=1, sticky="n", padx=(10,10))

    book_listbox = tk.Listbox(list_frame, width=50, height=25, font=("Helvetica", 10))
    book_listbox.grid(row=0, column=0, rowspan=11, sticky="n")

    scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=book_listbox.yview)
    scrollbar.grid(row=0, column=1, rowspan=11, sticky="ns")
    book_listbox.config(yscrollcommand=scrollbar.set)
    book_listbox.bind("<<ListboxSelect>>", on_book_select)

    btn_up = tk.Button(list_frame, text="↑ Move Up", command=move_book_up, font=entry_font, bg="#e7e7e7")
    btn_up.grid(row=11, column=0, sticky="ew", padx=(0, 0), pady=5)
    btn_down = tk.Button(list_frame, text="↓ Move Down", command=move_book_down, font=entry_font, bg="#e7e7e7")
    btn_down.grid(row=12, column=0, sticky="ew", padx=(0, 0))

    # --- Save Changes Button (κάτω αριστερά ή σε νέα γραμμή) ---
    btn_save = tk.Button(root, text="💾 Save Changes", command=save_changes, bg="#4CAF50", fg="white", font=("Helvetica", 11, "bold"))
    btn_save.grid(row=2, column=0, padx=10, pady=20, sticky="w")

    load_books()
    refresh_book_list()
    root.mainloop()

if __name__ == "__main__":
    main()
