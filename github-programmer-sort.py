#!/usr/bin/python
#-*- coding: latin-1 -*-
import urllib,re,xlwt
from operator import itemgetter, attrgetter 

s = 0
def add( itm ):
    global s
    s = itm + s
    return s


ids = ['ifeegoo','chiemy','misparking','wfiskz','subvin','iOnesmile','Jackwaiting','TalentsCZY','chenyunxuan','arrfu','luyonghe','huangshuhan','loveuqian','lhypro']

titleFormatter = "\t\t\t\t %10s \t %10s \t %10s \t %15s \t %25s \t %15s \t %15s \t %15s \t %19s \t  %19s\t"
contentFormatter = "%15s  %10s \t %10s \t %10s \t  %14i \t %25s \t %15s \t %15s \t %15s \t %20f \t "

baseurl = 'https://www.github.com/id'
repositoriesBaseUrl = 'https://github.com/id?tab=repositories'
gistUrl = 'https://gist.github.com/id'
global startNum

print '\t\t\tGitHub 	Ranking 	Situation\n\n'
dataList = []
title2 = ['Id','followers','Starred','Following','Organizations','Last Year Contributons','Longest Streak','Current Streak','Repositories','Stars Per Repository']
for i in xrange(0,len(ids)):
	url = re.sub('id','%s'%ids[i],baseurl,re.S)
	wp = urllib.urlopen(url)
	content = wp.read()
	#  organizationnum  
	orgInfo = re.findall('<h3>Organizations</h3>(.*?)</div>',content,re.S)
	OrganizationsInfo = ''
	if len(orgInfo) != 0:
		OrganizationsInfo = orgInfo[0]
	else :
		break
	# = re.findall('<h3>Organizations</h3>(.*?)</div>',content,re.S)[0]
	orgNum = re.findall('<a(.*?)/></a>',OrganizationsInfo,re.S)
	#print len(orgNum)
	#print OrganizationsInfo
	followerInfo = re.findall('<div class="vcard-stats border-top border-bottom border-gray-light mb-3 py-3">(.*?)</div>',content,re.S)[0]
	nums = re.findall('<strong class="vcard-stat-count d-block">(.*?)</strong>',followerInfo,re.S)
	followerNames = re.findall('<span class="text-muted">(.*?)</span>',followerInfo,re.S)
	contributionInfo = re.findall('<div class="contrib-column contrib-column-first table-column">(.*?)</div>',content,re.S)
	lastYearContributons =  re.findall('contrib-number">(.*?)</span>',content,re.S)
	Longeststreak =  lastYearContributons[1]
	Currentstreak =  lastYearContributons[2]


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
	aData = (ids[i],nums[0],nums[1],nums[2],len(orgNum),re.findall('(.*?) total',lastYearContributons[0],re.S)[0],lastYearContributons[1],lastYearContributons[2],len(repositoriesNum),perStarRatio)
	dataList.append(aData)
	reWp.close()
	wp.close()
#	gistWebInfo.close()


newDataList =  sorted(dataList, key=itemgetter(9,1,5,8),reverse = True)

book = xlwt.Workbook(encoding = 'utf-8',style_compression = 0)
sheet = book.add_sheet('sheet ',cell_overwrite_ok = True)
#title2 = ('个人ID ',' 赞同数','感谢数','提问数','回答数','文章数','收藏','关注了','关注者',' 专栏数','话题数','被浏览次数','综合排名')

for x in xrange(0,len(title2)):
	sheet.write(0,x,title2[x])

for x in xrange(0,len(newDataList)):
	row = newDataList[x]
	for col in xrange(0,len(row)):
		sheet.write(x + 1,col,row[col])
	sheet.write(x + 1,len(title2) - 1,x + 1)
	

savepath = '/Users/wangyunfeng/Desktop/GithuCrawer.xlsx'
book.save(savepath)

#titleContent = titleFormatter % title2

f = open('/Users/wangyunfeng/Desktop/Github.txt','w')
f.writelines(title2)

#print titleFormatter%('id','Agree Number','Thanks Number','Ask Number','Answer Number','Article Number','Collections','Focus Number','Be Focused','Special Column','Topics','Be Reviewed Number')
#newDataList =  sorted(dataList, key=itemgetter(1,2,8,6,11),reverse = True)
for x in xrange(0,len(newDataList)):
	DataContent =  contentFormatter % (newDataList[x])
	f.writelines(DataContent)
#	print contentFormatter % (newDataList[x])

#f.writelines(newDataList)
f.close()









