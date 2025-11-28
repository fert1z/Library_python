# Library management system with bookings and reports

An object-oriented library management system in Python, designed to manage the catalog of books, users, and accounting for book issuance.

## Project Description

The system allows you to:
- Manage the book catalog (add, delete)
- Manage library users
- Give out and return books
- Book unavailable books
- Generate various reports
- Save and upload data in JSON format

## Project structure

library-_-Management-main/
├── book.py # Class Book (book)
,── user.py # User class
├── loan.py # Class Loan (book withdrawal)
├── library.py # Library class
├── main.py # Main program with menu
,── requirements.txt # Project dependencies
,── README.md # Documentation

## Main classes

### Book
Stores information about the book:
- Title and author
- Availability status
- List of reservations

### User
Stores user information:
- User's name
- A list of borrowed books

### Loan
Connects the book and the user:
- User name and book ID
- Date of issue and return
- Checking the delay

### Library
Manages the entire system:
- Collection of books and users
- Book issuance
- Report generation
- Saving/loading data

## Installation and launch

1. Make sure you have Python 3.7 or higher installed.
2. Clone the repository or download the files
3. Run the program:

python main.py

## Usage

When the program starts, a menu with the following options is displayed:

1. Add a book - add a new book to the catalog
2. Delete a book - delete a book by ID (only if the book is not issued)
3. Add a user - register a new user
4. Delete user - delete user by ID (only if there are no books taken)
5. Take a book - giving the book to the user
6. Return the book - return the book to the library
7. Book a book - reserve an unavailable book
8. Show reports - View various reports:
- List of all books and their status
   - Users and their books
   - Expired books
   - Users with the most books
9. Save Data - save the library status to a JSON file
10. Upload Data - download data from a JSON file
0. Exit - program shutdown

## Saving data

The data is automatically saved to the library_data file.json` when exiting (if the user confirms). You can also save the data manually via the menu.

JSON file format:
``json
{
"books": [...],
"users": [...],
"loans": [...]
}
``

## Implementation features

- Object-oriented approach: all entities are represented by classes
- Pure functions: class methods minimize side effects
- Working with dates: automatic calculation of the return date and checking the delay
- Reservations: The system notifies about reservations when the book is returned
- Reports: various types of reports for analyzing the work of the library

## Requirements

- Python 3.7+
- Python Standard Library (json, datetime, typing)

## Author

The project was created as part of the study of object-oriented programming in Python.
