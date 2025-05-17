from aiogram import types, Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID
from sheets import send_to_google_sheets

router = Router()

class OSAGOForm(StatesGroup):
    car_model = State()
    year = State()
    city = State()
    driver_info = State()
    drivers_type = State()
    sts_number = State()

@router.message(F.text.lower() == "оформить осаго")
async def start_form(message: types.Message, state: FSMContext):
    await message.answer("Введите марку и модель авто:")
    await state.set_state(OSAGOForm.car_model)

@router.message(OSAGOForm.car_model)
async def ask_year(message: types.Message, state: FSMContext):
    await state.update_data(car_model=message.text)
    await message.answer("Введите год выпуска:")
    await state.set_state(OSAGOForm.year)

@router.message(OSAGOForm.year)
async def ask_city(message: types.Message, state: FSMContext):
    await state.update_data(year=message.text)
    await message.answer("Введите город регистрации:")
    await state.set_state(OSAGOForm.city)

@router.message(OSAGOForm.city)
async def ask_driver_info(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Возраст и стаж водителя (пример: 30 лет / 10 лет стажа):")
    await state.set_state(OSAGOForm.driver_info)

@router.message(OSAGOForm.driver_info)
async def ask_drivers_type(message: types.Message, state: FSMContext):
    await state.update_data(driver_info=message.text)
    await message.answer("Сколько водителей вписано? Или напишите 'без ограничений':")
    await state.set_state(OSAGOForm.drivers_type)

@router.message(OSAGOForm.drivers_type)
async def ask_sts(message: types.Message, state: FSMContext):
    await state.update_data(drivers_type=message.text)
    await message.answer("Введите номер СТС (если есть):")
    await state.set_state(OSAGOForm.sts_number)

@router.message(OSAGOForm.sts_number)
async def finish_form(message: types.Message, state: FSMContext):
    await state.update_data(sts_number=message.text)
    data = await state.get_data()
    info = (
        f"Заявка на ОСАГО:\n"
        f"Марка и модель: {data['car_model']}\n"
        f"Год выпуска: {data['year']}\n"
        f"Город: {data['city']}\n"
        f"Водитель: {data['driver_info']}\n"
        f"Тип водителей: {data['drivers_type']}\n"
        f"СТС: {data['sts_number']}"
    )
    await message.answer("Спасибо! Ваша заявка отправлена.")
    await message.bot.send_message(ADMIN_ID, info)
    send_to_google_sheets(data)
    await state.clear()
