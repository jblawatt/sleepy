
class EndlessIterator:

    actions = ()
    _current = 0

    def __init__(self, *actions):
        self.actions = actions

    def __iter__(self):
        # FIXME: Das kann so nicht ismmten
        raise NotImplementedError()
        while True:
            for i in self.actions:
                yield self.__next__()

    def __next__(self):
        """
        implements the iteration interface
        with __next__. return next or first
        value from the list of actions.
        """
        if len(self.actions) == 0:
            raise StopIteration()
        c = self._current
        self._current += 1
        try:
            return self.actions[c]
        except IndexError:
            self._current = 1
            return self.actions[0]

    def current(self):
        try:
            return self.actions[self._current - 1]
        except IndexError:
            return self.actions[0]

    def next(self):
        """
        returns the next value in iteratin.
        """
        try:
            return self.actions[self._current]
        except IndexError:
            return self.actions[0]
