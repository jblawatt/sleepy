

import vlc


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

    def set_volumne(value: int):
        print("SET VOLUME %s" % value)

    def fade_out(self, seconds: int):
        print("FADE OUT %s" % seconds)


class VLCPlayer(PlayerBase):

    _player: vlc.MediaPlayer = None
    _volume: int = 100
    _url: str = "http://wdr-1live-live.icecast.wdr.de/wdr/1live/live/mp3/128/stream.mp3"

    def __init__(self, volume=100):
        self._player = vlc.MediaPlayer(self._url)
        self._volume = volume

    def play(self, volume=None):
        self._player.play()
        v = self._volume if volume is None else volumne
        self._player.audio_set_volume(v)

    def stop(self):
        self._player.stop()

    def set_volume(self, value: int):
        self._player.audio_set_volume(value)

    def fade_out(self, seconds):
        self._player.audio_set_volume(0)
