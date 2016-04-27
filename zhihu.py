#!/usr/bin/python
#-*- coding: latin-1 -*-
import urllib2,re
from operator import itemgetter, attrgetter 

ids = ['ifeegoo','chiemy','misparking','wfiskz','subvin','iOnesmile','Jackwaiting','chen-yun-xuan-29','arrfu','yonghelu','li-hong-yuan-54','lan-jie-82-66','huangshuhan']

titleFormatter =   "\t%20s  \t\t%10s \t \t%10s \t    \t\t%10s \t \t\t  %10s \t \t %10s \t \t %10s \t \t %10s \t \t%10s \t \t%10s \t \t%10s \t  \t%20s \t"
contentFormatter = "%20s  %10s \t %10s \t %10s \t  %10s \t %10s \t %10s \t %10s \t %10s  %10s \t %10s \t %10s \t"

baseurl = 'https://www.zhihu.com/people/id'
abouturl = 'https://www.zhihu.com/people/id/about'
global startNum

dataList = []
print '\t\t\t\t This Is  Our 		Snaillove 		Team 		Zhihu 		Ranking \n'
for i in xrange(0,len(ids)): #   
	url = re.sub('id','%s'%ids[i],baseurl,re.S)
	wp = urllib2.urlopen(url)
	content = wp.read()
	agreeNum = re.findall(r'<span class="zm-profile-header-user-agree"><span class="zm-profile-header-icon"></span><strong>(.*?)</strong>',content,re.S)[0]
	thanksNum = re.findall(r'<span class="zm-profile-header-user-thanks"><span class="zm-profile-header-icon"></span><strong>(.*?)</strong>',content,re.S)[0]
	askNum = re.findall(r'<span class="num">(.*?)</span>',content,re.S)
	focusNumStruct = re.findall(r'<div class="zm-profile-side-following zg-clear">(.*?)</div>',content,re.S)[0]
	focusNum = re.findall(r'<strong>(.*?)</strong><label>',focusNumStruct,re.S)
	proFocus = re.findall(r'class="zg-link-litblue"><strong>(.*?)</strong>',content,re.S)

	beReviewed = re.findall(r'<div class="zm-side-section-inner">(.*?)</div>',content,re.S)[1]
	beReviewedNumber = re.findall(r'<strong>(.*?)</strong>',beReviewed,re.S)[0]
	if len(proFocus) == 1:
		proFocus.insert(0,'0')
	realProFocusNum = re.findall(r'(.*?) ',proFocus[0],re.S)
	focus = '0'
	if len(realProFocusNum) == 0:
		focus = proFocus[0]
	else:
		focus = realProFocusNum[0]

	aboutUrl = re.sub('id','%s'%ids[i],abouturl,re.S)
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'}
	req = urllib2.Request(url = aboutUrl,headers = header)
	#opener = urllib2.build_opener()
	feedData = urllib2.urlopen(req).read()
	collectionPage = re.findall(r'<div class="zm-profile-header-description editable-group " data-name="description">(.*?)<span class="content">',feedData,re.S)
	#print collectionPage
	aData = (ids[i],int(agreeNum),int(thanksNum),int(askNum[0]),int(askNum[1]),int(askNum[2]),int(askNum[3]),focusNum[0],focusNum[1],focus,re.findall(r'(.*? )',proFocus[1],re.S)[0],beReviewedNumber)
	dataList.append(aData)

#f = open('/Users/wangyunfeng/Desktop/zhihu.txt','w')
title2 = ('总排名','个人ID ',' 赞同数','感谢数','提问数','回答数','文章数','收藏','关注了','关注者',' 专栏数','话题数','被浏览次数')
#title = titleFormatter% title2 #('id','Agree Number','Thanks Number','Ask Number','Answer Number','Article Number','Collections','Focus Number','Be Focused','Special Column','Topics','Be Reviewed Number')

#print title
#f.writelines(title)

#print titleFormatter%('id','Agree Number','Thanks Number','Ask Number','Answer Number','Article Number','Collections','Focus Number','Be Focused','Special Column','Topics','Be Reviewed Number')
newDataList =  sorted(dataList, key=itemgetter(1,2,8,6,11),reverse = True)
#for x in xrange(0,len(newDataList)):
#	DataContent =  contentFormatter % (newDataList[x])
#	f.writelines(DataContent)
#	print contentFormatter % (newDataList[x])

#f.writelines(newDataList)
#f.close()




f = open('/Users/wangyunfeng/Desktop/Zhihu.txt','w')

ranktitle = ''
for x in xrange(0,len(title2)):
	ranktitle += '|%s'%title2[x]
ranktitle += '    \n'
print ranktitle
f.write(ranktitle)
tableFormatter = ''
for x in xrange(0,len(title2)):
	tableFormatter += '|---'
tableFormatter += '|    \n'
f.write(tableFormatter)


#print titleFormatter%('id','Agree Number','Thanks Number','Ask Number','Answer Number','Article Number','Collections','Focus Number','Be Focused','Special Column','Topics','Be Reviewed Number')

for x in xrange(0,len(newDataList)):
	rankContent = '|#%i'% int(x+1)
	DataContent =  newDataList[x]
	for j in xrange(0,len(DataContent)):
		if 0 == j:
			rankContent += '|[@%s](%s)'%(DataContent[0],re.sub('id','%s'%DataContent[0],baseurl,re.S))
		else:
			rankContent += '|%s'%DataContent[j]
	rankContent += '    \n'
	f.write(rankContent)
print rankContent



#	print contentFormatter % (newDataList[x])

#f.writelines(newDataList)
f.close()
