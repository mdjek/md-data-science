workspace {
    name "Сайт заказа услуг"
    description "Представление архитектуры в нотации C4"
    !docs documentation

    model {
        user = person "User" {
            description "Пользователь web-приложения"
        }

        profiRu = softwareSystem "Сайт profi.ru" {
            description "Сайт для поиска и заказа услуг"

            frontend = container "Frontend" {
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

            paymentService = container "Payment service" {
                description "Cервис для интеграции систем платежей"
                technology "T-API, MTS Pay"
            }

            orderDb = container "Order/task database" {
                description "Хранение данных о заказах (услугах)"
                technology "PostgreSQL"
                tags "Database"
            }

            userDb = container "User database" {
                description "Хранение данных о пользователях"
                technology "PostgreSQL"
                tags "Database"
            }

            cdn = container "Cdn"  {
                description "Хранилище статичных файлов, изображений, аватарок"
                technology "Nginx, Lua"
            }

            //  Сценарии взаимодействия с системой
            user -> frontend "Представление интерфейса для взаимодействия с системой"
            frontend -> cdn "Запрос статичных файлов для графического отображения в интерфейсах (шрифты, svg, webp)"
            frontend -> api "Отправление запросов к небходимым endpoint'ам"
            api -> userService "Запросы авторизации, CRUD пользователей"
            api -> orderService "Запросы CRUD заказов"
            api -> taskService "Запросы CRUD услуг"
            api -> paymentService "Запросы на проведение платежей"

            user -> userService "Управление аккаунтом"
            user -> orderService "Управление заказами"
            user -> taskService "Управление услугами"

            userService -> userDb "Чтение/запись данных в базе пользователей"
            orderService -> orderDb "Чтение/запись данных в базе заказов (услуг)"
            taskService -> orderDb "Чтение/запись данных в базе заказов (услуг)"

            // межсервисное взаимодействие
            orderService -> userService "Получение данных о пользователе"
            userService -> orderService "Получение данных о заказах"
            userService -> taskService "Получение данных об услугах"

            // Сценарии
            user -> frontend "Создание нового пользователя"
            frontend -> api "POST /users"
            api -> userService
            userService -> userDb
            userService -> user "Уведомление о создании пользователя"

            user -> frontend "Поиск пользователя по логину"
            frontend -> api "POST /search?login={str}"
            api -> userService
            userService -> userDb
            userService -> user "Уведомление о результате поиска"

            user -> frontend "Поиск пользователя по логину"
            frontend -> api "POST /search?firstname={firstname}&lastname={lastname}"
            api -> userService
            userService -> userDb
            userService -> user "Уведомление о результате поиска"

            user -> frontend "Создание новой услуги"
            frontend -> api "POST /tasks"
            api -> taskService
            taskService -> orderDb
            taskService -> user "Уведомление о создании услуги"

            user -> frontend "Получение списка услуг"
            frontend -> api "GET /tasks"
            api -> taskService
            taskService -> orderDb
            taskService -> user

            user -> frontend "Добавление услуги в заказ"
            frontend -> api "POST /orders/{orderId}/tasks/{taskId}"
            api -> orderService
            orderService -> orderDb
            orderService -> user

            user -> frontend "Получение заказа для пользователя"
            frontend -> api "GET /users/{userId}/orders/{orderId}"
            api -> userService
            userService -> orderService
            orderService -> orderDb
            orderService -> user
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

        dynamic profiRu "createOrderAndTask" "Создание нового заказа и услуги" {
            user -> profiRu.frontend "Создаёт нового пользователя"
            profiRu.frontend -> profiRu.api "POST /users"
            profiRu.api -> profiRu.userService
            profiRu.userService -> profiRu.userDb
            profiRu.userService -> user "Уведомление о создании пользователя"

            user -> profiRu.frontend "Создаёт новый заказ"
            profiRu.frontend -> profiRu.api "POST /orders"
            profiRu.api -> profiRu.orderService
            profiRu.orderService -> profiRu.orderDb
            profiRu.orderService -> user "Уведомление о создании нового заказа"

            user -> profiRu.frontend "Создание новой услуги в конкретном заказе"
            profiRu.frontend -> profiRu.api "POST /orders/{orderId}/tasks/"
            profiRu.api -> profiRu.taskService "POST /task"
            profiRu.taskService -> profiRu.orderDb
            profiRu.taskService -> user "Уведомление о создании новой услуги в заказе"
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
