class Book:
    def __init__(self, book_id, name, num_copies, max_borrow_days, late_charge):
        self.book_id = book_id
        self.name = name
        self.num_copies = num_copies
        self.max_borrow_days = max_borrow_days
        self.late_charge = late_charge
        self.borrowing_members = 0
        self.reservations = 0
        self.borrowing_days = []  # this will hold the borrow days for given book

    # Getters and Setters
    def get_id(self):
        return self.book_id

    def set_id(self, book_id):
        self.book_id = book_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_num_copies(self):
        return self.num_copies

    def set_num_copies(self, num_copies):
        self.num_copies = num_copies

    def get_max_borrow_days(self):
        return self.max_borrow_days

    def set_max_borrow_days(self, max_borrow_days):
        self.max_borrow_days = max_borrow_days

    def get_late_charge(self):
        return self.late_charge

    def set_late_charge(self, late_charge):
        self.late_charge = late_charge

    def borrow_book(self, days_borrowed):
        self.borrowing_days.append(days_borrowed)
        self.borrowing_members += 1

    def reserve_book(self):
        self.reservations += 1

    # Statistics methods
    def get_borrowing_statistics(self):
        if self.borrowing_days:
            min_days = min(self.borrowing_days)
            max_days = max(self.borrowing_days)
            avg_days = sum(self.borrowing_days) / len(self.borrowing_days)
        else:
            min_days, max_days, avg_days = 0, 0, 0

        return {
            "borrowing_members": self.borrowing_members,
            "reservations": self.reservations,
            "borrowing_days_range": [min_days, max_days],
            "average_borrowing_days": avg_days
        }

    def __str__(self):
        return (f"Book[ID={self.book_id}, Name={self.name}, "
                f"Copies={self.num_copies}, MaxBorrowDays={self.max_borrow_days}, LateCharge={self.late_charge}]")


class Textbook(Book):
    def __init__(self, book_id, name, num_copies, late_charge):
        super().__init__(book_id, name, num_copies, 14, late_charge)

    def set_max_borrow_days(self, max_borrow_days):
        if max_borrow_days != 14:
            raise ValueError(
                f"Textbook '{self.name}' (ID: {self.book_id}) must have 14 days as maximum borrowing days.")
        self.max_borrow_days = max_borrow_days

    def __str__(self):
        return f"Textbook[ID={self.book_id}, Name={self.name}, Copies={self.num_copies}, " \
               f"MaxBorrowDays={self.max_borrow_days}, LateCharge={self.late_charge}] "


class Fiction(Book):
    def __init__(self, book_id, name, num_copies, max_borrow_days, late_charge):
        if max_borrow_days <= 14:
            raise ValueError(
                f"Fiction book '{name}' (ID: {book_id}) must have more than 14 days as maximum borrowing days.")
        super().__init__(book_id, name, num_copies, max_borrow_days, late_charge)

    def set_max_borrow_days(self, max_borrow_days):
        if max_borrow_days <= 14:
            raise ValueError(
                f"Fiction book '{self.name}' (ID: {self.book_id}) must have more than 14 days as maximum borrowing days.")
        self.max_borrow_days = max_borrow_days

    def __str__(self):
        return f"Fiction[ID={self.book_id}, Name={self.name}, Copies={self.num_copies}, " \
               f"MaxBorrowDays={self.max_borrow_days}, LateCharge={self.late_charge}]"
