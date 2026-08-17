
from collections import UserDict

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

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):   
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone number {phone_number} not found.")
    # Реалызацыя з врахуванням рекомендацій ментора по уникненню дублювання коду 
    def edit_phone(self, old_phone_number, new_phone_number):
        if not self.find_phone(old_phone_number):
            raise ValueError(f"Phone number {old_phone_number} not found.")
        self.add_phone(new_phone_number)
        self.remove_phone(old_phone_number)

        
    '''
    Перша реалізація - є рекомендація ментора по уникненню дублювання коду,
    тому краще використовувати методи add_phone та remove_phone замість прямого
    доступу до списку phones.
    '''
    # def edit_phone(self, old_phone_number, new_phone_number):
    #     for phone in self.phones:
    #         if phone.value == old_phone_number:
    #             new_phone = Phone(new_phone_number)
    #             phone.value = new_phone.value
    #             return
    #     raise ValueError(f"Phone number {old_phone_number} not found.")


    '''
    В цій реалізації є проблема з тим, що якщо старий номер телефону не знайдено,
    то новий номер все одно додається до списку телефонів, що може призвести
    до неконсистентного стану. Тому краще спочатку перевіряти наявність
    старого номера перед додаванням нового.
    '''

    # def edit_phone(self, old_phone_number, new_phone_number):
    #     new_phone = Phone(new_phone_number)
    #     self.remove_phone(old_phone_number)
    #     self.phones.append(new_phone)


    # def edit_phone(self, old_phone_number, new_phone_number):
    #     if not self.find_phone(old_phone_number):
    #         raise ValueError(f"Phone number {old_phone_number} not found.")
    #     self.add_phone(new_phone_number)
    #     self.remove_phone(old_phone_number)


    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

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

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())




# Make a new address book
book = AddressBook()

# Make a new record for John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Add John's record to the address book
book.add_record(john_record)

# Make a new record for Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

print(book)


# Find and edit John's phone number
john = book.find("John")
john.edit_phone("1234567890", "1112223333")


print(john)  # Output: Contact name: John, phones: 5555555555; 1112223333


# Find a specific phone number in John's record
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Output: John: 5555555555

# Delete Jane's record
book.delete("Jane")

print(book)