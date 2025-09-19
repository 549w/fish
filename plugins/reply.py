from tools.api import send_group_msg
import json

async def reply(msg):

	with open('settings.json') as f:
		settings = json.load(f)

	group_id = msg['group_id']
	raw_message = msg['raw_message']
	user_id = msg['user_id']
	nickname = msg['sender']['nickname']
	message_id = msg['message_id']
	msgTime = msg['raw']['msgTime']
	peerName = msg['raw']['peerName']

	if raw_message.strip() == f'[CQ:at,qq={settings['self_id']}]':
		await send_group_msg(group_id, 'fish的使用说明还没写好')