import time
def report(report_msg):#后台上报日志，带时间
	print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), report_msg)