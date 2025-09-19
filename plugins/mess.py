import json
import random
from tools.api import send_group_msg
from tools.divide_words import seperate
from tools.report import report
async def mess(msg):

	group_id = msg['group_id']
	raw_message = msg['raw_message']
	user_id = msg['user_id']
	nickname = msg['sender']['nickname']
	message_id = msg['message_id']
	msgTime = msg['raw']['msgTime']
	peerName = msg['raw']['peerName']

	with open('.//data//record.json') as f:
		record = json.load(f)
	with open('.//data//group_functions.json') as f:
		g_f = json.load(f)
	with open('settings.json') as f:
		settings = json.load(f)

	if random.randint(1,10) == 1 and '[CQ:' not in raw_message:
		mess_message = seperate(raw_message)
		if len(mess_message) >= 3:
			random.shuffle(mess_message)
			mess_msg = ''
			for i in mess_message:
				mess_msg = mess_msg + i
			await send_group_msg(group_id, mess_msg)
			record.append([msgTime, 'mess', group_id, user_id])
			report(f'群【{peerName}】中【{nickname}】的消息被颠三倒四')
			with open('.//data//record.json', 'w') as f:
				json.dump(record, f)