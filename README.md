# Library Management System (Python)

A small, modular library management mini-project built with Python and SQLite. It provides book and member CRUD, book issue/return, inventory tracking, an overdue report, and a dashboard summary.

## Features
- **Book management:** add, search, update, and delete books.
- **Member management:** add, search, update, and delete members.
- **Circulation:** issue books, set a loan period, and record returns.
- **Reports:** active loans, overdue loans, and dashboard counts.
- **Data persistence:** SQLite database created automatically.
- **Validation:** required fields, email format, copy counts, duplicate ISBN/email constraints, and prevention of deleting records with active loans.
- **Tests:** unit tests for issue/return, unavailable inventory, and required fields.

## Technology
Python 3.10+ · SQLite · `unittest` (standard library)

## Project structure
```text
library_management_python/
├── main.py
├── library/
│   ├── __init__.py
│   ├── database.py
│   ├── services.py
│   └── cli.py
├── tests/
│   └── test_services.py
├── docs/
│   ├── design.md
│   └── report.pdf
├── statement.md
├── requirements.txt
└── README.md
```

## Installation and run
1. Install Python 3.10 or newer.
2. Download/clone this repository.
3. Open a terminal in the project folder.
4. Run:
   ```bash
   python main.py
   ```
The `library.db` file and database tables are created automatically on first run.

## Testing
Run from the project root:
```bash
python -m unittest discover -s tests -v
```

## Typical workflow
1. Add books and their total copy count.
2. Register members.
3. Issue a book using its book ID and a member ID.
4. Return the book using its loan ID.
5. Review active loans, overdue loans, and dashboard counts.

## GitHub upload
Create a new **public or private** repository on GitHub, for example `python-library-management`. Then run these commands from this folder:
```bash
git init
git add .
git commit -m "Initial library management mini-project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/python-library-management.git
git push -u origin main
```
Replace `YOUR-USERNAME` with the GitHub account name and use the repository URL shown by GitHub. Do not commit personal data or a populated `library.db`.

## Design documentation
See [`statement.md`](statement.md) and [`docs/design.md`](docs/design.md). The project report PDF is in `docs/report.pdf`.
