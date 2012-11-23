'''
NBA python box score scraper
obtains box scores from yahoo sports
Author: Nate Olson 11/10/12
'''

from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib2, re, time
from datetime import date, timedelta

def nba_scrape(table, output, DNP):
  for starters in table.findAll("div", attrs= {'class':'bd starters'}):
    rows = starters.findAll('tr')
    for tr in rows:
        re7 = '(title=)'
        re8 = '.*?'
        re9 = '(\\\".*?\\\")'
        rg = re.compile(re7 + re8 + re9)
        m = rg.search(str(tr))
        if m and not "Position" in m.group(2)[1:-1] and not "Minutes in Play" in m.group(2)[1:-1]:
          if m:
              cols = tr.findAll('td')
              stats = ','.join((nbaDateYest,m.group(2)[1:-1]))
              i = 1
              for td in cols:
                  if i != 1:
                    if td.find(text=True):
                        stats = ','.join((stats, td.find(text=True)))
                  i = i + 1
              output.write(stats + "\n")
  for bench in table.findAll("div", attrs= {'class':'bd bench'}):
    rows = bench.findAll('tr')
    for tr in rows:
        re7 = '(title=)'
        re8 = '.*?'
        re9 = '(\\\".*?\\\")'
        rg = re.compile(re7 + re8 + re9)
        m = rg.search(str(tr))
        if m and not "Position" in m.group(2)[1:-1] and not "Minutes in Play" in m.group(2)[1:-1]:
          if m:
              cols = tr.findAll('td')
              stats = ','.join((nbaDateYest,m.group(2)[1:-1]))
              stats = ''.join((stats,','))
              i = 1
              for td in cols:
                  if i != 1:
                    if td.find(text=True):
                        stats = ','.join((stats, td.find(text=True)))
                  i = i + 1
              if not "DNP" in stats:
                output.write(stats + "\n")
              else:
                DNP.write(stats + "\n")


g = open("NBAstats.csv", "w")
g.write("date,player,pos,min,FG,three,FT,P_M,OR,TR,A,T,S,BS,BA,PF,Pts\n")
dnp = open("NBAstatsDNP.csv","w")
dnp.write("date,player,pos,reason\n")

#iterate through a range of days (yesterday to the second number of days before)
for i in range(1,23):
  dateYest=date.today() - timedelta(i)
  nbaDateYest=dateYest.strftime("%Y-%m-%d")
  nbaScoresWeb="http://sports.yahoo.com/nba/scoreboard?d="+nbaDateYest
  page = urllib2.urlopen(nbaScoresWeb).read()
  soup = BeautifulSoup(page)
                     
  #iterate through game Ids and Scrape box at same time
  for b in soup.findAll('a', href=re.compile('/nba/boxscore')):
    url = b['href']
    fullUrl = "http://sports.yahoo.com" + str(url)
    boxurl = urllib2.urlopen(fullUrl).read()
    boxsoup = BeautifulSoup(boxurl)

    #Scrape Team Stats
    t = boxsoup.findAll('div', id = "ysp-reg-box-game_details-game_stats")
    for table in t:
      test = nba_scrape(table,g,dnp)



