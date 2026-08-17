# goit-core-hw-07

# Homework: OOP Console Assistant Bot

This repository contains the final version of the Command Line Interface (CLI) Assistant Bot. In this project, we integrated Object-Oriented Programming (OOP) principles, data validation, and robust error handling to create a functional and scalable address book application.

## Project structure

- `main.py` — Advanced OOP Console Assistant Bot

**Supported Commands:**
* `hello` - Greets the user.
* `add [name] [phone]` - Adds a new contact or appends a phone number to an existing one.
* `change [name] [old_phone] [new_phone]` - Updates a specific phone number for a contact.
* `phone [name]` - Displays all phone numbers for the specified contact.
* `delete [name]` - Completely removes a contact from the address book.
* `add-birthday [name] [DD.MM.YYYY]` - Adds or updates the birthday of a contact.
* `show-birthday [name]` - Displays the birthday of the specified contact.
* `birthdays` - Lists all contacts who have a birthday in the next 7 days.
* `all` - Displays all saved contacts with their phones and birthdays.
* `close` or `exit` - Terminates the application safely.