import random
import json
from tools.divide_words import pick_word
from tools.api import send_group_msg
from tools.report import report
async def confidence(msg):

	group_id = msg['group_id']
	raw_message = msg['raw_message']
	user_id = msg['user_id']
	nickname = msg['sender']['nickname']
	msgTime = msg['time']
	peerName = msg['raw']['peerName']

	with open('.//data//record.json') as f:
		record = json.load(f)
		
	if random.randint(1,10) == 1:
		pick_d = pick_word(raw_message, 'd')
		if pick_d:
			pick_d = pick_d[random.randint(0, len(pick_d) - 1)]
			await send_group_msg(group_id, f'自信点，把{pick_d}删掉')
			report(f'群【{peerName}】中【{nickname}】收获了自信')
			record.append([msgTime, 'confidence', group_id, user_id])
			with open('.//data//record.json', 'w') as f:
				json.dump(record, f)