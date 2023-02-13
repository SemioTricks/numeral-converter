# Module `text.py`
> Path: `numeral_converter/text.py`
## Function  `convert_numerical_in_text`
```text
Converts numerical string in text into integer values
```
        
### Argument(s)
+ `text`: str - input text
+ `lang`: str - input text language
+ `max_corrections`: Optional[int] - default value of maximum number of corrections
in the query key when searching for a matching dictionary key;
default = 2
+ `max_corrections_relative`: Optional[float] - default value to calculate
maximum number of corrections in the query key when searching
for a matching dictionary key; default = None
calculated as round(max_corrections_relative * token_length)
#### Declared returns: `str`