import watchdog
import os
import time
import mutagen
from mutagen.id3 import ID3
from django.core.management.base import BaseCommand
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler


class FileFilterMusicEventHandler(PatternMatchingEventHandler):
    patterns = ["*.mp3", ]

    def process(self, event):
        print("Processing: ", event.src_path)
        
        str_track_name = 'unknown'
        str_artist = 'unknown'
        str_album = 'unknown'
        str_track = '00'
        try:
            obj_info = mutagen.File(event.src_path)
            str_track_name = obj_info.tags['TIT2'].text[0]
            print('Found Track Name:', str_track_name)
            str_artist = obj_info.tags['TPE1'].text[0]
            print('Found Artist:', str_artist)
            str_album = obj_info.tags['TALB'].text[0]
            print('Found Album:', str_album)
            str_track = str(int(obj_info.tags['TRCK'].text[0]))
            print('Found Track Number:', str_track)
        except BaseException:
            print(
                'Missing Information: ',
                event.src_path,
                str_artist,
                str_album,
                str_track,
                str_track_name)

        str_path = os.path.join(os.getcwd(), 'sorted', str_artist, str_album)
        str_sorted_name = os.path.join(str_path, str('%02d' % int(
            str_track)) + ' - ' + str_track_name.replace('/', '') + '.mp3')
        if not os.path.exists(str_path):
            try:
                os.makedirs(str_path)
            except BaseException:
                print('Directory Existing: ', str_path)
        if not os.path.exists(str_sorted_name):
            try:
                os.rename(event.src_path, str_sorted_name)
                print("Moved To: ", str_sorted_name)
            except BaseException:
                print("Error Moving:", event.src_path, str_sorted_name)
        else:
            os.rename(
                event.src_path,
                os.path.join(
                    os.getcwd(),
                    'sorted',
                    'duplicate',
                    os.path.basename(event.src_path)))
            print("Possible Duplicate:", event.src_path, str_sorted_name)

    def on_created(self, event):
        self.process(event)


class Command(BaseCommand):
    def handle(self, **options):
        obj_observer = Observer()
        str_path = os.path.join(os.getcwd(), 'to_sort')
        str_duplicate = os.path.join(os.getcwd(), 'sorted', 'duplicate')
        if not os.path.exists(str_path):
            os.makedirs(str_path)
            print("Made directory: ", str_path)
        if not os.path.exists(str_duplicate):
            os.makedirs(str_duplicate)
            print("Made directory: ", str_duplicate)
        obj_observer.schedule(FileFilterMusicEventHandler(), str_path)
        print("Monitoring: ", str_path)
        obj_observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            obj_observer.stop()

        obj_observer.join()
