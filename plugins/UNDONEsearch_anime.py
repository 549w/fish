import requests
import re
import json
import time
from tools.api import send_group_msg
from tools.report import report

async def search_anime(msg):

	group_id = msg['group_id']
	raw_message = msg['raw_message']
	user_id = msg['user_id']
	nickname = msg['sender']['nickname']
	message_id = msg['message_id']
	msgTime = msg['raw']['msgTime']
	peerName = msg['raw']['peerName']
	
	if '找番' in raw_message and '[CQ:image' in raw_message and raw_message.count('[CQ:') == 1:
		start_time = int(time.time())
		with open('.//data//record.json') as f:
			record = json.load(f)
		search_code = re.compile(r'url=(.*)]')
		search_pic = search_code.search(str(raw_message))
		await send_group_msg(group_id, f'[CQ:at,qq={user_id}]收到图片，开始识别')
		
		search_result = requests.get(f'https://api.trace.moe/search?anilistInfo&url={search_pic.group(1)}'.replace('&amp;', '&')).json()
		print(search_result)
		print('#############')
		print(search_pic.group(1).replace('&amp;', '&'))
		anime_name = search_result['result'][0]['anilist']['title']['native']
		other_names = search_result['result'][0]['anilist']['synonyms']
		episode = search_result['result'][0]['episode']
		similarity = search_result['result'][0]['similarity'] * 100
		from_time = search_result['result'][0]['from']
		to_time = search_result['result'][0]['to']
		from_time = f'{int((from_time - from_time % 60) / 60)}分{int(from_time % 60)}秒'
		to_time = f'{int((to_time - to_time % 60) / 60)}分{int(to_time % 60)}秒'
		end_time = int(time.time())
		await send_group_msg(group_id, f'[CQ:reply,id={message_id}]番剧原名：【{anime_name}】\n集数：【{episode}】\n起止时刻：【{from_time} 至 {to_time}】\n其他名称：{other_names}\n相似度：【{similarity}%】\n识别用时：【{end_time - start_time}秒】')
		report(f'群【{peerName}】中【{nickname}】查找了番剧')
		record.append([msgTime, 'search_anime', group_id, user_id])
		with open('.//data//record.json', 'w') as f:
			json.dump(record, f)