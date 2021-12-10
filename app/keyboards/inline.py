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

    async def get(self, _):
        schema = [2]
        actions = [{'text': _('Да'), "callback_data": self.callback_data.new('yes')},
                   {'text': _('Нет'), "callback_data": self.callback_data.new('no')}]

        return self.markup(actions, schema)


class ChoiceChannelForPost(InlineMarkupConstructor):
    callback_data = CallbackData("id", 'value')

    def __init__(self, user, bot):
        super().__init__()
        self.user = user
        self.bot = bot

    async def get(self):
        try:
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
        except ValueError:
            return None


class TaskChannelMarkup(InlineMarkupConstructor):
    callback_data = CallbackData('id', 'value')

    def __init__(self, user, bot):
        super().__init__()
        self.user = user
        self.bot = bot

    async def get(self, _):
        try:
            tasks_user = self.user.tasks
            schema = []
            actions = []
            for task in tasks_user:
                title_channel, channel_id, message_id, from_chat_id, data_time = tasks_user[task]
                hour, minute, day, month, year = data_time
                actions.append(
                    {'text': _('Канал: {} дата: {}/{}/{} в {}:{}').format(title_channel, day, month, year, hour,
                                                                          minute),
                     "callback_data": self.callback_data.new(task)})
                schema.append(1)
            return self.markup(actions, schema)
        except ValueError:
            return None


class ActionTaskChannel(InlineMarkupConstructor):
    callback_data = CallbackData('id', 'value')

    def get(self, _):
        schema = [1, 1, 1]
        actions = [
            {'text': 'Отмена', "callback_data": self.callback_data.new(_('Отмена'))},
            {'text': 'Удалить', "callback_data": self.callback_data.new(_('Удалить'))},
            {'text': 'Изменить время', "callback_data": self.callback_data.new(_('Изменить время'))}]

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
