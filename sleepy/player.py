

import vlc
from sleepy import config

class PlayerBase:

    def play(self):
        pass

    def stop(self):
        pass

    def set_volumne(self, value: int):
        pass

    def fade_out(self, seconds: int):
        pass


class PlayerStub(PlayerBase):

    def play(self):
        print("PLAY")

    def stop(self):
        print("STOP")

    def set_volumne(self, value: int):
        print("SET VOLUME %s" % value)

    def fade_out(self, seconds: int):
        print("FADE OUT %s" % seconds)


class VLCPlayer(PlayerBase):

    _player: vlc.MediaPlayer = None
    _volume: int = 100
    _url: str = "song.mp3"
    # _url: str = "http://wdr-1live-live.icecast.wdr.de/wdr/1live/live/mp3/128/stream.mp3"

    def __init__(self, media_uri, volume=100):
        self._volume = volume
        self._url = media_uri

    def _ensure_player(self):
        # den player erst erstellen wenn er
        # gebraucht wird. sonst verliert er über nacht
        # beim wecker mal die verbindung bzw. die verbindung
        # muss nicht immer offen bleiben.
        if self._player is None:
            self._player = vlc.MediaPlayer(self._url)

    def play(self, volume=None):
        self._ensure_player()
        self._player.play()
        v = self._volume if volume is None else volume
        self._player.audio_set_volume(v)

    def stop(self):
        self._player.stop()
        self._player = None

    def set_volume(self, value: int):
        if self._player:
            self._player.audio_set_volume(value)

    def fade_out(self, seconds):
        if self._player:
            self._player.audio_set_volume(0)
            self._player.stop()
            self._player = None

    def is_playing(self):
        if self._player:
            return self._player.is_playing()
        return False


def player_factory(name):
    items = dict(config.get().items(name))
    module_path, player_type = items.pop('type').rsplit('.', 1)
    import importlib
    module = importlib.import_module(module_path)
    return getattr(module, player_type)(**items)

