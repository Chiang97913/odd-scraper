
import datetime
from unit.unit import robust_request


def get_matchs(dates):
    future_date = datetime.date.today() + datetime.timedelta(days=dates)
    #url1=f"https://www.start931.com/sports-service/sv/am/events?_g=1&btg=1&c=&d={future_date}&ec=&ev=&g=&inl=false&l=1&lg=&lv=&me=0&mk=0&more=false&o=1&ot=1&pa=0&pimo=0%2C1%2C8%2C39%2C3&pn=-1&sp=29&tm=0&v=0&wm=&locale=zh_CN&_=1702961763370&withCredentials=true"
    url=f"https://www.start931.com/sports-service/sv/compact/events?_g=1&btg=2&c=&cl=1&d={future_date}&inl=false&l=3&me=0&mk=0&more=false&o=0&ot=1&pa=0&pimo=0,1,8,39,3,6,7,4,5&pn=-1&sp=29&tm=0&v=0&locale=zh_CN&withCredentials=true"
    aaaa= robust_request(url,method="get").json()
    match_list=[]
    for i in  aaaa:
        if aaaa[i]!=None and aaaa[i]!=0 and aaaa[i]!=[]:
            for j in aaaa[i][0][2]:
                for k in j[2]:
                    leagua_name_cn=j[1]
                    leagua_name_en=j[-1]
                    home_team_cn= k[1]
                    home_team_en= k[24]
                    away_team_cn= k[2]
                    away_team_en= k[25]
                    if home_team_cn == "艾贝斯费特联" and home_team_en == "Ayr United":
                        home_team_cn = "艾尔"
                    if away_team_cn == "艾贝斯费特联" and away_team_en == "Ayr United":
                        away_team_cn = "艾尔"

                    match_time= int(int(k[4])/1000)
                    if k[8].get("0")!=None and k[8].get("0")[0][1]!='' and k[8].get("0")[0][1]!=None and (away_team_cn!="斯托克波特" and match_time!=1704553200):
                        home=float(k[8]["0"][0][1])
                        draw=float(k[8]["0"][0][2])
                        away=float(k[8]["0"][0][0])
                        match = {"leagua_name_cn": leagua_name_cn, "leagua_name_en": leagua_name_en,
                                 "match_time": match_time,
                                 "home_team_cn": home_team_cn, "home_team_en": home_team_en,
                                 "away_team_cn": away_team_cn, "away_team_en": away_team_en,
                                 "odds": [{"company": "pinnacle", "home": home, "draw": draw, "away": away}]
                                 }

                        print(f"发现平博比赛:{leagua_name_cn},{leagua_name_en},{datetime.datetime.fromtimestamp(match_time).strftime('%m-%d %H:%M')},{home_team_cn}{home_team_en}:{away_team_cn}{away_team_en},[{home},{draw},{away}]")
                        match_list.append(match)
    return match_list


def get_all_matchs():
    matchs=[]
    print("pinnacle 开始了！")
    for i in range(5):
        matchs=matchs+get_matchs(i)
    print("pinnacle 结束了！")
    return matchs
if __name__ == '__main__':

    print(get_all_matchs())

