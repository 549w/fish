import requests
import json

with open('settings.json') as f:
    settings = json.load(f)

headers = {
    'X-Auth-Token': settings['yuque_api'] # 不允许外传该Token!
}

def get_book(login): # 获取团队下的知识库
    resp = requests.get(f'https://nova.yuque.com/api/v2/groups/{login}/repos', headers = headers)
    if resp.status_code == 200:
        return resp.json()['data']
    else:
        print(f'ERROR. Status_code:{resp.status_code}')
        return 0

def get_docs(book_id, offset = 0): # 获取知识库下的文档
    resp = requests.get(f'https://nova.yuque.com/api/v2/repos/{book_id}/docs?offset={offset}', headers = headers)
    if resp.status_code == 200:
        return resp.json()['data']
    else:
        print(f'ERROR. Status_code:{resp.status_code}')
        return 0
    
def get_all_docs(book_id): # 获取知识库下的全部文档！
    resp = requests.get(f'https://nova.yuque.com/api/v2/repos/{book_id}/docs', headers = headers)
    if resp.status_code == 200:
        total = resp.json()['meta']['total']
    else:
        print(f'ERROR. Status_code:{resp.status_code}')
        return 0
    num_of_req = total // 100
    all_docs = []
    for i in range(num_of_req + 1):
        resp = requests.get(f'https://nova.yuque.com/api/v2/repos/{book_id}/docs?offset={i * 100}', headers = headers)
        if resp.status_code == 200:
            all_docs += resp.json()['data']
        else:
            print(f'ERROR. Status_code:{resp.status_code}')
    return all_docs

def get_doc_detail(book_id, doc_id): # 获取文档详情
    resp = requests.get(f'https://nova.yuque.com/api/v2/repos/{book_id}/docs/{doc_id}', headers = headers)
    if resp.status_code == 200:
        return resp.json()['data']
    else:
        print(f'ERROR. Status_code:{resp.status_code}')
        return 0