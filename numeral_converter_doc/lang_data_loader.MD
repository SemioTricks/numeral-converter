# Module `lang_data_loader.py`
> Path: `numeral_converter/lang_data_loader.py`
`__NAME_ENV_STDL` = "numeral_converter"
`NUMERAL_TREE`: Dict[str, Any] = dict()
`NUMERAL_DATA`: Dict[str, pd.DataFrame] = dict()
## Function  `get_available_languages`
```text
Check available languages
```
        
#### Declared returns: `List[str]`
## Function  `load_numeral_data`
```text
Loads language `lang` data
```
        
### Argument(s)
+ `lang`: str - language identifier
:Example:
>>> from numeral_converter import load_numeral_data
>>> load_numeral_data('uk')
## Function  `check_numeral_data_load`
### Argument(s)
+ `lang` - empty doc string
## Function  `__read_language_data`
### Argument(s)
+ `filename`: Path - empty doc string
#### Declared returns: `pd.DataFrame`
## Function  `__build_numeral_tree`
### Argument(s)
+ `df`: pd.DataFrame - empty doc string
#### Declared returns: `FuzzyMultiDict`
## Function  `__is_loaded`
### Argument(s)
+ `lang`: str - empty doc string
## Function  `__is_available`
### Argument(s)
+ `lang`: str - empty doc string
#### Declared returns: `bool`
## Function  `__update_numeral_word_value`
### Argument(s)
+ `x` - empty doc string
+ `y` - empty doc string