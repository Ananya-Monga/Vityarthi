"""Simple interactive command-line interface."""
from . import services as s

def ask(prompt):
    return input(prompt).strip()

def show(rows):
    if not rows:
        print("No records found.")
        return
    for r in rows:
        print(" | ".join(f"{k}={r[k]}" for k in r.keys()))

def run():
    while True:
        print("""
=== LIBRARY MANAGEMENT ===
1. Dashboard
2. List/search books
3. Add book
4. Update book
5. Delete book
6. List members
7. Add member
8. Update member
9. Delete member
10. Issue book
11. Return book
12. Active loans
13. Overdue report
0. Exit
""")
        choice = ask("Choose: ")
        try:
            if choice == "0": print("Goodbye."); break
            elif choice == "1": print(s.dashboard())
            elif choice == "2": show(s.list_books(ask("Search title/author/ISBN (blank = all): ")))
            elif choice == "3":
                print("Created book ID:", s.add_book(ask("Title: "),ask("Author: "),ask("ISBN (optional): "),ask("Copies: ")))
            elif choice == "4":
                s.update_book(int(ask("Book ID: ")),ask("Title: "),ask("Author: "),ask("ISBN: "),ask("Total copies: "))
                print("Book updated.")
            elif choice == "5": s.delete_book(int(ask("Book ID: "))); print("Book deleted.")
            elif choice == "6": show(s.list_members(ask("Search name/email (blank = all): ")))
            elif choice == "7":
                print("Created member ID:", s.add_member(ask("Name: "),ask("Email: "),ask("Phone: ")))
            elif choice == "8":
                s.update_member(int(ask("Member ID: ")),ask("Name: "),ask("Email: "),ask("Phone: "))
                print("Member updated.")
            elif choice == "9": s.delete_member(int(ask("Member ID: "))); print("Member deleted.")
            elif choice == "10":
                print("Loan ID:", s.issue_book(int(ask("Book ID: ")),int(ask("Member ID: ")),ask("Loan days [14]: ") or 14))
            elif choice == "11": s.return_book(int(ask("Loan ID: "))); print("Book returned.")
            elif choice == "12": show(s.list_loans("ISSUED"))
            elif choice == "13": show(s.overdue_loans())
            else: print("Invalid choice.")
        except (ValueError, TypeError) as e:
            print("Error:", e)
        except Exception as e:
            print("Operation failed:", e)
