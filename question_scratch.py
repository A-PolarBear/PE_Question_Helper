from ctypes.wintypes import WORD
from pickle import NONE
import re
import requests
from bs4 import BeautifulSoup as bf
from bs4 import Comment
import random
import time
from rich.progress import track
 
 
delay_choices = [1, 0.5, 3, 6, 0.05, 2]  #延遲的秒數

answer_list = ['A', 'B', 'C', 'D','E','F','G','H']

def execute(html,file,word=None):
    Flag = 1
    soup = bf(html, "lxml")
    questions = soup.find_all(name='div', style="border-bottom:1px dotted #ccc;margin: 10px")
    if questions is None: return
    if word is not None:
        temp=soup.find(string=re.compile(word))
        if temp is None: return
    Flag = 0
    for question in questions:
        # print(re.findall(r"<strong>(.*?)<\strong>",question))
        issue = question.find(name='strong').get_text()
        file.write(issue)
        file.write('\n')
        choice = question.find(name='blockquote')
        if choice is not None:
            file.write(choice.get_text())
            file.write('\n')
        answer = question.find(text=lambda text: isinstance(text, Comment))
        answer = re.findall(r"\d*\d", answer)[0]
        res = "标准答案为："
        for i in range(len(answer)):
            if choice is None:
                res += "对" if int(answer[i]) else "错"
            else:
                if int(answer[i]):
                    res += answer_list[i]
        file.write(res)
        file.write('\n')
        file.write('\n')
    return Flag

def main():
    file = open("Question.txt",'a',encoding='utf-8')

    base_url = "http://211.83.159.5/tyexam/redir.php?catalog_id=6&cmd=dajuan_chakan&huihuabh="
    end_url = "&mode=test"

    cnt = 0

    for i in track(range(457001,459400)):

        response = requests.get(base_url+str(i)+end_url)

        html = response.content
        # print(html)

        is_wait = execute(html,file)
        
        delay = random.choice(delay_choices)  #隨機選取秒數
        print("{} complete! Wait {}".format(i,delay))
        if is_wait:
            time.sleep(delay)  #延遲
            cnt += 1
    # response = requests.get(base_url+"459060"+end_url)
    # html = response.content
    # execute(html,file)
    print("Total:{}".format(cnt))


if __name__ == "__main__":
    main()