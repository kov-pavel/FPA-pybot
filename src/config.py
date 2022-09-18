import os

SECRET_KEY = os.getenv('BOT_KEY')
WATERMARKS = {
    'Тренд': "− •−• • −• −••",
    'Финтрендинг': "••−• •• −• − •−• • −• −•• •• −• −−•"
}

WIDTH_THRESHOLD = 1200
HEIGHT_THRESHOLD = 1200
OVERALL_THRESHOLD = 2073600
ARCHIVE_NAME = 'result.zip'

STATUSES = ('Пользователь', 'Администратор')
