# combine

`combine.py` merges files from multiple directories into a single text file based on a configuration file.

## Configuration format

```
#SETTINGS
RECURSIVE: TRUE
SEARCH MODE: SIMPLE FILE EXTENSION
SEARCH QUERY: txt;md;

#1:ROOT
SEARCH: /documents
IGNORE: photos
```

**SETTINGS** can appear anywhere in the file. Options:

- `RECURSIVE` – search subdirectories (`TRUE`/`FALSE`).
- `SEARCH MODE` – `SIMPLE FILE EXTENSION` or `REGEX`.
- `SEARCH QUERY` – list of file extensions separated by `;` (the dot is optional) when using simple mode, or a regex pattern when using regex mode.

Each numbered section defines a search location. Add `:ROOT` to resolve the `SEARCH` path relative to the current working directory. Within a section:

- `SEARCH` – directory to scan.
- `IGNORE` – `;` separated list of directories or files to ignore.

## Usage

```
python combine.py path/to/config.txt
```

The script saves the combined output in `./combined-files` by default. Use `-o` to specify a different directory.
Add `-t`/`--try-output` to preview the combined content without creating a file. When this option is used a file named `folders.txt` is created in the chosen output directory listing all folders that contained processed files.
