class StartWakeAction:

    def apply(self, wake_thread):
        wake_thread.activate()

    def get_text(self):
        return 'start'


class StopWakeAction:

    def apply(self, wake_thread):
        wake_thread.deactivate()

    def get_text(self):
        return 'stop'
