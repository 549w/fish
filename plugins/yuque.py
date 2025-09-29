import asyncio
import json
from tools.api import send_group_msg, send_private_msg
from tools.yuque_api import get_all_docs, search, get_doc_detail
from tools.report import report
from tools.llm import get_answer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import time

async def yuque(msg):

    group_id = msg['group_id']
    raw_message = msg['raw_message']
    #user_id = msg['user_id']
    #nickname = msg['sender']['nickname']
    #message_id = msg['message_id']
    #msgTime = msg['raw']['msgTime']
    #peerName = msg['raw']['peerName']

    with open('settings.json') as f:
        settings = json.load(f)

    if raw_message == 'yuque':
        with open('.//data//name_list.json', encoding = 'utf-8') as f:
            name_list = json.load(f)

        docs = get_all_docs(69189148)

        with open('docs.json', 'w', encoding='utf-8') as f:
            json.dump(docs, f, ensure_ascii=False)

        count = 0
        name_word = {}

        for name in name_list:
            name_word[name] = 0

        uncompleted_msg = '尚未完成的成员：\n'
        for name in name_list:
            completed_or_not = 0
            for doc in docs:
                if name == doc['user']['name'] and doc['word_count'] >= 1: # “论文的最少字数是1.”
                    completed_or_not = 1
                    name_word[name] += doc['word_count']
            if completed_or_not == 1:
                #print(f'{name}已完成√')
                count += 1
            else:
                uncompleted_msg += name + '\n'
                #print(f'{name}未完成×')

        max_word = 0
        for name, word in name_word.items():
            if word > max_word:
                max_word = word
        
        for name, word in name_word.items():
            name_word[name] = word / max_word
        
        # 创建词云对象
        wordcloud = WordCloud(
            font_path='C:\\Windows\\Fonts\\simsun.ttc',  # 设置中文字体，如果不需要显示中文可以删除
            width=800,
            height=600,
            background_color='white',  # 背景颜色
            #max_words=100,  # 最大显示词数
            colormap='viridis'  # 颜色方案
        )
        wordcloud.generate_from_frequencies(name_word)

        wordcloud.to_file('.//data//images//wordcloud.png')

        all_word_count = 0
        most_word = {'name': '', 'count': 0, 'title': ''}
        for doc in docs:
            all_word_count += doc['word_count']
            if doc['word_count'] > most_word['count']:
                most_word['count'] = doc['word_count']
                most_word['name'] = doc['user']['name']
                most_word['title'] = doc['title']
        
        await send_group_msg(group_id, f'语雀统计信息\n截至{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}\n已完成：{count}人，共{len(name_list)}人\n总字数：{all_word_count}\n最多字数为{most_word['count']},来自{most_word['name']}创作的{most_word['title']}。')
        await send_group_msg(group_id, '已完成成员：[CQ:image,file=file:///D:\\fish\\data\\images\\wordcloud.png]')
        await send_group_msg(group_id, uncompleted_msg)

async def yuque_private(msg):

    try:
        with open('.//data//criteria.json') as f:
            criteria = json.load(f)
    except FileNotFoundError:
        report('找不到文件.//data//criteria.json')

    user_id = msg['user_id']
    raw_message = msg['raw_message']

    with open('settings.json') as f:
        settings = json.load(f)

    if raw_message[:2] == '搜索':
        #print(search(raw_message[2:], 'doc'))
        search_result = search(raw_message[2:], 'doc')
        reply_msg = ''
        if search_result == []:
            reply_msg = "无结果，请换个搜索词试试。"
        else:
            reply_msg = f'搜索到{len(search_result)}篇文档:\n'
            i = 1
            for doc in search_result:
                reply_msg += f'{i}.{doc['title']} 创建时间：{doc['target']['created_at']}\n'
                i += 1
        await send_private_msg(user_id, reply_msg)

    if raw_message[:2] == '标准':
        criteria[user_id] = raw_message[3:]
        await send_private_msg(user_id, '已设定标准。如需改动，只需重新发送“标准 （标准内容）”。')
        with open('.//data//criteria.json', 'w') as f:
            json.dump(criteria, f)

async def update_monitor():
    doc_updateTime = {}
    raw_docs = get_all_docs(69189148)
    for doc in raw_docs:
        doc_updateTime[doc['id']] = doc['content_updated_at']
    with open('.//data//doc_updateTime.json', 'w') as f:
        json.dump(doc_updateTime, f)
    report('初始化完成')
    
    with open('.//data//criteria.json') as f:
        criteria = json.load(f)

    while True:
        with open('.//data//doc_updateTime.json') as f:
            doc_updateTime = json.load(f)
        raw_docs = get_all_docs(69189148)
        for doc in raw_docs:
            doc['id'] = str(doc['id'])# 转为字符串以匹配json文件中的key!!!!!!!!!!
            remind_or_not = 0
            if str(doc['id']) in doc_updateTime.keys() and doc['content_updated_at'] != doc_updateTime[doc['id']]:# 已有文档的更新:
                print(f'{doc['content_updated_at']} != {doc_updateTime[doc['id']]}')
                remind_or_not = 1
                print('文档有更新')
                doc_updateTime[doc['id']] = doc['content_updated_at']
                with open('.//data//doc_updateTime.json', 'w') as f:
                    json.dump(doc_updateTime, f)
            elif str(doc['id']) not in doc_updateTime.keys():# 新文档的创建
                remind_or_not = 1
                doc_updateTime[doc['id']] = doc['content_updated_at']
                with open('.//data//doc_updateTime.json', 'w') as f:
                    json.dump(doc_updateTime, f)
                print('新文档创建，标题为' + doc['title'])
            if remind_or_not == 1:
                for user_id, criterion in criteria.items():
                    answer = await get_answer(f"请根据用户定义的标准，判断该文档是否重要。如果不重要，只需回复0；如果重要，提示用户该文档重要，解释哪些地方符合用户定义的标准，总字数不超过100.文档内容：{get_doc_detail(69189148, doc['id'])['body']}； 用户标准：{criterion}")
                    if str(answer) == '0':
                        pass
                    else:
                        await send_private_msg(user_id, f'语雀文档有对你重要的更新。\n标题：{doc['title']}\n链接：https://nova.yuque.com/ph25ri/ua1c3q/{doc['slug']}\n理由：{answer}')

        await asyncio.sleep(1.0)