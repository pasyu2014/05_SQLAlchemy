# queries.py — файл с реализацией запросов
from sqlalchemy.orm import joinedload
from d_base.session import Session
from models.user import User
from models.post import Post
from models.comment import Comment
from models.tag import Tag
from models.subscription import Subscription

def select_user_and_show_posts(session):
    """Запрашивает выбор пользователя и выводит его посты."""
    print("Выберите пользователя:")
    users = session.query(User).all()
    #print (users)
    
    #for idx, user in enumerate(users):
        # print(f"{idx + 1}. {user.username}")
    #    print(f"{idx + 1}. {user.idx}")

    # Проходим по списку и печатаем каждого пользователя
    for user in users:
        print(f"ID: {user.id}, Имя пользователя: {user.username}, Email: {user.email}")
    
    choice = int(input("Ваш выбор по ID: "))
    selected_user = users[choice - 1]
    
    print(f"Посты пользователя '{selected_user.username}'")
    for post in selected_user.posts:
        print(f"- {post.title}")


def show_posts_with_comment_count(session):
    """Показывает список постов с указанием количества комментариев."""
    posts = session.query(Post).options(joinedload(Post.comments)).all()
    
    for post in posts:
        comment_count = len(post.comments)
        print(f'Пост "{post.title}" ({comment_count} комментарии)')


def show_posts_with_tags(session):
    """Отображает список постов с прикрепленными тегами."""
    posts = session.query(Post).options(joinedload(Post.tags)).all()
    
    for post in posts:
        tag_names = ', '.join(tag.name for tag in post.tags)
        print(f'Пост "{post.title}" с тегами: {tag_names}')


if __name__ == "__main__":
    with Session() as session:
        while True:
            print("\nМеню запросов:")
            print("1. Показать посты выбранного пользователя.")
            print("2. Список постов с количеством комментариев.")
            print("3. Список постов с тегами.")
            print("4. Выход.")
            
            choice = input("Выберите пункт меню: ")
            
            if choice == '1':
                select_user_and_show_posts(session)
            elif choice == '2':
                show_posts_with_comment_count(session)
            elif choice == '3':
                show_posts_with_tags(session)
            elif choice == '4':
                break
            else:
                print("Неверный ввод! Попробуйте снова.")