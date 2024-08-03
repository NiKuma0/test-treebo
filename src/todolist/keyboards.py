import calendar

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_data import CalendarCallbackData, CalendarGrade


def years_grade_keyboard(data: CalendarCallbackData) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[]])


def months_grade_keyboard(data: CalendarCallbackData) -> InlineKeyboardMarkup:
    header = InlineKeyboardBuilder(
        markup=[
            [
                InlineKeyboardButton(
                    text="Months",
                    callback_data=data.model_copy(
                        update={"selected_grade": CalendarGrade.grades}
                    ).pack(),
                )
            ]
        ]
    )
    footer = InlineKeyboardBuilder(
        markup=[
            [
                InlineKeyboardButton(
                    text=str(data.year),
                    callback_data=data.model_copy(
                        update={"selected_grade": CalendarGrade.years}
                    ).pack(),
                )
            ]
        ]
    )
    builder = InlineKeyboardBuilder()
    builder.attach(header)
    for i, month in enumerate(calendar.month_name):
        builder.add(
            InlineKeyboardButton(
                text=month,
                callback_data=data.model_copy(
                    update={"month": i, "selected_grade": CalendarGrade.days}
                ).pack(),
            )
        )
    builder.adjust(4, True)
    builder.attach(footer)
    return builder.as_markup()


def calendar_keyboard(data: CalendarCallbackData) -> InlineKeyboardMarkup:
    match data.selected_grade:
        case CalendarGrade.months:
            return months_grade_keyboard(data)
        case CalendarGrade.years:
            return years_grade_keyboard(data)
        case _:
            return InlineKeyboardMarkup(inline_keyboard=[[]])
