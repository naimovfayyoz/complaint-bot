import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, admin
import keyboard as kb
import functions as func
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.executor import start_webhook

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
connection = sqlite3.connect('data.db')
q = connection.cursor()


class st(StatesGroup):
    item = State()
    item2 = State()
    item3 = State()
    item4 = State()


@dp.message_handler(commands=['start'])
async def on_startup(message: types.Message):
    func.join(chat_id=message.chat.id)
    q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = q.fetchone()
    if result[0] == 0:
        if message.chat.id in admin:
            await message.answer('Добро пожаловать, босс.', reply_markup=kb.menu)

        else:
            await message.answer(
                'Это бот для АНОНИМНЫХ жалоб и предложений SamRafoatTextile. Ваша АНОНИМНАЯ жалоба/предложение будет напрямую рассмотрено начальством.Просьба - отправляйте жалобы в одном сообщении!\n')
            await message.answer(
                'Bu Anonim shikoyatlar va takliflar uchun SamRafoatTixtile ning boti. Sizning shikoyatlaringiz va takliflaringiz tugridan tugri boshliqlar tomonidan urganib chiqariladi. Iltimos, xabarlaringizni 1 ta xabar qilib junating!\n')
    else:
        await message.answer('Ты был заблокирован админом')


@dp.message_handler(content_types=['text'], text='👑 Админка')
async def handfler(message: types.Message, state: FSMContext):
    func.join(chat_id=message.chat.id)
    q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = q.fetchone()
    if result[0] == 0:
        if message.chat.id in admin:
            await message.answer('Добро пожаловать в админ-панель.', reply_markup=kb.adm)


@dp.message_handler(content_types=['text'], text='⏪ Назад')
async def handledr(message: types.Message, state: FSMContext):
    await message.answer('Добро пожаловать!.', reply_markup=kb.menu)


@dp.message_handler(content_types=['text'], text='👥 Юзеры')
async def handlaer(message: types.Message, state: FSMContext):
    func.join(chat_id=message.chat.id)
    q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = q.fetchone()
    if result[0] == 0:
        if message.chat.id in admin:
            q.execute(f"SELECT * FROM users ")
            result = q.fetchall()

            sl = []
            for index in result:
                i = index[0]
                # name = bot.send_message(i, message.from_user.first_name)
                # username = bot.send_message(message.from_user.id, message.from_user.mention)
                sl.append(i)

            ids = '\n'.join(map(str, sl))
            await message.answer(f'ID пользователей в боте:\n{ids}\nКолличество юзеров в боте: {len(result)}')


@dp.message_handler(content_types=['text'], text='👿 ЧС')
async def handlaer(message: types.Message, state: FSMContext):
    func.join(chat_id=message.chat.id)
    q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = q.fetchone()
    if result[0] == 0:
        if message.chat.id in admin:
            q.execute(f"SELECT * FROM users WHERE block == 1")
            result = q.fetchall()
            sl = []
            for index in result:
                i = index[0]
                sl.append(i)

            ids = '\n'.join(map(str, sl))
            await message.answer(f'ID пользователей в ЧС:\n{ids}')


@dp.message_handler(content_types=['text'], text='✅ Добавить в ЧС')
async def hanadler(message: types.Message, state: FSMContext):
    func.join(chat_id=message.chat.id)
    q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = q.fetchone()
    if result[0] == 0:
        if message.chat.id in admin:
            await message.answer(
                'Введите id пользователя, которого нужно заблокировать.\nДля отмены - нажмите на кнопку ниже',
                reply_markup=kb.back)
            await st.item3.set()


@dp.message_handler(content_types=['text'], text='❎ Убрать из ЧС')
async def hfandler(message: types.Message, state: FSMContext):
    func.join(chat_id=message.chat.id)
    q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = q.fetchone()
    if result[0] == 0:
        if message.chat.id in admin:
            await message.answer(
                'Введите id пользователя, которого нужно разблокировать.\nДля отмены - нажмите на кнопку ниже',
                reply_markup=kb.back)
            await st.item4.set()


@dp.message_handler(content_types=['text'], text='💬 Рассылка')
async def hangdler(message: types.Message, state: FSMContext):
    func.join(chat_id=message.chat.id)
    q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = q.fetchone()
    if result[0] == 0:
        if message.chat.id in admin:
            await message.answer('Введите текст для рассылки.\n\nДля отмены - нажми на кнопку ниже',
                                 reply_markup=kb.back)
            await st.item.set()


@dp.message_handler(content_types=['text'])
@dp.throttled(func.antiflood, rate=3)
async def h(message: types.Message, state: FSMContext):
    func.join(chat_id=message.chat.id)
    q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = q.fetchone()
    if result[0] == 0:
        if message.chat.id in admin:
            pass
        else:
            await message.answer('Сообщение отвправлано!.')
            for i in admin:
                print(i)
                await bot.send_message(i,
                                       f"<b>Получен новый вопрос!</b>\n<b>От:</b> {message.from_user.mention}\nID: {message.chat.id}\n<b>Сообщение:</b> {message.text}",
                                       reply_markup=kb.fun(message.chat.id), parse_mode='HTML')
    else:
        await message.answer('Вы были заблокированы за спам.')


@dp.callback_query_handler(lambda call: True)  # Inline часть
async def cal(call, state: FSMContext):
    if 'ans' in call.data:
        a = call.data.index('-ans')
        ids = call.data[:a]
        await call.message.answer('Введите ответ:', reply_markup=kb.back)
        await st.item2.set()  # админ отвечает пользователю
        await state.update_data(uid=ids)
    elif 'ignor' in call.data:
        await call.answer('Удалено')
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await state.finish()


@dp.message_handler(state=st.item2)
async def proc(message: types.Message, state: FSMContext):
    if message.text == '⏪ Отмена':
        await message.answer('Отмена! Возвращаю назад.', reply_markup=kb.menu)
        await state.finish()
    else:
        await message.answer('Сообщение отправлено.', reply_markup=kb.menu)
        data = await state.get_data()
        id = data.get("uid")
        await state.finish()
        await bot.send_message(id, 'Вам поступил ответ от администрации\n\nТекст: {}'.format(message.text))


@dp.message_handler(state=st.item)
async def process_name(message: types.Message, state: FSMContext):
    q.execute(f'SELECT user_id FROM users')
    row = q.fetchall()
    connection.commit()
    text = message.text
    if message.text == '⏪ Отмена':
        await message.answer('Отмена! Возвращаю назад.', reply_markup=kb.adm)
        await state.finish()
    else:
        info = row
        await message.answer('Рассылка начата!', reply_markup=kb.adm)
        for i in range(len(info)):
            try:
                await bot.send_message(info[i][0], str(text))
            except:
                pass
        await message.answer('Рассылка завершена!', reply_markup=kb.adm)
        await state.finish()


@dp.message_handler(state=st.item3)
async def proce(message: types.Message, state: FSMContext):
    if message.text == '⏪ Отмена':
        await message.answer('Отмена! Возвращаю назад.', reply_markup=kb.adm)
        await state.finish()
    else:
        if message.text.isdigit():
            q.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
            result = q.fetchall()
            connection.commit()
            if len(result) == 0:
                await message.answer('Такой пользователь не найден в базе данных.', reply_markup=kb.adm)
                await state.finish()
            else:
                a = result[0]
                id = a[0]
                if id == 0:
                    q.execute(f"UPDATE users SET block = 1 WHERE user_id = {message.text}")
                    connection.commit()
                    await message.answer('Пользователь успешно заблочен.', reply_markup=kb.adm)
                    await state.finish()
                    await bot.send_message(message.text, 'Ты забанен администрацией.')
                else:
                    await message.answer('Данный пользователь был заблокирован', reply_markup=kb.adm)
                    await state.finish()
        else:
            await message.answer('Ты вводишь буквы...\nВведи ID')


@dp.message_handler(state=st.item4)
async def proc(message: types.Message, state: FSMContext):
    if message.text == '⏪ Отмена':
        await message.answer('Отмена! Возвращаю назад.', reply_markup=kb.adm)
        await state.finish()
    else:
        if message.text.isdigit():
            q.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
            result = q.fetchall()
            connection.commit()
            if len(result) == 0:
                await message.answer('Такой пользователь не найден в базе данных.', reply_markup=kb.adm)
                await state.finish()
            else:
                a = result[0]
                id = a[0]
                if id == 1:
                    q.execute(f"UPDATE users SET block = 0 WHERE user_id = {message.text}")
                    connection.commit()
                    await message.answer('Пользователь успешно разбанен.', reply_markup=kb.adm)
                    await state.finish()
                    await bot.send_message(message.text, 'Вы были разблокированы администрацией.')
                else:
                    await message.answer('Данный пользователь не забанен.', reply_markup=kb.adm)
                    await state.finish()
        else:
            await message.answer('Ты вводишь буквы...\nВведи ID')


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

