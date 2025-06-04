Назначение скриптов и тестов в папке my_blog

seed.py - заполнение талиц тестовыми данными (python, ORM)
indoor_flowers3.db  должна отсутствовать.

test_session.py - тестирование (python, ORM) установление подключения к таблицам в indoor_flowers3.db

script_user_post.py  - запросы на выборку данных из базы (python, ORM)
    Выбор пользователя из выпадающего списка: вывод всех пользователей, выбор одного пользователя и 
	отображение его постов.
    Список постов с количеством комментариев: вывести список постов вместе с числом комментариев к ним.
    Список постов с тегами: показать каждый пост с соответствующими тегами.
	
queries.py  -  те же запросы, что и в  script_user_post.py, на есть меню выбора запросов

Запуск
cd ... /my_blog
\my_blog> python <name>.py

ТЕСТЫ на PYTEST

test_queries -  запросы на выборку данных из базы (pytest, ORM) как в script_user_post.py  и queries.py, 
но средствами pytest

test_main - - тестирование таблиц User Post Subscription  средствами pytest

Запуск

cd ... /my_blog
\my_blog> pytest -v  tests/test_queries.py
\my_blog> pytest -v  tests/test_main.py
