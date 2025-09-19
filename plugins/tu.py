import json
import random
import asyncio
from tools.api import send_group_msg, delete_msg
from tools.report import report

async def tu(msg):

	group_id = msg['group_id']
	raw_message = msg['raw_message']
	user_id = msg['user_id']
	nickname = msg['sender']['nickname']
	message_id = msg['message_id']
	msgTime = msg['raw']['msgTime']
	peerName = msg['raw']['peerName']

	with open('.//data//all_tu.json') as f:
		all_tu = json.load(f)
	with open('.//data//record.json') as f:
		record = json.load(f)

	if raw_message == '图':#tu响应
		tu_url = all_tu[random.randint(1, len(all_tu))]
		tu_message_id = await send_group_msg(group_id, f'[CQ:at,qq={user_id}][CQ:image,file={tu_url}]')
		report(f'群【{peerName}】中【{nickname}】请求了图')
		record.append([msgTime, 'tu', group_id, user_id])
		with open('.//data//record.json', 'w') as f:
			json.dump(record, f)
		
		await asyncio.sleep(60.0)
		await delete_msg(tu_message_id)