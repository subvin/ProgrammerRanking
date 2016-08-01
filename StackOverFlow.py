import urllib2,re
import time
from operator import itemgetter, attrgetter 

ids = ['2531888/ifeegoo','2744948/chiemy','5299868/misparking','5469727/chenyunxuan','5470510/ionesmile',
'5469824/fiskz','5467900/subvin','5470345/jackwaiting','5471377/arrfu','5482463/yonghelu','6092271/lihongyuan',
'6126930/lanjay','6143536/huangshuhan','6592747/sunshore','6546658/hellozihan'];

titleFormatter =   "%20s  %10s \t %10s \t %10s \t %10s \t %10s \t %10s \t %10s \t %10s \t %10s \t %10s \t  %20s \t"
contentFormatter = "%20s  %10s \t %10s \t %10s \t  %10s \t %10s \t %10s \t %10s \t %10s \t "

baseurl = 'http://stackoverflow.com/users/id'
global startNum

dataList = []
for i in xrange(0,len(ids)):    # len(ids)
	url = re.sub('id','%s'%ids[i],baseurl,re.S)
	header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
	req = urllib2.Request(url = url,headers = header)
	#opener = urllib2.build_opener()
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
	#print goldSivelBrone 

	AnswersAndQuestion = re.findall(r'<div class="user-links">(.*?)<div class="user-links">',feedData,re.S)
	answers = re.findall(r'<span class="number">(.*?)</span>',AnswersAndQuestion[0],re.S)
	reSultAnswer = ['0','0','0']
	if len(answers) != 0:
		reSultAnswer = answers
	
	haveTitle = re.findall(r'<h2 class="user-card-name">(.*?)</h2>',feedData,re.S)
	title = re.findall(r'top <b>(.*?)</b> ',haveTitle[0],re.S)
	isHaveTitle = 0;
	if len(title) != 0 :
		isHaveTitle = 1
	aData = (ids[i],repuNum,int(goldSivelBrone[0]),int(goldSivelBrone[1]),int(goldSivelBrone[2]),int(reSultAnswer[0]),int(reSultAnswer[1]),reSultAnswer[2],isHaveTitle)
	dataList.append(aData)
title2 =  ('Total Ranking','id','Reputation','Gold Badges','Silver Badges','Bronze Badges','Answers','Questions','People Reached','Have Title?')
#print titleFormatter%('id','Agree Number','Thanks Number','Ask Number','Answer Number','Article Number','Collections','Focus Number','Be Focused','Special Column','Topics','Be Reviewed Number')


newDataList =  sorted(dataList, key=itemgetter(1,2,3,4,5,8),reverse = True)
#for x in xrange(0,len(newDataList)):
#	print contentFormatter % (newDataList[x])


#f = open('/Users/wangyunfeng/Desktop/stackoverflow.txt','w')

#f.writelines(title)

#print titleFormatter%('id','Agree Number','Thanks Number','Ask Number','Answer Number','Article Number','Collections','Focus Number','Be Focused','Special Column','Topics','Be Reviewed Number')
#newDataList =  sorted(dataList, key=itemgetter(1,2,8,6,11),reverse = True)
#for x in xrange(0,len(newDataList)):
#	DataContent =  contentFormatter % (newDataList[x])
#	f.writelines(DataContent)
#	print contentFormatter % (newDataList[x])

#f.writelines(newDataList)
#f.close()
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
	print DataContent[0]
	name = re.findall('/(.*)',DataContent[0],re.S)[0]
	for j in xrange(0,len(DataContent)):
		if 0 == j:
			rankContent += '|[@%s](%s)'%(name,re.sub('id','%s'%DataContent[0],baseurl,re.S))
		else:
			rankContent += '|%s'%DataContent[j]
	rankContent += '    \n'
	f.write(rankContent)
f.close()





