#seed.py - Ввод тестовых данных
#from my_blog.database1 import init_db, Session
from d_base.session import Session, init_db
from models.user import User
from models.post import Post
from models.tag import Tag
from models.comment import Comment
from models.subscription import Subscription

def seed():
    init_db()
    session = Session()
    # Создаем пользователей
    users = [
        User(username='alice', email='alice@example.com'),
        User(username='bob', email='bob@example.com'),
        User(username='carol', email='carol@example.com')
    ]
    session.add_all(users)
    session.commit()

    # Создаем теги
    tags = [Tag(name='комнатные растения'), Tag(name='цветы'), Tag(name='уход')]
    session.add_all(tags)
    session.commit()

    # Создаем посты
    posts = [
        Post(title='Лучшие комнатные цветы', content='Описание комнатных цветов...', author=users[0], tags=[tags[0], tags[1]]),
        Post(title='Уход за фикусом', content='Советы по уходу за фикусом...', author=users[1], tags=[tags[2], tags[0]]),
        Post(title='Цветущие растения', content='Какие выбрать цветущие растения...', author=users[2], tags=[tags[1]])
    ]
    session.add_all(posts)
    session.commit()

    # Комментарии к постам
    comments = [
        Comment(content='Отличная статья!', user=users[1], post=posts[0]),
        Comment(content='Спасибо, очень полезно.', user=users[2], post=posts[0]),
        Comment(content='А как ухаживать зимой?', user=users[0], post=posts[1]),
        Comment(content='Подробный гайд!', user=users[2], post=posts[1]),
        Comment(content='Мои цветы цвели!', user=users[0], post=posts[2]),
        Comment(content='Интересно, спасибо!', user=users[1], post=posts[2])
    ]
    session.add_all(comments)

    # Подписки
    subs = [
        Subscription(user=users[0], post=posts[1]),
        Subscription(user=users[1], post=posts[2]),
        Subscription(user=users[2], post=posts[0])
    ]
    session.add_all(subs)

    session.commit()
    session.close()

if __name__ == '__main__':
    seed()