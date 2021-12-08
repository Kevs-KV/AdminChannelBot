from aiogram.types import KeyboardButtonPollType

from app.utils.markup_constructor import ReplyMarkupConstructor


class ExampleReplyMarkup(ReplyMarkupConstructor):

    def get(self):
        schema = [1, 2, 3, 3]
        actions = [
            {'text': '1', },
            {'text': '2', 'contact': True},
            {'text': '3', 'location': True},
            {'text': '4', 'pool': True},
            {'text': '5', 'request_contact': True},
            {'text': '6', 'request_location': True},
            {'text': '7', 'request_pool': None},
            {'text': '8', 'request_pool': "regular"},
            {'text': '9', 'request_pool': KeyboardButtonPollType("regular")},
        ]
        return self.markup(actions, schema)


class ActionTaskChannel(ReplyMarkupConstructor):

    def get(self, _):
        schema = [1, 1, 1]
        actions = [
            {'text': _('Отмена'), },
            {'text': _('Удалить'), },
            {'text': _('Изменить время'), }]

        return self.markup(actions, schema)


class CancelUserAction(ReplyMarkupConstructor):

    def get(self):
        schema = [1]
        actions = [{
            'text': 'cancel'
        }]

        return self.markup(actions, schema)
