'''

Доробіть консольного бота помічника з попереднього домашнього завдання та додайте обробку помилок за допомоги декораторів.

Вимоги до завдання:

1 - Всі помилки введення користувача повинні оброблятися за допомогою декоратора input_error. Цей декоратор відповідає 
за повернення користувачеві повідомлень типу "Enter user name", "Give me name and phone please" тощо.
2 - Декоратор input_error повинен обробляти винятки, що виникають у функціях — handler — і це винятки KeyError, 
ValueError, IndexError. Коли відбувається виняток декоратор повинен повертати відповідь користувачеві.
Виконання програми при цьому не припиняється.

 def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."

    return inner

    
Та обгорнемо декоратором функцію add_contact нашого бота, щоб ми почали обробляти помилку ValueError.

@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."

    

 Критерії оцінювання:

1 - Наявність декоратора input_error, який обробляє помилки введення користувача для всіх команд.
2 - Обробка помилок типу KeyError, ValueError, IndexError у функціях за допомогою декоратора input_error.
3 - Кожна функція для обробки команд має власний декоратор input_error, який обробляє відповідні помилки і повертає відповідні повідомлення про помилку.
4 - Коректна реакція бота на різні команди та обробка помилок введення без завершення програми.   


Приклад використання:

При запуску скрипту діалог з ботом повинен бути схожим на цей.

Enter a command: add
Enter the argument for the command
Enter a command: add Bob
Enter the argument for the command
Enter a command: add Jime 0501234356
Contact added.
Enter a command: phone
Enter the argument for the command
Enter a command: all
Jime: 0501234356 
Enter a command:

 
'''


def input_error(func):
    """
    Декоратор для обробки помилок введення користувача.
    Обробляє винятки KeyError, ValueError, IndexError та повертає відповідні повідомлення.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command."
    return inner





def parse_input(user_input):
    '''
   Reads the user input string and extracts the command and its arguments.
    '''

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):

    """
    Adds a new contact to the contacts dictionary.
    """
    name, phone = args[0], args[1]
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts): 
    
    '''
    Replaces the phone number for an existing contact in the contacts dictionary.
    '''

    name, new_phone = args[0], args[1]
    _ = contacts[name]  # This will raise KeyError if the contact does not exist
    contacts[name] = new_phone
    return "Contact updated."

@input_error
def show_phone(args, contacts):
    '''
    Shows the phone number for the specified contact.
    '''
    name = args[0]
    return f"Phone number for {name}: {contacts[name]}"
    
@input_error
def show_all_contacts(contacts):
    '''
    Shows all saved contacts with their phone numbers.
    '''
    if contacts:
        return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())
    else:
        return "No contacts found."

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            print("Please enter a command.")
            continue    
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all_contacts(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()