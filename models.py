import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f'Publisher: {self.id}: , Name: {self.name}'


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="book")

    def __str__(self):
        return f'Book: {self.id}: , Title: {self.title}, id_publisher: {self.id_publisher}'


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer)

    def __str__(self):
        return f'Stock: {self.id}: , id_book: {self.id_book}, id_shop: {self.id_shop}, count: {self.count}'


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f'Shop: {self.id}: , Name: {self.name}'


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float)
    date_sale = sq.Column(sq.Date)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer)

    def __str__(self):
        return f'Sale: {self.id}: , Price: {self.price}, Date_Sale: {self.date_sale}, id_stock: {self.id_stock}, count: {self.count} '


def books_by_publisher(session, publisher):
    q = sq.select(Book.title, Shop.name, Sale.price, Sale.date_sale) \
        .select_from(Book) \
        .join(Publisher, Publisher.id == Book.id_publisher) \
        .join(Stock, Stock.id_book == Book.id) \
        .join(Shop, Shop.id == Stock.id_shop) \
        .join(Sale, Sale.id_stock == Stock.id) \
        .where(Publisher.name == publisher)

    for book in session.execute(q).all():
        print(f'book: {book.title:<40}| shop: {book.name:<10}| price: {book.price:<6}| sale date: {book.date_sale}')
    return


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
