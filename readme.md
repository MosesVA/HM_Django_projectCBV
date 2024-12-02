# Django проект приюта для собак

## КАК УСТАНОВИТЬ И ЗАПУСТИТЬ СЕРВЕР

### Установка

1. Установить requirements
   ```shell
    pip3 install -r requirements.txt
   ```

2. Заполните .env файл согласно файлу .env_sample
3. Создайте базу данных при помощи команды
   ```shell
   python manage.py ccdb
   ```

4. Сделайте миграции
   ```shell
   python manage.py migrate
   ```

5. Создайте суперпользователя, модератора и обычного пользователя
   ```shell
   python manage.py ccsu
   ```

6. Для заполнения базы данных готовой фикстурой
   ```shell
   python manage.py loaddata data.json
   ```
### Запуск
1. Для начала запустите сервер [redis](https://skillbox.ru/media/base/kak_ustanovit_redis_v_os_windows_bez_ispolzovaniya_docker/)
   ```shell
   redis-server
   ```
   
2. Далее откройте второй powershell с включенным виртуальным окружением и находясь в корневой папке запустите сервер
   ```shell
   python manage.py runserver
   ```

## Информация

### Описания строк файла .env

#### Database:
* MS_SQL_USER - Имя пользователя для входа в MSSQL
* MS_SQL_KEY - Пароль для входа в MSSQL
* MS_SQL_SERVER - Сервер MSSQL
* MS_SQL_DATABASE - Название БД вашего проекта
* MS_SQL_PAD_DATABASE - Название БД (прокладки)
* MS_SQL_DRIVER - Драйвер который вы используете в MSSQL

#### Рассылка:
* YANDEX_MAIL - Ваш email с которого будет происходить рассылка
* YANDEX_PASSWORD_APP - Пароль от приложения-рассылки

#### Cache:
* CACHE_ENABLED - Работа кэша (True или False)
* CACHE_LOCATION - Ссылка на redis сервер
   