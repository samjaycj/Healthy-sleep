from jnius import autoclass
from random import sample, randint
from string import ascii_letters
from time import localtime, asctime, sleep
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient
import sched, time
import os

PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)
s = sched.scheduler(time.monotonic, time.sleep)
# get the MediaPlayer java class
MediaPlayer = autoclass('android.media.MediaPlayer')

# create our player
mPlayer = MediaPlayer()
soundpath=os.path.join(os.path.dirname(os.path.abspath(__file__)),'alarm.mp3')
mPlayer.setDataSource(soundpath)
mPlayer.prepare()

CLIENT = OSCClient('localhost', 3002)

def ping(alarmtime):
    'answer to ping messages'
    print(alarmtime)
    s.enter(alarmtime, 1, on_alarm)
    s.run()
    CLIENT.send_message(
        b'/message',
        [
            ''.join(sample(ascii_letters, randint(10, 20)))
            .encode('utf8'),
        ],
    )

def on_alarm():
    print("Alarm Alarm.. Wakeup Asshole")
    mPlayer.start()

def send_date():
    'send date to the application'
    CLIENT.send_message(
        b'/date',
        [asctime(localtime()).encode('utf8'), ],
    )


if __name__ == '__main__':
    SERVER = OSCThreadServer()
    SERVER.listen('localhost', port=3000, default=True)
    SERVER.bind(b'/ping', ping)
    while True:
        sleep(5)
