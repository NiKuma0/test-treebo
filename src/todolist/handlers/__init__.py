from aiogram import Router

from . import menu_handlers, notes_handlers, register_handler


def setup_handlers(router: Router):
    router.include_routers(
        menu_handlers.router,
        notes_handlers.router,
        register_handler.router,
    )
