import os, sys, time
import urllib2,re
import time
from operator import itemgetter, attrgetter 
import threading
import xlwt

ids = ['2531888/ifeegoo','2744948/chiemy','5299868/misparking','5469727/chenyunxuan','5470510/ionesmile','5469824/fiskz','5467900/subvin','5470345/jackwaiting','5471377/arrfu','5482463/yonghelu','6092271/lihongyuan','6126930/lanjay','6143536/huangshuhan']
realIds = ['ifeegoo','chiemy','misparking','chenyunxuan''ionesmile','fiskz','subvin','jackwaiting','arrfu','yonghelu','lihongyuan','lanjay','huangshuhan']
titleFormatter =   "%20s  %10s \t %10s \t %10s \t %10s \t %10s \t %10s \t %10s \t %10s \t "
contentFormatter = "%20s  %10s \t %10s \t %10s \t  %10s \t %10s \t %10s \t %10s \t %10s \t "

baseurl = 'http://stackoverflow.com/users/id'
global startNum

dataList = []
threads = []
print '\t   \t    \t  StackOverFlow 		Ranking 		Situation! \n\n'
class myThread (threading.Thread):
    def __init__(self,url,realId):
        threading.Thread.__init__(self)
        self.url = url
        self.realId = realId
    def run(self):
    	header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    	req = urllib2.Request(url = self.url,headers = header)
    	feedData = urllib2.urlopen(req).read()			
    	badges = re.findall(r'<div id="avatar-card" class="avatar-card">(.*?) <div class="row col-content">',feedData,re.S)
    	repuNum = 0
    	reputation = re.findall(r'title="reputation">(.*?)<span',badges[0],re.S)
    	if len(reputation) != 0:
    		repuNum = int(reputation[0])
		goldSivelBrone = ['0','0','0']
		if len(badges) != 0:
			item = re.findall(r'<span class="badgecount">(.*?)</span>',badges[0],re.S)
		 	if len(item) == 1:
				goldSivelBrone = ['0','0',item[0]]
			elif len(item) == 2:
				goldSivelBrone = ['0',item[0],item[1]]
			elif len(item) == 3:
				goldSivelBrone = [item[0],item[1],item[2]]
		AnswersAndQuestion = re.findall(r'<div class="user-links">(.*?)<div class="user-links">',feedData,re.S)
		answers = re.findall(r'<span class="number">(.*?)</span>',AnswersAndQuestion[0],re.S)
		reSultAnswer = ['0','0','0']
		if len(answers) != 0:
			reSultAnswer = answers
		haveTitle = re.findall(r'<h2 class="user-card-name">.*?</h2>',feedData,re.S)
		title = re.findall(r'<script>(.*?)</script>',haveTitle[0],re.S)
		isHaveTitle = 0;
		if len(title) != 0 :
			isHaveTitle = 1

		mutex = threading.Lock()
		mutex.acquire()
		aData = (self.realId,repuNum,int(goldSivelBrone[0]),int(goldSivelBrone[1]),int(goldSivelBrone[2]),int(reSultAnswer[0]),int(reSultAnswer[1]),reSultAnswer[2],isHaveTitle)
		dataList.append(aData)
		print aData
		mutex.release()


for i in xrange(0,len(ids)):  # 
	url = re.sub('id','%s'%ids[i],baseurl,re.S)
	athread = myThread(url,ids[i])
	athread.setDaemon(True)
	athread.start()
	threads.append(athread)

for t in threads:
    t.join()


book = xlwt.Workbook(encoding = 'utf-8',style_compression = 0)
sheet = book.add_sheet('sheet ',cell_overwrite_ok = True)
title2 = ('Total Ranking','id ','Reputation','Gold Badges','Silver Badges','Bronze Badges','Answers','Questions','People Reached','Have Title?')

for x in xrange(0,len(title2)):
	sheet.write(0,x,title2[x])

newDataList =  sorted(dataList, key=itemgetter(1,2,3,4,5,8),reverse = True)
#for x in xrange(0,len(newDataList)):
#	row = newDataList[x]
#	for col in xrange(0,len(row)):
#		sheet.write(x + 1,col,row[col])
#	sheet.write(x + 1,len(title2) - 1,x + 1)
	

#savepath = '/Users/wangyunfeng/Desktop/StackOverFlowCrawer.xlsx'
#book.save(savepath)

#title =  '                  id ','Reputation','\tGold Badges','\tSilver Badges','\tBronze Badges','\t\tAnswers','\tQuestions','\tPeople Reached','\tHave Title?'
#print titleFormatter%('id','Agree Number','Thanks Number','Ask Number','Answer Number','Article Number','Collections','Focus Number','Be Focused','Special Column','Topics','Be Reviewed Number')
#print titleFormatter % title2


f = open('/Users/wangyunfeng/Desktop/StackOverFlow.txt','w')
ranktitle = ''
for x in xrange(0,len(title2)):
	ranktitle += '|%s'%title2[x]
ranktitle += '    \n'
f.write(ranktitle)
tableFormatter = ''
for x in xrange(0,len(title2)):
	tableFormatter += '|---'
tableFormatter += '|    \n'
f.write(tableFormatter)
for x in xrange(0,len(newDataList)):
	rankContent = '|#%i'% int(x+1)
	DataContent =  newDataList[x]
	for j in xrange(0,len(DataContent)):
		if 0 == j:
			rankContent += '|[@%s](%s)'%(re.findall('%s',DataContent[0],re.S),re.sub('id','%s'%DataContent[0],baseurl,re.S))
		else:
			rankContent += '|%s'%DataContent[j]
	rankContent += '    \n'
	f.write(rankContent)
f.close()
