#d_base/session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL


# Создаем движок
engine = create_engine(DATABASE_URL, echo=True)
print (engine)

# Создаем базовый класс
Base = declarative_base()

# Фабрика сессия
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
    print('Готово! Создал таблицы')

