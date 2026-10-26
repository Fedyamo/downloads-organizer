from pathlib import Path
from organaizer import DownloadsOrganaizer
from logger_setup import setup_logger


def main():
    logger = setup_logger()
    logger.info('Приложение "Умный организатор Downloads" запущено')

    organaizer = DownloadsOrganaizer(Path.home() / 'Downloads', logger=logger)
    stats = organaizer.organaize()

    print('\n' + '=' * 60)
    print('РЕЗУЛЬТАТЫ:')
    print(f'  Обработано: {stats["total_files"]} файлов')
    print(f'  Перемещено: {stats["moved_files"]} файлов')
    if stats['errors']:
        print(f'  Ошибок: {stats["errors"]}')
    print('=' * 60)


if __name__ == '__main__':
    main()
