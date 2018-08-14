# -*- coding: utf-8 -*-

import os
import re
import pymssql
import requests
import datetime


def print_tuple (tuple):
    if len(tuple) == 0:
        print u"[ ]"
    else:
        string = u"["
        for i in range(0, len(tuple) - 1):
            if tuple[i] is not None:
                if isinstance(tuple[i], int) or isinstance(tuple[i], long) or isinstance(tuple[i], float):
                    string = string + unicode(tuple[i]) + u", "
                else:
                    string = string + tuple[i] + u", "
            else:
                string += u"None, "
        string = string + str(tuple[-1]) + u"]"
        print string.encode('utf-8')

conn = pymssql.connect(host='.', port='5889', user='Data@Ngoic.org', password='58891135@#*Ngoic',
                               database='NgoicDataAutoCollection', charset='utf8')
cur = conn.cursor()
pythonTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
cur.execute("update SYS_GlabFlag set PythonTime = %s where Module = 'Illinois压榨利润'", pythonTime)
try:
    conn.commit()
except:
    print "Error at sql."
    conn.rollback()
endDate = datetime.date.today()
cur.execute('SELECT PublishTime FROM SYS_GlabFlag WHERE Module = \'Illinois压榨利润\'')
res = cur.fetchone()
beginDate = res[0].date()
d = beginDate
while d < endDate:
    d = d + datetime.timedelta(7)
    if d.month < 10:
        dMonth = '0' + str(d.month)
    else:
        dMonth = str(d.month)
    if d.day < 10:
        dDate = '0' + str(d.day)
    else:
        dDate = str(d.day)
    r = requests.get('https://search.ams.usda.gov/mndms/' + str(d.year) + '/' + dMonth + '/' + 'GX_GR211' + str(d.year)
                     + dMonth + dDate + '.TXT')
    dStore = d
    if r.text[:9] == '<!DOCTYPE':
        d = d - datetime.timedelta(7)
    while r.text[:9] == '<!DOCTYPE':
        print 'Wrong at ' + 'GX_GR211' + str(d.year) + dMonth + dDate
        d = d + datetime.timedelta(1)
        if d > endDate:
            break
        if d.month < 10:
            dMonth = '0' + str(d.month)
        else:
            dMonth = str(d.month)
        if d.day < 10:
            dDate = '0' + str(d.day)
        else:
            dDate = str(d.day)
        r = requests.get('https://search.ams.usda.gov/mndms/' + str(d.year) + '/' + dMonth + '/' + 'GX_GR211' +
                         str(d.year) + dMonth + dDate + '.TXT')
    if d > endDate:
        break
    with open('GX_GR211' + str(d.year) + dMonth + dDate + '.TXT', 'w') as f:
        f.write(r.text.encode('utf-8'))
        l = r.text.splitlines()
        startLine = 0
        for i in range(0, len(l)):
            if l[i][:len('Soybean prices compared')] == 'Soybean prices compared':
                startLine = i
        currentLine = startLine + 2
        word = re.split('\s+', l[currentLine].strip('\n').strip())
        date = []
        scripts = []
        while word[0] != u'Unit':
            currentLine += 1
            word = re.split('\s+', l[currentLine].strip('\n').strip())
        if len(word) == 10:
            for i in range(0, 3):
                date.append(word[1 + i * 3] + ' ' + word[2 + i * 3] + ' ' + word[3 + i * 3])
        else:
            word = re.split('\s\s+', l[currentLine].strip('\n').strip())
            for i in range(1, 4):
                date.append(word[i])
        currentLine += 1
        attributeLength = [3, 2, 2, 3, 2, 2, 3, 3, 3, 2]
        attributeStart = [u'Soybean oil, crude', u'Oil yield per', u'Value from bushel', u'48% Soybean Meal',
                          u'Meal yield per', u'Value from bushel', u'Value of oil and', u'No. 1 Yellow Soybeans',
                          u'Difference between', u'Estimated Processing']
        firstTime = True
        for i in range(0, len(attributeLength)):
            if attributeLength[i] == 2:
                attribute = l[currentLine].strip('\n').strip() + ' '
                currentLine += 1
            else:
                attribute = l[currentLine].strip('\n').strip() + ' '
                currentLine += 1
                if attribute == ' ':
                    attribute = l[currentLine].strip('\n').strip() + ' '
                else:
                    attribute = attribute + l[currentLine].strip('\n').strip() + ' '
                currentLine += 1
            word = re.split('\s\s+', l[currentLine].strip('\n').strip()[:16])
            attribute += word[0]
            if attribute == u'Value from bushel of soybeans':
                if firstTime:
                    firstTime = False
                else:
                    attribute += u' 1'
            word = re.split('\s+', l[currentLine][16:].strip('\n').strip())
            unit = word[0]
            for j in range(1, 4):
                try:
                    if word[j] == '#N/A':
                        scripts.append((date[j - 1], attribute, unit, None, str(d)))
                    else:
                        scripts.append((date[j - 1], attribute, unit, float(word[j]), str(d)))
                except ValueError:
                    print str(d), l[currentLine].encode('utf-8'), word[j].encode('utf-8')
                except IndexError:
                    print str(d), l[currentLine].encode('utf-8')
            while i + 1 < len(attributeLength) and l[currentLine].strip('\n').strip() != attributeStart[i + 1]:
                currentLine += 1
        cur.executemany(
            "insert into AMS_IllinoisSoybeanSqueezeProfit ("
            "Date, Attribute, "
            "Unit, Value, "
            "PublishDate"
            ") values (%s, %s, %s, %d, %s)"
            , scripts)
        publishTime = d.isoformat()
        cur.execute("update SYS_GlabFlag set PublishTime = %s where Module = 'Illinois压榨利润'", publishTime)
        try:
            conn.commit()
        except:
            print "Error at sql."
            conn.rollback()
        for i in scripts:
            print_tuple(i)
cur.close()
conn.close()
print 'Successful.'
