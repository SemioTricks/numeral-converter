# Module `constants.py`
> Path: `numeral_converter/constants.py`
`DEFAULT_MORPH`: Dict[str, Any] = OrderedDict([('case', 'nominative'), ('num_class', 'cardinal'), ('number', 'singular'), ('gender', 'masculine')])
`MORPH_FORMS`: Dict[str, Any] = {
            "case": ("accusative", "dative", "genetive", "instrumental", "nominative", "prepositional"),
"num_class": ("cardinal", "collective", "ordinal"),
"gender": ("feminine", "masculine", "neuter"),
"number": ("plural", "singular")
            }
`REGEX_PATTERN_WORDS` = re.compile("[a-zA-Zа-яА-ЯїЇґҐєЄёЁіІ'’]+")