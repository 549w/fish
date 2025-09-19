import requests
import json
from tools.report import report
def g_q_i(qq):#返回指定QQ的昵称和头像url
	qq_info = {}
	resp = requests.get(f'https://v.api.aa1.cn/api/qqimg/index.php?qq={qq}&type=json')
	qq_img = json.loads(resp.text)
	if qq_img['code'] == 200:
		return qq_img['qq_img']
	else:
		report(f'获取{qq}头像失败')