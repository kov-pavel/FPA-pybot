from db import Database


def admin(bot):
    def inner(func):
        def wrapper(message):
            with Database() as db:
                if not db.is_admin(message.from_user.id):
                    return bot.reply_to(message, "Доступ запрещен\n"
                                                 f"Ваш ID: {message.from_user.id}\n"
                                                 f"Отправьте его администратору")
            return func(message)

        return wrapper

    return inner


def user(bot):
    def inner(func):
        def wrapper(message):
            with Database() as db:
                if not db.is_user(message.from_user.id):
                    return bot.reply_to(message, "Доступ запрещен\n"
                                                 f"Ваш ID: {message.from_user.id}\n"
                                                 f"Отправьте его администратору")
            return func(message)

        return wrapper

    return inner
