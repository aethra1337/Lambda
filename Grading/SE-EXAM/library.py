class Book:
    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.is_available = True

    def borrow(self):
        if self.is_available:
            self.is_available = False
            return True
        return False

    def return_book(self):
        self.is_available = True


class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.borrow():
            self.borrowed_books.append(book)
            print(f"{self.name} successfully borrowed '{book.title}'.")
        else:
            print(f"Sorry, '{book.title}' is currently not available.")

    def return_book(self, book):
        if book in self.borrowed_books:
            book.return_book()
            self.borrowed_books.remove(book)
            print(f"{self.name} returned '{book.title}'.")
        else:
            print(f"{self.name} does not have this book.")


class Library:
    def __init__(self, name):
        self.name = name
        self.books = []
        self.members = []

    def add_book(self, book):
        self.books.append(book)
        print(f"Added book: '{book.title}' to the library.")

    def register_member(self, member):
        self.members.append(member)
        print(f"Registered member: {member.name}")

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None


# Testing the automation script
if __name__ == "__main__":
    # Create library
    my_library = Library("City Library")
    print("--- Library Setup ---")

    # Create books and members
    book1 = Book("111", "The Little Prince", "Antoine de Saint-Exupéry ")
    book2 = Book("222", "1984", "George Orwell")
    
    my_library.add_book(book1)
    my_library.add_book(book2)
    
    user = Member("M01", "Talha Kocaaga")
    my_library.register_member(user)
    
    print("\n--- Testing Borrow & Return ---")
    
    # Try to find and borrow a book
    target_book = my_library.find_book("1984")
    if target_book:
        user.borrow_book(target_book)
    
    # Try to borrow the same book again (Should fail)
    user2 = Member("M02", "Celal Kalmis")
    user2.borrow_book(book2)
    
    # Return book
    print("\n--- Returning Process ---")
    user.return_book(book2)
    
    # Try again after return
    user2.borrow_book(book2)