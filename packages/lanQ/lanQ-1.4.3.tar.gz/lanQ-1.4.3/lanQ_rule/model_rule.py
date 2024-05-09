import os
import sys

sys.path.append(os.path.dirname(__file__))

import lanQ_rule.config.customize as cm
from lanQ_rule.base_func.base import *
from lanQ_rule.config.const import *

def model_advertisement(content: str) -> dict:
    """check whether content has advertisement"""
    res = {'error_status': False}
    ad_list_en = ['deadlinesOrder', 'Kindly click on ORDER NOW to receive an']
    matches = re.findall('|'.join(ad_list_en), content)
    if matches:
        res["error_status"] = True
        res["error_type"] = ERROR_ADVERTISEMENT
        res['error_reason'] = matches
    return res

def model_watermark(content: str) -> dict:
    """check whether content has watermark"""
    res = {'error_status': False}
    watermark_list = cm.model_watermark['key_list']
    matches = re.findall('|'.join(watermark_list), content)
    if matches:
        res["error_status"] = True
        res["error_type"] = ERROR_WATERMARK
        res['error_reason'] = '存在水印'
    return res