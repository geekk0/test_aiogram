async def send_initial_message(chat_id, user_name):
    await bot.send_message(chat_id, f"Привет, {user_name}! Как ты сегодня?", reply_markup=types.ReplyKeyboardRemove())
    job = scheduler.add_job(send_reminder, 'date', run_date=datetime.now() + timedelta(minutes=15), args=[chat_id])
    user_reminders[chat_id] = job

async def send_reminder(chat_id):
    await bot.send_message(chat_id, "Вы забыли ответить")
    user_reminders.pop(chat_id, None)