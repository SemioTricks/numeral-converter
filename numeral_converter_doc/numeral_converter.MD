# Module `numeral_converter.py`
> Path: `numeral_converter/numeral_converter.py`
`NumberItem` = namedtuple('NumberItem', 'value order scale')
`NumeralWord` = namedtuple('NumeralWord', 'default alt')
`logger` = logging.getLogger(__name__)
## Function  `numeral2int`
```text
Converts input numeral in language `lang` into integer value
```
        
### Argument(s)
+ `numeral`: str - input numeral in language `lang`
+ `lang`: str - language
#### Declared returns: `Optional[int]`
## Function  `int2numeral`
```text
Converts input integer number into a numeral in language `lang`
into a morphological form given by the argument-parameters:
"case": 'accusative', 'dative', 'genetive', 'instrumental', 'nominative' or
'prepositional';
"num_class": 'collective', 'ordinal' or 'quantitative';
"gender": 'feminine', 'masculine' or 'neuter';
"number": 'plural' or 'singular'.
```
        
### Argument(s)
+ `value`: int - input integer value
+ `lang`: str - language identifier
+ **`kwargs` - empty doc string
## Function  `numeral2number_items`
### Argument(s)
+ `numeral`: str - empty doc string
+ `lang`: str - empty doc string
## Function  `number_items2int`
### Argument(s)
+ `number_items`: List[NumberItem] - empty doc string
#### Declared returns: `int`
## Function  `int2number_items`
### Argument(s)
+ `number`: int - empty doc string
#### Declared returns: `List[NumberItem]`
## Function  `int2numeral_word`
### Argument(s)
+ `value`: int - empty doc string
+ `lang`: str - empty doc string
+ **`kwargs` - empty doc string
#### Declared returns: `NumeralWord`
## Function  `number_items2numeral`
### Argument(s)
+ `number_items`: List[NumberItem] - empty doc string
+ `lang`: str - empty doc string
+ **`kwargs` - empty doc string
## Function  `__check_kwargs`
### Argument(s)
+ `kwargs` - empty doc string
## Function  `__process_numbers`
### Argument(s)
+ `numbers`: List[NumeralWord] - empty doc string
+ `number_items` - empty doc string
+ `lang`: str - empty doc string
#### Declared returns: `Dict[str, Any]`
## Function  `__preprocess_numeral`
### Argument(s)
+ `numeral`: str - empty doc string
+ `lang`: str - empty doc string
#### Declared returns: `str`
## Function  `__delete_ordinal_from_numeral_word_info`
### Argument(s)
+ `number_word_info`: List[Dict[str, Any]] - empty doc string
#### Declared returns: `List[Dict[str, Any]]`