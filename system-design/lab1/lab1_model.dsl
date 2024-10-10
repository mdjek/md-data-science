workspace {
    name "Сайт заказа услуг"
    description "Представление архитектуры в нотации C4"
    !docs documentation

    model {
        user = person "Пользователь" "Использует сайт"

        profiRu = softwareSystem "Сайт заказа услуг" {
            description "Сайт для поиска и размещения заказов/услуг"

            frontend = container "Frontend" {
                description "Web приложение"
                technology "HTML/CSS, React, JS"
            }

            backend = container "Backend" {
                description "Обработка бизнес-логики"
                technology "Node.js, Python"
            }

            db = container "Database" {
                description "Хранение данных о пользователях, заказах"
                technology "Postgresql"
            }

            payment = container "Payment" {
                description "Сторонний сервис для интеграции систем оплат"
                technology "T‑API, MTS Pay"
            }

            cdn = container "Cdn"  {
                description "Хранилище статичных файлов, изображений, аватарок"
                technology "Nginx, Lua"
            }
        }
    }

    views {
        theme default

        systemContext profiRu "SystemContext" {
            include *
            autolayout lr
    }
}
