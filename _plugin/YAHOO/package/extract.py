# -*- coding: utf8 -*-
import re,os
import time 
from time import gmtime, strftime
  
class extract : 
 OVER_WRITE = False
 folder_Collect = ''
 folder_log = ''
 folder = ''
 THRESHOLD = 10
 UPDATE_MODE = True
 
 def __init__(self,folder_Source,folder_Article,folder_Log,UPDATE_MODE,THRESHOLD):
  self.folder_Collect = folder_Source 
  self.folder = folder_Article 
  self.folder_log = folder_Log
  self.UPDATE_MODE = UPDATE_MODE
  self.THRESHOLD  = THRESHOLD
     
  if not os.path.exists(self.folder):
   os.mkdir(self.folder)
  if not os.path.exists(self.folder_log):
   os.mkdir(self.folder_log)

 def move(self,folder_path,fn,LogNotMatch):
   folder_LogNotMatch = self.folder_log +LogNotMatch
   if not os.path.exists(folder_LogNotMatch):
    os.mkdir(folder_LogNotMatch)
   time.sleep(1)
   command = 'move '+os.path.join(folder_path, fn)+' '+folder_LogNotMatch
   os.system(command)  
 
 def sorted_ls(self,path): 
     list_dir = os.listdir(path)
     list_file = list() 
     for f in list_dir:
       try :
        
        t = os.stat(os.path.join(path, f)).st_mtime
        list_file.append(f)
       except :
        print 'YAHOO: Unsupported characters in input :',f
        print os.path.join(path, f.replace('?','_'))
        folder_UnsupportedChar = self.folder_log +'UnsupportedChar\\'
        if not os.path.exists(folder_UnsupportedChar):
          os.mkdir(folder_UnsupportedChar)
        time.sleep(1)  
        os.system('move '+os.path.join(path, f)+' '+folder_UnsupportedChar)
         
        continue
     mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
     return list(sorted(list_file, key=mtime ,reverse=True))

   
     
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
 
  
  
 def getCategory(self,Page):
   try: 
     match = re.search(r'<li class="navitem selected(.*?)</li>',Page,re.S)
     match_category = re.search('<span>(.*?)</span>',match.group(1),re.S)
     if match_category :
       category = match_category.group(1)
       category = self.reduceSymbol(category)
       return category
     else:
       #print '>>getCategory : not match.'  
       return None   
   except:
    #print '>>getCategory : except.'     
    return None
  
 
 def getContent(self,Page): 
    match_content = re.search(r"<!-- google_ad_section_start -->(.*?)<!-- google_ad_section_end -->",Page,re.S)
    if match_content :
      content = match_content.group(1)
      content = self.removeTag(content)
      return content
    else:
      #print '>>GetContent : not match '  
      return None
 
 
 def run(self):

  if os.path.exists(self.folder_Collect): 
   list_news = self.sorted_ls(self.folder_Collect)    
   count = 1
   for news in list_news:
    ####  check finished
    if count > self.THRESHOLD and self.UPDATE_MODE  :
      break 
    Page = open(self.folder_Collect+news).read()
    
    category = self.getCategory(Page) 
    content = self.getContent(Page)

    if category == None :
      self.move(self.folder_Collect,news,'NotMatchCat')
      continue
    elif content == None :
      self.move(self.folder_Collect,news,'NotMatchContent')   
      continue
    
    
    news = (news).decode('cp950').encode('utf8')
    dir_cat = self.folder+category+"\\"
    
    dir_cat_utf8 = dir_cat.decode('utf8')
    if not os.path.exists(dir_cat_utf8):
     os.mkdir(dir_cat_utf8)
    path_news = (dir_cat+news).replace('.html','')
    path_news_utf8 = path_news.decode('utf8')
    
    if os.path.exists(path_news_utf8) and self.OVER_WRITE == False:
      print 'YAHOO: Extract file exists. %s' %(path_news.decode('utf8'))
      count += 1
      continue
    try :
      
     txt = open(path_news_utf8 ,'w')
     txt.write(content )
     txt.flush()
     txt.close()
     count = 0  
     if not self.OVER_WRITE :
       print 'YAHOO: Extract --> '+path_news.decode('utf8')
     else: 
       print 'YAHOO: Extract --> (Overwrite) '+path_news
     
    except  Exception, e:
     print e
     str_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
     ERROR = open(self.folder_log+'\\ERROR_parser.log','a')
     ERROR.write(str_time+'\n'+path_news +":\n"+str(e)+'\n\n')
     ERROR.flush()
     ERROR.close()
     continue
  else:
     print 'YAHOO: Not found '+self.folder_Collect 
  
 
if __name__ == '__main__':
    
   p = extract('Source\\','Article\\','Log\\')
   p.run()
    
 
 
 
 
 
 
 
 
 
 














