# -*- coding: utf8 -*-
import re,os,sys
from time import gmtime, strftime


class extract:

 THRESHOLD = 100
 OVER_WRITE = False
 folder_Collect = ''
 folder_log = ''
 folder = ''
 UPDATE_MODEL = True
 
 def __init__(self,folder_Source,folder_Article,folder_log,UPDATE_MODEL,THRESHOLD):
  self.folder_Collect = folder_Source
  self.folder_log = folder_log
  self.folder = folder_Article
  self.UPDATE_MODEL = UPDATE_MODEL
  self.THRESHOLD = THRESHOLD
  
  if not os.path.exists(self.folder):
   os.mkdir(self.folder)
  if not os.path.exists(self.folder_log):
   os.mkdir(self.folder_log)
 
 def Log(self,fn,msg):
     str_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
     ERROR = open(self.folder_log+'ERROR_parser.log','a')
     ERROR.write(str_time+'\n'+fn+": "+str(msg)+'\n\n')
     ERROR.flush()
     ERROR.close()  
 
 def reduceSymbol(self,sring):
    list_Symbol = ['<','>','?','"','\'','\\','/',':','\n','\r','\t','|']
    for s in list_Symbol:
      sring = sring.replace(s,'')
    return sring  
 
 def removeTag(self,Page):
  new_Page = re.sub("<[^>]*>",'', Page)
  new_Page = re.sub('&#[0-9]*;','',new_Page)
  list_Symbol = ['&nbsp;','&hellip;','\n','\t','&amp;','&gt;','&lt;','&mdash;','&rsquo;']
  for s in list_Symbol:
    new_Page = new_Page.replace(s,'') 
  
  return new_Page
 
 def CutUnderCenter(self,Page):
   try:
     match_Page = re.search(r"(.*)(</center>)+" ,Page,re.S)
     New_Page = match_Page.group(1)
     return New_Page
   except:
     return Page  
  
 def getTitle_Info(self,Page):
   try:  
     match_title = re.search(r"(<title>)+(.*)(</title>)+",Page,re.S)
     if match_title :
       title_info = match_title.group(2)
       return title_info
     else:
       print '>>GetTitle_Info : not match.'  
       return None   
   except:
    print '>>GetTitle_Info : except.'     
    return None
 
 def getTitleCategory(self,Title_Info):
    try : 
     tmp = Title_Info.split("|")
     title = self.reduceSymbol(tmp[0].strip())
     category = self.reduceSymbol(tmp[1].strip())
     if cmp(category,'') == 0:
      category = '其他'
     return title,category
    except:
     return None,None   
    
 
 def getContent(self,Page): 
    match_content = re.search(r"(<span id='main-news'>)+(.*)(</span>)+",Page,re.S)
    if match_content :
      content = match_content.group(2)
      content = self.removeTag(content)
      return content
    else:
      print '>>GetContent : not match '  
      return None
 
 
 def run(self):
  if not os.path.exists(self.folder_Collect):
   print 'MERIT: Not found '+self.folder_Collect+' folder.'
  else: 
   list_news = sorted(os.listdir(self.folder_Collect),reverse=True)
   count = 0 
   for news in list_news:
   ####  check finished
    if count > self.THRESHOLD and  self.UPDATE_MODEL :
        break
      
    Page = open(self.folder_Collect+news).read()
    Page = self.CutUnderCenter(Page) 
    Title_Info = self.getTitle_Info(Page)
    title , category = self.getTitleCategory(Title_Info)
    if title ==None or category == None:
       print 'Title or Category is NoneType'
       self.Log(news,'Title or Category is NoneType')
       continue 
    dir_cat = self.folder+category+"\\"
    dir_cat_utf8 = dir_cat.decode('utf8')
    
    if not os.path.exists(dir_cat_utf8):
     os.mkdir(dir_cat_utf8)
   
      
    content = self.getContent(Page)
    
    path_news = (dir_cat+title).decode('utf8')
    if os.path.exists(path_news) and self.OVER_WRITE == False:
      print 'MERIT: File exists. '+path_news
      count += 1
      continue
    try : 
     txt = open(path_news,'w')
     txt.write(content)
     txt.flush()
     txt.close()
     count = 0  
     if not self.OVER_WRITE :
       print 'MERIT: Extract --> '+news+' to '+path_news
     else: 
       print news+' --> (Overwrite) '+path_news
     
    except Exception ,e:
     print 'MERIT: Exception: '+str(e)
     self.Log(path_news.encode('utf8'),str(e))
     continue
        
  
  
  
if __name__ == '__main__':
 
  extract('Source\\','Article\\','Log\\').run()  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
