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
	print("LogService trigger and send data to FunctionCompute test output, The content of event is : %s" % (evt))

	# AK/SK
	accessKeyId = 'LTAIzozEawa7dTgq'    
	accessKey = '21JIIj9oKJDrSRR61flpNl0rqN8KrJ'     

	# 从event中获取数据
	endpoint = evt['source']['endpoint']      
	project = evt['source']['projectName']
	logstore = evt['source']['logstoreName']
	shard_id = evt['source']['shardId']
	start_cursor = evt['source']['beginCursor']
	end_cursor = evt['source']['endCursor']

	# 构建一个client
	client = LogClient(endpoint, accessKeyId, accessKey)
  
	# 计算sharedID中beginCursor和endCursor之间有多少条消息
	counter=0
	while True:
		loggroup_count = 100  # 每次读取100个包
		res = client.pull_logs(project, logstore, shard_id, start_cursor, loggroup_count, end_cursor)
		#res.log_print()
		counter=counter+res.get_log_count()
		next_cursor = res.get_next_cursor()
		if next_cursor == start_cursor:
			break
		start_cursor = next_cursor
	
	print("LogService trigger and send data to FunctionCompute test output:\
	 The shard_id is: %d, the start_cursor is: %s, the end_cursor is: %s, the count of log events is : %d" \
	 % (shard_id, start_cursor, end_cursor, counter))
		
	return counter
  
  
  
# __source__:  
# __topic__:  eric-fc-service
# functionName:  test-sls-2-fc
# message:  LogService trigger and send data to FunctionCompute test output, The content of event is : 
# { 
#   "taskId": "5f3ad58b-42d0-4e28-a8bb-69a9a8802f58",
# 	"jobName": "399b4017460185cfef14f0e7371e02df5fe8e440",
# 	"cursorTime": 1531913736, 
#   "source": {
# 		"endpoint": "http://cn-hangzhou-intranet.log.aliyuncs.com",
# 		"projectName": "eric-nginx-logstore",
# 		"shardId": 0,
# 		"logstoreName": "eric-nginx-access-log-store",
# 		"endCursor": "MTUyNzEwNDIzODkyNTYxMTA1Mg==",
# 		"beginCursor": "MTUyNzEwNDIzODkyNTYxMTAxOA=="
# 	},
# 	"parameter": {
# 	}
# }
