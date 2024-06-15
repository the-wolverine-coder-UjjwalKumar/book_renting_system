class Member:
    def __init__(self, member_id, first_name, last_name, dob, max_borrow_reserve_limit):
        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.borrowed_books = {}  # Each entry will be a key (book_type),
        # value(days_borrowed, days_reserved, total_textbooks_borrowed)
        self.max_borrow_reserve_limit = max_borrow_reserve_limit
        # Each entry will be a tuple (book_type, # max_allowed_to_borrow_reserve)
        self.late_fee = 0.00

    # Getter for member_id
    def get_member_id(self):
        return self.member_id

    # Setter for member_id
    def set_member_id(self, value):
        self.member_id = value

    def get_late_fees(self):
        return self.late_fee

    def set_late_fees(self, value):
        self.late_fee = value

    # Getter and Setter for first_name
    def get_first_name(self):
        return self.first_name

    def set_first_name(self, value):
        self.first_name = value

    # Getter and Setter for last_name
    def get_last_name(self):
        return self.last_name

    def set_last_name(self, value):
        self.last_name = value

    # Getter and Setter for dob
    def get_dob_formatted(self):
        return self.dob.strftime('%d-%b-%Y')

    def get_dob(self):
        return self.dob

    def set_dob(self, value):
        self.dob = value

    # Getter and Setter for borrowed_books
    def get_borrowed_books(self):
        return self.borrowed_books

    def set_borrowed_books(self, value):
        self.borrowed_books = value

    def compute_statistics(self):
        num_textbooks = self.borrowed_books.get("Textbook", [0, 0, 0])
        num_fictions = self.borrowed_books.get("Fiction", [0, 0, 0])
        total_days = num_fictions[0] + num_textbooks[0]
        total_books = num_textbooks[2] + num_fictions[2]
        avg_days = round(total_days / total_books, 2) if self.borrowed_books else 0
        return {
            'num_textbooks': num_textbooks[2],
            'num_fictions': num_fictions[2],
            'avg_days_borrowed': avg_days
        }

    def get_max_borrow_reserve_limit(self):
        return self.max_borrow_reserve_limit

    def check_borrowing_limits(self):
        raise NotImplementedError("Subclasses should implement this method")

    def __str__(self):
        return f"{self.member_id}: {self.first_name} {self.last_name} ({self.__class__.__name__})"


class StandardMember(Member):
    def __init__(self, member_id, first_name, last_name, dob, max_borrow_reserve_limit):
        super().__init__(member_id, first_name, last_name, dob, max_borrow_reserve_limit)

    def get_member_id(self):
        return self.member_id

    def get_borrowed_books(self):
        return self.borrowed_books

    def check_borrowing_limits(self):
        data = self.compute_statistics()
        num_textbooks = data.get("num_textbooks", 0)
        num_fictions = data.get("num_fictions", 0)

        # fetching the max allowed values
        max_values = {type_: val for type_, val in self.max_borrow_reserve_limit}

        max_allowed_textbooks = max_values.get("Textbook", 0)
        max_allowed_fictions = max_values.get("Fiction", 0)
        return {
            "Textbook": num_textbooks > max_allowed_textbooks,
            "Fiction": num_fictions > max_allowed_fictions
        }


class PremiumMember(Member):
    def __init__(self, member_id, first_name, last_name, dob, max_borrow_reserve_limit):
        super().__init__(member_id, first_name, last_name, dob, max_borrow_reserve_limit)

    def get_member_id(self):
        return self.member_id

    def get_borrowed_books(self):
        return self.borrowed_books

    def check_borrowing_limits(self):
        data = self.compute_statistics()
        num_textbooks = data.get("num_textbooks", 0)
        num_fictions = data.get("num_fictions", 0)

        # fetching the max allowed values
        max_values = {type_: val for type_, val in self.max_borrow_reserve_limit}

        max_allowed_textbooks = max_values.get("Textbook", 0)
        max_allowed_fictions = max_values.get("Fiction", 0)
        return {
            "Textbook": num_textbooks > max_allowed_textbooks,
            "Fiction": num_fictions > max_allowed_fictions
        }
