
from collections import UserDict
from datetime import datetime, timedelta

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
        except ValueError as e:
            return str(e) if str(e) else "Give me name and phone/birthday please."
        except IndexError:
            return "Enter the argument for the command."
    return inner

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be exactly 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            self.value = value
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):   
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone number {phone_number} not found.")

    def edit_phone(self, old_phone_number, new_phone_number):
        if not self.find_phone(old_phone_number):
            raise ValueError(f"Phone number {old_phone_number} not found.")
        self.add_phone(new_phone_number)
        self.remove_phone(old_phone_number)

    

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
        
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Record with name {name} not found.")
      
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []
        
        for record in self.data.values():
            if record.birthday:
                # Перетворюємо рядок дати на об'єкт datetime
                b_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                # Змінюємо рік на поточний
                b_date_this_year = b_date.replace(year=today.year)
                
                # Якщо день народження вже пройшов цього року, переносимо на наступний
                if b_date_this_year < today:
                    b_date_this_year = b_date_this_year.replace(year=today.year + 1)
                    
                # Рахуємо різницю в днях
                delta_days = (b_date_this_year - today).days
                
                # Якщо ДН в межах наступних 7 днів
                if 0 <= delta_days <= 7:
                    # Якщо випадає на вихідний - переносимо на понеділок
                    if b_date_this_year.weekday() == 5: # Субота
                        b_date_this_year += timedelta(days=2)
                    elif b_date_this_year.weekday() == 6: # Неділя
                        b_date_this_year += timedelta(days=1)
                        
                    upcoming_birthdays.append({
                        "name": record.name.value, 
                        "birthday": b_date_this_year.strftime("%d.%m.%Y")
                    })
                    
        return upcoming_birthdays

    def __str__(self):
        if not self.data:
            return "Address book is empty."
        return '\n'.join(str(record) for record in self.data.values())  
    
#================================
# HANDLERS
#================================    

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook): 
    if len(args) != 3:
        raise ValueError("Usage: change [name] [old_phone] [new_phone]")
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."
    
@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if not record.phones:
        return "No phones found for this contact."
    return f"{name}'s phones: {', '.join(p.value for p in record.phones)}"

@input_error
def show_all_contacts(args, book: AddressBook):
    if not book.data:
        return "No contacts found."
    return str(book)

@input_error
def delete_contact(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("Usage: delete [name]")
    
    name = args[0]
    
    book.delete(name)
    return f"Contact '{name}' successfully deleted."

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError("Usage: add-birthday [name] [DD.MM.YYYY]")
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.birthday is None:
        return "Birthday not set."
    return f"Birthday for {name}: {record.birthday.value}"

@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays within the next 7 days."
    
    result = "Upcoming birthdays:\n"
    for info in upcoming:
        result += f" - {info['name']}: {info['birthday']}\n"
    return result.strip()

#================================
# MAIN FUNCTION
#================================

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        
        if not user_input.strip():
            continue
            
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all_contacts(args, book))
        elif command == "delete":
            print(delete_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()




# test commands: 
# Hello
# add John 1234567890 
# phone John
# change John 1234567890 0987654321
# add-birthday John 15.09.1990
# show-birthday John
# birthdays
# add Jane 0987654335
# add-birthday Jane 21.08.1992
# birthdays
# all
# delete John
# all
# exit