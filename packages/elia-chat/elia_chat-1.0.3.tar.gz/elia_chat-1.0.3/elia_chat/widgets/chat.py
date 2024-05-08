from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from textual import log, on, work, events
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.css.query import NoMatches
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget

from elia_chat.chats_manager import ChatsManager
from elia_chat.models import ChatData, ChatMessage
from elia_chat.screens.chat_details import ChatDetails
from elia_chat.widgets.agent_is_typing import AgentIsTyping
from elia_chat.widgets.chat_header import ChatHeader
from elia_chat.widgets.prompt_input import PromptInput
from elia_chat.models import (
    EliaChatModel,
    get_model_by_name,
)
from elia_chat.widgets.chatbox import Chatbox


if TYPE_CHECKING:
    from elia_chat.app import Elia
    from litellm.types.completion import (
        ChatCompletionUserMessageParam,
        ChatCompletionAssistantMessageParam,
    )


class Chat(Widget):
    BINDINGS = [
        Binding("escape", "close", "Close", key_display="esc"),
        Binding("shift+down", "scroll_container_down", show=False),
        Binding("shift+up", "scroll_container_up", show=False),
        Binding(
            key="g",
            action="focus_first_message",
            description="First message",
            key_display="g",
            show=False,
        ),
        Binding(
            key="G",
            action="focus_latest_message",
            description="Latest message",
            show=False,
        ),
        Binding(key="f2", action="details", description="Chat info"),
    ]

    allow_input_submit = reactive(True)
    """Used to lock the chat input while the agent is responding."""

    def __init__(self, chat_data: ChatData) -> None:
        super().__init__()
        self.chat_data = chat_data
        self.elia = cast("Elia", self.app)
        self.model = get_model_by_name(chat_data.model_name, self.elia.launch_config)

    @dataclass
    class AgentResponseStarted(Message):
        pass

    @dataclass
    class AgentResponseComplete(Message):
        chat_id: int | None
        message: ChatMessage
        chatbox: Chatbox

    @dataclass
    class FirstMessageSent(Message):
        chat_data: ChatData

    @dataclass
    class UserMessageSubmitted(Message):
        chat_id: int
        message: ChatMessage

    def compose(self) -> ComposeResult:
        yield ChatHeader(chat=self.chat_data, model=self.model)

        with VerticalScroll(id="chat-container") as vertical_scroll:
            vertical_scroll.can_focus = False

        yield PromptInput(id="prompt")
        yield AgentIsTyping()

    async def on_mount(self, _: events.Mount) -> None:
        """
        When the component is mounted, we need to check if there is a new chat to start
        """
        await self.load_chat(self.chat_data)

        # TODO - The code below shouldn't be required.
        #  Seems like a Textual bug.
        self.set_timer(
            0.05,
            callback=lambda: self.chat_container.scroll_end(animate=False, force=True),
        )

    @property
    def chat_container(self) -> VerticalScroll:
        return self.query_one("#chat-container", VerticalScroll)

    @property
    def is_empty(self) -> bool:
        """True if the conversation is empty, False otherwise."""
        return len(self.chat_data.messages) == 1  # Contains system message at first.

    def scroll_to_latest_message(self):
        container = self.chat_container
        container.refresh()
        container.scroll_end(animate=False, force=True)

    def key_d(self):
        print(self.chat_container.scroll_y)
        print(self.chat_container.max_scroll_y)

    async def new_user_message(self, content: str) -> None:
        log.debug(f"User message submitted in chat {self.chat_data.id!r}: {content!r}")
        now_utc = datetime.datetime.now(datetime.UTC)
        user_message: ChatCompletionUserMessageParam = {
            "content": content,
            "role": "user",
        }
        user_chat_message = ChatMessage(
            user_message, now_utc, self.chat_data.model_name
        )
        self.chat_data.messages.append(user_chat_message)
        await ChatsManager.add_message_to_chat(
            chat_id=self.chat_data.id, message=user_chat_message
        )

        self.post_message(
            Chat.UserMessageSubmitted(
                chat_id=self.chat_data.id, message=user_chat_message
            )
        )
        user_message_chatbox = Chatbox(user_chat_message, self.chat_data.model_name)

        assert (
            self.chat_container is not None
        ), "Textual has mounted container at this point in the lifecycle."

        await self.chat_container.mount(user_message_chatbox)
        self.scroll_to_latest_message()
        self.stream_agent_response()

    @work
    async def stream_agent_response(self) -> None:
        log.debug(
            f"Creating streaming response with model {self.chat_data.model_name!r}"
        )
        model: EliaChatModel = get_model_by_name(
            self.chat_data.model_name, self.elia.launch_config
        )

        from litellm import ModelResponse, acompletion
        from litellm.utils import trim_messages

        raw_messages = [message.message for message in self.chat_data.messages]
        messages: list[ChatCompletionUserMessageParam] = trim_messages(
            raw_messages, model.name
        )  # type: ignore
        response = await acompletion(
            messages=messages,
            stream=True,
            model=model.name,
            temperature=model.temperature,
            max_retries=model.max_retries,
        )
        ai_message: ChatCompletionAssistantMessageParam = {
            "content": "",
            "role": "assistant",
        }
        now = datetime.datetime.now(datetime.UTC)
        message = ChatMessage(message=ai_message, model=model.name, timestamp=now)

        assert self.chat_data.model_name is not None
        response_chatbox = Chatbox(
            message=message,
            model_name=self.chat_data.model_name,
            classes="response-in-progress",
        )
        assert (
            self.chat_container is not None
        ), "Textual has mounted container at this point in the lifecycle."

        try:
            chunk_count = 0
            async for chunk in response:
                chunk = cast(ModelResponse, chunk)
                response_chatbox.border_title = "Agent is responding..."

                if chunk_count == 0:
                    self.post_message(self.AgentResponseStarted())
                    await self.chat_container.mount(response_chatbox)

                chunk_content = chunk.choices[0].delta.content
                if isinstance(chunk_content, str):
                    response_chatbox.append_chunk(chunk_content)
                else:
                    break

                scroll_y = self.chat_container.scroll_y
                max_scroll_y = self.chat_container.max_scroll_y
                if scroll_y in range(max_scroll_y - 3, max_scroll_y + 1):
                    self.chat_container.scroll_end(animate=False)

                chunk_count += 1
        except Exception:
            self.notify(
                "There was a problem using this model. "
                "Please check your configuration file.",
                title="Error",
                severity="error",
                timeout=15,
            )
        else:
            self.post_message(
                self.AgentResponseComplete(
                    chat_id=self.chat_data.id,
                    message=response_chatbox.message,
                    chatbox=response_chatbox,
                )
            )

    @on(AgentResponseComplete)
    def agent_finished_responding(self, event: AgentResponseComplete) -> None:
        # Ensure the thread is updated with the message from the agent
        self.chat_data.messages.append(event.message)
        event.chatbox.border_title = "Agent"
        event.chatbox.remove_class("response-in-progress")

    @on(PromptInput.PromptSubmitted)
    async def user_chat_message_submitted(
        self, event: PromptInput.PromptSubmitted
    ) -> None:
        if self.allow_input_submit is True:
            user_message = event.text
            await self.new_user_message(user_message)
            event.prompt_input.clear()

    @on(PromptInput.CursorEscapingTop)
    async def on_cursor_up_from_prompt(self) -> None:
        self.focus_latest_message()

    def get_latest_chatbox(self) -> Chatbox:
        return self.query(Chatbox).last()

    def focus_latest_message(self) -> None:
        try:
            self.get_latest_chatbox().focus()
        except NoMatches:
            pass

    def action_focus_latest_message(self) -> None:
        self.focus_latest_message()

    def action_focus_first_message(self) -> None:
        try:
            self.query(Chatbox).first().focus()
        except NoMatches:
            pass

    def action_scroll_container_up(self) -> None:
        if self.chat_container:
            self.chat_container.scroll_up()

    def action_scroll_container_down(self) -> None:
        if self.chat_container:
            self.chat_container.scroll_down()

    async def action_details(self) -> None:
        await self.app.push_screen(ChatDetails(self.chat_data))

    async def load_chat(self, chat_data: ChatData) -> None:
        assert self.chat_container is not None
        chatboxes = [
            Chatbox(chat_message, self.chat_data.model_name)
            for chat_message in self.chat_data.non_system_messages
        ]
        await self.chat_container.mount_all(chatboxes)
        self.chat_container.scroll_end(animate=False, force=True)
        chat_header = self.query_one(ChatHeader)
        chat_header.update_header(
            chat=chat_data,
            model=get_model_by_name(chat_data.model_name, self.elia.launch_config),
        )

        # If the last message didn't receive a response, try again.
        messages = chat_data.messages
        if messages and messages[-1].message["role"] == "user":
            self.stream_agent_response()

    def action_close(self) -> None:
        self.app.clear_notifications()
        self.app.pop_screen()
