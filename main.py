import json
import models as m
import os
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

def output_publ(name,id=None):
    if id is not None:
        for result in session.query(m.Shop).join(m.Stock.shop).join(m.Stock.book).join(m.Book.publisher).filter(m.Publisher.id == id).all():
            print(result)
    else:
        for result in session.query(m.Shop).join(m.Stock.shop).join(m.Stock.book).join(m.Book.publisher).filter(m.Publisher.name == name).all():
            print(result)



if __name__ is "__main__":

    load_dotenv()
    driver = os.getenv('DRIVER')
    aut = os.getenv('AUT')
    host = os.getenv('DRIVER')
    data_base_name = os.getenv('NAME_DB')
    DSN = f'{driver}://{aut}@{host}/{data_base_name}'

    engine = sq.create_engine(DSN)
    Session = sessionmaker(bind=engine)
    session = Session()

    with open('fixtures.json', encoding='utf-8') as f:
        file_content = json.loads(f.read())


    for line in file_content:
        if line['model'] == 'publisher':
            pub = m.Publisher(id=line['pk'], name=line['fields']['name'])
            session.add(pub)
        if line['model'] == 'book':
            book = m.Book(id=line['pk'], title=line['fields']['title'], id_publisher=line['fields']['id_publisher'])
            session.add(book)
        if line['model'] == 'shop':
            shop = m.Shop(id=line['pk'], name=line['fields']['name'])
            session.add(shop)
        if line['model'] == 'stock':
            stock = m.Stock(id=line['pk'], id_shop=line['fields']['id_shop'], id_book=line['fields']['id_book'],
                        count=line['fields']['count'])
            session.add(stock)
        if line['model'] == 'sale':
            sale = m.Sale(id=line['pk'], price=line['fields']['price'], date_sale=line['fields']['date_sale'],
                        count=line['fields']['count'], id_stock=line['fields']['id_stock'])
            session.add(sale)
        else:
            pass
        session.commit()

    output_publ(1,'Колотушкин')