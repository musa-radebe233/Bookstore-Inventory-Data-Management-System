# Bookstore-Inventory-Data-Management-System
## Overview

ShelfTrack is a Python-based bookstore inventory management system backed by a SQLite database.
The project simulates a real-world operational data workflow where a bookstore clerk captures, 
updates, validates, and retrieves structured data while maintaining referential integrity between related datasets.

From a Data Analyst perspective, this project demonstrates how raw operational inputs are transformed into reliable, queryable, and decision-ready data.

## Business Problem

Bookstores rely on accurate inventory and author data to:

Track stock levels

Correct data entry errors

Maintain consistent author information

Retrieve meaningful insights from their catalogue

Manual tracking (e.g. spreadsheets) increases the risk of inconsistent data, duplication, and reporting errors.
This project addresses that risk by enforcing structured data storage and controlled updates via a database-driven system.

## Key Features

The system allows a user (bookstore clerk) to:

Add new books to the database

Update book information, with quantity as the default update

Delete books from the database

Search books by title

View full book details, including author name and country

All actions interact directly with a relational database rather than in-memory data only.

## Database Design

The project uses a relational database (SQLite) called ebookstore with two tables:

### book table

Stores transactional inventory data:

id (Primary Key)

title

authorID (Foreign Key)

qty

### author table

Stores reference (dimension-style) data:

authorID (Primary Key)

name

country

### Why this matters (Data Perspective)

Separating books and authors avoids data duplication

Author details are updated once and reflected across related books

Foreign key relationships ensure data integrity

Mirrors real-world OLTP systems used in operations and finance

## Menu-Driven Workflow

The user interacts with the system via a command-line menu:

1. Enter book
2. Update book
3. Delete book
4. Search books
5. View details of all books
0. Exit

Each option maps to a specific database operation (INSERT, UPDATE, DELETE, SELECT).

## Technical Stack

Python – application logic

SQLite – relational database

SQL – data querying and manipulation

Object-Oriented Design – Book and Author entities

Exception Handling – protects data integrity
