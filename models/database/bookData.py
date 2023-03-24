import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


from models.database.database import Database

class BookData:
    TABLE_NAME: str = "books"

    """Insert record into table. True on success, false if unique value was taken."""
    @classmethod
    def insert(cls, title:str, price_cents:int, description:str, category:str) -> bool:
        if Database.is_unique_value_free(BookData.TABLE_NAME, 'title', title):
            Database.execute(f"""INSERT INTO {BookData.TABLE_NAME} (title, price_cents, description, category) 
                                VALUES (?, ?, ?, ?)""", (title, price_cents, description, category))
            return True
        return False

    """Update record into table by id. True on success, false if unique value was taken or id is empty."""
    @classmethod
    def update(cls, id:int, title:str, price_cents:int, description:str, category:str) -> bool:
        if Database.is_unique_value_free(BookData.TABLE_NAME, 'id', id):
            return False
        if (Database.get_by_unique_value(BookData.TABLE_NAME,'id', id)[1] != title and
            not Database.is_unique_value_free(BookData.TABLE_NAME, 'title', title)):
            return False
        QUERY = f"""UPDATE {BookData.TABLE_NAME}
                    SET title = ?, price_cents = ?, description = ?, category = ?
                    WHERE id = ?;"""
        Database.execute(QUERY, (title, price_cents, description, category, id))
        return True