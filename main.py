from _plugin.ETTODAY.ettoday import * 
from _plugin.YAHOO.yahoo import *
from _plugin.UDN.udn import *
from _plugin.MERIT.merit import *

def checkDir(path):
 if not os.path.exists(path):
  os.mkdir(path)
      

Source = 'Source\\'
Article = 'Article\\'
Log = 'Log\\'
UPDATE_MODEL = True
THRESHOLD = 20000

checkDir(Source)
checkDir(Article)
checkDir(Log)

#e = ettoday(Source,Article,Log,UPDATE_MODEL,THRESHOLD)
#e.collect()
#e.extract()

y = yahoo(Source,Article,Log,UPDATE_MODEL,THRESHOLD)
y.collect()
#y.extract()



#u = udn(Source,Article,Log,UPDATE_MODEL,THRESHOLD)
#u.collect()
#u.extract()

#m = merit(Source,Article,Log,UPDATE_MODEL,THRESHOLD)
#m.collect()
#m.extract()
