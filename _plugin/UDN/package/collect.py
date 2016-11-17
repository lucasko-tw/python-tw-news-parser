# -*- coding: utf8 -*-
import re
import urllib,urllib2,os
from time import gmtime, strftime

class collect:

 OVERWRITE = False
 folder = ''
 folder_log = ''
 THRESHOLD = 5
 UPDATE_MODEL = True
 list_cat = ['news','world','edu','people','sports','digital','life'] 
 
 def __init__(self,folder_Source,folder_Log,UPDATE_MODEL,THRESHOLD):
  self.folder = folder_Source
  self.folder_log = folder_Log
  self.UPDATE_MODEL = UPDATE_MODEL
  self.THRESHOLD = THRESHOLD
     
  if not os.path.exists(self.folder):
   os.mkdir(self.folder)
  if not os.path.exists(self.folder_log):
   os.mkdir(self.folder_log)
 
 def getMaxPageNum(self,Page): 
    match_number = re.search(r'<font color="#FF6600">(.*?)</font>',Page,re.S)
    if match_number :
      num = match_number.group(1) 
      return int(num)
    else:
      print '>>getMaxPageNum : not match '  
      return None
  
 def getTitle(self,info): 
    title = re.sub("<[^>]*>",'', info) 
    title = self.reduceSymbol(title)
    if cmp(title.strip(),'') == 0:
      return None
    else : 
      return title
  
 def getLink(self,cat,info): 
    match_link = re.findall(r'href="(.*?)"',info)
    if match_link : 
     link = 'http://mag.udn.com/mag/'+cat+'/'+match_link[0]
     return link
    else:
     return None
 
 def getList_LinkInfo(self,cat,Page):
    list_linkinfo = list() 
    list_info = re.findall(r'<td class="subcategory_topic">(.*?)</td>',Page)
    for info in list_info: 
      title = self.getTitle(info) 
      link = self.getLink(cat,info) 
      if None is not link and None is not title :     
       list_linkinfo.append([title,link])
    return list_linkinfo  
      
 def reduceSymbol(self,sring):
    list_Symbol = ['<','>','?','"','\'','/',':']
    for s in list_Symbol:
      sring = sring.replace(s,'')
    return sring   
 
 def getPage(self,url):
  req = urllib2.Request(url)  
  Page = urllib2.urlopen(req).read()
  return Page
 
 
 def run(self):
  for cat in self.list_cat:
   count = 1
   idx = 0
   while True:
    if count > self.THRESHOLD :
      break     
    url = 'http://mag.udn.com/mag/'+cat+'/index.jsp?f_ORDER_BY=D&pno='+str(idx)+'#itemlist' 
    print 'UDN: %s, Idx:%s'%(cat,str(idx))
    try:   
     Page = self.getPage(url)
     maxNum = self.getMaxPageNum(Page)
     thisNum = (idx)*30
     if thisNum > maxNum :
        break
     else:
          
        #print url
        list_linkinfo = self.getList_LinkInfo(cat,Page)
        
        for title,link in list_linkinfo: 
          path_news = self.folder+"\\"+title
          if os.path.exists(path_news)  :
           print 'UDN: Download file exists.'
           if self.UPDATE_MODEL:
             count += 1
           if count> self.THRESHOLD :
               break
           continue 
             
          
             
         
          page = self.getPage(link)           
          print 'UDN: Download --> '+title
          txt = open(path_news,'w')
          txt.write(page)
          txt.flush()
          txt.close()
          #break
    except Exception,e:
     print str(e)
     str_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
     error = open(self.folder_log+'\\ERROR_collector.log','a')
     error.write(str_time+'\n'+url+':'+str(e)+'\n\n')
     error.flush()
     error.close()   
    finally: 
     idx += 1      
   
if __name__ == '__main__':
   p = collect('Source\\','Log\\')
   p.run()
      
