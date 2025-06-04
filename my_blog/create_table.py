#create_table
from d_base.session import engine, Base
from models.comment import Comment
from models.post import Post
from models.subscription import Subscription
from models.tag import Tag
from models.user import User


if __name__ == '__main__':
    print('Создаем таблицы')
    Base.metadata.create_all(engine)
    print('Готово! Создал таблицы')