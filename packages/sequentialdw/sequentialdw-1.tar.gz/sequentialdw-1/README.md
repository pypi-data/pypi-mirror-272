## sequentialdw

Package to help myself scrapping website files automatically with only one functions:
```py
seqdownload(base_url, start_index, end_index, custom_iterator, file_extension, output_folder)
```

## Usage
Example of usage
```py
import sequentialdw

seqdownload("https://example.com/scripts/python", 0, 100, "", "py", "output")
```
##