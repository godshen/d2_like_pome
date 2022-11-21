import json
import aiohttp
from typing import Dict, List
from botpy.types.message import ArkObj, ArkObjKv


async def create_ark_obj_list(weather_dict) -> List[ArkObj]:
    obj_list = [
        ArkObj(obj_kv=[
            ArkObjKv(key="desc", value=
                            weather_dict['result']['citynm'] + " " +
                            weather_dict['result']['weather'] + " " +
                            weather_dict['result']['days'] + " " +
                            weather_dict['result']['week'])
            ]
        ),
        ArkObj(obj_kv=[ArkObjKv(key="desc", value="当日温度区间：" + weather_dict['result']['temperature'])]),
        ArkObj(obj_kv=[ArkObjKv(key="desc", value="当前温度：" + weather_dict['result']['temperature_curr'])]),
        ArkObj(obj_kv=[ArkObjKv(key="desc", value="当前湿度：" + weather_dict['result']['humidity'])])
    ]
    return obj_list


async def get_weather(city_name: str) -> Dict:
    """
    获取天气信息
    :return: 返回天气数据的json对象
    """
    weather_api_url = "http://api.k780.com/?app=weather.today&cityNm=" + \
                      city_name + \
                      "&appkey=%s&sign=%s&format=%s" % \
                      ("10003", "b59bc3ef6191eb9f747dd4e83c99f2a4", "json")
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=weather_api_url,
                timeout=5,
        ) as resp:
            content = await resp.text()
            content_json_obj = json.loads(content)
            return content_json_obj
