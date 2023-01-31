# numeral-converter

Numeral converter:
- converts an integer value into a numerator in natural language, bringing it into the form given by the arguments
- converts the numerator from natural language to integer value
- handles spelling errors


# Installation

> pip install numeral_converter

# Quickstart

```python
from numeral_converter import (
    get_available_languages, 
    load,
    numeral2int,
    int2numeral
)
get_available_languages()
# ['uk']

load('uk')

numeral2int("дві тисячі двадцять третій", lang="uk")
# 2023

numeral2int("двох тисяч двадцяти трьох", lang="uk")
# 2023

numeral2int("сто тисяч мільйонів", lang="uk")
# 100000000000

numeral2int("сто тисяч", lang="uk")
# 100000

numeral2int("три десятки", lang="uk")
# 30

numeral2int("три тисячі три сотні три десятки три", lang="uk")
# 3333

numeral2int("дви тисичи двадцить тре", lang="uk")
# 2023

numeral2int("дві тисячі двадцять три роки", lang="uk")
# ValueError('can\'t convert "роки" to integer')
        
numeral2int("три мільярди тисяча пятдесят пять мільонів", lang="uk")
# ValueError(
#     "position 1: order of 1000000000:9 is less/equal "
#     "of summary order in next group: 9")

numeral2int("три мільярди тисячний пятдесят пятий мільон", lang="uk")
# ValueError("the number in the middle of the numeral cannot be ordinal")
          
int2numeral(2023, case="nominative", num_class="quantitative")
# {
#   'numeral': 'дві тисячі двадцять три', 
#   'numeral_forms': ['дві тисячі двадцять три', ]
# }

int2numeral(
    2021, 
    case="nominative",
    gender="neuter",
    num_class="quantitative")
# {
#   'numeral': 'дві тисячі двадцять одне (одно)', 
#   'numeral_forms': [
#       'дві тисячі двадцять одне',
#       'дві тисячі двадцять одно'
#    ]
# } 

int2numeral(
    89, 
    case="prepositional", 
    num_class="quantitative")
# {
#   'numeral': 'вісімдесяти (вісімдесятьох) дев’яти (дев’ятьох)', 
#   'numeral_forms': [
#       'вісімдесяти дев’яти',
#       'вісімдесяти дев’ятьох',
#       'вісімдесятьох дев’яти',
#       'вісімдесятьох дев’ятьох'
#    ]
# }    

int2numeral(
    111212313415515, 
    case="prepositional",
    num_class="quantitative")['numeral']

# "ста одинадцяти (одинадцятьох) трильйонах двохстах дванадцяти (дванадцятьох) "
# "мільярдах трьохстах тринадцяти (тринадцятьох) мільйонах чотирьохстах "
# "п’ятнадцяти (п’ятнадцятьох) тисячах п’ятистах п’ятнадцяти (п’ятнадцятьох)"
