import os
import re
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TRCK, TDRC, TXXX, ID3NoHeaderError


class MP3Tagger:
    """
    Iterate over music folders and tag mp3s by extracting the details from
    the structure of the folder and the files.
    Note: The structure has to be very specific. See example for structure info.
    E.g.
        Music Band - Album Name (year)/
            01 - First Song.mp3
            02 - Second Song.mp3
            ...
        Another Band - Different Albums/    # 2 cds
            01 - 01 - Song One.mp3          # Track number will appear as 0101
            01 - 02 - Song Two.mp3
            ...
            02 - 01 - Song One, Second CD.mp3
            02 - 02 - Song Two, Second CD.mp3
            ...
    """
    tag_fields = {
        "TIT2": TIT2,               # Track title
        "TALB": TALB,               # Album name
        "TPE1": TPE1,               # Artist
        "TRCK": TRCK,               # Track number
        "TDRC": TDRC,               # Year
        "TXXX:TRACKTOTAL": TXXX     # Other
    }
    # Regex to verify if year is appended to the end of the album name
    year_regex = re.compile(r".* \(\d{4}\)$")
    # Regex to verify if track number is prefixed by album number
    double_album_regex = re.compile(r"\d{2} - \d{2} - .*")
    # The separator between the track number and the song name
    song_split = " - "

    def run(self, root_folder):
        """
        Entry point for running the MP3Tagger
        """
        for folder in os.listdir(root_folder):
            if os.path.isdir(folder):
                self.parse_folder(os.path.join(root_folder, folder))

    def replace_metadata(self, filename, data):
        """
        Remove any previous tags from the file and write new ones
        :param str filename: The full path for the mp3 file to be tagged
        :param dict data: The tag data in the form of valid_tag_field_name:value
        """
        try:
            tags = ID3(filename)
            tags.delete()  # Remove all previous tags
        except ID3NoHeaderError:
            tags = ID3()
        for field in data:
            tags[field] = self.tag_fields[field](encoding=3, text=data[field])
        tags.save(filename)
        print(f"Updated {filename}")

    def parse_folder(self, folder_full_path):
        """
        Extract band and album names from the folder name.
        Optionally, extract the year if one can be found at the end of the folder name in parenthesis
        :param str folder_full_path: Absolute full path of the target folder
        """
        current_album_data = {}
        try:
            folder_name = os.path.split(folder_full_path)[-1]
            artist_name, album_name = folder_name.split(" - ")
            if self.year_regex.match(album_name):
                year_index = album_name.rfind("(")
                current_album_data["TDRC"] = album_name[year_index + 1: -1]
                album_name = album_name[:year_index]
            current_album_data["TALB"] = album_name
            current_album_data["TPE1"] = artist_name
            for f in os.listdir(folder_full_path):
                full_file_name = os.path.join(folder_full_path, f)
                if os.path.isfile(full_file_name) and f.endswith(".mp3"):
                    self.update_file_in_folder(folder_full_path, f, current_album_data)
            print(f"Finished parsing {folder_name}")
        except Exception as exp:
            print(f"Error parsing {folder_full_path}: {exp}")

    def update_file_in_folder(self, full_path, file_name, album_data):
        """
        Prepare the tag data with the currently available info from the folder and the filename
        :param str full_path: The path the file is located in
        :param str file_name: The name of the target file
        :param dict album_data: Data already extracted from the folder name
        """
        # Handle case where the track number is prefixed by the album number
        if self.double_album_regex.match(file_name):
            album_data["TRCK"] = "".join(file_name.split(self.song_split)[:2])
        else:
            album_data["TRCK"] = file_name.split(self.song_split)[0]
        album_data["TIT2"] = file_name[file_name.find(self.song_split) + len(self.song_split):]
        self.replace_metadata(os.path.join(full_path, file_name), album_data)


if __name__ == '__main__':
    from sys import argv
    try:
        if len(argv) == 2:
            start_folder = argv[1]
            if os.path.isdir(start_folder):
                mp3tagger = MP3Tagger()
                mp3tagger.run(os.path.dirname(__file__))
            else:
                print(f"{start_folder} isn't a valid folder to start with")
        else:
            script_name = os.path.split(__file__)[-1]
            print(f"{script_name.split('.')[0]}\n"
                  f"{MP3Tagger.__doc__}\n"
                  f"Usage:\n\tpython {script_name} /path/to/target/folder")
    except Exception as e:
        print(f"Encountered a problem: {e}")
