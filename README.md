# Ресторан "Республика"

**Принцип работы**: постраничный рендеринг

**Структура проекта**: 
- /django - серверная логика, html-шаблоны, статика. 
- /svelte - элементы svelte, исключительно фронтенд.
- /django/db.sqlite3 - файл базы данных. В нём содержатся данные о пользователях, меню, ресторанах, заказов... В случае проблем можно его удалять и вставлять другой файл бд.
- /django/media/tables - svg файлы карт ресторанов.
- /svelte/app - здесь находятся изображения и шрифты, которые перемещаются в /django/static/app, а также файлы фронтенда, не относящиеся к svelte. index.scss \- глобальный файл стилей. index.js \- глобальный js файл, используется jquery. Используется преимущественно для модальных окон, а также на этом файле завязана логика слайдеров и некоторых других элементов.

**Как запускать**: Необходимо два окна консоли.
1. Открываем первое окно и перемещаемся в папку *svelte*
2. Вводим `yarn` или `npm i` (для установки зависимостей, при первом запуске)
3. Вводим `yarn dev` или `npm run dev` - проект запускается в режиме разработки
4. Переходим со второго окна окна в папку *django*
5. Вводим `pipenv shell`
6. Вводим `pipenv install` (для установки зависимостей, при первом запуске)
7. Вводим `python manage.py runserver`
<br/>

**Как собрать**:
1. Вводим `cd /svelte`
2. Вводим `yarn build`

Сервер выдает файлы из /static, при изменении файлов django перезапускать не надо. 

**Панель администратора**: Для перехода в панель администратора необходимо перейти по адресу http://127.0.0.1:8000/admin. Имя пользователя и пароль: admin.




