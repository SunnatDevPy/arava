import asyncio

from aiogram import Router, html, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from apps.models import User
from bot.buttuns.inline import main_menu, language_inl, get_location, confirm_register_inl, menu
from bot.state.states import Contact, Location

start_router = Router()


def register_detail(msg, data=None):
    return html.bold(f'''
Username: @{msg.from_user.username}
☎Raqam: {data.get('contact')}
''')


@start_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    data = await state.get_data()
    locale = data.get('locale')
    if locale == 'rus':
        til = "Выберите язык"
    else:
        til = 'Til tanlang'
    await message.answer(til, reply_markup=language_inl())

    # if ' ' in message.text:
    #     args = message.text.split(' ')[1]
    #     print(args)
    # else:
    #     args = None
    #
    # if args:
    #     inviter_id = int(args)
    #     user = await User.get(inviter_id)
    #     referred = await Referral.get_from_referral_and_referred(inviter_id, message.from_user.id)
    #     if referred == None:
    #         await Referral.create(referrer_id=inviter_id, referred_user_id=message.from_user.id)
    #         await User.update(inviter_id, coins=user.coins + 5000)
    #     else:
    #         await state.update_data(referred_id=inviter_id, referred_user_id=message.from_user.id)


# menu()

@start_router.message(Contact.phone)
async def register_full_name(msg: Message, state: FSMContext):
    await state.set_state(Contact.location)
    if msg.contact:
        await state.update_data(contact=msg.contact.phone_number)
        await msg.answer(html.bold("📍Locatsiya yuboring📍"), reply_markup=get_location(), parse_mode="HTML")
    else:
        try:
            contact = int(msg.text[1:])
            await state.update_data(contact=msg.text)
            await msg.answer(html.bold("📍Locatsiya yuboring📍"), reply_markup=get_location(), parse_mode="HTML")
        except:
            await msg.answer(html.bold("Telefon raqamni tog'ri kiriting"), parse_mode="HTML")


@start_router.message(Contact.location)
async def register_full_name(msg: Message, state: FSMContext):
    if msg.location:
        await state.update_data(long=msg.location.longitude, lat=msg.location.latitude)
        await state.set_state(Contact.confirm)
        data = await state.get_data()
        await msg.answer(html.bold("Ma'lumotingiz to'g'rimi?"), reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
        await msg.answer(register_detail(msg, data), parse_mode='HTML',
                         reply_markup=confirm_register_inl())
    else:
        await msg.answer(html.bold("Iltimos locatsiya jo'nating"), parse_mode="HTML")


@start_router.callback_query(Contact.confirm, F.data.endswith('_register'))
async def register_full_name(call: CallbackQuery, state: FSMContext):
    confirm = call.data.split('_')
    data = await state.get_data()
    from_user = call.from_user
    await call.message.delete()
    if confirm[0] == 'confirm':
        user_data = {'id': from_user.id, 'username': from_user.username,
                     'first_name': from_user.first_name, "last_name": from_user.last_name, "long": data.get('long'),
                     "lat": data.get('lat'), "contact": str(data.get('contact')),
                     'status': "SUPERUSER" if from_user.id == 5649321700 else "USER", 'type': 'one'}
        await User.create(**user_data)
        if call.from_user.id in [5649321700, ]:
            await call.message.answer(f'Xush kelibsiz Admin {call.from_user.first_name}',
                                      reply_markup=menu(call.from_user.id))
        else:
            await call.message.answer(f'Xush kelibsiz {call.from_user.first_name}',
                                      reply_markup=menu(call.from_user.id))
        await asyncio.sleep(60)
        await call.message.delete()
        await call.message.answer("Bosh Menu", reply_markup=ReplyKeyboardRemove())
        await call.message.answer("", reply_markup=main_menu())

        await state.clear()
    else:
        await state.set_state(Contact.phone)
        await call.message.answer("Qayta ro'yxatdan o'ting")


@start_router.callback_query(F.data == 'menu')
async def register_full_name(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.set_state(Location.location)
    await call.message.answer("Mahsulotni qayerga jo'natish uchun locatsiya kiriting!", reply_markup=get_location())


@start_router.message(Location.location)
async def register_full_name(message: Message, state: FSMContext):
    if message.location:
        data = await state.get_data()
        await User.update(message.from_user.id, lat=message.location.latitude, long=message.location.longitude)
        await message.answer("Menu", reply_markup=menu(message.from_user.id, language=data.get('locale')))
        await asyncio.sleep(60)
        await message.delete()
        await message.answer("Bosh Menu", reply_markup=main_menu())
        await state.clear()
    else:
        await message.answer("Locatsiya kiriting", reply_markup=get_location())
