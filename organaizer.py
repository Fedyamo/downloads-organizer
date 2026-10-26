from pathlib import Path
import shutil
import datetime
import logging
from typing import Dict, Optional

from config import FILE_CATEGORIES

class DownloadsOrganaizer:
    def __init__(self, downloads_folder: Path, logger: Optional[logging.Logger] = None):
        self.downloads_folder = downloads_folder
        # Если логгер не передали - используем "немой" логгер без хендлеров,
        # чтобы класс работал даже без явной настройки логирования (например, в тестах)
        self.logger = logger or logging.getLogger('DownloadsOrganizer')
        self.stats = {
            'total_files': 0,
            'deleted_files': 0,
            'moved_files': 0,
            'errors': 0,
        }

    def categorize_file(self, file: Path) -> str:
        suffix = file.suffix.lower()
        for category, keys in FILE_CATEGORIES.items():
            if suffix in keys:
                return category
        else:
            return 'Others'

    def get_target_folder(self, file: Path) -> Path:
        category = self.categorize_file(file)
        chislo = file.stat().st_mtime
        date = datetime.datetime.fromtimestamp(chislo)
        target = self.downloads_folder / str(date.year) / f'{date.month:02d}' / category
        return target

    def rename(self, file: Path) -> str:
        chislo = file.stat().st_mtime
        date = datetime.datetime.fromtimestamp(chislo).strftime("%Y-%m-%d")

        new_name = f'{date}_{file.stem}{file.suffix}'
        return new_name

    def move_file(self, file: Path, target_folder: Path, new_name: str) -> bool:

        try:
            target_folder.mkdir(parents=True, exist_ok=True)

            target_path = target_folder / new_name

            new_name_path = Path(new_name)
            count = 1
            while target_path.exists():
                target_path = target_folder / f'{new_name_path.stem}_{count}{new_name_path.suffix}'
                count += 1

            shutil.move(str(file), str(target_path))
            self.stats['moved_files'] += 1
            self.logger.info(f'Перемещён: {file.name} -> {target_path.relative_to(self.downloads_folder)}')
            return True
        except Exception as e:
            self.stats['errors'] += 1
            self.logger.error(f'Ошибка при перемещении {file.name}: {e}')
            return False

    def organaize(self) -> Dict[str, int]:
        self.logger.info('=' * 60)
        self.logger.info(f'Начало организации папки: {self.downloads_folder}')

        files = [file for file in self.downloads_folder.iterdir() if file.is_file()]
        self.stats['total_files'] = len(files)
        self.logger.info(f'Найдено файлов: {self.stats["total_files"]}')

        for f in files:
            target_folder = self.get_target_folder(file=f)
            new_name = self.rename(file=f)
            self.move_file(file=f, target_folder=target_folder, new_name=new_name)

        self.logger.info('Итоги организации:')
        self.logger.info(f'  Обработано: {self.stats["total_files"]}')
        self.logger.info(f'  Перемещено: {self.stats["moved_files"]}')
        self.logger.info(f'  Ошибок: {self.stats["errors"]}')
        self.logger.info('=' * 60)

        return self.stats


