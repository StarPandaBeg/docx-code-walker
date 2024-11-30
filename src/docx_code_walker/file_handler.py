import os
import ignorelib

def iterate_files(entry: str, keep_folder_name: bool = False, only_name: bool = False):
  if os.path.isfile(entry):
    yield _to_file_entry(entry, os.path.dirname(entry), only_name)
    return
  filter = _setup_ignorefilter(entry)
  for dpath, _, fnames in filter.walk():
    for fname in fnames:
      path = os.path.join(dpath, fname)
      yield _to_file_entry(path, entry, keep_folder_name, only_name)


def _to_file_entry(entry: str, path: str, keep_folder_name: bool = False, only_name: bool = False):
  realpath = os.path.realpath(entry)
  relpath = os.path.relpath(entry, path)
  if keep_folder_name:
    rpath = os.path.realpath(path)
    dname = os.path.basename(rpath)
    relpath = os.path.join(dname, relpath)
  if only_name:
    relpath = os.path.basename(relpath)
  return (realpath, relpath)

def _setup_ignorefilter(path):
  return ignorelib.IgnoreFilterManager(path, 
    ignore_file_name=".gitignore",
    global_filters=[
      ignorelib.IgnoreFilter(
        patterns=[
          ".git",
          ".gitignore",
        ]
      )
    ]
  )