import typing as t
import abc

from aiogram import Bot
from aiogram.types import (
    Message,
    MessageEntity,
    LinkPreviewOptions,
    ReplyParameters,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
    TelegramObject,
    CallbackQuery,
)


def to_html_str(obj: t.Any) -> str:
    string = str(obj)
    return string.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")


class AnswerToAbc(abc.ABC):
    async def delete_message(self, to_delete: Message | t.Any):
        try:
            await to_delete.delete()
        except Exception:
            return

    @abc.abstractmethod
    async def __call__(
        self,
        text: str,
        parse_mode: str | None = None,
        entities: list[MessageEntity] | None = None,
        link_preview_options: LinkPreviewOptions | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        allow_sending_without_reply: bool | None = None,
        disable_web_page_preview: bool | None = None,
        reply_to_message_id: int | None = None,
        delete_message: bool = True,
        **kwargs: t.Any,
    ) -> Message: ...


class AnswerToNotImplemented(AnswerToAbc):
    async def __init__(self, answer_to_type: TelegramObject):
        self._answer_to_type = TelegramObject

    async def __call__(
        self,
        text: str,
        parse_mode: str | None = None,
        entities: list[MessageEntity] | None = None,
        link_preview_options: LinkPreviewOptions | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        allow_sending_without_reply: bool | None = None,
        disable_web_page_preview: bool | None = None,
        reply_to_message_id: int | None = None,
        delete_message: bool = True,
        **kwargs: t.Any,
    ) -> Message:
        raise NotImplementedError(
            f"AnswerTo is not implemented for type '{type(self._answer_to_type).__name__}'"
        )


class AnswerToMessage(AnswerToAbc):
    def __init__(self, message: Message):
        self._message = message

    async def __call__(
        self,
        text: str,
        parse_mode: str | None = None,
        entities: list[MessageEntity] | None = None,
        link_preview_options: LinkPreviewOptions | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        allow_sending_without_reply: bool | None = None,
        disable_web_page_preview: bool | None = None,
        reply_to_message_id: int | None = None,
        delete_message: bool = True,
        **kwargs: t.Any,
    ) -> Message:
        if delete_message:
            await self.delete_message(self._message)
        return await self._message.answer(
            text,
            parse_mode,
            entities,
            link_preview_options,
            disable_notification,
            protect_content,
            message_effect_id,
            reply_parameters,
            reply_markup,
            allow_sending_without_reply,
            disable_web_page_preview,
            reply_to_message_id,
            **kwargs,
        )


class AnswerToCallbackQuery(AnswerToAbc):
    def __init__(self, callback: CallbackQuery, bot: Bot) -> None:
        self._callback = callback
        self._bot = bot

    async def __call__(
        self,
        text: str,
        parse_mode: str | None = None,
        entities: list[MessageEntity] | None = None,
        link_preview_options: LinkPreviewOptions | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        allow_sending_without_reply: bool | None = None,
        disable_web_page_preview: bool | None = None,
        reply_to_message_id: int | None = None,
        delete_message: bool = True,
        **kwargs: t.Any,
    ) -> Message:
        if self._callback.message is None:
            return await self._bot.send_message(
                self._callback.from_user.id,
                text,
                parse_mode,
                entities=entities,
                link_preview_options=link_preview_options,
                disable_notification=disable_notification,
                protect_content=protect_content,
                message_effect_id=message_effect_id,
                reply_parameters=reply_parameters,
                reply_markup=reply_markup,
                allow_sending_without_reply=allow_sending_without_reply,
                disable_web_page_preview=disable_web_page_preview,
                reply_to_message_id=reply_to_message_id,
                **kwargs,
            )
        if isinstance(self._callback.message, Message) and delete_message:
            await self.delete_message(self._callback.message)
        return await self._bot.send_message(
            self._callback.message.chat.id,
            text,
            parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
            allow_sending_without_reply=allow_sending_without_reply,
            disable_web_page_preview=disable_web_page_preview,
            reply_to_message_id=reply_to_message_id,
            **kwargs,
        )
