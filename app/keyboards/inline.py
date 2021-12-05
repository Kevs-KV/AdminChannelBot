from aiogram.utils.callback_data import CallbackData

from app.utils.markup_constructor import InlineMarkupConstructor


class ExampleInlineKb(InlineMarkupConstructor):
    callback_data = CallbackData('test', 'number')

    def get(self):
        schema = [3, 2, 1]
        actions = [
            {'text': '1', 'callback_data': self.callback_data.new('1')},
            {'text': '2', 'callback_data': self.callback_data.new('2')},
            {'text': '3', 'callback_data': '3'},
            {'text': '4', 'callback_data': self.callback_data.new('4')},
            {'text': '5', 'callback_data': (self.callback_data, '5')},
            {'text': '6', 'callback_data': '6'},
        ]
        return self.markup(actions, schema)


class CancelKb(InlineMarkupConstructor):

    def get(self):
        schema = [1]
        actions = [
            {'text': 'Отмена', 'callback_data': 'cancel'},
        ]
        return self.markup(actions, schema)


class ChannelUserMarkup(InlineMarkupConstructor):

    def __init__(self, user, bot):
        super().__init__()
        self.user = user
        self.bot = bot

    async def get(self):
        channels_user = self.user.channels
        print(channels_user)
        schema = [1]
        actions = []
        for channel in channels_user:
            channel_info = await self.bot.get_chat(chat_id=channel)
            actions.append({'text': channel_info["title"], 'url': channel_info["invite_link"]})

        return self.markup(actions, schema)


class ConfirmationMarkup(InlineMarkupConstructor):
    callback_data = CallbackData("confirmation", "agreement")

    async def get(self):
        schema = [2]
        actions = [{'text': 'Да', "callback_data": self.callback_data.new('yes')},
                   {'text': 'Нет', "callback_data": self.callback_data.new('no')}]

        return self.markup(actions, schema)


class ChoiceChannelForPost(InlineMarkupConstructor):
    callback_data = CallbackData("id", 'value')

    def __init__(self, user, bot):
        super().__init__()
        self.user = user
        self.bot = bot

    async def get(self):
        channels_user = self.user.channels
        schema = []
        actions = []
        for channel in channels_user:
            channel_info = await self.bot.get_chat(chat_id=channel)
            title = channel_info["title"]
            id = str(channel_info["id"])
            actions.append({'text': title, "callback_data": self.callback_data.new(id)})
            schema.append(1)

        return self.markup(actions, schema)


class TaskChannelMarkup(InlineMarkupConstructor):
    callback_data = CallbackData('id', 'value')

    def __init__(self, user, bot):
        super().__init__()
        self.user = user
        self.bot = bot

    async def get(self):
        try:
            tasks_user = self.user.tasks
            schema = []
            actions = []
            for task in tasks_user:
                title_channel, channel_id, message_id, from_chat_id, data_time = tasks_user[task]
                actions.append(
                    {'text': f'{title_channel} {data_time}', "callback_data": self.callback_data.new(task)})
                schema.append(1)
            return self.markup(actions, schema)
        except ValueError:
            return None


class ActionTaskChannel(InlineMarkupConstructor):
    callback_data = CallbackData('id', 'value')

    def get(self):
        schema = [1, 1, 1]
        actions = [
            {'text': 'Отмена', "callback_data": self.callback_data.new('Отмена')},
            {'text': 'Удалить', "callback_data": self.callback_data.new('Удалить')},
            {'text': 'Изменить время', "callback_data": self.callback_data.new('Изменить время')}]

        return self.markup(actions, schema)


class ChoiceLanguageUser(InlineMarkupConstructor):
    callback_data = CallbackData('id', 'language')

    def get(self):
        schema = [1, 1]

        actions = [
            {'text': 'ru', 'callback_data': self.callback_data.new('ru')},
            {'text': 'en', 'callback_data': self.callback_data.new('en')},
        ]
        return self.markup(actions, schema)
