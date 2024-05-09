import json
from configparser import ExtendedInterpolation
import configparser
import re
from datetime import datetime
import time
import threading
import sqlite3
import lyyddforward
import lyycfg
from lyylog import log
import lyyddsender
import lyytext
import lyyprocess
import lyyre
from collections import defaultdict, deque
import requests
import json
import os
teachers_last_msg = {}
LASTjson = last_msg = None
resource_path = r"D:/UserData/resource/ddForward"
text_rule_dict = None
text_config= None
engine, conn, session = lyycfg.con_aliyun_sqlalchemy()
number_chinese_dict = number_pinyin_dict =wss_name_chinesename_dict = None



def ocr_panddle_jd_server(img_link,server_url="http://117.72.45.252:10028/ocr", ocr_red_text=False, debug=False, timeout=10):
    """
    Perform OCR using Panddle JD server.

    Args:
    img_link (str): The image URL for OCR.
    ocr_red_text (bool): Flag to specify OCR red text. Default is False.
    debug (bool): Flag to enable debug printing. Default is False.
    timeout (int): Timeout limit for the HTTP request in seconds. Default is 10.

    Returns:
    str: The OCR text extracted from the image.
    """
    
    # Target URL

    # Data to be sent
    post_data = {"img_url": img_link}

    try:
        # Send POST request with timeout
        response = requests.post(server_url, json=post_data, timeout=timeout,verify=False)

        # Check if response is successful
        if response.status_code == 200:
            # Parse JSON response
            result = response.json()
            if debug:
                print("====ocr_panddle_jd_server====", result)
            return result.get("ocr_text", None)
        else:
            # If response is not successful, print error message
            print(f"Error: {response.status_code}{response.text}")
            return None
    except requests.exceptions.Timeout:
        print("Error: Request timed out")
        return None


def download_and_ocr(lyywin, img_url, debug=False):
    print("in process_url, img_url -= ", img_url)
    width, height = lyyre.get_img_size_from_url(img_url)
    if width > 1000 or height > 1500:
        print("图片width> 000 or height>1500像素，不识别")
        return None
    else:
        print("图片尺寸没有超过，继续ocr")
    img_filename = f"{datetime.now().microsecond}.jpg"
    try:
        response = requests.get(img_url)
    except Exception as e:
        log(f"in download&ocr,request_url_error,msg={e}. will return None as ocr result")
        return None
    if response.status_code != 200:
        log("in  download and ocr, response_code!=200")
        return None  # jsonify({"error": "Failed to download image"}), 500
    # print("response.content",response.content)
    with open(img_filename, "wb") as img_file:
        img_file.write(response.content)
    try:
        result = lyywin.paddle_local_ocr(img_filename)
        extracted_texts = []
        for line in result[0]:
            text = line[1][0]
            extracted_texts.append(text)
        text_results = "".join(extracted_texts)
        return text_results
    except Exception as e:
        return None

class TeacherMessageThrottler:
    def __init__(self):
        # 使用defaultdict来存储每个老师的消息队列
        self.messages = defaultdict(deque)

    def _cleanup(self, teacher):
        # 移除指定老师1分钟前的消息
        current_time = time.time()
        while self.messages[teacher] and current_time - self.messages[teacher][0][1] > 160:
            self.messages[teacher].popleft()

    def should_send_message(self, teacher, message):
        self._cleanup(teacher)
        # 检查指定老师的消息是否在最近1分钟内发送过
        for msg, _ in self.messages[teacher]:
            if lyytext.are_sentences_similar(msg, message):
                # if msg == message:
                return False  # 如果发送过，不再发送
        # 如果没有发送过，记录消息和当前时间戳
        self.messages[teacher].append((message, time.time()))
        return True  # 允许发送消息
throttler = TeacherMessageThrottler()  # 用来过滤同一个老师重复消息




def process_ocr(lyywin, msg_json, text_config, deny_ocr_text_patterns_list, ocr_engine, retry=True, debug=False):
    try:
        print("in process_ocr, of dd01msg, 有img字段且未在禁止ocr名单中，尝试ocr")

        ocr_result_text = download_and_ocr(lyywin, msg_json["img"], debug=True)
        print("1,ocr result =",ocr_result_text)
        if ocr_result_text is None:
            log("ocr result is None, imgurl=" + msg_json["img"])
            return
        ocr_result_text = lyyre.replace_keys_with_values(ocr_result_text, text_config.get("text_replacement", {}), debug=False)
        print("2,ocr result =",ocr_result_text)
        print(f"来自{msg_json['chinesename']}群的图片ocr结束，过滤看是否有用：，无用则直接跳过回到正常图片处理流程")

        if not lyytext.ocr_text_not_useful(ocr_result_text, deny_ocr_text_patterns_list):
            print("排除了其它不保留的OCR情况。开始处理")
            msg_json_with_ocr_text = lyytext.format_url_in_ocr_text_include_markdown_img(msg_json, ocr_result_text, debug=True)

            # lyyddforward.dd_to_db(engine, ocr_result_text, 消息中文群名, 来源群拼音,                                     msg_json['groupid'], msg_json['cmd'])

            if len(ocr_result_text) < 3 and (ocr_result_text.isascii()):
                log("---------ok ocr result--------" + ocr_result_text + ",img=" + str(msg_json))
                return
            else:
                print("<<<<OK ocr_text=", msg_json_with_ocr_text)
                return msg_json_with_ocr_text
        else:
            log("OCR_text没通过测试，")
    except Exception as e:
        return None


def Process_Data(lyywin, msg_json, all_config_dict,df_teacherlist, 来源群拼音=None, retry=True, debug=False):
    """
      3. 通用消息处理函数
    :param param1: tkinter类
    :param param2: 组pinyin
    :return: 直接处理无返回值
    """
    if debug: print("enter Process_Data function")
    if not throttler.should_send_message(msg_json.get("chinesename"), msg_json["markdown"]["text"]):
        print("==========重复信息============")
        return
    global text_rule_dict, text_config
    if text_config is None:
        text_config = all_config_dict.get("text_format")
    if text_rule_dict is None:
        text_rule_dict = all_config_dict.get("system8").get("text")

    lyywin.message_id += 1
    if debug:
        print("[" + str(lyywin.message_id) + "] : " + str(datetime.now()) + "in Process_data, msgjson=\n", json.dumps(msg_json, ensure_ascii=False))

    消息中文群名 = msg_json["chinesename"]
    来源群拼音 = msg_json["name"]

    # 群名格式化
    msg_json["chinesename"] = lyyre.replace_keys_with_values(msg_json["chinesename"], text_config.get("group_name_replacement"), debug=False)  # 去除群中文中额外字符

    # 3.2 ---------------------------------组ID/名黑名单屏蔽---------------------------------
    block_reason = text_config.get("block_group").get(来源群拼音) or text_config.get("block_group").get(str(消息中文群名)) or text_config.get("block_group").get(msg_json["groupid"])
    if block_reason:
        print(str(lyywin.message_id) + ": 空消息、关键词或者群组在禁止列表中,忽略并返回。 reason=" + block_reason + "。群号=" + str(消息中文群名) + ", 消息=" + str(msg_json["markdown"]["text"]))
        return 0

    # 内容格式化
    msg_json["markdown"]["text"] = lyyre.replace_keys_with_values(msg_json.get("markdown", {}).get("text", ""), text_config.get("text_formatment", {}), debug=False)

    # 3.1 ---------------------------------内容黑名单屏蔽---------------------------------

    for keywords in text_config.get("block_keywords", []):
        if keywords in msg_json["markdown"]["text"]:
            log("黑名单关键字=[" + keywords + "]")
            return
    
    if msg_json["markdown"]["text"].isascii() and len(msg_json["markdown"]["text"])<5:
        log("msg too short and not chinese")
        return 

    # 3.6 ---------------------------------如果是图片且符合条件，则OCR并替换原来---------------------------------
    if "img" not in msg_json.keys() or msg_json["chinesename"] in text_config.get("deny_ocr_group_chinese_name"):
        if debug:
            print("不需要ocr:", "img" not in msg_json.keys(), msg_json["chinesename"] in text_config.get("deny_ocr_group_chinese_name"))
    else:
        with lyywin.ocr_lock:
            msg_json_with_ocr_text = process_ocr(lyywin, msg_json, text_config, text_config.get("deny_ocr_group_chinese_name"), ocr_engine="ocr_panddle")
        if msg_json_with_ocr_text is not None:
            Process_Data(lyywin, msg_json_with_ocr_text,all_config_dict,df_teacherlist)
            return

    # # 3.7 全局消息替换正则 全局子文本替换 去除消息里面的组名
    # msg_json["markdown"]["text"] = lyyddforward.process_format_msg_text(msg_json, text_rule_dict, debug=True)

    # 处理命令文本
    if 来源群拼音 == "shuruceshi":
        if msg_json["markdown"]["text"].startswith("查询结果:"):
            return
        elif msg_json["markdown"]["text"].startswith("查询"):
            msg_json["markdown"]["text"] = process_lyycmd(msg_json["markdown"]["text"])
            print(str(lyywin.message_id) + ": " + "群查询分析完成 。不存数据库不处理转发。")
            return

    # 存数据库
    if debug:
        print(str(lyywin.message_id) + ": " + "#存数据库")
    if len(msg_json["markdown"]["text"]) < 1:
        print("内容为空，返回")
        return

    # lyyddforward.dd_to_SQLite(msg_json, mysql_text, conn_text="D:\\UserData\\stock_info\\" + msg_json["cmd"] + ".db", debug=debug)

    # 根据配置文件转发
    # 假设dataframe已经存在,名为df
    #if all_config_dict.get("ddForward").get("from_group_name")== msg_json["chinesename"]:
    matching_rows = df_teacherlist[df_teacherlist["from_group_name"] == msg_json["chinesename"]]

    result = lyyddforward.forward_msg_group_by_group(matching_rows, msg_json, debug=True) if not matching_rows.empty else ""

    if result != "nosql":
        lyywin.process_mysql(msg_json)
    print(str(lyywin.message_id) + ": " + "fwsd result=", result)



def get_mengxia_markdown_content(msg_json):
    print("enter get_mengxia_mark content")
    msg_type = msg_json.get("type", "")
    if msg_type == "text":
        print("mengxia msg_type== text")
        content = msg_json.get("msg", "").replace("\\/", "/").replace(r"/////", r"//")
    elif msg_type == "pic":
        print("mengxia= msg_type=pic")
        content = msg_json["url"].replace("\\/", "/").replace(r"/////", r"//")
        img = content
    elif msg_type == "file":
        content = msg_json["url"].replace("\\/", "/").replace(r"/////", r"//")
    else:
        lognew.error("in format all msg for mengxia get_msg_content_from_json, 出现第4种情况 " + str(msg_json))
    return msg_type, content

def format_mx(msg):
    if debug:
        print("这是format_mx 消息包含type字段")  # {"type":"roommsg","ly":1,"msg":"[{\"type\":\"pic\",\"url\":\"https:\\/\\/static.dingtalk.com\\/media\\/lALPM3V2qt_2YLjNAVTNBRQ_1300_340.png?bizType=im\"}]","mb":9160,"uid":0,"timestamp":"2024-04-25T01:01:52.000Z"}
    cmd = "mengxia"
    groupid = msg_json.get("mb")
    msg = msg_json.get("msg", {})
    if debug:
        print("get msg,msg=", msg, type(msg))
    msg_list = json.loads(msg) if isinstance(msg, str) else msg
    if debug:
        print(type(groupid), "groupidtype")
    name = number_pinyin_dict.get((groupid), "weizhiqunzu")
    chinesename = number_chinese_dict.get((groupid), "未知群组")

    for msg_json in msg_list:
        msg_type = msg_json.get("type", "")
        if msg_type == "text":
            print("mengxia msg_type== text")
            content = msg_json.get("msg", "").replace("\\/", "/").replace(r"/////", r"//")
        elif msg_type == "pic":
            print("mengxia= msg_type=pic")
            content = msg_json["url"].replace("\\/", "/").replace(r"/////", r"//")
            img = content
        elif msg_type == "file":
            content = msg_json["url"].replace("\\/", "/").replace(r"/////", r"//")
        else:
            lognew.error("in format all msg for mengxia get_msg_content_from_json, 出现第4种情况 " + str(msg_json))
        new_json = {"msgtype": "markdown", "markdown": {"title": {}, "text": content}, "groupid": groupid, "name": name, "chinesename": chinesename, "cmd": cmd}
        print("mengxia newjson=", new_json)
        self.format_all_msg(new_json)


def get_xbot_content(msg_json):
    print("in get_xbot_content",type(msg_json),msg_json)
    if msg_json.get("msgtype") == "text":
        print("msgtype=text")
        content = msg_json.get("text", {}).get("content")
    elif msg_json.get("msgtype") == "actionCard":
        print("you got an actionCard")
        content = msg_json["actionCard"]["text"]
        title = msg_json["actionCard"]["title"]
    else:  # "markdown"
        print("you got markdown")
        content = msg_json["markdown"]["text"]
    return content

def format_all_msg(msg: dict | str, all_config_dict:dict, debug: bool = False):
    """
    萌侠: 3个主键: type, msg, mb
    WS： 2个主键, msg, mb
    xbot: 从属于ws的msg键
    """
    if debug:
        print("enter format_all_msg")

    global text_rule_dict, text_config,number_chinese_dict,number_pinyin_dict,wss_name_chinesename_dict
    if text_config is None:
        text_config = all_config_dict.get("text_format")
    if text_rule_dict is None:
        text_rule_dict = all_config_dict.get("system8").get("text")
    if number_chinese_dict is None:
        number_chinese_dict = all_config_dict.get("number_chinese")
        number_chinese_dict.update(text_config.get("group_name",{}))
    if number_pinyin_dict is None:
        number_pinyin_dict = all_config_dict.get("number_pinyin")
    if wss_name_chinesename_dict is None:
        wss_name_chinesename_dict=all_config_dict.get("ws_name_chinese_name")

    json_msg_result_list = []
    msg_json = json.loads(msg) if isinstance(msg, str) else msg
    title = image = cmd = None
    new_json = {"msgtype": "markdown", "markdown": {"title": "", "text": ""}, "groupid": "", "name": "", "chinesename": "", "cmd": ""}

    if "type" in msg_json.keys():
        print("收到萌侠消息")
        groupid = str(msg_json.get("mb"))
        name = number_pinyin_dict.get((groupid), "weizhiqunzu")
        chinesename = number_chinese_dict.get((groupid), "未知群组")

        mx_msg_list:list[dict] = json.loads(msg_json.get("msg", {})) 
        for item in mx_msg_list:#item为列表中的字典类型
            cmd = "mengxia"
            title, text = get_mengxia_markdown_content(item)
            good_json = {"msgtype": "markdown", "markdown": {"title": title, "text": text}, "groupid": groupid, "name": name, "chinesename": chinesename, "cmd": "mengxia"}

            json_msg_result_list.append(good_json)


    else:
        if "msg" in msg_json.keys():
            cmd = "showwss"
            print("这是ws消息", msg_json, type(msg_json))  # {"msg":"{\"msgtype\":\"markdown\",\"markdown\":{\"title\":\"![](@lALPM3V2qt_2YLjNAVTNBRQ)\",\"text\":\"![](@lALPM3V2qt_2YLjNAVTNBRQ)\"},\"at\":{\"atMobiles\":[],\"isAtAll\":false}}","mb":"wenyingzhilu"}
            name = msg_json.get("mb")
            chinesename = wss_name_chinesename_dict.get(name, name)
            print("mb=", name, "chinesename=", chinesename)
            msg_json = msg_json.get("msg")
            groupid="0"
            if isinstance(msg_json,str):
                msg_json = json.loads(msg_json)

        else:
            print("这是xbot消息")
            cmd = "showmsg"
            groupid = msg_json.get("groupid")
            name = msg_json.get("name")
            chinesename = msg_json.get("chinesename")

        msg_list = lyyre.extracet_img_packet( get_xbot_content (msg_json))
        for item in msg_list:
            good_json = {"msgtype": "markdown", "markdown": {"title":item.get("type"), "text": item.get("text") }, "groupid": groupid or "0", "name": name, "chinesename": chinesename, "cmd": cmd}
            if item.get("type")=="img":
                good_json['img'] = item.get("text")    
                good_json['title'] = "图片"     

            json_msg_result_list.append(good_json)

    return json_msg_result_list



if __name__ == "__main__":
    import pickle
    import lyyddmsg
    import os

    with open(r"D:\UserData\resource\ddForward\mengxia_3.pickle", "rb") as f:
        msg = pickle.load(f)
    print(msg, type(msg))

    import xbot_client

    os.chdir(r"D:\UserData\resource\ddForward")

    from xbot_client import all_config_dict

    t = lyyddmsg.format_all_msg(msg, all_config_dict)