# Module `numeral_converter.py`
> Path: `numeral_converter/numeral_converter.py`
`NumberItem` = namedtuple('NumberItem', 'value order scale')
`NumeralWord` = namedtuple('NumeralWord', 'default alt')
`logger` = logging.getLogger(__name__)
## Function  `numeral2int`
```text
Converts input numeral in language `lang` into integer value
To find out the order (log10(n)) of the maximum number that can be converted
by the module use `maximum_number_order_to_convert()`
```
        
### Argument(s)
+ `numeral`: str - input numeral in language `lang`
+ `lang`: str - language identifier;
to find out the list of available languages, use `get_available_languages()`
#### Declared returns: `Optional[int]`
## Function  `int2numeral`
```text
Converts input integer number into a numeral in language `lang`
into a morphological form given by the argument-parameters
To find out the order (log10(n)) of the maximum number that can be converted
by the module use `maximum_number_order_to_convert()`
Possible argument-parameters and their possible values:
- "case": nominative', 'genetive', 'dative', 'instrumental', 'accusative'
or 'prepositional';
- "num_class": 'ordinal', 'cardinal' or 'collective';
- "gender": 'masculine', 'feminine' or 'neuter';
- "number": 'plural' or 'singular'
```
        
### Argument(s)
+ `value`: int - input integer value
+ `lang`: str - language identifier;
to find out the list of available languages, use `get_available_languages()`
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
+ `lang`: str - empty doc string
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
## Function  `preprocess_numeral`
### Argument(s)
+ `numeral`: str - empty doc string
+ `lang`: str - empty doc string
#### Declared returns: `str`
## Function  `__delete_ordinal_from_numeral_word_info`
### Argument(s)
+ `number_word_info`: List[Dict[str, Any]] - empty doc string
#### Declared returns: `List[Dict[str, Any]]`
## Function  `__check_correct_order`
### Argument(s)
+ `number_items`: List[NumberItem] - empty doc string
+ `start`: int - empty doc string
+ `end`: int - empty doc string
+ `inner_order`: Optional[int] - empty doc string
## Function  `__search_block`
### Argument(s)
+ `number_items` - empty doc string
+ `start` - empty doc string
+ `num_block_order` - empty doc string
## Function  `__check_number_is_correct_scale`
### Argument(s)
+ `number_items` - empty doc string
+ `i_number` - empty doc string
+ `int_value` - empty doc string
## Function  `__kwargs2str`
### Argument(s)
+ `value` - empty doc string
+ `kwargs` - empty doc string
## Function  `__define_morph_number`
### Argument(s)
+ `global_number`: str - empty doc string
+ `number_items`: List[NumberItem] - empty doc string
+ `i`: int - empty doc string
#### Declared returns: `str`
## Function  `__define_morph_case`
### Argument(s)
+ `global_case` - empty doc string
+ `number_items` - empty doc string
+ `i` - empty doc string
+ `global_num_class` - empty doc string
## Function  `__define_morph_gender`
### Argument(s)
+ `number_items` - empty doc string
+ `i` - empty doc string