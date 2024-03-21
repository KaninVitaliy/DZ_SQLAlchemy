import sqlalchemy
import psycopg2
import json
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Stock, Shop, Sale, books_by_publisher

DSN = 'postgresql://postgres:v12mm1997@localhost:5432/python_orm'
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

def insert_data():
    with open("tests_data.json", "r") as file:
        file = json.load(file)

    for str in file:
        if str["model"] == "publisher":
            id_name_publisher = Publisher(id=str["pk"], name=str["fields"]["name"])
            session.add(id_name_publisher)

        elif str["model"] == "book":
            book = Book(id=str["pk"], title=str["fields"]["title"], id_publisher=str["fields"]["id_publisher"])
            session.add(book)

        elif str["model"] == "shop":
            shop = Shop(id=str["pk"], name=str["fields"]["name"])
            session.add(shop)

        elif str["model"] == "stock":
            stock = Stock(id=str["pk"], id_book=str["fields"]["id_book"], id_shop=str["fields"]["id_shop"],
                          count=str["fields"]["count"])
            session.add(stock)

        elif str["model"] == "sale":
            sale = Sale(id=str["pk"], price=float(str["fields"]["price"]), date_sale=str["fields"]["date_sale"],
                        id_stock=str["fields"]["id_stock"], count=str["fields"]["count"])
            session.add(sale)

        session.commit()


if __name__ == "__main__":
    create_tables(engine)
    insert_data()
    print("Введите имя писателя")
    publisher = input()
    books_by_publisher(session, publisher)
