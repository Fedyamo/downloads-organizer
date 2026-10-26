import logging
from pathlib import Path


def setup_logger(log_file: Path = Path('downloads_organized.log')) -> logging.Logger:
    """
    Создаёт логгер с выводом в файл (все уровни) и в консоль (INFO и выше).
    """
    logger = logging.getLogger('DownloadsOrganizer')
    logger.setLevel(logging.DEBUG)

    # Защита от повторного добавления хендлеров, если setup_logger вызовут
    # несколько раз в одном процессе (например, в тестах)
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt='[%(asctime)s] %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
