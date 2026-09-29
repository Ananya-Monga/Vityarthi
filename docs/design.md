# Design and Technical Documentation

## Functional requirements
- FR1: Create, search, update, and delete book records.
- FR2: Register, search, update, and delete library members.
- FR3: Issue an available book to a registered member.
- FR4: Record returns and restore available inventory.
- FR5: List active loans and overdue loans.
- FR6: Display catalogue, inventory, member, active-loan, and overdue counts.

## Non-functional requirements
- **Usability:** menu-driven CLI with clear prompts and errors.
- **Reliability:** SQLite transactions and foreign-key constraints.
- **Data integrity:** checks prevent negative stock; unique ISBN/email values are enforced.
- **Maintainability:** database, business logic, and interface are separated into modules.
- **Performance:** indexed loan status; suitable for a small local dataset.
- **Portability:** uses Python standard library; no third-party runtime dependencies.

## Architecture
```mermaid
flowchart TD
    U[Library Staff / Student] --> CLI[CLI: library/cli.py]
    CLI --> S[Service Layer: library/services.py]
    S --> DB[(SQLite Database)]
    DB --> B[Books]
    DB --> M[Members]
    DB --> L[Loans]
```

## Workflow
```mermaid
flowchart TD
    A([Start]) --> B[Initialize database]
    B --> C[Show menu]
    C --> D{Select operation}
    D -->|Book/member CRUD| E[Validate input and save]
    D -->|Issue book| F{Book available and member valid?}
    F -->|Yes| G[Create loan and decrement stock]
    F -->|No| H[Show validation error]
    D -->|Return book| I{Loan active?}
    I -->|Yes| J[Mark returned and increment stock]
    I -->|No| H
    E --> C
    G --> C
    J --> C
    H --> C
    D -->|Exit| K([End])
```

## Use-case diagram
```mermaid
flowchart LR
    Staff([Library Staff]) --> UC1((Manage Books))
    Staff --> UC2((Manage Members))
    Staff --> UC3((Issue Book))
    Staff --> UC4((Return Book))
    Staff --> UC5((View Reports))
```

## Sequence diagram: issue a book
```mermaid
sequenceDiagram
    actor Staff
    participant CLI
    participant Service
    participant DB as SQLite
    Staff->>CLI: Enter book ID and member ID
    CLI->>Service: issue_book(book_id, member_id)
    Service->>DB: Validate book/member/stock
    DB-->>Service: Records
    Service->>DB: Insert loan; decrement available copies
    DB-->>Service: Commit
    Service-->>CLI: Loan ID and due date
    CLI-->>Staff: Display confirmation
```

## Class/component overview
```mermaid
classDiagram
    class Database {
      +connect()
      +initialize()
    }
    class LibraryService {
      +add_book()
      +update_book()
      +delete_book()
      +add_member()
      +issue_book()
      +return_book()
      +list_loans()
      +overdue_loans()
      +dashboard()
    }
    class CLI {
      +run()
      +show()
    }
    CLI --> LibraryService
    LibraryService --> Database
```

## ER diagram and schema
```mermaid
erDiagram
    BOOKS ||--o{ LOANS : has
    MEMBERS ||--o{ LOANS : borrows
    BOOKS {
      int id PK
      string title
      string author
      string isbn UK
      int total_copies
      int available_copies
    }
    MEMBERS {
      int id PK
      string name
      string email UK
      string phone
    }
    LOANS {
      int id PK
      int book_id FK
      int member_id FK
      date issue_date
      date due_date
      date return_date
      string status
    }
```

## Design decisions and rationale
- **SQLite:** lightweight, serverless, and available in Python's standard library.
- **Layered modules:** keeps persistence, business rules, and interaction separate.
- **Loan history:** returned loans remain stored for traceability.
- **Inventory invariant:** available copies are adjusted only when a loan is created or returned.
- **CLI:** keeps the mini-project small and easy to run without external packages.

## Testing approach
Run `python -m unittest discover -s tests -v`. Tests cover inventory changes during issue/return, rejection of an issue when no copy is available, and required-field validation.

## Future enhancements
Role-based login, fine calculation, CSV export, barcode support, GUI/web interface, email reminders, and multi-branch support.
