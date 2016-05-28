import sqlite3
import sys
import re
import json
from collections import OrderedDict

evidence = r'superspeed'

GOOD_RESULT = 0

try:
	conn = sqlite3.connect("TaskDb.dat")
except:
	print '[-]Error: connect Error'
	sys.exit(0)

cursor = conn.cursor()

res = cursor.execute("select * from Module")
#print res

superspeedtables = []

for i in res:
	tmp = re.findall(evidence, i[0])
	if len(tmp) != 0:
		superspeedtables.append(i[0])

for curtable in superspeedtables:
	sql = "select * from %s"%curtable
	ret = cursor.execute(sql)
	for record in ret:
		tmpstr = str(record[3])
		content = tmpstr.strip()
		dlist = json.loads(content, object_pairs_hook=OrderedDict)
		if dlist['Result'] != GOOD_RESULT:
			dlist['Result'] = GOOD_RESULT
			dlist['Message'] = '\u6b63\u5e38'
			UserData = json.dumps(dlist, sort_keys=True)
			print '[+]UserData: ' + UserData
			try:
				keysql = 'update %s set UserData = (?) where LocalTaskId = %s'%(curtable, record[0])
				print keysql
				cursor.execute(keysql, (UserData,))
				
			except Exception, e:
				print e
				print '[-]Error: update error'
					

conn.commit()
cursor.close()
conn.close()