####Не тестировалась на Unix

Справедливо для windows 10x64


Установите python 3.9


Клонируйте проект средствами git

> git clone https://github.com/TiredFingers/idagroup.git


Перейдите в директорию проекта

> cd idagroup


Создайте виртуальное окружение

> py -m venv venv

Активируйте виртуальное окружение

> venv/scripts/activate


Установите зависимости

> pip install -r requirements.txt


Перейдите в директорию proj
Инициализируйте БД

> py manage.py makemigrations imageshaper

> py manage.py migrate

Запустите проект
> py manage.py runserver


