LEXICON: dict[str, str] = {
    '/start': 'Привет!\n\nЯ бот, который поможет вам следить за '
    'настроением.\n\n'
    'Вы можете вносить записи о своем настроении, а также получать статистику '
    'и график.\n\n'
    'Для получения списка доступных команд, отправьте /help.',
    '/help': 'Доступные команды:\n'
    '/mood - внести запись о настроении\n'
    '/settime - настроить время уведомления\n'
    '/delete - удалить ранее введенное настроение\n'
    '/chart - получить график настроения\n',
    '/mood': 'Введите ваше текущее настроение от 1 до 10, где 1 - очень '
    'плохое настроение, а 10 - отличное настроение.',
    '/edit': 'Выберите номер записи, которую хотите изменить:',
    '/settime': 'Выберите удобное время для уведомлений или '
    'отключите уведомления:',
    '/delete': 'Выберите номер записи, которую хотите удалить:',
    '/chart': 'Выберите период времени для построения графика:',
    'yes_button': 'Да😊',
    'no_button': 'Нет😒',
    'write_button': '📝Внести запись',
    'settime_button': '⏰Время уведомлений',
    'deletenotification_button': '🚫Убрать напоминания',
    'del_button': '❌Удалить запись',
    'graphic_button': '📈График настроения',
    'help_button': '🛟Помощь',
    'no_choice': 'Хорошо! Вы можете настроить их в любое время)',
    'start_settings_button': 'Хотите ли вы, чтобы я напоминал вам о '
    'необходимости внести запись о настроении?',
    'reminderset': 'В какое время по МСК вам удобно получить от меня сообщение '
    'с напоминанием?\nНажмите на соответствующую кнопку.\n\nЕсли вам не нравятся предложенные варианты, просто '
    'напишите нужное вам время в формате HH:MM.',
    'setdone': 'Напоминание установлено! Я напишу вам в назначенное время.',
    'invalid_message': 'Похоже я не знаю как обработать такое сообщение, проверьте корректно ли оно.',
    'today_mood': 'Оцените свое настроение от 1 до 10.',
    'invalid_mood': 'Пожалуйста, введите настроение от 1 до 10.',
    'mood_saved': 'Запись о вашем настроении сохранена.',
    'depression_detected': 'Я заметил, что в последнее время ваше настроение несколько ниже обычного 😔 '
    'Это может быть признаком депрессии. Важно обсудить это с психологом. '
    'Я рекомендую обратиться к Бэлле (https://www.b17.ru/id709403). Заботьтесь о своем психическом здоровье! 🌟',
    'repeat_depression': 'Я снова заметил, что в последнее время ваше настроение несколько ниже обычного 😔 '
    'Важно обсудить ваше самочувствие и получить поддержку. В этом может помочь психолог.  Берегите себя! 🌟'}

LEXICON_COMMANDS: dict[str, str] = {
    '/mood': '📝Внести запись',
    '/delete': '❌Удалить запись',
    '/chart': '📈График настроение',
    '/settime': '⏰Время уведомлений',
    '/deletenotification': '🚫Убрать напоминания',
    '/help': '🛟Справка по работе бота'
}
