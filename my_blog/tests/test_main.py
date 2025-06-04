#test/test_main.py
import pytest
#from my_blog.database1 import init_db, Session
from d_base.session import Session, init_db
from models.user import User
from models.post import Post
from models.tag import Tag
from models.comment import Comment
from models.subscription import Subscription
from seed import seed  # Импортируем функцию seed из модуля ввода тестовых данных

@pytest.fixture(scope="module")
def db_session():
    """
    Фикстура для подготовки базы данных и открытия сессии
    """
    init_db()  # Вызываем инициализацию базы данных один раз для всего набора тестов
    session = Session()
    yield session
    session.close()

@pytest.fixture(autouse=True)
def clear_data(db_session):
    """
    Фикстура для полной очистки данных перед каждым тестом
    """
    from sqlalchemy.sql.expression import text
    # Сначала очищаем промежуточные таблицы
    db_session.execute(text("DELETE FROM post_tags;")) 
    db_session.query(Subscription).delete()
    db_session.query(Comment).delete()
    db_session.query(Tag).delete()
    db_session.query(Post).delete()
    db_session.query(User).delete()
    db_session.commit()

@pytest.fixture(autouse=True)
def populate_data(clear_data, db_session):
    #Фикстура для автоматического заполнения тестовыми данными
    seed()
    db_session.commit()  # Обязательно зафиксировать изменения!


def test_users_count(db_session):
    """
    тест проверяет общее количество пользователей в базе данных. Он корректен, так как 
    утверждение assert len(users) == 3 
    """
    session = Session()
    users = session.query(User).all()
    assert len(users) == 3
    session.close()

def test_posts_tags_comments(db_session):
    """"
    тест проверяет количество тегов и комментариев у конкретного поста. Утверждения len(post.tags) >= 1 и 
    len(post.comments) >= 1 имеют смысл, так как проверяют минимальную достаточность тегов и комментариев. 
    Также корректна проверка принадлежности комментариев соответствующему посту (c.post_id == post.id)
    """
    session = Session()
    post = session.query(Post).filter_by(title='Лучшие комнатные цветы').one()
    assert len(post.tags) >= 1
    assert len(post.comments) >= 1
    # Проверка что комментарии принадлежат правильному посту
    for c in post.comments:
        assert c.post_id == post.id
    session.close()

def test_subscriptions(db_session):
    """
    тест проверяет количество подписок и уникальность подписок 
    (чтобы одна пара "пользователь-пост" встречалась только один раз).
    """
    session = Session()
    subs = session.query(Subscription).all()
    assert len(subs) >= 3
    # Проверка что подписки уникальны
    user_post_pairs = {(sub.user_id, sub.post_id) for sub in subs}
    assert len(user_post_pairs) == len(subs)
    session.close()