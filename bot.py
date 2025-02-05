from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram import Router
import asyncio
from aiogram.types import FSInputFile
import django
from asgiref.sync import sync_to_async
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from amin.models import Tovar


BOT_API_TOKEN = '7342677552:AAF1ZTotSTb4ObFMvZUKElreZoqpslifpi0'

bot = Bot(token=BOT_API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()


@router.message(Command("start"))
async def send_welcome(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Каталог товаров 🛒", callback_data="catalog")],
        [InlineKeyboardButton(text="партнерство", callback_data="reviews")],
        [InlineKeyboardButton(text="Часто задаваемые вопросы", callback_data="materials")],
        [InlineKeyboardButton(text="Связаться с нами 💬", callback_data="contact")]
    ])
    await message.answer(
        "Yamagata Shop Bot — ваш гид в мире эксклюзивных катан и самурайских доспехов! ⚔️\n\n"
        "Бот поможет:\n\n"
        "• Посмотреть каталог товаров 🛒\n"
        "• Оформить заказ 📦\n"
        "• Узнать о материалах и качестве 🏣\n"
        "• Связаться с нами или оставить отзыв 💬\n\n"
        "✨ Добро пожаловать в мир японских традиций и мастерства! ✨",
        reply_markup=keyboard
    )
@router.callback_query(lambda c: c.data in ['contact'])
async def handle_callback_query(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data=='contact':
        await callback_query.message.answer('Связь с нами:\nНаш телеграм:@Creator_Beyond_X \nWhatsApp: +996 (554) 633-637 \nнаш телеграм-канал: https://t.me/YamagataCatalog \nСайт:https://yamagata.kz \nТик-ток:https://www.tiktok.com/@yamagata.kg \nЮтуб канал: https://www.youtube.com/@yamagatakg')


@router.callback_query(lambda callback: callback.data == "catalog")
async def handle_catalog(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="экслюзивные товары 🛒", callback_data="exclusive_0")],
        [InlineKeyboardButton(text="Боевые катаны 🛒", callback_data="fight_katan_0")],
        [InlineKeyboardButton(text="Не боевые катаны 📦", callback_data="katan_replic_0")],
        [InlineKeyboardButton(text="Разница между боевым и не боевым 🏣", callback_data="sovet")],
    ])
    await callback_query.message.answer(
        "Каталог Yamagata Shop \n\n"
        "Добро пожаловать в наш каталог! Здесь вы найдете уникальные товары, созданные мастерами с использованием традиционных японских технологий.",
        reply_markup=keyboard
    )
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data.startswith("fight_katan"))
async def handle_fight_katan(callback_query: CallbackQuery):
    try:
        products = await sync_to_async(list)(
            Tovar.objects.filter(category="fight_katan")
        )

        if not products:
            await callback_query.message.answer("Продукты не найдены для этой категории.")
            return

        data_parts = callback_query.data.split("_")
        current_index = int(data_parts[-1]) if len(data_parts) > 2 else 0

        if "next" in callback_query.data:
            current_index = (current_index + 1) % len(products)
        elif "back" in callback_query.data:
            current_index = (current_index - 1) % len(products)

        product = products[current_index]

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Назад", callback_data=f"fight_katan_back_{current_index}"),
                InlineKeyboardButton(text="Купить", callback_data=f"buy_{product.id}"),
                InlineKeyboardButton(text="Дальше", callback_data=f"fight_katan_next_{current_index}"),
            ]
        ])

        from django.conf import settings
        if product.image and product.image.name:
            image_path = os.path.join(settings.MEDIA_ROOT, product.image.name)

            if os.path.exists(image_path):
                await callback_query.message.edit_media(
                    media=types.InputMediaPhoto(
                        media=FSInputFile(image_path),
                        caption=f"{product.name}\n{product.description}\n\nСНГ страны - {product.price_sng}€💶\n🥷 EUROPE and AMERICA - {product.price_EUROPE_AMERICA}€💶 \n⚔️ Africa, Australia - {product.price_Africa_Australia}€💶"
                    ),
                    reply_markup=keyboard
                )
            else:
                await callback_query.message.edit_text("Изображение не найдено на сервере.")
        else:
            await callback_query.message.edit_text("У продукта нет изображения.", reply_markup=keyboard)

    except Exception as e:
        await callback_query.message.answer(f"Произошла ошибка: {e}")

@router.callback_query(lambda callback: callback.data.startswith("katan_replic"))
async def handle_katan_replic(callback_query: CallbackQuery):
    try:
        products = await sync_to_async(list)(
            Tovar.objects.filter(category="katan_replic")
        )

        if not products:
            await callback_query.message.answer("Продукты не найдены для этой категории.")
            return

        data_parts = callback_query.data.split("_")
        current_index = int(data_parts[-1]) if len(data_parts) > 2 else 0

        if "next" in callback_query.data:
            current_index = (current_index + 1) % len(products)
        elif "back" in callback_query.data:
            current_index = (current_index - 1) % len(products)

        product = products[current_index]

        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="Назад", callback_data=f"katan_replic_back_{current_index}"),
            InlineKeyboardButton(text="Купить", callback_data=f"buy_{product.id}"),
            InlineKeyboardButton(text="Дальше", callback_data=f"katan_replic_next_{current_index}"),
        ]])

        from django.conf import settings
        if product.image and product.image.name:
            image_path = os.path.join(settings.MEDIA_ROOT, product.image.name)

            if os.path.exists(image_path):
                try:
                    await callback_query.message.edit_media(
                        media=types.InputMediaPhoto(
                            media=FSInputFile(image_path),
                            caption=f"{product.name}\n{product.description}\n\nСНГ страны - {product.price_sng}€💶\n🥷 EUROPE and AMERICA - {product.price_EUROPE_AMERICA}€💶 \n⚔️ Africa, Australia - {product.price_Africa_Australia}€💶"
                        ),
                        reply_markup=keyboard
                    )
                except Exception as e:
                    await callback_query.message.answer_photo(
                        photo=FSInputFile(image_path),
                        caption=f"{product.name}\n{product.description}\nЦена: {product.price} ₽",
                        reply_markup=keyboard
                    )
            else:
                await callback_query.message.answer("Изображение не найдено на сервере.")
        else:
            await callback_query.message.answer("У продукта нет изображения.", reply_markup=keyboard)

    except Exception as e:
        await callback_query.message.answer(f"Произошла ошибка: пожалуста напишете сюда @bekatur32")



@router.callback_query(lambda callback: callback.data.startswith("exclusive"))
async def handle_fight_katan(callback_query: CallbackQuery):
    try:
        products = await sync_to_async(list)(
            Tovar.objects.filter(category="exclusive")
        )

        if not products:
            await callback_query.message.answer("Продукты не найдены для этой категории.")
            return

        data_parts = callback_query.data.split("_")
        current_index = int(data_parts[-1]) if len(data_parts) > 2 else 0

        if "next" in callback_query.data:
            current_index = (current_index + 1) % len(products)
        elif "back" in callback_query.data:
            current_index = (current_index - 1) % len(products)

        product = products[current_index]

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Назад", callback_data=f"exclusive_back_{current_index}"),
                InlineKeyboardButton(text="Купить", callback_data=f"buy_{product.id}"),
                InlineKeyboardButton(text="Дальше", callback_data=f"exclusive_next_{current_index}"),
            ]
        ])

        from django.conf import settings
        if product.image and product.image.name:
            image_path = os.path.join(settings.MEDIA_ROOT, product.image.name)

            if os.path.exists(image_path):
                await callback_query.message.edit_media(
                    media=types.InputMediaPhoto(
                        media=FSInputFile(image_path),
                        caption=f"{product.name}\n{product.description}\n\n🗡СНГ страны - {product.price_sng}€💶\n🥷 EUROPE and AMERICA - {product.price_EUROPE_AMERICA}€💶 \n⚔️ Africa, Australia - {product.price_Africa_Australia}€💶"
                    ),
                    reply_markup=keyboard
                )
            else:
                await callback_query.message.edit_text("Изображение не найдено на сервере.")
        else:
            await callback_query.message.edit_text("У продукта нет изображения.", reply_markup=keyboard)

    except Exception as e:
        await callback_query.message.answer(f"Произошла ошибка: пожалуста напишете сюда @bekatur32")


@router.callback_query(lambda callback: callback.data.startswith("materials"))
async def handle_reviews(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛠 Качество товаров", callback_data="tov"),
            InlineKeyboardButton(text="💳 Оплата", callback_data="oplata")
        ],
        [
            InlineKeyboardButton(text="🚚 Доставка", callback_data="dhl")
        ],
        [
            InlineKeyboardButton(text="🎨 Индивидуальные заказы", callback_data="imp"),
        ],

        [InlineKeyboardButton(text="Связаться с менеджером", callback_data="contact")]
    ])
    await callback_query.message.answer(
        "Выберите интересующий вас вопрос:",
        reply_markup=keyboard
    )

#from aiogram.types import LabeledPrice


# оплата надо потом добавить
# @router.callback_query(lambda callback: callback.data.startswith("buy_"))
# async def handle_buy(callback_query: CallbackQuery):
#     product_id = int(callback_query.data.split("_")[1])
#     product = await sync_to_async(Tovar.objects.get)(id=product_id)
#
#     prices = [LabeledPrice(label=product.name, amount=int(product.price * 100))]
#
#     await callback_query.bot.send_invoice(
#         chat_id=callback_query.from_user.id,
#         title=product.name,
#         description=product.description,
#         payload=f"product_{product.id}",
#         provider_token="YOUR_PROVIDER_TOKEN",  # Укажите токен провайдера от BotFather
#         currency="SOM",  # Валюта (например, RUB, USD, EUR)
#         prices=prices,
#         start_parameter="buy-product"
#     )
#     await callback_query.answer("Счёт отправлен! Проверьте ваш чат.")
# @router.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
# async def successful_payment(message: types.Message):
#     product_id = int(message.successful_payment.invoice_payload.split("_")[1])
#     await message.answer(
#         f"Оплата успешно завершена! Спасибо за покупку. "
#         f"Мы свяжемся с вами для уточнения деталей."
#     )



@router.callback_query(lambda c: c.data in ["tov", "oplata", "dhl", "imp"])
async def handle_question(callback_query: CallbackQuery):
    # Словарь с текстами для каждого варианта
    responses = {
        "tov": (
            "✨ *Качество товаров*\n\n"
            "Наши катаны изготавливаются вручную из высококачественной стали. "
            "Каждая деталь — результат кропотливой работы мастеров. Вы получите не только оружие, "
            "но и настоящее произведение искусства!"
        ),
        "oplata": (
            "💳 *Способы оплаты*\n\n"
            "Мы поддерживаем любой удобный способ оплаты: банковские карты, электронные кошельки, "
            "PayPal, криптовалюту и другие. Просто выберите подходящий вариант при оформлении заказа!"
        ),
        "dhl": (
            "🚚 *Доставка*\n\n"
            "Мы доставляем наши катаны по всему миру! Партнёрские службы, такие как DHL, "
            "обеспечат безопасную и быструю доставку до вашего порога. Свяжитесь с нами для уточнения сроков."
        ),
        "imp": (
            "🖌️ *Индивидуальные заказы*\n\n"
            "Мы можем изготовить катану по вашим пожеланиям! Выберите материалы, дизайн, длину клинка, "
            "узор рукояти и даже добавьте персональную гравировку. Обсудите детали с нашим мастером!"
        )
    }
    response = responses.get(callback_query.data, "К сожалению, информация недоступна.")
    await callback_query.message.answer(response, parse_mode="Markdown")
    await callback_query.answer()

@router.callback_query(lambda callback: callback.data.startswith("reviews"))
async def handle_reviews(callback_query: CallbackQuery):
    await callback_query.message.answer(
        "✨ Партнёрство с Yamagata Shop ✨\n\n"
        "Станьте частью мира японских традиций и мастерства! Мы открыты для сотрудничества с блогерами, магазинами, дизайнерами и любыми проектами, которые разделяют нашу любовь к уникальным товарам.\n\n"
        "🎯 Что мы предлагаем:\n"
        "• Уникальные условия для партнёров.\n"
        "• Индивидуальный подход к каждому проекту.\n"
        "• Возможность совместных акций и мероприятий.\n\n"
        "📩 Напишите нам, и мы обсудим все детали сотрудничества!\n\n"
        "Наш телеграм: @Creator_Beyond_X\n"
        "WhatsApp: +996 (554) 633-637"
    )



dp.include_router(router)

async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
