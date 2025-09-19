'''
编写和使用evalp()的目的，
是将输入字符串内的null等特殊关键字修改为相应字符串,
防止eval()报错。
'''

def evalp(content):
    content = content.replace('null', '\'null\'')
    content = content.replace('false', '\'false\'')
    content = content.replace('true', '\'true\'')

    content = eval(content)
    return content