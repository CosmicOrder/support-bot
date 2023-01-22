# Боты службы поддержки

Данные боты обучены нейросетью DialogFLow, отвечать на типичные вопросы 
пользователей онлайн-издательства "Игра глаголов". 

DialogFlow - Это облачный сервис распознавания естественного языка от Google.


## Как установить

Скачайте код.

Создайте виртуальное окружение:

```
python3 -m venv venv
```

Активируйте виртуальное окружение:

- для Windows:
    ```
    venv\Scripts\activate 
    ```
- для Linux:
    ```
    source venv/bin/activate 
    ```

Установите зависимости командой:

```
pip install -r requirements.txt
```

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить,
создайте файл `.env` в корне проекта и запишите туда данные в таком
формате: `ПЕРЕМЕННАЯ=значение`.

Доступны следующие переменные:

- `SUPPORT_BOT_TOKEN` — токен, который необходим для управления телеграм-ботом службы поддержки через API
- `CHAT_ID` — ID чата, в который бот будет отправлять логи 
- `VK_GROUP_TOKEN` - токен, который необходим для управления Вк-ботом службы поддержки через API
- `GOOGLE_APPLICATION_CREDENTIALS` - учётные данные для облачных сервисов Google (в том числе DialogFlow)

## Запуск

Чтобы запустить телеграмм-бота, введите в терминале:

```
python main_tg.py 
```

Чтобы запустить вк-бота, введите в терминале:

```
python main_vk.py 
```

В результате, если вы всё сделали правильно, боты будет отвечать на типичные 
вопросы пользователей (см. гифки ниже).

![](https://github.com/CosmicOrder/support-bot/blob/master/vk_support.gif)
![](https://github.com/CosmicOrder/support-bot/blob/master/tg_support.gif)

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для
веб-разработчиков [dvmn.org](https://dvmn.org/).