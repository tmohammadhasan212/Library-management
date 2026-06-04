# 📚 Library Management System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Pydantic-Validation-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Pytest-Testing-green?style=for-the-badge&logo=pytest" />
  <img src="https://img.shields.io/badge/Storage-JSON%20%7C%20CSV-orange?style=for-the-badge" />
</p>

A simple and clean **command-line Library Management System** built with Python.  
This project helps manage a small library inventory, track borrowed and returned books, and store data locally using **JSON** and **CSV** files.

---

## ✨ Overview

This project provides a lightweight library workflow where users can:

- add books
- view books
- borrow books
- return books
- check borrow history
- save data locally

It uses **Pydantic** for data validation and **Pytest** for testing.

---

## 🚀 Features

✅ Add new books to the library  
✅ View all books  
✅ View available books  
✅ View borrowed books  
✅ Borrow books by book ID  
✅ Return borrowed books by borrow record ID  
✅ View complete borrow history  
✅ Store book inventory in a JSON file  
✅ Store borrow records in a CSV file  
✅ Validate data using Pydantic models  
✅ Handle custom library exceptions  
✅ Includes unit tests with Pytest  

---

## 🧱 Project Structure

```text
Library-management/
├── library_system/
│   ├── __init__.py
│   ├── data_storage.py
│   ├── exceptions.py
│   └── main.py
├── models/
│   ├── __init__.py
│   ├── book.py
│   ├── borrow_record.py
│   └── library.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_books.py
│   ├── test_data_storage.py
│   └── test_library.py
└── .gitignore
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| 🐍 Python | Main programming language |
| ✅ Pydantic | Data validation |
| 🧪 Pytest | Unit testing |
| 📄 JSON | Store book inventory |
| 📊 CSV | Store borrow records |

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/tmohammadhasan212/Library-management.git
cd Library-management
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### 🪟 Windows

```bash
.venv\Scripts\activate
```

### 🍎 macOS / Linux

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
pip install pydantic pytest
```

---

## ▶️ How to Run

Run the application from the project root:

```bash
python -m library_system.main
```

After running the command, the program opens a command-line menu for managing the library.

---

## 📋 Menu Options

```text
Library Management
==============================
1. View all books
2. View available books
3. View borrowed books
4. Add book
5. Borrow book
6. Return book
7. View borrow history
8. Save and exit
```

---

## 💾 Data Storage

The application stores data locally in a `data/` directory.

The directory is created automatically when needed.

```text
data/
├── books_inventory.json
└── borrow_records.csv
```

### 📘 books_inventory.json

Stores the library book inventory.

### 📗 borrow_records.csv

Stores borrow and return history.

---

## 🧩 Main Components

### 📕 Book Model

The `Book` model represents a book in the library.

Main fields:

| Field | Description |
|---|---|
| `uid` | Unique book ID |
| `title` | Book title |
| `author` | Book author |
| `status` | Book availability status |

A book can have one of the following statuses:

```text
available
borrowed
```

---

### 📝 BorrowRecord Model

The `BorrowRecord` model represents a borrowing transaction.

Main fields:

| Field | Description |
|---|---|
| `uid` | Unique borrow record ID |
| `book_uid` | ID of the borrowed book |
| `borrower_name` | Name of the borrower |
| `title` | Borrowed book title |
| `status` | Borrow status |
| `borrow_time` | Time of borrowing |
| `return_time` | Time of return |

A borrow record can have one of the following statuses:

```text
borrowed
returned
```

---

### 🏛️ Library Model

The `Library` model contains the main business logic of the project.

It is responsible for:

- adding books
- listing books
- borrowing books
- returning books
- tracking borrow history
- comparing stored data with imported file data

---

## 🧪 Running Tests

Run all tests with:

```bash
pytest
```

The tests cover:

- book validation
- assignment validation
- duplicate book handling
- borrowing logic
- returning logic
- borrow history
- JSON export and import
- CSV export and import
- invalid input handling
- edge cases

---

## 🔄 Example Workflow

```text
1. Run the application
2. Choose option 4 to add a new book
3. Choose option 1 to view all books
4. Choose option 5 to borrow a book
5. Choose option 7 to view borrow history
6. Choose option 6 to return a book
7. Choose option 8 to save and exit
```

---

## 📌 Notes

- This project is a command-line application.
- It does not require a database.
- Data is saved using JSON and CSV files.
- Pydantic is used for model validation.
- The project currently does not include a `requirements.txt` file, so dependencies should be installed manually.

---

## 🌱 Future Improvements

Possible future improvements:

- 📦 Add a `requirements.txt` file
- ⚙️ Add a `pyproject.toml` file
- 🔍 Add book search functionality
- 👤 Add user/member management
- 📅 Add due dates for borrowed books
- ⏰ Add late return tracking
- 🖥️ Add a graphical user interface
- 🌐 Add a web-based version
- 📈 Improve reporting and export features

---

## 👨‍💻 Author

Created by [tmohammadhasan212](https://github.com/tmohammadhasan212).

---

<p align="center">
  Made with ❤️ using Python
</p>
