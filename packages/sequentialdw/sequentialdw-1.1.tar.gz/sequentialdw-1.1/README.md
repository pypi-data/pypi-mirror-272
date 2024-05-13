## sequentialdw

Package to help myself scrapping website files automatically with only one functions:
```py
seqdownload(base_url, start_index, end_index, custom_iterator, file_extension, output_folder)
```

## Usage

`pip install sequentialdw` 

Then import the package as example:
```py
import sequentialdw

seqdownload("https://example.com/scripts/python", 0, 100, "", "py", "output")
```
##