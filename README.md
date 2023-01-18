# procPDF

A CLI tool for processing pdf files.  
Built using [PyPDF2](https://github.com/py-pdf/pypdf)

## Installation

```shell
pip install -r requirements.txt
```

## Usage

```shell
python procpdf.py <command> [option]
```

**List of Commands and Options**

- ```
  listall [-e EXTENSION]
  ```

- ```
  merge (-a | -n | -s FILENAME...| -e FILENAME...) [-o OUTPUT_FILENAME]
  ```

- ```
  encrypt FILENAME [-r]
  ```

- ```
  decrypt FILENAME [-r]
  ```

- ```
  extractImg FILENAME

  # make sure the folder *extracted_images* is empty, if exists
  ```

- ```
  compress FILENAME
  ```
  
- ```
  metadata -r FILENAME
  metadata -w FILENAME [--author AUTHOR] [--creator CREATOR] [--producer PRODUCER] 
                       [--subject SUBJECT] [--title TITLE] [--new-filename FILENAME]
  ```

Run `python procpdf.py <command> [-h]` for more details.