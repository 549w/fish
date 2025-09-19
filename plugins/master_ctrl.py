import json
from tools.api import send_group_msg
from tools.report import report
import asyncio
async def master_ctrl(msg):

	group_id = msg['group_id']
	raw_message = msg['raw_message']
	user_id = msg['user_id']
	nickname = msg['sender']['nickname']
	message_id = msg['message_id']
	msgTime = msg['raw']['msgTime']
	peerName = msg['raw']['peerName']

	with open('.//data//group_list.json') as f:
		group_list = json.load(f)
	with open('settings.json') as f:
		settings = json.load(f)

	if user_id == settings['master_id']:
		
		if raw_message == 'stop':#关闭
			report(f'作者在群【{peerName}】中关闭了fish')
			await send_group_msg(group_id, 'fish已关闭。')
			exit()
		
		if raw_message == '所有群':#上报所有群
			count = 1
			for a_group in group_list:
				await send_group_msg(group_id, f'{count}.{a_group['group_name']}')
				count += 1
				await asyncio.sleep(1.0)
		
		if raw_message[:2] == '群发' and raw_message.strip() != '群发':
			for a_group in group_list:
				await send_group_msg(a_group['group_id'], f'{raw_message[2:]}\n——作者群发')