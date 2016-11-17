# -*- coding: utf8 -*-
import re,os 
from time import gmtime, strftime



class extract: 
 OVER_WRITE = False
 folder_Collect = ''
 folder_log = ''
 folder = ''
 THRESHOLD = 10
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
 
 def sorted_ls(self,path):
     mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
     return list(sorted(os.listdir(path), key=mtime ,reverse=True))
 
 def reduceSymbol(self,sring):
    list_Symbol = ['<','>','?','"','\'','\\','/',':','|']
    for s in list_Symbol:
      sring = sring.replace(s,'')
    return sring
 
 def removeSeq(self,string):
  list_Sequence = ['\n','\r','\t']
  for s in list_Sequence:
    string = string.replace(s,'')  
  return string   
     
 
 def removeTag(self,Page):
  new_Page = re.sub("<[^>]*>",'', Page)
  new_Page = re.sub('&#[0-9]*;','',new_Page)
  list_Symbol = ['&nbsp;','&hellip;','\n','\r','\t','&amp;','&gt;','&lt;','&mdash;','&rsquo;','  ']
  for s in list_Symbol:
    new_Page = new_Page.replace(s,'') 
  
  return new_Page
 
  
  
 def getCategory(self,Page):
   try: 
     match = re.search(r'<td class="path">(.*?)</td>',Page,re.S)
     if match :
       list_a = match.group(0)
       path_Category = re.sub("<[^>]*>",'', list_a).replace('\n','').replace(' ','')
       Category = path_Category.split('/')[2]
       Category = self.removeSeq((Category))
       return Category
     else:
       #print '>>getCategory : not match.'  
       return '其他'   
   except Exception, e: 
    #print '>>getCategory : '+str(e)     
    return '其他'
  
 
 def getContent(self,Page): 
    match_content = re.search(r'<td class="story">(.*?)<td>',Page,re.S)
    if match_content :
      content = match_content.group(1)
      content = self.removeTag(content)
       
      return content
    else:
      print '>>GetContent : not match '  
      return None
 
 
 def run(self) :
  if not os.path.exists(self.folder_Collect):
   print 'UDN: Not found '+self.folder_Collect   
  else:
   list_news = self.sorted_ls(self.folder_Collect)
   
    
   count = 0
   for news in list_news:    
    if count >= self.THRESHOLD:
      
      break  
    Page = open(self.folder_Collect+'\\'+news).read()
    title = news
    
    category = self.getCategory(Page) 
    dir_cat = self.folder+category+"\\" 
    if not os.path.exists(dir_cat):
     print dir_cat 
     os.mkdir(dir_cat)
    path_news = (dir_cat+news)  
    
    if os.path.exists(path_news) and self.OVER_WRITE == False:
      print 'UDN: Extract file exists. '+path_news
      if self.UPDATE_MODEL :
       count += 1
      if count > self.THRESHOLD  :
          break
      continue
    try : 
     content = self.getContent(Page) 
     txt = open(path_news ,'w')
     txt.write(content )
     txt.flush()
     txt.close()
     count = 0  
     if not self.OVER_WRITE :
       print 'UDN: Extract --> '+path_news
     else: 
       print 'UDN: Extract --> (Overwrite) '+path_news
     
    except  Exception, e:
     print e
     str_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
     ERROR = open(self.folder_log+'\\ERROR_parser.log','a')
     ERROR.write(str_time+'\n'+path_news +":"+str(e)+'\n\n')
     ERROR.flush()
     ERROR.close()
     continue
        
    
 

if __name__ == '__main__':
   p = extract('Source\\','Article\\','Log\\')
   p.run()
















