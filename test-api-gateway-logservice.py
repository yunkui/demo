# -*- coding:utf-8 -*-
 
import logging
import json
import time
# for LogService - Begin
from aliyun.log.logitem import LogItem
from aliyun.log.logclient import LogClient
from aliyun.log.getlogsrequest import GetLogsRequest
from aliyun.log.putlogsrequest import PutLogsRequest
from aliyun.log.listlogstoresrequest import ListLogstoresRequest
from aliyun.log.gethistogramsrequest import GetHistogramsRequest
# for LogService - End 

def handler(event, context):
  evt = json.loads(event)

  #input your app code
  uid = evt['queryParameters']['uid']
  ip = evt['queryParameters']['ip']
  device = evt['queryParameters']['device']
  
  # print("test-api-gateway output: The uid is %s, the ip address is %s and the device type is %s. " % (uid, ip, device))
  
  endpoint = 'cn-hangzhou.log.aliyuncs.com'       # 选择与上面步骤创建Project所属区域匹配的Endpoint
  accessKeyId = 'LTAIzozEawa7dTgq'    # 使用您的阿里云访问密钥AccessKeyId
  accessKey = '21JIIj9oKJDrSRR61flpNl0rqN8KrJ'      # 使用您的阿里云访问密钥AccessKeySecret
  project = 'eric-nginx-logstore'        # 上面步骤创建的项目名称
  logstore = 'eric-nginx-access-log-store'       # 上面步骤创建的日志库名称
  
  # 构建一个client
  client = LogClient(endpoint, accessKeyId, accessKey)
  topic = ""
  source = ""
  
  # 向logstore写入数据
  logitemList = []  # LogItem list
  contents = [('ip',ip), ('uid',uid), ('device',device)]
  print("FunctionCompute --> LogService test output: " + ip + " - " + uid + " - " + device)
  logItem = LogItem()
  logItem.set_time(int(time.time()))
  logItem.set_contents(contents)
  logitemList.append(logItem)
  req2 = PutLogsRequest(project, logstore, topic, source, logitemList)
  res2 = client.put_logs(req2)
  res2.log_print()


  response_content = "you can return any string"
  api_rep = {
    "isBase64Encoded":"false",
    "statusCode":"200",
    "headers":{"x-custom-header":"your header"},
    "body":response_content
  }
  return json.dumps(api_rep)