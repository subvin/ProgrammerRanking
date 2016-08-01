#!/usr/bin/python
#-*- coding: latin-1 -*-
import urllib,re,xlwt
from operator import itemgetter, attrgetter 

ids = ['ifeegoo','chiemy','misparking','wfiskz','subvin','iOnesmile',
'jackwaiting','chenyunxuan','arrfu','luyonghe','Lewanny','jarylan',
'huangshuhan','HelloZihan','sunshore'];

titleFormatter = "\t\t\t\t %10s \t %10s \t %10s \t %15s \t %25s \t %15s \t %15s \t %15s \t %19s \t  %19s\t"
contentFormatter = "%15s  %10s \t %10s \t %10s \t  %14i \t %25s \t %15s \t %15s \t %15s \t %20f \t "

baseurl = 'https://www.github.com/id'
repositoriesBaseUrl = 'https://github.com/id?tab=repositories'
gistUrl = 'https://gist.github.com/id'
global startNum

print '\t\t\tGitHub 	Ranking 	Situation\n\n'
dataList = []
title2 = ['Total Ranking','Id','followers','Starred','Following','Organizations','Repositories','Stars Per Repository']
print len(ids)
for i in xrange(0,len(ids)):  # len(ids)
	url = re.sub('id','%s'%ids[i],baseurl,re.S)
	print url
	wp = urllib.urlopen(url)
	content = wp.read()
	#  organizationnum  
	orgInfo = re.findall('<h3>Organizations</h3>(.*?)</div>',content,re.S)
	OrganizationsInfo = ''
	if len(orgInfo) != 0:
		OrganizationsInfo = orgInfo[0]
	# = re.findall('<h3>Organizations</h3>(.*?)</div>',content,re.S)[0]
	if OrganizationsInfo != '':
		orgNum = re.findall('<a(.*?)/></a>',OrganizationsInfo,re.S)

	#print len(orgNum)
	#print OrganizationsInfo
	followerInfo = re.findall('<div class="vcard-stats border-top border-bottom border-gray-light mb-3 py-3">(.*?)</div>',content,re.S)[0]
	nums = re.findall('<strong class="vcard-stat-count d-block">(.*?)</strong>',followerInfo,re.S)
	followerNames = re.findall('<span class="text-muted">(.*?)</span>',followerInfo,re.S)
	contributionInfo = re.findall('<div class="contrib-column contrib-column-first table-column">(.*?)</div>',content,re.S)
	#lastYearContributons =  re.findall('contrib-number">(.*?)</span>',content,re.S)
	#print lastYearContributons
	#Longeststreak =  lastYearContributons[1]
	#Currentstreak =  lastYearContributons[2]


	repositoriesUrl = re.sub('id','%s'%ids[i],repositoriesBaseUrl,re.S)  #//repositoriesBaseUrl
	reWp = urllib.urlopen(repositoriesUrl)
	repositoriesContent = reWp.read()

	repositoriesNum = re.findall('<div class="repo-list-stats">(.*?)</div>',repositoriesContent,re.S)
	starNum = 0
	for x in xrange(0,len(repositoriesNum)):
		repData = repositoriesNum[x]
	   	starNum += int(re.findall('</path></svg>(.*?)</a>',repData,re.S)[0])
	perStarRatio = 0.0
	if len(repositoriesNum) != 0:
		perStarRatio = float(float(starNum)/len(repositoriesNum))



	#if (i == 0):
	#	title2 = ['Id',followerNames[0],followerNames[1],followerNames[2],'Organizations','Last Year Contributons','Longest Streak','Current Streak','Repositories','Stars Per Repository']
	orgCount = 0
	if len(orgNum) != 0:
		orgCount = len(orgNum)
		
	#re.findall('(.*?) total',lastYearContributons[0],re.S)[0],lastYearContributons[1],lastYearContributons[2],
	aData = (ids[i],nums[0],nums[1],nums[2],orgCount,len(repositoriesNum),perStarRatio)
	dataList.append(aData)
	reWp.close()
	wp.close()
#	gistWebInfo.close()


newDataList =  sorted(dataList, key=itemgetter(6,1,5),reverse = True)

print len(newDataList)

f = open('/Users/wangyunfeng/Desktop/Github.txt','w')
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
			rankContent += '|[@%s](%s)'%(DataContent[0],re.sub('id','%s'%DataContent[0],baseurl,re.S))
		else:
			rankContent += '|%s'%DataContent[j]
	rankContent += '    \n'
	f.write(rankContent)
f.close()
