# Система защиты фотографий от кражи.

## Мотивация
Продавцы товаров в интернет магазинах зачастую обращаются к профессиональным фото-студиями, чтобы представить свой продукт в лучшем виде. Как правило,
создание фотографий хорошего качества обходится не дешево.

К сожалению, недобросовестный продавец может попросту украсть фотографии товара и использовать их в качестве своих собственных. Владельцы магазинов по этому поводу могут обратиться в суд, однако у них должны быть доказательства, что фотография изначально принадлежала именно им. Один из способов доказательства - наличие водяного знака на фотографии.

Популярные маркетплейсы, такие, как Ozon или Wildberries, запрещают загружать на свои площадки фотографии товаров с явными водяными знаками, что исключает возможность наложения таковых на фотографию. Закодировать вотермарку в код фотографии тоже не получится, поскольку при загрузке на сервис она подвергается алгоритмам сжатия. Настоящий бот призван решить эту проблему принципиально новым способом наложения водяного знака на фотографию.

## Идея
Бот принимает изображение (или архив изображений) и кодирует на каждом из них некоторую ключевую фразу по правилам азбуки морзе в виде точек на изображении. Точки получаются достаточно большими, чтобы остаться после сжатия торговой площадкой, но достаточно маленькими, чтобы быть незаметными и не нарушать правил площадки.

В итоге владелец, предъявив расположение точек на сворованной фотографии, может доказать факт кражи.

## Использование бота

### Установка
Для запуска бота вам потребуется установленный язык программирования ```python3```, а также менеджер python-пакетов ```pip```.

После скачивания репозитория, находясь в корне, напишите в терминале ```pip install -r requirements.txt```, чтобы установить необходимые зависимости.

Программа ищет токен бота в переменной окружения ```BOT_KEY```.

### Команды бота
```/start``` - получить приветственное сообщение

```/help``` - получить справку по функциям бота

```/change``` - изменить кодируемое слово

```/add``` - добавить нового пользователя

```/remove``` - удалить нового пользователя

```/list``` - вывести список пользователей

### Использованные библиотеки
<b>Библиотека бота</b> - https://github.com/eternnoir/pyTelegramBotAPI

## Участники команды
* Александр Косницкий - 3530904/00103
* Кирилл Победоносцев - 3530904/00103
* Павел Коваленко - 3530904/00103
* Артём Трофимов - 3530904/00103
* Артём Щередин - 3530904/00102
* Владислав Почернин - 3530904/00104
