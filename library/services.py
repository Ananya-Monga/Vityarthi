"""Business logic for books, members, circulation, and reports."""
from datetime import date, timedelta
from .database import connect

def _required(value, label):
    value = (value or "").strip()
    if not value:
        raise ValueError(f"{label} is required")
    return value

def add_book(title, author, isbn, copies):
    title, author = _required(title, "Title"), _required(author, "Author")
    copies = int(copies)
    if copies < 1:
        raise ValueError("Copies must be at least 1")
    with connect() as c:
        cur = c.execute("INSERT INTO books(title,author,isbn,total_copies,available_copies) VALUES(?,?,?,?,?)",
                        (title, author, (isbn or "").strip() or None, copies, copies))
        return cur.lastrowid

def list_books(search=""):
    q = f"%{(search or '').strip()}%"
    with connect() as c:
        return c.execute("""SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ? OR COALESCE(isbn,'') LIKE ?
            ORDER BY title""", (q,q,q)).fetchall()

def update_book(book_id, title, author, isbn, total_copies):
    title, author = _required(title, "Title"), _required(author, "Author")
    total_copies = int(total_copies)
    if total_copies < 1:
        raise ValueError("Total copies must be at least 1")
    with connect() as c:
        row = c.execute("SELECT * FROM books WHERE id=?", (book_id,)).fetchone()
        if not row: raise ValueError("Book not found")
        checked_out = row["total_copies"] - row["available_copies"]
        if total_copies < checked_out:
            raise ValueError("Total copies cannot be less than copies currently on loan")
        available = total_copies - checked_out
        c.execute("""UPDATE books SET title=?,author=?,isbn=?,total_copies=?,available_copies=? WHERE id=?""",
                  (title,author,(isbn or "").strip() or None,total_copies,available,book_id))

def delete_book(book_id):
    with connect() as c:
        active = c.execute("SELECT COUNT(*) n FROM loans WHERE book_id=? AND status='ISSUED'", (book_id,)).fetchone()["n"]
        if active: raise ValueError("Cannot delete a book with active loans")
        c.execute("DELETE FROM books WHERE id=?", (book_id,))

def add_member(name, email, phone=""):
    name, email = _required(name, "Name"), _required(email, "Email")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Enter a valid email address")
    with connect() as c:
        cur = c.execute("INSERT INTO members(name,email,phone) VALUES(?,?,?)",
                        (name,email,(phone or "").strip()))
        return cur.lastrowid

def list_members(search=""):
    q = f"%{(search or '').strip()}%"
    with connect() as c:
        return c.execute("""SELECT * FROM members
            WHERE name LIKE ? OR email LIKE ? OR COALESCE(phone,'') LIKE ?
            ORDER BY name""", (q,q,q)).fetchall()

def update_member(member_id, name, email, phone=""):
    name, email = _required(name, "Name"), _required(email, "Email")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Enter a valid email address")
    with connect() as c:
        if not c.execute("SELECT 1 FROM members WHERE id=?", (member_id,)).fetchone():
            raise ValueError("Member not found")
        c.execute("UPDATE members SET name=?,email=?,phone=? WHERE id=?",
                  (name,email,(phone or "").strip(),member_id))

def delete_member(member_id):
    with connect() as c:
        active = c.execute("SELECT COUNT(*) n FROM loans WHERE member_id=? AND status='ISSUED'", (member_id,)).fetchone()["n"]
        if active: raise ValueError("Cannot delete a member with active loans")
        c.execute("DELETE FROM members WHERE id=?", (member_id,))

def issue_book(book_id, member_id, loan_days=14):
    with connect() as c:
        book = c.execute("SELECT * FROM books WHERE id=?", (book_id,)).fetchone()
        member = c.execute("SELECT * FROM members WHERE id=?", (member_id,)).fetchone()
        if not book: raise ValueError("Book not found")
        if not member: raise ValueError("Member not found")
        if book["available_copies"] < 1: raise ValueError("No copies available")
        if int(loan_days) < 1: raise ValueError("Loan duration must be positive")
        today = date.today()
        due = today + timedelta(days=int(loan_days))
        cur = c.execute("""INSERT INTO loans(book_id,member_id,issue_date,due_date)
                           VALUES(?,?,?,?)""", (book_id,member_id,today.isoformat(),due.isoformat()))
        c.execute("UPDATE books SET available_copies=available_copies-1 WHERE id=?", (book_id,))
        return cur.lastrowid

def return_book(loan_id):
    with connect() as c:
        loan = c.execute("SELECT * FROM loans WHERE id=?", (loan_id,)).fetchone()
        if not loan: raise ValueError("Loan not found")
        if loan["status"] == "RETURNED": raise ValueError("This loan has already been returned")
        c.execute("UPDATE loans SET status='RETURNED',return_date=? WHERE id=?",
                  (date.today().isoformat(),loan_id))
        c.execute("UPDATE books SET available_copies=available_copies+1 WHERE id=?", (loan["book_id"],))

def list_loans(status=None):
    with connect() as c:
        sql = """SELECT l.*, b.title, m.name AS member_name
                 FROM loans l JOIN books b ON b.id=l.book_id
                 JOIN members m ON m.id=l.member_id"""
        args = ()
        if status:
            sql += " WHERE l.status=?"
            args = (status,)
        return c.execute(sql + " ORDER BY l.id DESC", args).fetchall()

def overdue_loans():
    today = date.today().isoformat()
    with connect() as c:
        return c.execute("""SELECT l.*,b.title,m.name AS member_name,m.email
            FROM loans l JOIN books b ON b.id=l.book_id
            JOIN members m ON m.id=l.member_id
            WHERE l.status='ISSUED' AND l.due_date < ? ORDER BY l.due_date""", (today,)).fetchall()

def dashboard():
    with connect() as c:
        return {
            "titles": c.execute("SELECT COUNT(*) n FROM books").fetchone()["n"],
            "copies": c.execute("SELECT COALESCE(SUM(total_copies),0) n FROM books").fetchone()["n"],
            "available": c.execute("SELECT COALESCE(SUM(available_copies),0) n FROM books").fetchone()["n"],
            "members": c.execute("SELECT COUNT(*) n FROM members").fetchone()["n"],
            "active_loans": c.execute("SELECT COUNT(*) n FROM loans WHERE status='ISSUED'").fetchone()["n"],
            "overdue": len(overdue_loans())
        }
