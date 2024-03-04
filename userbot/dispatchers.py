from aiogram import Dispatcher


class Dispatchers:

    dps: list[Dispatcher]

    def __init__(self, dps: list[Dispatcher]) -> None:
        self.dps = dps

    def message_handler(self, *custom_filters, commands=None, regexp=None, content_types=None, state=None,
                        run_task=None, **kwargs):

        def decorator(callback):
            for dp in self.dps:
                dp.register_message_handler(callback, *custom_filters,
                                            commands=commands, regexp=regexp, content_types=content_types,
                                            state=state, run_task=run_task, **kwargs)
            return callback

        return decorator

    def callback_query_handler(self, *custom_filters, state=None, run_task=None, **kwargs):

        def decorator(callback):
            for dp in self.dps:
                dp.register_callback_query_handler(callback, *custom_filters, state=state, run_task=run_task, **kwargs)
            return callback

        return decorator
