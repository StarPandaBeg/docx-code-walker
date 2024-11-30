import os

def iterate_files(entry: str, keep_folder_name: bool = False):
  if os.path.isfile(entry):
    yield _to_file_entry(entry, os.path.dirname(entry))
    return
  for dpath, _, fnames in os.walk(entry):
    for fname in fnames:
      path = os.path.join(dpath, fname)
      yield _to_file_entry(path, entry, keep_folder_name)


def _to_file_entry(entry: str, path: str, keep_folder_name: bool = False):
  realpath = os.path.realpath(entry)
  relpath = os.path.relpath(entry, path)
  if keep_folder_name:
    rpath = os.path.realpath(path)
    dname = os.path.basename(rpath)
    relpath = os.path.join(dname, relpath)
  return (realpath, relpath)