# -*- coding:utf-8 -*-

import os
import re
import requests
from bs4 import BeautifulSoup

f = open('blog.md', 'w')

Latextag = 0

def GetHtmlText(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""

def Clear(text):
    flag = True
    while flag:
        flag = False
        try:
            index = text.index('$$$')
            if Latextag == 0:
                pass
            elif Latextag == 1:
                text = text[:index] + text[index + 1:]
            elif Latextag == 2:
                text = text[:index] + text[index + 2:]
            flag = True
        except:
            break
    return text

def FindInfo(soup, url):
    AllInfo = soup.find('div', {'class', 'problemindexholder'})
    divs = AllInfo.find_all('div')
    title = '# ' + divs[3].get_text()
    f.write('%s\n' % title)
    problem = '## Description:\n' + divs[12].get_text()
    #print(problem)
    problem = Clear(problem)
    f.write('%s\n' % problem)
    Input = '## Input:\n'+ divs[13].get_text()[5:]
    Input = Clear(Input)
    f.write('%s\n' % Input)
    Output = '## Output\n'+ divs[15].get_text()[6:]
    Output = Clear(Output)
    f.write('%s\n' % Output)
    Sample = soup.find('div', {'class', 'sample-test'})
    SampleInputs = Sample.find_all('div', {'class', 'input'})
    SampleOutputs = Sample.find_all('div', {'class', 'output'})
    for i in range(len(SampleInputs)):
        SampleInput = SampleInputs[i].get_text()
        SampleOutput = SampleOutputs[i].get_text()
        f.write('## Sample Input:\n```%s```\n' % SampleInput[5:])
        f.write('## Sample Output:\n```%s```\n' % SampleOutput[6:])
    f.write('### [题目链接](%s)\n\n' % url)
    f.write('## AC代码:\n```c++\n```\n')
def GetProblems(ContestID):
    url='http://codeforces.com/contest/'+ContestID
    #"/contest/1262/problem/B"
    #print(url)
    problems=re.findall('/contest/[1-9].*?/problem/.*?"',GetHtmlText(url))
    return problems
def main():
    global Latextag
    print('Welcome to use codeforces contest crawler\n')
    #Latextag = int(input("Please enter the Latex tag you need(0:'$$$',1:'$$',2:'$'):\n"))
    Latextag=2
    Url = os.getcwd().split('/')[-1]
    print(Url)
    Problem = GetProblems(Url)
    Url ="http://codeforces.com"
    inx=0
    for i in Problem:
        url = Url + i[:-1];
        inx+=1
        if inx&1:
            continue;
        print(url)
        html = GetHtmlText(url).replace('<br />', '\n').replace('</p>', '\n').replace('<img class="tex-graphics" src="','\n![img](http:').replace('" style="max-width: 100.0%;max-height: 100.0%;" />',')\n')
        #html = GetHtmlText(url).replace('<br />', '\n').replace('</p>', '\n')
        soup = BeautifulSoup(html, "html.parser")
        FindInfo(soup, url)
    f.close()

if __name__ == '__main__':
    main()


