import os
from dotenv import load_dotenv
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import json

load_dotenv()
DSN = os.getenv('DSN')
Base = declarative_base()


class Publisher(Base):

    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)


class Book(Base):

    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="books")


class Shop(Base):

    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f'Магазин: {self.id} : {self.name}'


class Stock(Base):

    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship(Book, backref='stocks')
    shop = relationship(Shop, backref='stocks')


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref='sales')

def create_tables(engine):
    Base.metadata.create_all(engine)


engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

with open('fixtures.json', encoding='utf-8') as f:
    file_content = json.loads(f.read())


Session = sessionmaker(bind=engine)
session = Session()

for line in file_content:
    if line['model'] == 'publisher':
        pub = Publisher(id=line['pk'], name=line['fields']['name'])
        session.add(pub)
    if line['model'] == 'book':
        book = Book(id=line['pk'], title=line['fields']['title'], id_publisher=line['fields']['id_publisher'])
        session.add(book)
    if line['model'] == 'shop':
        shop = Shop(id=line['pk'], name=line['fields']['name'])
        session.add(shop)
    if line['model'] == 'stock':
        stock = Stock(id=line['pk'], id_shop=line['fields']['id_shop'], id_book=line['fields']['id_book'],
                      count=line['fields']['count'])
        session.add(stock)
    if line['model'] == 'sale':
        sale = Sale(id=line['pk'], price=line['fields']['price'], date_sale=line['fields']['date_sale'],
                    count=line['fields']['count'], id_stock=line['fields']['id_stock'])
        session.add(sale)
    else:
        pass
    session.commit()


search = str(input('Введите id (для поиска по id издателя) или name (для поиска по имени издателя): '))

if search.lower() == 'di':
    id_publisher = str(input('Введите id издателя: '))
    for result in session.query(Shop).join(Stock.shop).join(Stock.book).join(Book.publisher).filter(Publisher.id == id_publisher).all():
        print(result)

if search.lower() == 'name':
    name_publisher = str(input('Введите имя издателя: '))
    for result in session.query(Shop).join(Stock.shop).join(Stock.book).join(Book.publisher).filter(Publisher.name == name_publisher).all():
        print(result)

else:
    print('Введены некорректные данные или издатель отсутствует в БД!')