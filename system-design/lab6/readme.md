# Лабораторная работа 6

1. Создайте сервис на Python, который реализует сервисы, спроектированные в первом задании (по проектированию). Должно быть реализовано как минимум два сервиса (управления пользователем и хотя бы один бизнес-сервис)
2. Сервис должен поддерживать аутентификацию с использованием JWT
3. Сервис должен реализовывать как минимум GET/POST методы
4. Данные сервиса должны храниться в PostgreSQL
5. В целях проверки должен быть заведён мастер-пользователь (имя admin, пароль secret)
6. Одна из сущностей должна храниться в mongoDB
7. Сервис должен осуществлять создание и чтение нужного документа из
   mongoDB
8. Должны быть построены индексы соответственно критерию запроса
9. Одна из сущностей, которая хранится в PostgreSQL должна кешироваться в Redis
10. Реализовать паттерн «сквозное чтение» для работы с Redis
11. **Реализовать паттерн CQRS для одной из сущностей**
12. **Метод POST должен публиковать сообщение о создании в очередь kafka,
    отдельный сервис должен читать сообщения и записывать их в базу**

## Примечания

1. **Для сервиса `orders` реализован механизм работы с сообщениями посредством kafka.**
2. Для сервиса `orders` добавлен кеш `redis`.
3. Для запуска проекта необходимо запустить контейнеры `app`, `pgdb`, `mongo`, `redis`, `kafka1`, в докере (в директории`.devcontainer`выполнить`docker-compose up --build`):
   - после запуска приложение инициализируется, будет наполнено тестовыми данными.
4. Для взаимодействия необходимо авторизоваться: отправить `POST` запрос `/token`, время действия `ACCESS_TOKEN_EXPIRE_MINUTES`. Далее запросам нужно добавлять header `Authorization Bearer` со значением jwt-токена.
