import click
import docx_code_walker.file_handler as fh

@click.command()
@click.argument("path", required=True, type=click.Path(file_okay=True, dir_okay=True, readable=True, exists=True), nargs=-1)
@click.option("-p", "--preserve-directory", type=bool, is_flag=True, help="Сохранять имя папки при выводе пути к файлу")
def cli(path: click.Path, preserve_directory: bool):
  """Простая программа для формирования docx документа из списка файлов
  
  Пригодится для оформления листинга кода в лабораторных, курсовых работах, дипломах и т.д.
  """
  for entry in path:
    process_entry(entry, preserve_directory)

def process_entry(entry: str, preserve_directory: bool):
  for path, name in fh.iterate_files(entry, preserve_directory):
    print("Обработка файла: ", name)