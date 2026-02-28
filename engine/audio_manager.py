# engine/audio_manager.py
import os
import pygame


class AudioManager:

    _initialized = False
    _sounds = {}
    _music_playing = None

    @classmethod
    def init(cls):
        if not cls._initialized:
            pygame.mixer.init()
            cls._initialized = True

    @classmethod
    def load_sound(cls, key, file_path):
        cls.init()

        if not os.path.exists(file_path):
            print(f"[AudioManager] File not found: {file_path}")
            return

        cls._sounds[key] = pygame.mixer.Sound(file_path)

    @classmethod
    def play(cls, key, volume=1):
        if not (0.0 <= volume <= 1.0):
            raise ValueError(f"Volume must be between 0.0 and 1.0, got {volume}")
        cls.init()
        sound = cls._sounds.get(key)

        if sound is None:
            print(f"[AudioManager] Sound not loaded: {key}")
            return
        pygame.mixer.Sound.set_volume(sound, volume)
        sound.play()

    @classmethod
    def play_music(cls, file_path, volume, loops=-1, start=0.0, fade_ms=0):
        if not (0.0 <= volume <= 1.0):
            raise ValueError(f"Volume must be between 0.0 and 1.0, got {volume}")

        cls.init()

        if not os.path.exists(file_path):
            print(f"[AudioManager] Music file not found: {file_path}")
            return

        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops=loops, start=start, fade_ms=fade_ms)
        cls._music_playing = file_path

    @classmethod
    def stop_music(cls, fade_ms=0):
        if fade_ms > 0:
            pygame.mixer.music.fadeout(fade_ms)
        else:
            pygame.mixer.music.stop()
        cls._music_playing = None

    @classmethod
    def pause_music(cls):
        pygame.mixer.music.pause()

    @classmethod
    def unpause_music(cls):
        pygame.mixer.music.unpause()
