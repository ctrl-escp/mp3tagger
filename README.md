# MP3Tagger
Tag MP3 files with info extracted from the file and folder structure.

## Description
Iterate over music folders and tag mp3s by extracting the details from
the structure of the folder and the files.

Note: The structure has to be very specific. See example for structure info.

### Supported Folder/Filename Structure
```    
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
```

## Usage Instructions

* Clone the project locally <br/>
  `git clone https://github.com/ctrl-escp/mp3tagger.git && cd mp3tagger`
* Install the requirements (Python 3.8+)<br/>
  `python -m pip -r requirements.txt`
* Run the script on the target folder containing the music folders you'd like to tag <br/>
`python mp3tagger.py /path/to/target/folder`
* ...
* Profit!
