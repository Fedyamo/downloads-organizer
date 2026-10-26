from pathlib import Path

DOWNLOADS_FOLDER = Path.home() / 'Downloads'

FILE_CATEGORIES = {
    'Documents': {'.doc', '.docx', '.pdf', '.txt', '.md', '.odt'},
    'Images': {'.png', '.jpg', '.jpeg', '.svg'},
    'Videos': {'.mp4', '.m4v', '.webm'},
    'Torrents': {'.torrent'},
    'Apps': {'.exe', '.app'},
    'Archives': {'.zip', '.7z', '.rar'},
    'Excel': {'.xlsx', '.xls', '.csv', '.ods'},
    'Presentations': {'.pptx'},
    'Books': {'.epub', '.fb2'},
    'Fonts': {'.ttf'},
    'Music': {'.mp3', '.wav', '.m4a'},
}