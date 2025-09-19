'''
与napcat接口通信的各种函数。
函数名和形参与接口字符串和参数一致。
有些函数内置了超时，因为它们主要是被其他协程函数调用，最后包装成task执行，需要避免等待使主程序停滞；
有些函数在使用时设置超时；
有些函数没有返回值，所以不用设置超时。
'''

import json
import asyncio
import websockets
import time
from tools.report import report
from tools.evalp import evalp

with open('settings.json') as f:
	settings = json.load(f)
uri = f"ws://localhost:{settings["port"]}/"

async def send_group_msg(group_id, message):
	async with websockets.connect(uri) as ws:
		req = {
			"action": "send_group_msg",
			"params": {"group_id": group_id, "message": message},
			"echo": "test"
		}
		await ws.send(json.dumps(req))
		start_time = int(time.time())
		while True:
			current_time = int(time.time())
			msg = evalp(await ws.recv())
			if "status" in msg.keys():
				return msg["data"]["message_id"]
			elif current_time - start_time > 30:
				report('获取已发送群消息message_id超时')

async def send_private_msg(user_id, message):
	async with websockets.connect(uri) as ws:
		req = {
			"action": "send_private_msg",
			"params": {'user_id': user_id, 'message': message},
			"echo": "test"
		}
		await ws.send(json.dumps(req))
		start_time = int(time.time())
		while True:
			current_time = int(time.time())
			msg = evalp(await ws.recv())
			if "status" in msg.keys():
				return msg["data"]["message_id"]
			elif current_time - start_time > 30:
				report('获取已发送私聊消息message_id超时')

async def delete_msg(message_id):
	async with websockets.connect(uri) as ws:
		req = {
			"action": "delete_msg",
			"params": {'message_id': message_id},
			"echo": "test"
		}
		await ws.send(json.dumps(req))

async def get_group_list():#获取群列表并保存到group_list.json，然后返回
	async with websockets.connect(uri) as ws:
		req = {
			"action": "get_group_list",
			"params": {'no_cache': False},
			"echo": "test"
		}
		await ws.send(json.dumps(req))
		start_time = int(time.time())
		while True:
			current_time = int(time.time())
			msg = evalp(await ws.recv())
			if "status" in msg.keys():
				with open('.//data//group_list.json', 'w') as f:
					json.dump(msg['data'], f)
				return msg['data']
			elif current_time - start_time > 30:
				report('获取群列表超时')

async def get_login_info():
	async with websockets.connect(uri) as ws:
		req = {
			"action": "get_login_info",
			"params": {},
			"echo": "test"
		}
		await ws.send(json.dumps(req))
		while True:
			msg = evalp(await ws.recv())
			if "status" in msg.keys():
				return msg['data']['user_id']