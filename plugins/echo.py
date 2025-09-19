import random
import json
from tools.api import send_group_msg
from tools.report import report
async def echo(msg):

	group_id = msg['group_id']
	raw_message = msg['raw_message']
	user_id = msg['user_id']
	nickname = msg['sender']['nickname']
	message_id = msg['message_id']
	msgTime = msg['raw']['msgTime']
	peerName = msg['raw']['peerName']

	with open('.//data//record.json') as f:
		record = json.load(f)

	if random.randint(1,10) == 1:
		await send_group_msg(group_id, raw_message)
		report(f'群【{peerName}】中【{nickname}】的消息被回声')
		record.append([msgTime, 'echo', group_id, user_id])#TODO:把record搞成字典。 
		with open('.//data//record.json', 'w') as f:
			json.dump(record, f)