#from sqlalchemy.orm import Session
from d_base.session import Session
from models.user import User
from models.post import Post
from models.comment import Comment
from models.tag import Tag
from models.subscription import Subscription  

def test_session_query(session):
    try:
        result = session.query(User).first()
        if result:
            print("Подключение к базе данных успешно установлено.")
        else:
            print("Нет данных в базе.")
    except Exception as err:
        print(f"Ошибка при проверке соединения: {err}")

# Используйте вашу реальную сессию
test_session_query(Session())