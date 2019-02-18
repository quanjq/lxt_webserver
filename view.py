# -*- coding:utf-8 -*-
import sys
import os
dir_sign=os.path.split(os.path.realpath(__file__))[0] #将当前的目录sign加入sys的path路径，方便 python执行时能够找到自定义的库
sys.path.append(dir_sign)
import time
import json
from lib.EncryptUtil import  EncryptUtil
pub_key_path=dir_sign+'/lib/pub.key'
pri_key_path=dir_sign+'/lib/pri.key'
enc=EncryptUtil(pub_key_path,pri_key_path)
from lib.Logger import Logger
log_debug = Logger('all.log',level='debug')
log_error=Logger('error.log', level='error')

html='''<html>
 <head><meta charset="utf-8"></head>
 <body>
      <div>
          回调pjs的url:<br>
          <textarea id="urlid" name="msg_recevieUrl" form="sform_update" style="width:500px;height:30px;">%s</textarea><br>
          接收到的报文解析后的数据xml:<br>
        <textarea id="textareaid" name="msg_from_pjs" form="sform_update" style="width:500px;height:300px;">%s</textarea><br>
          联信通返回给pjs的数据:<br>
        <textarea id="retmsgid" name="msg_from_lxt"  form="sform_update" style="width:500px;height:100px;">%s</textarea><br>
       <form id="sform_update" action="/update-action/"  method="post">
          <button class="bsubmit" type="submit">修改联信通返回给pjs的数据</button>
      </form>

    </div>
      <form id="sform" action=%s method="post">
          <input  name="encryptMsg" style="width:500px;height:50px;"  value=%s />
          <button class="bsubmit" type="submit">提交报文</button>
      </form>
 </body>
</html>'''


def proce(encryptMsg,dict_text):
     #1、解密提取报文信息
     dec_ext=json.loads(enc.decrypt(encryptMsg)) #解密提取报文信息json.loads()函数是将json格式数据转换为字典
     log_debug.logger.info('接收到pjs的请求：%s' %dec_ext)
     #2、提取custId、custNm、recevieUrl，新生成traceNo并组装返回给pjs的post报文
     recevieUrl,res_data,retmsg=pack_msg(dec_ext,dict_text)
     log_debug.logger.info('回调pjs的报文明文：%s' %retmsg)
     res_data=res_data.decode('utf-8')
     log_debug.logger.info('回调pjs的报文密文：%s' %res_data)
     dec_ext=json.dumps(dec_ext)
     res_data=json.dumps(res_data)
     recevieUrl="'"+recevieUrl+"'"
     response_body=html %(recevieUrl,dec_ext,retmsg,recevieUrl,res_data)
     return response_body

def pack_msg(dec_ext,dict):
    traceNo=time.strftime('%y%m%d%H%M%S',time.localtime(time.time()))+'T9990000001'
    frzNo=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'01'
    settleDay=time.strftime('%y%m%d',time.localtime(time.time()))
    authNo=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'60000001'

    ret_text={}
    for key,valu in dict.items():  #复制dict的值而不改变dict的值
        ret_text[key]=valu
    for ke,v in ret_text.items():
        if v[0]==0:   #0取dict本身的值，1取得dec_ext的值，2取公共的
            ret_text[ke]=v[1]
        elif v[0]==1:
            ret_text[ke]=dec_ext[ke]
        elif v[0]==2:
            if ke =='traceNo':
                ret_text[ke]=traceNo
            elif ke =='frzNo':
                 ret_text[ke]=frzNo
            elif ke =='authNo' :
                ret_text[ke]=authNo
            elif ke =='settleDay':
                ret_text[ke]=settleDay

    recevieUrl=str(dec_ext['recevieUrl'])
    retmsg=json.dumps(ret_text) #建行/联信通返回的数据
    res_data=enc.encrypt(json.dumps(ret_text).encode('utf-8')) #json.dumps()函数是将一个Python数据类型列表进行json格式的编码
    return  recevieUrl,res_data,retmsg


recharge_confirm_dict={"orgCode":[1],
           "custId":[1],
           "traceNo":[2],
           "reqSn":[1],
		   "errCode":[0,'0000'],
		   "errMsg":[0,'success'],
		   "settleDay":[2],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."]}
def index_of_recharge_confirm(encryptMsg):
    dict_tex=recharge_confirm_dict
    response_body=proce(encryptMsg,dict_tex)
    return [response_body]

withdrawals_confirm_dict={"orgCode":[1],
           "custId":[1],
           "traceNo":[2],
           "reqSn":[1],
		   "accBal":[0,''],
		   "frzNo":[2],
		   "freezeAmt":[0,''],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."]}
def index_of_withdrawals_confirm(encryptMsg):
    dict_tex=withdrawals_confirm_dict
    response_body=proce(encryptMsg,dict_tex)
    return [response_body]
investment_freeze_confirm_dict={"orgCode":[1],
           "custId":[1],
           "traceNo":[2],
           "refNo":[1],
            "frzNo":[2],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."]}
def index_of_investment_freeze_confirm(encryptMsg):
    dict_tex=investment_freeze_confirm_dict
    response_body=proce(encryptMsg,dict_tex)
    return [response_body]
bespeak_investment_freeze_confirm_dict={"orgCode":[1],
           "custId":[1],
           "traceNo":[2],
           "refNo":[1],
            "frzNo":[2],
            "frzType":[1],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."]}
def index_of_bespeak_investment_freeze_confirm(encryptMsg):
    dict_tex=bespeak_investment_freeze_confirm_dict
    response_body=proce(encryptMsg,dict_tex)
    return [response_body]
business_authorize_confirm_dict={"orgCode":[1],
           "custId":[1],
           "traceNo":[2],
           "refNo":[1],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."]}

def index_of_business_authorize_confirm(encryptMsg):
    dict_tex=business_authorize_confirm_dict
    response_body=proce(encryptMsg,dict_tex)
    return [response_body]
payment_confirm_dict={"orgCode":[1],
           "custId":[1],
           "traceNo":[2],
           "authNo":[1],
           "refNo":[1],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."]}
def index_of_payment_confirm(encryptMsg):
    dict_tex=payment_confirm_dict
    response_body=proce(encryptMsg,dict_tex)
    return [response_body]
unsubscribe_dict={"orgCode":[1],
           "custId":[1],
           "custNm":[1],
           "telNo":[0,"13580420001"],
           "bankNm":[0,"308"],
           "acctNo":[0,"99990000000001"],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."],
           "traceNo":[2],
           "oprFlag":[0,'0004']}
def index_of_unsubscribe(encryptMsg):
    dict_tex=unsubscribe_dict
    response_body=proce(encryptMsg,dict_tex)
    return [response_body]
unbind_dict={"orgCode":[1],
           "custId":[1],
           "custNm":[1],
           "telNo":[0,"13580420001"],
           "bankNm":[0,"308"],
           "acctNo":[0,"99990000000001"],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."],
           "traceNo":[2],
           "oprFlag":[0,'0005']}
def index_of_unbind(encryptMsg):
    dict_tex=unbind_dict
    response_body=proce(encryptMsg,dict_tex)
    return [response_body]
reset_password_dict={"orgCode":[1],
           "custId":[1],
           "custNm":[1],
           "telNo":[0,"13580420001"],
           "bankNm":[0,"308"],
           "acctNo":[0,"99990000000001"],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."],
           "traceNo":[2],
           "oprFlag":[0,'0007']}
def index_of_reset_password(encryptMsg):
    dict_tex=reset_password_dict
    response_body=proce(encryptMsg,dict_tex)
    return [response_body]
stock_customer_dict={"orgCode":[1],
           "custId":[1],
           "custNm":[1],
           "telNo":[0,"13580420001"],
           "bankNm":[0,"308"],
           "acctNo":[0,"99990000000001"],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."],
           "traceNo":[2],
           "oprFlag":[0,'0003']}
def index_of_stock_customer(encryptMsg):
    dict_tex=stock_customer_dict
    response_body=proce(encryptMsg,dict_tex)
    return [response_body]

open_acct_dict={"orgCode":[1],
           "custId":[1],
           "custNm":[1],
           "telNo":[0,"13580420001"],
           "bankNm":[0,"308"],
           "acctNo":[0,"99990000000001"],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."],
           "traceNo":[2],
           "oprFlag":[0,'0001']}
def index_of_open_acct(encryptMsg):
    dict_tex=open_acct_dict
    response_body=proce(encryptMsg,dict_tex)
    return [response_body]
change_bank_card_dict={"orgCode":[1],
           "custId":[1],
           "custNm":[1],
           "telNo":[0,"13580420001"],
           "bankNm":[0,"308"],
           "acctNo":[0,"99990000000001"],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."],
           "traceNo":[2],
           "oprFlag":[0,'0002']}
def index_of_change_bank_card(encryptMsg):
    dict_tex=change_bank_card_dict
    response_body=proce(encryptMsg,dict_tex)
    return [response_body]

pay_confirm_dict={"orgCode":[1],
           "custId":[1],
           "traceNo":[2],
           "authNo":[2],
           "refNo":[1],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."]}
def index_of_pay_confirm(encryptMsg):
    dict_tex=pay_confirm_dict
    response_body=proce(encryptMsg,dict_tex)
    return [response_body]

def update_action(msg_recevieUrl,msg_from_pjs,msg_from_lxt):
    res_data=enc.encrypt(msg_from_lxt.encode('utf-8'))
    res_data=res_data.decode('utf-8')
    log_debug.logger.info('修改的报文密文：%s' %res_data)
    res_data=json.dumps(res_data)
    response_body=html %(msg_recevieUrl,msg_from_pjs,msg_from_lxt,msg_recevieUrl,res_data)
    return [response_body]

