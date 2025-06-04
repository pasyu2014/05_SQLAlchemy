"""
Ниже приведен пример скрипта на Python, который реализует указанный функционал. Для простоты я 
использую `input()` для выбора пользователя и вывод информации на консоль. Предполагается, что у вас уже 
есть настроенная сессия и модели, как в вашем проекте.
"""

# script_user_post.py
from d_base.session import Session, init_db
from models.user import User
from models.post import Post
from models.comment import Comment
from models.tag import Tag
from models.subscription import Subscription

def main():
    init_db()
    session = Session()
    

    # 1. Выбор пользователя из выпадающего списка
    users = session.query(User).all()
    print("Выберите пользователя:")
    for idx, user in enumerate(users, start=1):
        print(f"{idx}. {user.username} ({user.email})")
    try:
        choice = int(input("Введите номер пользователя: "))
        if choice < 1 or choice > len(users):
            print("Некорректный выбор.")
            return
    except ValueError:
        print("Некорректный ввод.")
        return

    selected_user = users[choice - 1]
    print(f"\nВы выбран пользователь: {selected_user.username}\n")

    # 2. Вывести списком посты данного пользователя
    #user_posts = session.query(Post).filter_by(author_id=selected_user.id).all()
    user_posts = session.query(Post).filter_by(user_id=selected_user.id).all()
    print("Посты пользователя:")
    for post in user_posts:
        print(f"- {post.title}")

    # 3. Вывести список постов и количество комментариев к каждому посту
    print("\nКоличество комментариев к постам:")
    for post in user_posts:
        comments_count = session.query(Comment).filter_by(post_id=post.id).count()
        print(f"- {post.title}: {comments_count} комментариев")

    # 4. Вывести список постов и теги к каждому посту
    print("\nТеги постов:")
    for post in user_posts:
        # Предполагается, что у Post есть отношение tags
        # Если у вас оно называется иначе, исправьте
        tags = getattr(post, 'tags', None)
        if tags is None:
            # Если отношение не загружено, можно сделать запрос
            post_full = session.query(Post).filter_by(id=post.id).first()
            tags = getattr(post_full, 'tags', [])
        tag_names = [tag.name for tag in tags] if tags else []
        print(f"- {post.title}: {', '.join(tag_names) if tag_names else 'Нет тегов'}")

    session.close()

if __name__ == "__main__":
    main()
"""

**Обратите внимание:**
- Убедитесь, что у модели `Post` есть отношение `tags`. Обычно это реализуется через `relationship` с 
помощью `association table`.
- В вашем коде, например, в `models/post.py`, должно быть что-то вроде:

```python
# models/post.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from d_base.session import Base

# Ассоциативная таблица для Many-to-Many между Post и Tag
post_tag_association = Table(
    'post_tag',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey('users.id'))

    # Связи
    author = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post', cascade='all, delete-orphan')
    tags = relationship('Tag', secondary=post_tag_association, back_populates='posts')
```

- Также, убедитесь, что у модели `Tag` есть обратная связь:

```python
# models/tag.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from d_base.session import Base

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    posts = relationship('Post', secondary='post_tag', back_populates='tags')
```

Если у вас есть вопросы по моделям или нужно помочь с их настройкой — пишите!
"""