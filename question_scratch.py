import re
import requests
from bs4 import BeautifulSoup as bf
from bs4 import Comment
import random
import time
import sqlite3
from rich.progress import track

MIN_VALUE = 459200
MAX_VALUE = 459750
 
delay_choices = [1, 0.5, 3, 6, 0.05, 2]  #延遲的秒數

answer_list = ['A', 'B', 'C', 'D','E','F','G','H']

def process(question):
    issue = question.find(name='strong').get_text()
        
    choice = question.find(name='blockquote')
    
    answer = question.find(text=lambda text: isinstance(text, Comment))
    answer = re.findall(r"\d*\d", answer)[0]
    res = ""
    for i in range(len(answer)):
        if choice is None:
            res += "对" if int(answer[i]) else "错"
        else:
            if int(answer[i]):
                res += answer_list[i]
        
    return issue,choice,res

def run(html,file=None,word=None,db:sqlite3.Cursor=None):
    Flag = 1
    c= db.cursor()
    soup = bf(html, "lxml")
    questions = soup.find_all(name='div', style="border-bottom:1px dotted #ccc;margin: 10px")
    if questions is None: return
    if word is not None:
        temp=soup.find(string=re.compile(word))
        if temp is None: return
    Flag = 0
    for question in questions:
        # print(re.findall(r"<strong>(.*?)<\strong>",question))
        issue,choice,res = process(question)
        if file is not None:
            if choice is not None:
                file.write(issue+'\n'+choice.get_text()+'\n'+res+'\n\n')
        if db is not None:
            if choice is not None:
                s = c.execute("SELECT * FROM QUESTIONS WHERE ISSUE=? and CHOICE=?",(issue,choice.get_text()))
                if len(list(s))>0:
                    continue
                para = (issue,choice.get_text(),res)
                db.execute("INSERT INTO  QUESTIONS(ISSUE,CHOICE,ANSWER) VALUES(?,?,?)",para)
            else:
                para = (issue,res)
                db.execute("INSERT INTO  QUESTIONS(ISSUE,ANSWER) VALUES(?,?)",para)
    return Flag

def main():
    # fp = open("Question.txt",'a',encoding='utf-8')
    db1 = sqlite3.connect('question.db')
    c = db1.cursor()

    base_url = "http://211.83.159.5/tyexam/redir.php?catalog_id=6&cmd=dajuan_chakan&huihuabh="
    end_url = "&mode=test"

    cnt = 0

    for i in track(range(MIN_VALUE,MAX_VALUE)):

        response = requests.get(base_url+str(i)+end_url)

        html = response.content

        is_wait= run(html,db=db1)
        db1.commit()

        delay = random.choice(delay_choices)  #隨機選取秒數
        print("{} complete! Wait {}".format(i,delay))
        if is_wait:
            time.sleep(delay)  #延遲
        if not is_wait:
            cnt += 1
    # response = requests.get(base_url+"459060"+end_url)
    # html = response.content
    # execute(html,file)
    print("Total:{}".format(cnt))
    db1.close()

if __name__ == "__main__":
    main()