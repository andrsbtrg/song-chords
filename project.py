from html.parser import HTMLParser
import requests
from colorama import init
from colorama import Fore
import argparse
from fpdf import FPDF


class SongPdfExporter(FPDF):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def write_song(self, text):
        self.add_page()
        # encoded = text.encode('ascii', 'ignore')
        # decoded = encoded.decode()
        decoded = text.replace('\u2018', ' ')
        self.set_font('helvetica', 'B', 20)
        self.write(10, decoded)
        self.output(self.path, 'F')


class HTMLSongParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cursor = []
        self.in_lyrics = False
        self.in_header = False
        self.chord_color = Fore.RED
        self.lyric_color = Fore.WHITE
        self.ignore = ['ChordName', 'ToolTipTextR']

        self.lyrics = {}
        self.sections = {}
        self.breaks = []

        self.lyric_count = 0

    def handle_starttag(self, tag, attrs):
        class_name = '_'
        for attr in attrs:
            if attr[0] == 'class':
                class_name = attr[1]
        self.cursor.append(class_name)

        if tag == 'td' and class_name == 'Lyrics':
            self.in_lyrics = True
        elif tag == 'span' and class_name == 'SectionHeader':
            self.in_header = True
        elif tag == 'table' and class_name == 'Lyrics':
            self.breaks.append(self.lyric_count)

    def handle_endtag(self, tag):
        self.cursor.pop()
        if tag == 'td' and self.in_lyrics:
            self.in_lyrics = False
            self.lyric_count += 1
        elif tag == 'span' and self.in_header:
            self.in_header = False

    def handle_data(self, data):
        if self.in_header:
            self.sections[self.lyric_count] = data
            return

        if not self.in_lyrics:
            return
        size = len(self.cursor)
        if size == 0:
            return
        current = self.cursor[size - 1]
        if current not in self.ignore:
            if self.lyric_count not in self.lyrics:
                this_chord = {'lyrics': '', 'data': ''}
            else:
                this_chord = self.lyrics[self.lyric_count]
            if current == 'Lyrics':
                this_chord['lyrics'] = data
            elif current == 'ToolTipR':
                this_chord['data'] = data
            self.lyrics[self.lyric_count] = this_chord

    def pretty_print(self):
        output = ''
        breaks = set(self.breaks)
        for key in self.lyrics:
            if key in breaks:
                output += '\n'
            if key in self.sections:
                output += f'\n\n{self.sections[key].upper()}\n\n'
            chord = self.lyrics[key]['data']
            if chord:
                output += f'{self.chord_color}[{chord}] '
            lyrics = self.lyrics[key]['lyrics']
            if lyrics:
                output += f'{self.lyric_color}{lyrics} '
        return output

    def print(self):
        self.chord_color = ''
        self.lyric_color = ''
        return self.pretty_print()


if __name__ == "__main__":
    # colorama init
    init()
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='a song url')
    parser.add_argument(
        '-o', '--output', help='output.pdf')

    args = parser.parse_args()

    song_url = args.url
    resp = requests.get(song_url)

    song_parser = HTMLSongParser()
    song_parser.feed(resp.text)
    if args.output:
        print(args.output)
        output = song_parser.print()
        exporter = SongPdfExporter(args.output)
        exporter.write_song(output)
    else:
        output = song_parser.pretty_print()
        print(output)
