from aiogram import Router, F
# from filters.admin_filter import IsAdmin

user_router = Router()
admin_router = Router()

# user_router.message.filter(F.chat.type.in_(["private"]))
# user_router.callback_query.filter(F.message.chat.type.in_(["private"]))

# admin_router.message.filter(IsAdmin())
# admin_router.callback_query.filter(IsAdmin())