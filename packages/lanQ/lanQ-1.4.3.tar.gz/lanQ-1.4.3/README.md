# lanQ v1.2

English | [简体中文](README_ZH.md)

Language quality evaluation tool.

## Run it

Clone the project into your environment.

```
git clone ssh://git@gitlab.pjlab.org.cn:1122/qa/lanq.git
```

Install the requirement packages.

```
pip install -r requirements.txt
```

Add the test data file `test_data.json` into `data/predictions` directory.  
Then execute `main.py` with parameter `-i`.

```
python main.py -i test_data.json
```

You will get the result file `data_predictions_test_data.json` in `data/results`.

If you want to test files in directory, you just need to change to file name to directory name in `data/predictions`, such as:

```
python main.py -i directory_name
```

## Data format

There are 2 data format supported.  
One is model type, contain `id`, `prompt` and `prediction` keys, as follows:  

```
{"id": "0", "prompt": "how old are you?", "prediction": "I am 8 years old."}
```

Another is data type, have `id` and `content` keys, such as:

```
{"id":"Bl1b6P41SlcCHv8gfhLy","content":"秦始皇嬴政，从此结束了贵族王侯专政的王国时代，进入了君主专制的帝国时代。"}
```

No matter what data format is, each line of data is `json` type and each data file only has one format data.   
Besides, data exits in data file with `jsonline` style, refering to `test_data1.json` or `test_data2.json`.

## Reading result

The file in `data/results` directory has format as follows:

```
{
    "score": 50.0,
    "num_good": 1,
    "num_bad": 1,
    "total": 2,
    "ERROR_RULE_COLON_END": {
        "count": 1,
        "ratio": 0.5,
        "detail": [
            {
                "id": "0",
                "error_reason": "冒号结尾"
            }
        ]
    },
}
```

key name | description
-|-
`score` | `num_good` / `total`, means the quality of data.  
`num_good` | the count of good data.  
`num_bad` | the count of bad data, which has some error.  
`total` | the count of all data.  
`ERROR_RULE_COLON_END` | the error name.  
`count` | the number of error appearance.    
`ratio` | `count` / `total`, means the ratio of error appearance.  
`detail` | the information of error.  
`id` | the data id with error.  
`error_reason` | the reason why judge the data has error. 

## How to Use

First, you should install the package.

```
pip install lanQ
```

After installing the tool in python environment, wo can import it in our project as follows.

```
from lanQ_rule import common_rule
```

At this time, we can use all functions in `common_rule.py`. The parameter `content` is must `string` type, such as:

```
common_bracket_unmatch(content)
```

We will get a result, which is a json type and has a key `error_status`.  
If `error_status` is `True`, which means content has problem, the result will have other 2 keys: `error_type` and `error_reason`, for example:  

```
{
   'error_status': True, 
   'error_type': 'ERROR_RULE_COLON_END', 
   'error_reason': '冒号结尾'
}
```

## Upload 

Update the version number in `setup.py`

```
setup(
    name="lanQ",
    version="x.y",
    ...
)
```

Make a .tar file for using in other project. 
You will get a .tar file in `lanQ/dist/`

```
python setup.py sdist
```

Upload the .tar file to Internet.

```
twine upload dist/lanQ-x.y.tar.gz
```

## Summary of Quality Functions

The Category in below table is the same name `.py` file in `lanQ/lanQ_rule/` path.  
Function's name are arranged in alphabetical order.

Function Name | Error Rule | Description                                             | Category 
-|-|---------------------------------------------------------|----------
common_anti_crawler_zh | ERROR_CRAWL_ANTI | check weather the content contains anti crawl text |  common  
common_bracket_unmatch | ERROR_BRACKET_UNMATCH | check whether bracket is matches                        | common   
common_chaos_en | ERROR_CHAOS_EN | check whether content has English messy code            | common   
common_chaos_symbol |ERROR_CHAOS_SYMBOL | check whether content has a lot of meaningless words    | common   
common_chaos_zh | ERROR_CHAOS_ZH | check whether content has Chinese messy code            | common   
common_check_photo | ERROR_CHECK_PHOTO | check whether content has photo | common 
common_colon_end | ERROR_RULE_COLON_END | check whether the last char is ':'                      | common   
common_content_null | ERROR_CONTENT_NULL | check whether content is null | common   
common_doc_repeat | ERROR_DOC_REPEAT | check whether content repeats                           | common   
common_ellipsis_ratio | ERROR_ELLIPSIS_RATIO |  check whether ratio of lines end with ellipsis is bigger than 75% | common 
common_emoj_characters | ERROR_EMOJ_CHAR | check whether content contains emoji charactors | common 
common_enter_more | ERROR_ENTER_MORE | check whether content has more than 8 continious enter | common   
common_enter_ratio_more | ERROR_ENTER_RATIO_MORE | check whether enter / content is more than 25% | common   
common_html_entity | ERROR_HTML_ENTITY | check whether content has html entity | common 
common_img_html_tag | ERROR_IMG_HTML_TAG | check whether content has img tag or html tag | common 
common_invalid_web | ERROR_INVALID_WEB | check whether the content is invalid | common  
common_invisible_char | ERROR_INVISIBLE_CHAR | check whether content has invisible char | common 
common_joint_special_symbol | ERROR_JOINT_SPECIAL_SYMBOL | check if there are special symbols composed of multiple symbols spliced together | common 
common_language_mixed | ERROR_LANGUAGE_MIXED | check whether content is mixed in Chinese and English   | common   
common_license_key | ERROR_LICENSE_KEY | check if the content contains license key| common 
common_no_punc | ERROR_NO_PUNC | check whether content has paragraph without punctuations | common   
common_space_more | ERROR_SPACE_MORE | check whether content has more than 500 space | common   
common_special_character | ERROR_SPECIAL_CHARACTER | check whether special char in content, such as '�'      | common   
common_special_mark | ERROR_SPECIAL_MARK | check if the content contains special mark | common |1.2
common_unconverted_symbol | ERROR_UNCONVERTED_SYMBOL | check if the content contains special symbols for conversion failure | common 
common_underscore_length | ERROR_UNDERSCORE_LENGTH | check whether the content contains underscores whose length is longer than 15 | common 
common_url_only | ERROR_URL_ONLY | check whether content is all urls | common   
common_word_stuck | ERROR_WORD_STUCK | check whether words are stuck | common   
model_advertisement | ERROR_ADVERTISEMENT | check whether content has model advertisement | model    
model_watermark | ERROR_WATERMARK | check whether content has watermark | model    
prompt_chinese_produce_english | ERROR_CHINESE_PRODUCE_ENGLISH | check whether chinese prompt produce english prediction | prompt   
prompt_english_produce_chinese | ERROR_ENGLISH_PRODUCE_CHINESE | check whether english prompt produce chinese prediction | prompt   

## RoadMap
 - 1.6:
   - add benchmark for rules
 - 1.5:
   - add convert for different data type
 - 1.4:
   - add config of functions

## Release Notes
 - 1.3:
   - reorganize `config.py`, let user can configure
   - add error ratio
   - `main.py` and `convert` support input directory
 - 1.2:
   - add v1.2 rules
   - update `main.py` and `config` module, use callable type to organize functions
   - add convert folder, support stringline type
   - `readme` add usage and data type
 - 1.1:
   - add `base.py` contain base functions
   - sort functions by alphabetic order
 - 1.0:   
   - add 1.0 functions
   - add common_rule module
   - add model_rule module 
   - add prompt_rule module
   - add convert function
   - add `main.py`