import sqlite3
from tabulate import tabulate
import random


class Book:

    def __init__(self, id, title, authorID, qty):
        self.id = int(id)
        self.title = title
        self.authorID = int(authorID)
        self.qty = int(qty)

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_authorID(self):
        return self.authorID

    def get_qty(self):
        return self.qty

    def __str__(self):
        return (
            f"{'Book ID:':<15} {self.id}\n"
            f"{'Title:':<15} {self.title}\n"
            f"{'Author ID:':<15} {self.authorID}\n"
            f"{'Quantity:':<15} {self.qty}\n"
            f"----------------------------------"
        )


class Author:
    def __init__(self, id, name, country):
        self.id = int(id)
        self.name = name
        self.country = country

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_country(self):
        return self.country

    def __str__(self):
        return (
            f"{'Author ID:':<15} {self.id}\n"
            f"{'Author name:':<15} {self.name}\n"
            f"{'Author Country:':<15} {self.country}\n"
            f"----------------------------------"
        )


def db_connection(database_name):
    db = sqlite3.connect(database_name)
    cursor = db.cursor()

    return db, cursor


def initialize_db(books, authors):
    try:
        db, cursor = db_connection("ebookstore.db")

        # Create the author table if it does not already exist
        # - id is the primary key
        # - name is mandatory
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS author(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT
            )
            '''
        )

        # Create the book table if it does not already exist
        # - authorID is a foreign key referencing author(id)
        # - ON DELETE CASCADE: deleting an author deletes related books
        # - ON UPDATE CASCADE: updating author.id updates book.authorID
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS book(
            id INTEGER PRIMARY KEY,
            title text,
            authorID INTEGER,
            qty INTEGER,
            FOREIGN KEY(authorID) REFERENCES author(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
            )
            '''
        )

        # Check whether the author table already contains data
        cursor.execute(
            '''
            SELECT COUNT(*)
            FROM author
            '''
        )

        # If no authors exist, insert default author records
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                '''
                INSERT INTO author(id, name, country)
                VALUES(?, ?, ?)
                ''', [(1290, 'Charles Dickens', 'England'),
                      (8937, 'J.K. Rowling', 'England'),
                      (2356, 'C.S. Lewis', 'Ireland'),
                      (6380, 'J.R.R. Tolkien', 'South Africa'),
                      (5620, 'Lewis Carroll', 'England')
                      ]
            )

        # Check whether the book table already contains data
        cursor.execute(
            '''
            SELECT COUNT(*)
            FROM book
            '''
        )

        # If no books exist, insert default book records
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                '''
                INSERT INTO book(id, title, authorID, qty)
                VALUES(?, ?, ?, ?)
                ''', [(3001, 'A Tale of Two Cities', 1290, 30),
                      (3002, "Harry Potter and the Philosopher's Stone", 8937,
                       40),
                      (3003, 'The Lion, the Witch and the Wardrobe', 2356, 25),
                      (3004, 'The Lord of the Rings', 6380, 37),
                      (3005, "Alice's  Adventures  in Wonderland", 5620, 12)
                      ]
            )
        # Load all authors from the database into the authors list
        cursor.execute(
            '''
             SELECT id, name, country
             FROM author
            '''
            )
        # Ensures there are no duplicate objects
        authors.clear()
        for row in cursor.fetchall():
            authors.append(Author(row[0], row[1], row[2]))

        cursor.execute(
            '''
             SELECT id, title, authorID, qty
             FROM book
            '''
            )

        # Load all books from the database into the books list
        books.clear()
        for row in cursor.fetchall():
            books.append(Book(row[0], row[1], row[2], row[3]))

        db.commit()

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


def add_book(books, authors):
    try:
        db, cursor = db_connection("ebookstore.db")

        # Generates a new book ID based on the last book ID
        book_id = 3000 + len(books) + 1

        # Generates a random 4 digit author ID
        authorID = random.randint(1000, 9999)
        book_title = input("\nEnter book title: ")

        while True:
            try:
                book_qty = int(input("Enter book quantity: "))
                break
            except ValueError:
                print("Invalid input, enter digital number")

        author_name = input("Enter author's name: ")
        author_country = input("Enter author's country: ")

        book = Book(book_id, book_title, authorID, book_qty)
        books.append(book)

        author = Author(authorID, author_name, author_country)
        authors.append(author)

        # Insert the new author into the author table
        # using the object created
        cursor.execute(
            '''
            INSERT INTO author(id, name, country)
            VALUES(?, ?, ?)
            ''', (author.id, author.name, author.country)
        )

        # Insert the new book into the book table
        # using the object created
        cursor.execute(
            '''
            INSERT INTO book(id, title, authorID, qty)
            VALUES(?, ?, ?, ?)
            ''', (book.id, book.title, book.authorID, book.qty)
        )
        db.commit()
        print("Book successfully entered")

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def view_books(authors=None):
    try:
        db, cursor = db_connection("ebookstore.db")

        # Default table headers for book-only view
        headers = ["ID", "Title", "Author ID", "Quantity"]

        cursor.execute(
            '''
            SELECT id, title, authorID, qty
            FROM book
            '''
        )

        rows = cursor.fetchall()

        # Where book table is empty
        if not rows:
            print("\nNo books found")
            return

        # If no authors argument is provided, display books only
        if authors is None:
            print("\nList of books available:")
            print(tabulate(rows, headers=headers, tablefmt="grid"))

        # If authors argument is provided, display books
        # with author details
        else:
            headers = ["Title", "Author's Name", "Author's Country"]

            # Join book and author tables using the
            # foreign key relationship
            cursor.execute(
                '''
                SELECT book.title, author.name, author.country
                FROM book INNER JOIN author
                ON book.authorID = author.id
                '''
            )

            rows = cursor.fetchall()

            if not rows:
                print("\nNo books found")
                return

            print("\nList of books with their authors:")
            print(tabulate(rows, headers=headers, tablefmt="grid"))

    except Exception as e:
        raise e
    finally:
        db.close()


def update_book(books,
                authors,
                book_id,
                qty,
                title=None,
                new_author_id=None,
                author_name=None,
                author_country=None):
    try:
        db, cursor = db_connection("ebookstore.db")
        cursor.execute("PRAGMA foreign_keys = ON")

        # qty is always updated by default
        book_fields = ["qty = ?"]
        book_values = [qty]

        # Optional title update
        if title is not None:
            book_fields.append("title = ?")
            book_values.append(title)

        # Optional authorID correction
        if new_author_id is not None:
            # Ensures the referenced author exists before updating FK
            cursor.execute(
                '''
                SELECT 1
                FROM author
                WHERE id = ?
                ''', (new_author_id,)
            )

            if cursor.fetchone() is None:
                raise ValueError(
                    f"Author with ID {new_author_id} does not exist"
                )

        book_fields.append("authorID = ?")
        book_values.append(new_author_id)

        # Add book_id last for the WHERE clause when updating
        book_values.append(book_id)

        # Execute parameterised UPDATE statement
        # Column names are fixed, values are safely parameterised
        cursor.execute(
            f"""
            UPDATE book
            SET {", ".join(book_fields)}
            WHERE id = ?
            """, book_values
        )

        # If no rows were updated, the book does not exist
        if cursor.rowcount == 0:
            return False

        books.clear()
        # reloads data from the database into book lists
        # after a successful update
        cursor.execute(
            '''
            SELECT id, title, authorID, qty
            FROM book
            '''
        )

        for row in cursor.fetchall():
            books.append(Book(row[0], row[1], row[2], row[3]))

        if author_name is not None or author_country is not None:
            author_fields = []
            author_values = []

            # Optional author name update
            if author_name is not None:
                author_fields.append("name = ?")
                author_values.append(author_name)

            # Optional author country update
            if author_country is not None:
                author_fields.append("country = ?")
                author_values.append(author_country)

            # Get the author linked to the book
            cursor.execute(
                '''
                SELECT authorID
                FROM book
                WHERE id = ?
                ''', (book_id,)

            )
            author_id = cursor.fetchone()[0]

            # Add author_id for WHERE clause
            author_values.append(author_id)

            # Execute parameterised UPDATE on author
            # to avoid sql injection
            cursor.execute(
                f"""
                UPDATE author
                SET {", ".join(author_fields)}
                WHERE id = ?
                """, author_values
            )

            # Refresh authors list after updating
            authors.clear()
            cursor.execute(
                '''
                SELECT id, name, country
                FROM author
                '''
            )

            for row in cursor.fetchall():
                authors.append(Author(row[0], row[1], row[2]))

        db.commit()

        return True

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def delete_book(books, book_id):
    try:
        db, cursor = db_connection("ebookstore.db")
        db.execute("PRAGMA foreign_keys = ON")

        # Delete book by primary key
        cursor.execute(
            '''
            DELETE
            FROM book
            WHERE id = ?
            ''', (book_id,)
        )

        if cursor.rowcount == 0:
            return False

        # Refresh books list after deletion
        books.clear()
        cursor.execute(
            '''
            SELECT id, title, authorID, qty
            FROM book
            '''
        )

        for row in cursor.fetchall():
            books.append(Book(row[0], row[1], row[2], row[3]))

        db.commit()
        return True

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def search_book(title):
    try:
        db, cursor = db_connection("ebookstore.db")

        # Execute a parameterised SELECT query to safely search for books
        # The LIKE operator allows partial title matching
        # '%' before and after the title enables substring searches
        cursor.execute(
            '''
            SELECT *
            FROM book
            WHERE title like ?
            ''', (f"%{title}%",)
        )

        search = cursor.fetchall()

        # If at least one book matches the search term,
        # return the results
        if search:
            return search

        # If no matches are found, notify the user and return
        # an empty list
        else:
            print("Book was not found")
            return []

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


books = []

authors = []

initialize_db(books, authors)

menu = input("1. Enter book\n"
             "2. Update book\n"
             "3. Delete book\n"
             "4. Search books\n"
             "5. View details of all books\n"
             "0. Exit\n")

while menu != "0":

    if menu == "1":
        add_book(books, authors)

    elif menu == "2":
        # Display all current books before updating
        view_books()

        while True:
            try:
                # Validate that the book ID is a 4-digit number
                while True:
                    book_id = int(input("\nEnter ID of the book to update: "))
                    if len(str(book_id)) == 4:
                        break
                    else:
                        print("ID was be 4 digits, try again")

                new_qty = int(input("Enter new quantity: "))

                # Optional book title or authorID updates
                new_title = None
                new_authorID = None

                if input("Update title or author ID? (Y/N): ").strip() \
                        .upper() == "Y":
                    new_title = input("Enter new title (leave blank to "
                                      "keep current): ").strip()
                    new_title = new_title if new_title else None

                    # Validate that author ID is a 4-digit number
                    while True:
                        author_input = input("Enter new author ID (leave blank"
                                             " to keep current): ").strip()
                        if len(str(author_input)) == 4:
                            break
                        else:
                            print("ID was be 4 digits, try again")

                    new_authorID = int(author_input) if author_input else None

                # Optional author name or country updates
                new_name = None
                new_country = None

                if input("Update author name or country? (Y/N): ").strip() \
                        .upper() == "Y":
                    # Display all current books with author names
                    view_books(authors)
                    new_name = input("Enter new author name (leave blank to "
                                     "keep current): ").strip()
                    new_name = new_name if new_name else None

                    country_input = input("Enter new country (leave blank to "
                                          "keep current): ").strip()
                    new_country = country_input if country_input else None

                if update_book(
                    books,
                    book_id,
                    new_qty,
                    new_title,
                    new_authorID,
                    new_name,
                    new_country
                ):
                    print("Book successfully updated")
                else:
                    print(f"Book with ID {book_id} was not found")

                break

            except ValueError:
                print("Invalid input. Please enter digital number where "
                      "applicable.")

    elif menu == "3":
        # Display all current books before deleting
        view_books()
        while True:
            try:
                book_id = int(input("\nEnter ID of a book you want to "
                                    "delete: "))
                if delete_book(books, book_id):
                    print("Book successfully deleted")
                else:
                    print(f"Book with ID {book_id} was not found")
                break
            except ValueError:
                print("Invalid input, enter digital number")

    elif menu == "4":
        title = input("\nEnter the title of the book you want: ")
        result = search_book(title)

        if result:
            for row in result:
                book_id = row[0]

                for book in books:
                    if book.id == book_id:
                        print(book)

    elif menu == "5":
        # Display books with their authors
        view_books(authors)

    else:
        print("Invalid input, please select from the menu provided")

    menu = input("\n1. Enter book\n"
                 "2. Update book\n"
                 "3. Delete book\n"
                 "4. Search books\n"
                 "5. View details of all books\n"
                 "0. Exit\n")
