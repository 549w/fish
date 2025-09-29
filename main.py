#使用group_id必须转换成str类型！
import json
import asyncio
import websockets

from plugins.confidence import confidence
from plugins.echo import echo
from plugins.master_ctrl import master_ctrl
from plugins.mess import mess
from plugins.reply import reply
#from plugins.search_anime import search_anime
from plugins.tu import tu
from plugins.yuque import yuque
from plugins.yuque import yuque_private
from plugins.yuque import update_monitor

from tools.api import get_group_list
from tools.api import get_login_info
from tools.api import send_group_msg
from tools.evalp import evalp
from tools.report import report

with open('settings.json') as f:
    settings = json.load(f)

async def deal_msg():
    uri = f"ws://localhost:{settings["port"]}/"
    async with websockets.connect(uri) as ws:

        #获取自身qq号
        try:
            self_id = await asyncio.wait_for(get_login_info(), timeout=5.0)
        except asyncio.TimeoutError:
            report('获取自身qq号超时')
        except Exception as e:
            report(f'获取自身qq号错误：{e}')
        settings['self_id'] = self_id
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

        #初始化群列表和群功能
        await get_group_list()
        with open('.//data//group_list.json') as f:
            group_list = json.load(f)
        with open('.//data//group_functions.json') as f:
            group_functions = json.load(f)

        #将新群的功能初始化并保存
        for group in group_list:
            if str(group['group_id']) not in group_functions.keys():
                group_functions[group['group_id']] = {"quiet": 1}
                report(f'群{group['group_name']}安静功能初始化')
        with open('.//data//group_functions.json', 'w') as f:
            json.dump(group_functions, f)
        while True:
            msg = evalp(await ws.recv())
            with open('.//data//group_functions.json') as f:
                group_functions = json.load(f)
            
            #群功能test
            if msg['post_type'] == 'message' and msg['message_type'] == 'group' and msg['user_id'] != settings['self_id']:

                msg['group_id'] = str(msg['group_id'])

                asyncio.create_task(master_ctrl(msg))
                asyncio.create_task(reply(msg))
                asyncio.create_task(tu(msg))
                asyncio.create_task(yuque(msg))

                if group_functions[str(msg['group_id'])]['quiet'] == 0:
                    asyncio.create_task(confidence(msg))
                    asyncio.create_task(echo(msg))
                    asyncio.create_task(mess(msg))
                
                #asyncio.create_task(search_anime(msg))
            
                if msg['raw_message'].strip() == '安静模式':
                    group_functions[str(msg['group_id'])]['quiet'] = 1
                    with open('.//data//group_functions.json', 'w') as f:
                        json.dump(group_functions, f)
                    await send_group_msg(msg['group_id'], '已开启安静模式')
                elif msg['raw_message'].strip() == '活跃模式':
                    group_functions[str(msg['group_id'])]['quiet'] = 0
                    with open('.//data//group_functions.json', 'w') as f:
                        json.dump(group_functions, f)
                    await send_group_msg(msg['group_id'], '已开启活跃模式')

            if msg['post_type'] == 'message' and msg['message_type'] == 'private' and msg['user_id'] != settings['self_id']:
                asyncio.create_task(yuque_private(msg))

async def main():
    await asyncio.gather(
        deal_msg(),
        update_monitor()
    )

try:    
    asyncio.run(main())
except websockets.exceptions.ConnectionClosedError:
    report('websocket连接断开')