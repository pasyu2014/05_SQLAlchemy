# tests/test_queries.py
import pytest
#from sqlalchemy.orm import Session
from d_base.session import Session, init_db
from models.user import User
from models.post import Post
from models.tag import Tag
from models.comment import Comment
from models.subscription import Subscription
# from d_base.seed import seed  # Импортируем функцию seed из модуля ввода тестовых данных
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

def test_get_posts_by_user(db_session):
    
    #Тест: получение постов конкретного пользователя
   
    # Берём первого пользователя из базы
    first_user = db_session.query(User).first()
    assert first_user is not None, "Пользователь не найден!"

    # Получаем посты этого пользователя
    posts = db_session.query(Post).filter(Post.author == first_user).all()
    assert len(posts) > 0, f"У пользователя {first_user.username} нет постов."

    # Выводим заголовки постов для наглядности
    for post in posts:
        print(f"Заголовок поста: {post.title}")

def test_post_comments_count(db_session):

    #Тест: получение постов с количеством комментариев
    # Получаем все посты
    posts = db_session.query(Post).all()
    assert len(posts) > 0, "Нет ни одного поста в базе данных!"

    # Формируем словарь с количеством комментариев
    posts_with_comments = {}
    for post in posts:
        #count = db_session.query(Comment).filter(Comment.post == post).count()
        count = db_session.query(Comment).filter(Comment.post_id == post.id).count()
        posts_with_comments[post.title] = count

    # Выводим результат
    for title, count in posts_with_comments.items():
        print(f"Название поста: {title}, Количество комментариев: {count}")

def test_posts_with_tags(db_session):

    #Тест: получение постов с тегами
    # Получаем все посты
    posts = db_session.query(Post).all()
    assert len(posts) > 0, "Нет ни одного поста в базе данных!"

    # Формируем словарь с названиями тегов
    posts_with_tags = {}
    for post in posts:
        tag_names = ", ".join([tag.name for tag in post.tags])
        posts_with_tags[post.title] = tag_names

    # Выводим результат
    for title, tags in posts_with_tags.items():
        print(f"Название поста: {title}, Теги: {tags}")

