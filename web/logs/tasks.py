import os

from celery import shared_task
from core.utils import (
    analyze_coefficient,
    analyze_regex,
    analyze_simple,
    get_datetime_from_line,
    get_ip_from_line,
)
from logs.models import LogFile


def prepare_lines(lines: list[str]) -> list[str]:
    """Подготавливает строки к анализу.

    Принимает список строк, убирает переносы и пустые строки,
    затем возвращает подготовленный список строк.
    """
    stripped_lines = map(str.strip, lines)
    non_empty_lines = [line for line in stripped_lines if line]
    return non_empty_lines


@shared_task
def analyze_log_lines(log_file_id: int, lines: list[str]) -> None:
    prepared_lines = prepare_lines(lines)
    log_file = LogFile.objects.get(id=log_file_id)
    log_file_type = log_file.type
    search_patterns = log_file_type.search_patterns.all()
    for line in prepared_lines:
        print(f'LOG FILE: {log_file} | SCAN LINE: "{line}"')
        datetime_of_line = get_datetime_from_line(line)
        ip_of_line = get_ip_from_line(line)
        for search_pattern in search_patterns:
            try:
                match search_pattern.search_type:
                    case "SIMPLE":
                        analyze_simple(
                            line, search_pattern, log_file, datetime_of_line, ip_of_line
                        )
                    case "REGEX":
                        analyze_regex(
                            line, search_pattern, log_file, datetime_of_line, ip_of_line
                        )
                    case "COEFFICIENT":
                        analyze_coefficient(
                            line, search_pattern, log_file, datetime_of_line, ip_of_line
                        )
            except Exception as e:
                print("CANT SCAN, BAD LINE, ERROR: " + str(e))
    if log_file.one_time_scan:
        log_file.one_time_scan_is_done = True
        log_file.save()


@shared_task
def read_log_files_task() -> None:
    """Анализирует лог-файлы на предмет новых строк.

    Проходится по каждому лог-файлу в поиске новых строк,
    которые будут переданы в функцию построчного анализа
    с использованием паттернов.
    """
    log_files = LogFile.objects.filter(one_time_scan=False)
    for log_file in log_files:
        with open(os.path.join("/outer", log_file.path[1:]), mode="r") as file:
            if not log_file.last_positions:
                file.seek(0, 2)
            else:
                file.seek(log_file.last_positions)
            new_lines = file.readlines()
            new_position = file.tell()
            log_file.last_positions = new_position
            log_file.save()
            analyze_log_lines.delay(log_file.id, new_lines)


@shared_task
def read_log_file_task(log_file_id: int) -> None:
    """Анализирует конкретный лог-файл на предмет новых строк.

    Проходится по каждому лог-файлу в поиске новых строк,
    которые будут переданы в функцию построчного анализа
    с использованием паттернов.
    """
    log_file = LogFile.objects.get(id=log_file_id)
    with open(os.path.join("/outer", log_file.path[1:]), mode="r") as file:
        lines = file.readlines()
        analyze_log_lines.delay(log_file.id, lines)
