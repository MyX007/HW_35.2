# Трекер привычек

## Возможности:
- **Создание и отслеживание привычек**
- **Система наград**
- **Подключение напоминаний через Telegram**
- **Возможность делиться достижениями**

### 1. Требования:
- **Удаленный серевер с утановленным Docker**
- **Учетная запись Docker Hub**
- **Доступ к репозиторию на GitHub**

### 2. Установка и настройка:
1. #### Обновление системных пакетов
   ```bash
    sudo apt update
    sudo apt upgrade
    ```
2. #### Утановка Docker и Docker Compose
   ```bash
    sudo apt update && sudo apt install -y docker.io docker-compose
    sudo systemctl enable docker
    sudo usermod -aG docker $USER && newgrp docker
    ```
3. #### Установка репозитория  
     ```bash
     git clone https://github.com/MyX007/Course_work_7.git /var/www/habit_tracker
     ```
4. #### Настройка переменных окружения
   1. **Создайте в корневой папке проекта файл .env**
   2. **Заполните его в соответствии с образцом, указанном ниже:**
      ```
      # Сектретный ключ djnago. 
      SECRET_KEY=django-insecure-qwwertytyuiuioopp123
      
      # Настройки redis
      CACHE_ENABLED=True
      CACHE_LOCATION=redis://127.0.0.1:6379

      # Настройка почтового сервиса
      EMAIL_HOST='smpt.yandex.ru'
      EMAIL_PORT=465
      EMAIL_USE_TLS=False
      EMAIL_USE_SSL=True
      EMAIL_HOST_USER=example@email.com
      EMAIL_HOST_PASSWORD=hgklgjkhtrptr

      # Настройка доступа к базе данных
      POSTGRES_USER=postgres
      POSTGRES_PASSWORD=112233
      POSTGRES_HOST=db   
      POSTGRES_DB="Database"

      # Настройка доступа к API Telegram
      API_KEY = "sk_test_grhrgrogjirj0grjiporjrphjpo[htrp[h5kh-5kpkjbjprjpbkmop5r"

      # Настройка Celery
      CELERY_BROKER_URL = 'redis://redis:6379/0'
      CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
      CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
      ```  
5. #### Основные команды управления проектом
   - **Сборка и запуск**
      ```bash
      docker compose up -d --build
      ```
   - **Просмотр логов**
     ```bash
     docker compose logs
     ```
   - **Остановка**
     ```bash
     docker compose down
     ```

6. #### GitHub Actions
   - **К проекту подключен GitHub Actions, позволяющий автоматизировать тестирование, сборку и деплой на удаленный сервер**

   - **GitHub actions запускается автоматически при push или pull request**

   - **Порядок действий:**
     1. **Проверка кода линтером Flake8**
     2. **Тестирование кода с применением временной базы данных SQLite**
     3. **Сборка Docker-образа и пуш на DockerHub**
     4. **Деплой на удаленный сервер и запуск через docker compose**
   
   

7. #### Примечания
   - **Миграции применяются автоматически**
   - **Локально роект запускается на локальном порту 8000**
   - **На удаленном сервере проект работает на порту 8880(server_ip:8880)**
   - **Celery и Celery Beat запускаются автоматически**
   - **При пуше изменений на GitHub происходит атоматическое тестирование, сборка и деплой проекта на удаленный сервер**
