import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


from models.database.database import Database
from models.database.bookData import BookData

class Book:

    """Creates book object from title. If object with title exists in database returns object from db."""
    def __init__(self, title:str, price_cents:int = None, description:str = None, category:str = None, id:int = -1):
        self.ID = id
        self.title = title
        self.price_cents = price_cents
        self.description = description
        self.category = category
        if self.ID == -1 and not Book.is_title_unique(self.title):
            b = Book.from_title(self.title)
            self.price_cents = b.price_cents
            self.description = b.description
            self.category = b.category
            self.ID = b.ID
    
        if self.ID == -1:
            self.save()

    def save(self) -> bool:
        if None in [self.category, self.description, self.price_cents]:
            return False
        if self.ID == -1:
            BookData.insert(self.title, self.price_cents, self.description, self.category)
            self.ID = Book.from_title(self.title).ID
        else:
            BookData.update(self.ID, self.title, self.price_cents, self.description, self.category)
        return True

    def __repr__(self):
        return f"<Book: {self.ID}, {self.title}>"

    """Create Book object from tuple returned from DB."""
    @classmethod
    def from_tuple(cls, t:tuple):
        return Book(t[1], t[2], t[3], t[4], t[0])
    
    @classmethod
    def from_id(cls, id:int):
        t = Database.get_by_unique_value(BookData.TABLE_NAME, 'id', id)
        if t:
            return Book.from_tuple(t)

    @classmethod
    def from_title(cls, title:str):
        t = Database.get_by_unique_value(BookData.TABLE_NAME, 'title', title)
        if t:
            return Book.from_tuple(t)

    @classmethod
    def is_title_unique(cls, title:str):
        return Database.is_unique_value_free(BookData.TABLE_NAME, 'title', title)

    """Return list of Books from db."""
    @classmethod
    def all(cls, offset:int = None, limit:int = None) -> list:
        t = Database.fetch_all(BookData.TABLE_NAME, offset=offset, limit=limit)
        l =[]
        for b in t:
            l.append(Book.from_tuple(b))
        return l
    