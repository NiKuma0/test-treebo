from aiogram import Router

from . import menu_handlers


def setup_handlers(router: Router):
    router.include_routers(
        menu_handlers.router,
    )
