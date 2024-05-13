## sequentialdw

Package to help myself scrapping website files automatically with only one functions:
```py
seqdownload(base_url, start_index, end_index, custom_iterator, file_extension, output_folder, mode, timed_out&seconds)
## MODE 1 for replacing duplicate filename, MODE 2 for ignoring the duplicate filaname
```

## Usage

`pip install sequentialdw` 

Then import the package as example:
```py
from sequentialdw import seqdownload

seqdownload("https://example.com/scripts/python", 0, 100, "", "py", "output", 1, 60)
```
##