workspace {
    name "Сайт заказа услуг"
    description "Представление архитектуры в нотации C4"
    !docs documentation
    !identifiers hierarchical

    model {
        # Участники
        user = person "User" {
            description "Пользователь сайта"
        }

        # Внешние системы
        paymentSystem = softwareSystem "Payment system" {
            description "Внешняя система для платежей"
            tags "T-API, MTS Pay"
        }

        # Сайт ProfiRu
        profiRu = softwareSystem "Сайт profi.ru" {
            description "Сайт для поиска и заказа услуг"

            webApp = container "webApp" {
                description "Web-приложение, позволяет пользоваться функционалом посредством браузера"
                technology "HTML/CSS, React, JS"
            }

            api = container "API Gateway" {
                description "Обработка бизнес-логики"
                technology "Python, FastAPI"
            }

            orderService = container "Order service" {
                description "Сервис обработки заказов"
            }

            taskService = container "Task service" {
                description "Сервис обработки услуг"
            }

            userService = container "User service" {
                description "Сервис управления пользователями"
            }

            userDb = container "User database" {
                description "Хранение данных о пользователях"
                technology "PostgreSQL"
                tags "Database"
            }

            orderDb = container "Order database" {
                description "Хранение данных о заказах"
                technology "PostgreSQL"
                tags "Database"
            }

            taskDb = container "Task database" {
                description "Хранение данных о услугах"
                technology "PostgreSQL"
                tags "Database"
            }

            cdn = container "Cdn"  {
                description "Хранилище статичных файлов, изображений, аватарок"
                technology "Nginx, Lua"
            }

            # Сценарии взаимодействия межкду пользователем и системой
            user -> webApp "Взаимодействие с системой посредством веб-приложения"
            webApp -> api "Отправление запросов к небходимым endpoint'ам"

            # Взаимодействие api с контенерами и внешними системами
            api -> userService "Запросы авторизации, CRUD пользователей"
            api -> orderService "Запросы CRUD заказов"
            api -> taskService "Запросы CRUD услуг"
            api -> paymentSystem "Проведение платежей"
            api -> cdn "Запрос статичных файлов"

            // # Управление данными
            user -> userService "Управление аккаунтом"
            user -> orderService "Управление заказами"
            user -> taskService "Управление услугами"

            # Взаимодействие сервисов с базами
            userService -> userDb "Чтение/запись данных в базе пользователей"
            orderService -> orderDb "Чтение/запись данных в базе заказов"
            taskService -> taskDb "Чтение/запись данных в базе услуг"

            # Межсервисное взаимодействие
            orderService -> userService "Получение данных о пользователе"
            userService -> orderService "Получение данных о заказах"
            userService -> taskService "Получение данных об услугах"
            orderService -> taskService "Получение данных об услугах в заказе"
        }
    }

    views {
        systemContext profiRu "SystemContext" {
            include *
            autolayout lr
        }

        container profiRu {
            include *
            autolayout lr
        }


        dynamic profiRu "createUser" "Создание нового пользователя" {
            user -> profiRu.webApp
            profiRu.webApp -> profiRu.api "POST /users"
            profiRu.api -> profiRu.userService
            profiRu.userService -> profiRu.userDb
            profiRu.userService -> user "Уведомление о создании пользователя"
            autolayout lr
        }

         dynamic profiRu "searchUser" "Поиск пользователя по логину" {
            user -> profiRu.webApp
            profiRu.webApp -> profiRu.api "POST /search?login={str}"
            profiRu.api -> profiRu.userService
            profiRu.userService -> profiRu.userDb
            profiRu.userService -> user "Отображение результатов поиска"
            autolayout lr
        }

        dynamic profiRu "searchUserByFirstnameOrLastname" "Поиск пользователя по имени/фамилии" {
            user -> profiRu.webApp
            profiRu.webApp -> profiRu.api "POST /search?firstname={firstname}&lastname={lastname}"
            profiRu.api -> profiRu.userService
            profiRu.userService -> profiRu.userDb
            profiRu.userService -> user "Отображение результатов поиска"
            autolayout lr
        }

        dynamic profiRu "createTask" "Создание услуги"{
            user -> profiRu.webApp
            profiRu.webApp -> profiRu.api "POST /tasks"
            profiRu.api -> profiRu.taskService
            profiRu.taskService -> profiRu.taskDb
            profiRu.taskService -> user "Уведомление о создании услуги"
            autolayout lr
        }

        dynamic profiRu "getTasks" "Получение списка услуг" {
            user -> profiRu.webApp
            profiRu.webApp -> profiRu.api "GET /tasks"
            profiRu.api -> profiRu.taskService
            profiRu.taskService -> profiRu.taskDb
            profiRu.taskService -> user
           autolayout lr
        }

        dynamic profiRu "addTaskInOrder" "Добавление услуг в заказ" {
            user -> profiRu.webApp
            profiRu.webApp -> profiRu.api "POST /orders/{orderId}/tasks/{taskId}"
            profiRu.api -> profiRu.orderService
            profiRu.taskService -> profiRu.orderService
            profiRu.orderService -> profiRu.orderDb
            profiRu.orderService -> user
            autolayout lr
        }

        dynamic profiRu "getOrderToUser" "Получение заказа для пользователя" {
            user -> profiRu.webApp
            profiRu.webApp -> profiRu.api "GET /users/{userId}/orders/{orderId}"
            profiRu.api -> profiRu.userService
            profiRu.userService -> profiRu.orderService
            profiRu.orderService -> profiRu.orderDb
            profiRu.orderService -> user
            autolayout lr
        }

        // Оформление
        styles {
            element "Database" {
                background #55aa55
                shape Cylinder
            }
        }

        theme default
}
