from collections import UserDict
from datetime import datetime
import json


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if value.isdigit() and len(value) == 10:
            self.__value = value
        else:
            raise ValueError("Phone number must be a ten digit string of digits")


class Name(Field):
    pass


class Birthday(Field):
    @Field.value.setter
    def value(self, value: str):
        try:
            self.__value = datetime.strptime(value, "%Y.%m.%d")
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name, birthday):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        # phone.validate(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)

    def find_phone(self, value):
        for phone in self.phones:
            if value == phone.value:
                return phone

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return f"Contact was update"
        else:
            raise ValueError

    def days_to_birthday(self):
        if self.birthday:
            birthdate = datetime(
                self.birthday.year, self.birthday.month, self.birthday.day
            )
            date_now = datetime(date_now.year, date_now.month, date_now.day)
            if date_now.date() > birthdate.date():
                next_birthday = birthdate.replace(year=date_now.year + 1)
            else:
                next_birthday = birthdate.replace(year=date_now.year)
            days_till_birthday = (next_birthday - date_now).days
            return days_till_birthday
        else:
            return None

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone_number == phone.value:
                self.phones.remove(phone)
            return f"Phone was delete"
        else:
            raise ValueError


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        pass

    def add(self):
        pass

    def iterator(self, item_number):
        counter = 0
        result = ""
        for item, record in self.data.items():
            result += f"{item}: {record}\n"
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ""

    def load_user(self):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump((self.record_id, self.record), f)

    def read_user(self):
        if not self.file.exists():
            return
        with open(self.file, "r", encoding="utf-8") as f:
            self.record_id, self.record = json.load(f)

    def find_percon(self):
        element = input("Input some information: ")
        for el in self.data.values():
            info = str(el.name).find(element)
            info2 = str([phone.value for phone in el.phones]).find(element)
            info3 = str(el.birthday).find(element)
            if info > -1 or info2 > -1 or info3 > -1:
                print(el)
