import sys

from assignment.book_renting_system.Records import Record


def print_records_table(record: Record):
    record.display_records()


def print_books_table(record: Record, table_split: bool):
    record.display_books(table_split)


def print_members_table(record: Record, table_split: bool):
    record.display_members(table_split)


def initialize_records(record_file_name, record):
    record_file_name = record_file_name.strip()
    record.read_records(record_file_name)


def initialize_books(book_file_name, record):
    book_file_name = book_file_name.strip()
    record.read_books(book_file_name)


def initialize_members(member_file_name, record):
    member_file_name = member_file_name.strip()
    record.read_members(member_file_name)


def pass_level(command_arguments, record: Record):
    if len(command_arguments) <= 1:
        print("[Usage:] python script.py <records.txt>")
        exit()

    record_file_name = command_arguments[1]

    initialize_records(record_file_name, record)
    print_records_table(record)


def credit_level(command_arg, record: Record):
    book_file_name = None
    record_file_name = None
    if len(command_arg) < 2:
        print("[Usage:] python script.py <records.txt> <books.txt>")
        exit()
    elif len(command_arg) == 2:
        record_file_name = command_arg[1]
    elif len(command_arg) == 3:
        record_file_name = command_arg[1]
        book_file_name = command_arg[2]

    if book_file_name is not None:
        # initialize book
        initialize_books(book_file_name, record)

    if record_file_name is not None:
        # initialize records
        initialize_records(record_file_name, record)

    # print record table
    if len(record.records) > 0:
        print_records_table(record)

    if len(record.books) > 0:
        # print book table
        print_books_table(record, False)


def di_level(command_arg, record):
    record_file_name, book_file_name, member_file_name = None, None, None

    if len(command_arg) < 2:
        print("[Usage:] python script.py <records.txt> <books.txt> <members.txt>")
        exit()
    elif len(command_arg) == 2:
        record_file_name = command_arg[1]
    elif len(command_arg) == 3:
        record_file_name = command_arg[1]
        book_file_name = command_arg[2]
    elif len(command_arg) == 4:
        record_file_name = command_arg[1]
        book_file_name = command_arg[2]
        member_file_name = command_arg[3]

    if member_file_name is not None:
        # initialize members
        initialize_members(member_file_name, record)

    if book_file_name is not None:
        # initialize book
        initialize_books(book_file_name, record)

    if record_file_name is not None:
        # initialize records
        initialize_records(record_file_name, record)

    if len(record.records) > 0:
        # print record table
        print_records_table(record)

    if len(record.books) > 0:
        # print book table
        print_books_table(record, False)

    if len(record.members) > 0:
        # print members table
        print_members_table(record, False)


def hd_level(command_arg, record, split_req):
    record_file_name, book_file_name, member_file_name = None, None, None

    if len(command_arg) < 2:
        print("[Usage:] python script.py <records.txt> <books.txt> <members.txt>")
        exit()
    elif len(command_arg) == 2:
        record_file_name = command_arg[1]
    elif len(command_arg) == 3:
        record_file_name = command_arg[1]
        book_file_name = command_arg[2]
    elif len(command_arg) == 4:
        record_file_name = command_arg[1]
        book_file_name = command_arg[2]
        member_file_name = command_arg[3]

    if member_file_name is not None:
        # initialize members
        initialize_members(member_file_name, record)

    if book_file_name is not None:
        # initialize book
        initialize_books(book_file_name, record)

    if record_file_name is not None:
        # initialize records
        initialize_records(record_file_name, record)

    if len(record.records) > 0:
        # print record table
        print_records_table(record)

    if len(record.books) > 0:
        # print book table
        print_books_table(record, split_req)

    if len(record.members) > 0:
        # print members table
        print_members_table(record, split_req)


def main():
    record = Record()

    # PASS LEVEL
    # pass_level(sys.argv, record)

    # CREDIT LEVEL
    # credit_level(sys.argv, record)

    # DI LEVEL
    di_level(sys.argv, record)

    # HD LEVEL
    # hd_level(sys.argv, record, True)


if __name__ == "__main__":
    main()
