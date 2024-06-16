from datetime import datetime

from assignment.book_renting_system.Book import Book, Textbook, Fiction
from assignment.book_renting_system.Member import Member, StandardMember, PremiumMember


class Record:
    def __init__(self):
        self.records = {}
        self.record_book_ids = set()
        self.books: [Book] = list()
        self.members: [Member] = list()

    def validate_book_id(self, book_id):
        return book_id.startswith('B') and book_id[1:].isdigit()

    def validate_member_id(self, member_id):
        return member_id.startswith('M') and member_id[1:].isdigit()

    def validate_state(self, state):
        return state == 'R' or state.isdigit()

    def get_book_type(self, book: Book):
        return "Fiction" if isinstance(book, Fiction) else "Textbook"

    def get_memeber_type(self, member):
        return "Premium" if isinstance(member, PremiumMember) else "Standard"

    def read_records(self, file_name):
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                parts = line.split(', ')
                book_id = parts[0]
                parts = parts[1:]
                existing_book: Book = next((book for book in self.books if book.book_id == book_id), None)
                for part in parts:
                    member_id, state = part.split(': ')
                    existing_member: Member = next(
                        (member for member in self.members if member.get_member_id() == member_id),
                        None)

                    if not self.validate_book_id(book_id):
                        raise ValueError(f"Invalid book ID: {book_id}")
                    if not self.validate_member_id(member_id):
                        raise ValueError(f"Invalid member ID: {member_id}")
                    if not self.validate_state(state):
                        raise ValueError(f"Invalid state: {state}")

                    if member_id not in self.records:
                        self.records[member_id] = {}
                    self.records[member_id][book_id] = state
                    self.record_book_ids.add(book_id)

                    if existing_book is not None:
                        # updating the book -> borrow entries if found
                        reserve_days = 0
                        if state == 'R':
                            existing_book.reserve_book()
                            reserve_days += 1
                        elif state.isdigit():
                            days = int(state)
                            existing_book.borrow_book(int(state))

                        # updating the borrow state for members
                        if existing_member is not None:
                            book_type = self.get_book_type(existing_book)
                            existing_borrow_stats = existing_member.get_borrowed_books()

                            existing_borrow_stats_book_type_data = existing_borrow_stats.get(book_type, [0, 0, 0])
                            existing_borrow_stats_book_type_data[0] = existing_borrow_stats_book_type_data[0] + days
                            existing_borrow_stats_book_type_data[1] = existing_borrow_stats_book_type_data[
                                                                          1] + reserve_days
                            existing_borrow_stats_book_type_data[2] = existing_borrow_stats_book_type_data[2] + 1

                            existing_borrow_stats[book_type] = existing_borrow_stats_book_type_data
                            existing_member.set_borrowed_books(existing_borrow_stats)

                            # updating the late fee if required
                            if existing_book.get_max_borrow_days() > days:
                                late_fee = round(existing_book.get_late_charge() *
                                                 abs(days - existing_book.get_max_borrow_days()), 2)
                                existing_member.set_late_fees(existing_member.get_late_fees() + late_fee)

    def display_records(self):
        members = sorted(self.records.keys())
        books = sorted(self.record_book_ids)

        # Print header
        header = '| MemberId                ' + '   '.join(books) + '   |'
        divider = '-' * len(header)
        print(divider)
        print(header)
        print(divider)

        # Print each member's record
        total_borrow_avg_days = 0
        for member_id in members:
            total_borrow_day = 0
            total_book_count = 0
            row = '| ' + member_id.ljust(20) + ' '
            for book_id in books:
                if book_id in self.records.get(member_id):
                    days = self.records.get(member_id).get(book_id)
                    if days == 'R':
                        row += '--'.rjust(6)
                    else:
                        row += days.rjust(6)
                        total_borrow_day += int(days)
                        total_book_count += 1
                else:
                    row += 'xx'.rjust(6)
            row += '|'.rjust(4)
            print(row)
            total_borrow_avg_days += round(total_borrow_day / total_book_count, 2)

        print(divider)
        print("RECORDS SUMMARY")
        print(f"There are {len(members)} members and {len(books)} books")
        print(f"The average number of borrow days is {round(total_borrow_avg_days / len(members), 2)} days\n")

    def read_books(self, book_file_name):
        try:
            with open(book_file_name, 'r') as file:
                for line in file:
                    parts = line.strip().split(', ')
                    if len(parts) != 6:
                        print(f"Invalid line format: {line}")
                        continue

                    book_id, name, book_type, num_copies, max_borrow_days, late_charge = parts
                    num_copies = int(num_copies)
                    max_borrow_days = int(max_borrow_days)
                    late_charge = float(late_charge)

                    if book_type == 'T':
                        book = Textbook(book_id, name, num_copies, late_charge)
                    elif book_type == 'F':
                        book = Fiction(book_id, name, num_copies, max_borrow_days, late_charge)
                    else:
                        print(f"Invalid book type for book {name} (ID: {book_id})")
                        continue

                    self.books.append(book)

        except FileNotFoundError:
            print(f"File {book_file_name} not found.")
        except ValueError as e:
            print(f"Error parsing file {book_file_name}: {e}")

    def display_books(self, table_split: bool):

        if table_split:
            self.print_books_by_type("Textbook")
            self.print_books_by_type("Fiction")
        else:
            self.print_books_by_type("All")

    def sort_books(self, books: [Book]):
        def sort_key(book):
            return book.name

        # Sort first by book name
        return sorted(books, key=sort_key)

    def print_books_by_type(self, type_to_print):
        print("BOOK INFORMATION"),
        header = "| Book IDs    Name          Type        NCopy    Maxday    Lcharge    Nborrow" \
                 "    Nreserve      Range  |"
        divider = '-' * len(header)
        print(divider)
        print(header)
        print(divider)

        max_borrowed_book: Book = None
        max_borrowed_day = 0
        popular_book: Book = None
        popular_book_borrowers = 0
        if type_to_print != "All":
            self.books = self.sort_books(self.books)

        for book in self.books:
            process_book: Book = None
            if self.get_book_type(book) == type_to_print or type_to_print == "All":
                process_book = book

            if process_book is not None:

                book_id = book.get_id()
                name = book.get_name()
                book_type = self.get_book_type(book)
                n_copy = book.get_num_copies()
                max_day = book.get_max_borrow_days()
                l_charge = book.get_late_charge()
                borrow_stats = book.get_borrowing_statistics()
                n_borrow = borrow_stats.get("borrowing_members")
                n_reserve = borrow_stats.get("reservations")
                n_borrow_range = borrow_stats.get("borrowing_days_range")
                if n_borrow_range[1] > max_borrowed_day:
                    max_borrowed_book = book
                    max_borrowed_day = n_borrow_range[1]
                n_range = '-'.join(map(str, n_borrow_range))

                if n_borrow > popular_book_borrowers + n_reserve:
                    popular_book = book
                    popular_book_borrowers = n_borrow + n_reserve

                # print row
                row = "|".ljust(2) + book_id.ljust(12) + name.ljust(14) + book_type.ljust(16) + str(n_copy).ljust(9) \
                      + str(max_day).ljust(10) + str(l_charge).ljust(13) + str(n_borrow).ljust(12) \
                      + str(n_reserve).ljust(8) + str(n_range).ljust(6) + "|"

                print(row)

        print(divider)
        print("BOOK SUMMARY")
        print(f"The most popular book is {popular_book.get_name()}")
        print(f"The book {max_borrowed_book.get_name()} has the longest borrow days "
              f"({max_borrowed_day} days)\n")

    def read_members(self, member_file_name):
        with open(member_file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                member_data = line.strip().split(', ')
                member_id = member_data[0]
                first_name = member_data[1]
                last_name = member_data[2]
                dob = datetime.strptime(member_data[3].strip(), '%d/%m/%Y').date()
                member_type = member_data[4]
                if member_type == 'Standard':
                    max_borrow_reserve_limit = [("Textbook", 1), ("Fiction", 2)]
                    member = StandardMember(member_id, first_name, last_name, dob, max_borrow_reserve_limit)
                elif member_type == 'Premium':
                    max_borrow_reserve_limit = [("Textbook", 2), ("Fiction", 3)]
                    member = PremiumMember(member_id, first_name, last_name, dob, max_borrow_reserve_limit)
                else:
                    raise ValueError(f"Unknown member type: {member_type}")
                self.members.append(member)

    def sort_members(self, members: [Member]):
        def sort_key(member: Member):
            return member.get_late_fees()

        # Sort first by late fee
        return sorted(members, key=sort_key, reverse=True)

    def print_members_by_type(self, type_to_print, table_s: bool):

        print("MEMBER INFORMATION")
        header = "| Member IDs    FName        LName               Type             DOB" \
                 "        Ntextbook     Nfiction       Average |"

        if table_s:
            header = "| Member IDs    FName        LName               Type             DOB" \
                     "        Ntextbook     Nfiction       Average             Fee |"

        divider = '-' * len(header)

        print(divider)
        print(header)
        print(divider)

        active_members: [Member] = []
        least_avg_member = None
        max_borrowed = 0
        min_avg = 100

        if table_s:
            self.members = self.sort_members(self.members)

        for member in self.members:
            process_member: Member = None

            if self.get_memeber_type(member) == type_to_print or type_to_print == "All":
                process_member = member

            if process_member is not None:
                member_id = member.get_member_id()
                f_name = member.get_first_name()
                l_name = member.get_last_name()
                member_type = self.get_memeber_type(member)
                dob = member.get_dob_formatted()
                borrow_stats = member.compute_statistics()
                n_textbook = borrow_stats.get("num_textbooks")
                n_fiction = borrow_stats.get("num_fictions")
                n_avg = borrow_stats.get("avg_days_borrowed")
                late_fee = member.get_late_fees()

                # updating active members
                if max_borrowed < n_fiction + n_textbook:
                    d = []
                    max_borrowed = n_textbook + n_fiction
                    d.append(member)
                    active_members = d
                elif max_borrowed == n_fiction + n_textbook:
                    active_members.append(member)

                # updating min avg members
                if min_avg >= n_avg:
                    min_avg = n_avg
                    least_avg_member = member

                is_over_limit = member.check_borrowing_limits()
                if is_over_limit.get("Textbook"):
                    n_textbook = str(n_textbook) + "!"
                if is_over_limit.get("Fiction"):
                    n_fiction = str(n_fiction) + "!"

                row = "|".ljust(2) + member_id.ljust(14) + f_name.ljust(13) + l_name.ljust(16) + member_type.rjust(8) \
                      + str(dob).rjust(16) + str(n_textbook).rjust(16) + str(n_fiction).rjust(14) \
                      + str(self.format_average(n_avg)).rjust(14) + " |"

                if table_s:
                    row = "|".ljust(2) + member_id.ljust(14) + f_name.ljust(13) + l_name.ljust(16) + member_type.rjust(
                        8) \
                          + str(dob).rjust(16) + str(n_textbook).rjust(14) + str(n_fiction).rjust(14) \
                          + str(self.format_average(n_avg)).rjust(16) + str(self.format_average(late_fee)).rjust(
                        16) + " |"

                print(row)

        print(divider)
        print("MEMBER SUMMARY")
        active_member_name = ", ".join(
            member.get_first_name() + " " + member.get_last_name() for member in active_members)
        least_avg_member_name = least_avg_member.get_first_name() + " " + least_avg_member.get_last_name()
        print(f"The most active members are {active_member_name} with {max_borrowed} borrowed/reserved")
        print(f"The member with the least average number of borrowing days "
              f"is {least_avg_member_name} with {min_avg} days.\n")

    def display_members(self, table_s: bool):

        if table_s:
            self.print_members_by_type("Standard", table_s)
            self.print_members_by_type("Premium", table_s)
        else:
            self.print_members_by_type("All", table_s)

    def format_average(self, avg_value):
        rounded_avg = round(avg_value, 2)  # Round to two decimal places
        formatted_avg = f"{rounded_avg:.2f}"  # Format to ensure two decimal places

        # Check if formatted_avg ends with '.0' and if so, append '.00'
        if formatted_avg.endswith('.0'):
            formatted_avg += '0'

        return formatted_avg
