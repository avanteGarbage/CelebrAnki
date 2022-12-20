from PyQt5.QtWidgets import QFileDialog, QAction
from aqt.sound import AVPlayer, play, clearAudioQueue
from aqt import gui_hooks, tr, qconnect
import os
from aqt import mw

addon_path = os.path.dirname(__file__)
user_files = os.path.join(addon_path, "user_files")
config = mw.addonManager.getConfig(__name__)

if config["sound"]:
    sound_file = config["sound"]
else:
    sound_file = os.path.join(user_files, "nyt.mp3")
    setting = {"sound": sound_file}
    mw.addonManager.writeConfig(__name__, setting)


def myfunc():  # FIXME: addons21\978869609\__init__.py:21:to avoid memory leaks, pass an appropriate parent to progress.timer() or use progress.single_shot()
    clearAudioQueue()
    mw.progress.timer(
        1, lambda: play(sound_file), False
    )


gui_hooks.reviewer_will_end.append(myfunc)


def _play_tags(self, tags):
    self._enqueued = tags[:]
    if self.interrupt_current_audio and False:
        self._stop_if_playing()
    self._play_next_if_idle()


AVPlayer.play_tags = _play_tags


def updateSound():
    global sound_file, config
    file_name = QFileDialog.getOpenFileName(mw, "Change sound", user_files, "Sound Files (*.wav *.mp3 *.mp4)")
    if file_name != sound_file:
        sound_file = file_name[0]
        setting = {"sound": sound_file}
        mw.addonManager.writeConfig(__name__, setting)
        gui_hooks.reviewer_will_end.remove(myfunc)
        gui_hooks.reviewer_will_end.append(myfunc)


action = QAction("Change completion jingle")
qconnect(action.triggered, updateSound)
mw.form.menuTools.addAction(action)
