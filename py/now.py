# -*- coding: utf-8 -*-
import requests
import sys
import re
import os
import string
import time
import datetime
from bs4 import BeautifulSoup
import json

def MkdirFolder(path,Flag=True):
  folder=os.path.exists(path)
  if not folder or Flag:
  	if not folder:
  		os.makedirs(path)
  else:
    x=input("file already exists,overwrite?y/n")
    while x!='y' and x!='n':
      x = input("invalid input,please input again: y/n")
    if x=='n':
      sys.exit()
def ParseData(path,url,headers):
	html = requests.get(url+'A', headers=headers)
	htmlbs=BeautifulSoup(html.text,"html.parser")

	#判断cookie是否已经过期
	if str(htmlbs.title)=='<title>登录_牛客网</title>':
		print("Cookie is out of date, please update it")
		sys.exit()

	#创建比赛文件夹
	MkdirFolder(path,False)
	for id in string.ascii_uppercase:
		html = requests.get(url+id, headers=headers)
		urls=re.findall('data-clipboard-text="[\s\S]*?"',html.text)
		if len(urls)==0:
			sys.exit()
		cpath = path + "/" + id.lower()+"/"
		MkdirFolder(cpath)
		inx=0
		while(inx<len(urls)):
			with open(cpath+"in"+str(int(inx/2+1))+".txt", 'w') as file:
				file.write(urls[inx][21:-1])
			with open(cpath + "ans" + str(int(inx/2+1)) + ".txt", 'w') as file:
				file.write(urls[inx+1][21:-1])
			inx=inx+2
		print(str(id) + " with " + str(int(len(urls) / 2)) + " examples")

#获得要提交问题的questionId
def Get_questionId(text,headers):
	s=re.findall("questionId:[\s\S]*?,",text)
	return int(re.findall(r"\d+",s[0])[0])
#获得要提交问题的tagId
def Get_tagId(text,headers):
	s=re.findall("tagId:[\s\S]*?,",text)
	return int(re.findall(r"\d+",s[0])[0])
#获得要提交问题的subTagId
def Get_subTagId(text,headers):
	s=re.findall("subTagId:[\s\S]*?,",text)
	return int(re.findall(r"\d+",s[0])[0])
#获得要提交问题的doneQuestionId
def Get_doneQuestionId(text,headers):
	s=re.findall("doneQuestionId:[\s\S]*?,",text)
	return int(re.findall(r"\d+",s[0])[0])

def SubmitCode(headers,code,questionId,tagId,subTagId,doneQuestionId):
	url="https://ac.nowcoder.com/nccommon/submit_cd?"
	data = {'questionId': questionId,'tagId': tagId,'subTagId': subTagId,'content':code,'language': 2,'languageName': 'C++11(clang++ 3.9)','doneQuestionId': doneQuestionId}
	r =requests.post(url,headers=headers,data=data)

	#返回代码的提交ID
	return int(re.findall(r"\d+",r.text)[1])

def main():
	#print(os.path.abspath('.').split('/')[-1])
	#print(os.path.abspath('.').split('/')[-2])
	with open("/home/mysakure/.cookie/NowCoderCookie", 'r') as myfile:
		cookie = myfile.read()
	headers = {'Sec-Fetch-Mode': 'no-cors',
			'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36',
           'Referer': 'https://ac.nowcoder.com/acm/contest/1112',
           'cookie':cookie[0:-1]}
	if len(sys.argv)==1:
		print("Usage:\n  now parse [<contest-id>]")
		print("Usage:\n  now submit")
		sys.exit()
	if sys.argv[1]=="parse":
		if len(sys.argv)!=3:
			print("Usage:\n  now parse [<contest-id>]")
			sys.exit()
		url="https://ac.nowcoder.com/acm/contest/"+sys.argv[2]+"/"
		ParseData(sys.argv[2],url,headers)
	if sys.argv[1]=="submit":
		problemid=os.path.abspath('.').split('/')[-1]
		contestid=os.path.abspath('.').split('/')[-2]
		url="https://ac.nowcoder.com/acm/contest/"+contestid+'/'+problemid
		problemhtml=requests.get(url,headers=headers)
		html_bs=BeautifulSoup(problemhtml.text,"html.parser")
		if str(html_bs.title)=='<title>登录_牛客网</title>':
			print("Cookie is out of date, please update it")
			sys.exit()
		prob=str(html_bs.title)
		if problemhtml.status_code==404:
			print("cant access this problem")
			sys.exit()
		questionId=Get_questionId(problemhtml.text,headers)
		tagId=Get_tagId(problemhtml.text,headers)
		subTagId=Get_subTagId(problemhtml.text,headers)
		doneQuestionId=Get_doneQuestionId(problemhtml.text,headers)
		with open(problemid+".cpp", 'r') as myfile:
			code = myfile.read()
		#print("Submit 1277 D GNU G++17 7.3.0")
		submissionId=SubmitCode(headers,code,questionId,tagId,subTagId,doneQuestionId)
		print("Submitted")
		inx = 1
		status_code=0
		print("      #: %d"%submissionId)
		print("   when: %s"%datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		#print("   prob: %s - %s"%(problemid,prob[7:-7]))
		print("   prob: %s"%prob[7:-8])
		while status_code==0:
			submissionTime=round((time.time()-800) * 1000)
			data={'submissionId':submissionId,'tagId':tagId,'subTagId':subTagId,'_':submissionTime}
			response=requests.get("https://ac.nowcoder.com/nccommon/status",params=data)
			status=json.loads(response.text)
			status_code=status["status"]
			if status_code==0:
				print("\r status: running",end="")
			elif status_code==5:
				print("\r status: %s"%status["desc"])
				print("   time: %d ms"%status["seconds"])
				print(" memory: %d KB"%status["memory"])
			else :
				print("\r status: %s"%status["desc"])
				print("\r   memo: %s"%status["memo"][:-5])
			#print(type(status["desc"]))
			inx=inx+1
			time.sleep(1)
#https://ac.nowcoder.com/nccommon/status?submissionId=42562195&tagId=4&subTagId=1&_=1577116814181
main()

'''
	  #: 67499001
   when: 2019-12-24 10:44
   prob: D - Let's Play the Words?
   lang: GNU C++17
 status: Accepted                    
   time: 436 ms
 memory: 33.59 MB

'''
  


