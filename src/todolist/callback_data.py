import enum

from aiogram.filters.callback_data import CallbackData


class CalendarGrade(enum.StrEnum):
    years = enum.auto()
    months = enum.auto()
    days = enum.auto()
    grades = enum.auto()


class CalendarCallbackData(CallbackData, prefix="calendar"):
    year: int
    month: int
    day: int
    hours: int
    minutes: int
    selected_grade: CalendarGrade
