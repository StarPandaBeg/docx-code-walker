import click
import docx_code_walker.file_handler as fh
from docx_code_walker.document import WordDocument

CONTEXT_SETTINGS = dict(
  help_option_names=['-h', '--help']
)

@click.command(
  context_settings=CONTEXT_SETTINGS,
  epilog="Больше информации Вы можете найти на странице проекта https://github.com/StarPandaBeg/docx-code-walker",
)
@click.argument("path", required=True, type=click.Path(file_okay=True, dir_okay=True, readable=True, exists=True), nargs=-1)
@click.option("-p", "--preserve-directory", type=bool, is_flag=True, help="Сохранять имя папки при выводе пути к файлу")
@click.option("-n", "--only-name", type=bool, is_flag=True, help="Сохранять только имя файла при выводе пути")
@click.option("-c", "--columns", default=2, show_default=True, help="Количество столбцов в итоговом документе")
@click.option("-e", "--encoding", default='utf-8', show_default=True, help="Кодировка файлов")
@click.option("-o", "--output", type=click.Path(file_okay=True, writable=True), default="output.docx", show_default=True, help="Итоговый файл")
@click.option("--font", type=(str, int), default=("Consolas", 7), show_default=True, help="Шрифт")
def cli(path: click.Path, preserve_directory: bool, only_name: bool, columns: int, encoding: str, output: click.Path, font: tuple[str, int]):
  """Простая программа для формирования docx документа из списка файлов
  
  Пригодится для оформления листинга кода в лабораторных, курсовых работах, дипломах и т.д.
  """
  if font[1] <= 0:
    click.echo("Неверный размер шрифта", err=True)
    return
  
  document = WordDocument(columns, font)
  for entry in path:
    process_entry(document, entry, preserve_directory, only_name, encoding)
  document.save(output)

def process_entry(document: WordDocument, entry: str, preserve_directory: bool, only_name: bool, encoding: str):
  for path, name in fh.iterate_files(entry, preserve_directory, only_name):
    print(f"Обработка файла: {click.format_filename(name)}")
    with click.open_file(path, 'r', encoding=encoding) as f:
      content = f.read().strip()
      if len(content) == 0:
        continue
      document.add_header(f"Файл {name}")
      document.add_content(content)