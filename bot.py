from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import logging

# Включим логирование для отслеживания ошибок
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
WAITING_FOR_NAME, WAITING_FOR_SURNAME = range(2)

# Замените 'YOUR_BOT_TOKEN_HERE' на реальный токен вашего бота
BOT_TOKEN = '8212668348:AAGE8zi0XtoX5mnKGj5g3n2-32qBODImugA'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает команду /start и начинает диалог"""
    user = update.message.from_user
    logger.info("Пользователь %s начал диалог.", user.first_name)
    
    # Просим ввести имя
    await update.message.reply_text(
        'Привет! 👋\n'
        'Я бот для сбора информации.\n\n'
        'Пожалуйста, введите ваше имя:',
        reply_markup=ReplyKeyboardRemove()  # Убираем клавиатуру если была
    )
    
    return WAITING_FOR_NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получает имя и просит ввести фамилию"""
    user_input = update.message.text
    context.user_data['first_name'] = user_input
    
    logger.info("Имя пользователя: %s", user_input)
    
    await update.message.reply_text(
        f'Отлично, {user_input}! Теперь введите вашу фамилию:'
    )
    
    return WAITING_FOR_SURNAME

async def get_surname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получает фамилию и завершает диалог"""
    user_input = update.message.text
    context.user_data['last_name'] = user_input
    
    first_name = context.user_data.get('first_name', '')
    last_name = context.user_data.get('last_name', '')
    
    logger.info("Пользователь %s %s завершил ввод данных", first_name, last_name)
    
    # Отправляем подтверждение с собранными данными
    await update.message.reply_text(
        f'✅ Спасибо! Ваши данные сохранены:\n\n'
        f'👤 Ваше имя и фамилия: {first_name} {last_name}\n\n'
        f'Для начала заново отправьте /start'
    )
    
    # Очищаем данные пользователя
    context.user_data.clear()
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отменяет диалог"""
    user = update.message.from_user
    logger.info("Пользователь %s отменил диалог.", user.first_name)
    
    await update.message.reply_text(
        'Диалог отменен. Если хотите начать заново, отправьте /start',
        reply_markup=ReplyKeyboardRemove()
    )
    
    context.user_data.clear()
    return ConversationHandler.END

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает ошибки"""
    logger.error('Ошибка при обработке сообщения: %s', context.error, exc_info=context.error)

def main() -> None:
    """Запускает бота"""
    # Создаем Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Настраиваем ConversationHandler для управления диалогом
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WAITING_FOR_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)
            ],
            WAITING_FOR_SURNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_surname)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Добавляем обработчики
    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()