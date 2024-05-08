from lazysdk import lazyrequests
from lazysdk import lazymd5
import copy


def postback(
        token: str,
        bd_vid: str,
        new_type_list: list,
        convert_time: int = None,
        convert_value: int = None,

        deviceType=None,
        deviceId=None,
        isConvert=None,
        confidence=None,
        ext_info=None,
        theaterId=None,
        theaterShortPlayId=None,
        theaterUserId=None
):
    """
    百度回传
    :param token:
    :param bd_vid:
    :param new_type_list:
    :param convert_time: unix时间戳（精确到秒）;选填，转化类型为45、46、47、48时必填
    :param convert_value: 转化金额（单位分）;选填，回传具体商品金额有助于提升模型优化准确性（数值需大于0）
    :param confidence: 置信度，0-100数字
    参考文档：https://dev2.baidu.com/content?sceneType=0&pageId=101211&nodeId=658
    """
    post_types = list()
    for each in new_type_list:
        each_data = {
            'logidUrl': f'https://open.fanshang888.com/api/cache/receive/open_api/ad/baidu/track?&bd_vid={bd_vid}',
            'newType': each
        }
        if convert_time:
            each_data['convertTime'] = convert_time
        if convert_value:
            each_data['convertValue'] = convert_value

        if deviceType:
            each_data['deviceType'] = deviceType
        if deviceId:
            each_data['deviceId'] = deviceId
        if isConvert:
            each_data['isConvert'] = isConvert
        if confidence:
            each_data['confidence'] = confidence
        if ext_info:
            each_data['ext_info'] = ext_info
        if theaterId:
            each_data['theaterId'] = theaterId
        if theaterShortPlayId:
            each_data['theaterShortPlayId'] = theaterShortPlayId
        if theaterUserId:
            each_data['theaterUserId'] = theaterUserId

        post_types.append(
            each_data
        )
    url = 'https://ocpc.baidu.com/ocpcapi/api/uploadConvertData'
    return lazyrequests.lazy_requests(
        method='POST',
        url=url,
        json={
            'token': token,
            'conversionTypes': post_types
        },
        return_json=True,
        timeout=5
    )


def postback_flow_app_v1(
        callback_url: str,
        a_type: str = "enter_bookstore_read",
        a_value: int = 0,
        join_type: str = "ip",
        akey: str = "NTQ3MTYyNzE="
):
    """
    信息流-应用API埋码回传（v1版本）
    成功：{'error_code': 0, 'error_msg': '请求成功'}

    开发文档：
    https://dev2.baidu.com/content?sceneType=0&pageId=101213&nodeId=663&subhead=
    """
    inner_callback_url = copy.deepcopy(callback_url)  # 拷贝一份以备使用
    inner_callback_url_with_a_type = inner_callback_url.replace("{{ATYPE}}", str(a_type))  # 替换ATYPE
    inner_callback_url_with_a_type_value = inner_callback_url_with_a_type.replace("{{AVALUE}}", str(a_value))  # 替换AVALUE
    callback_url_with_join_type = f"{inner_callback_url_with_a_type_value}&join_type={join_type}"  # 增加join_type
    callback_url_with_akey = f"{callback_url_with_join_type}{akey}"  # 增加akey
    callback_url_sign = lazymd5.md5_str(content=callback_url_with_akey)  # 计算签名
    callback_url_get = f"{callback_url_with_join_type}&sign={callback_url_sign}"  # 拼接url，增加签名
    res = lazyrequests.lazy_requests(
        method="GET",
        url=callback_url_get
    )
    return res
