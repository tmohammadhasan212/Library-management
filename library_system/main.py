from pydantic import ValidationError

from models.book import Book
from models.library import Library
from library_system.data_storage import DataStorage


def load_library(storage: DataStorage) -> Library:
    try:
        books = storage.import_from_json()
    except FileNotFoundError:
        books = []

    try:
        borrow_records = storage.import_from_csv()
    except FileNotFoundError:
        borrow_records = []

    return Library(inventory=books, borrow_records=borrow_records)


def save_library(storage: DataStorage, library: Library) -> None:
    if library.inventory:
        storage.export_to_json(library.inventory)

    if library.borrow_records:
        storage.export_to_csv(library.borrow_records)


def show_menu() -> None:
    print("\nLibrary Management")
    print("=" * 30)
    print("1. View all books")
    print("2. View available books")
    print("3. View borrowed books")
    print("4. Add book")
    print("5. Borrow book")
    print("6. Return book")
    print("7. View borrow history")
    print("8. Save and exit")


def main() -> None:
    storage = DataStorage()
    library = load_library(storage)

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                Library.view_books(library.inventory)

            elif choice == "2":
                library.view_available_books()

            elif choice == "3":
                library.view_borrowed_books()

            elif choice == "4":
                title = input("Book title: ")
                author = input("Book author: ")

                book = Book(title=title, author=author)
                library.add_book(book)

                print("Book added successfully.")

            elif choice == "5":
                Library.view_books(library.inventory)

                borrower_name = input("Borrower name: ")
                book_id = int(input("Book ID: "))

                library.borrow_book(
                    borrower_name=borrower_name,
                    book_id=book_id,
                )

                print("Book borrowed successfully.")

            elif choice == "6":
                library.view_borrowed_history()

                record_id = int(input("Borrow record ID: "))

                library.return_book(record_id=record_id)

                print("Book returned successfully.")

            elif choice == "7":
                library.view_borrowed_history()

            elif choice == "8":
                save_library(storage, library)
                print("Library saved. Goodbye.")
                break

            else:
                print("Invalid option. Try again.")

        except (ValueError, TypeError, ValidationError) as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()