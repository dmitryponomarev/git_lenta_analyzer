from lxml import html
from datetime import date
from datetime import timedelta
import requests
import sqlite3

conn = sqlite3.connect('testDB.db')
conn.execute("CREATE TABLE TITLES(Id INTEGER PRIMARY KEY NOT NULL, Title STRING NOT NULL, Date STRING NOT NULL)")

startDate = date(1999, 9, 6)
todayDate = date.today()

id = 1

delta = (todayDate-startDate).days

for x in range(0, delta):
    
    dateToString = startDate.strftime("%Y/%m/%d")

    page = requests.get('https://lenta.ru/%s/' % dateToString)
    tree = html.fromstring(page.content.decode('utf_8', 'ignore'))

    news = tree.xpath('/html/body/div[*]/section[*]/div[*]/div/div[*]/section/div[*]/div[*]/h3/a/text()')

    for new in news:

        conn.execute("INSERT INTO TITLES VALUES (?, ?, ?)", (id, new, dateToString))
        id += 1
    startDate = startDate + timedelta(days=1)
    print x
    conn.commit()
