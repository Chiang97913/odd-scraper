import datetime
import time

from lxml import html
from unit.unit import robust_request
import execjs
def listurl():
    start_date = datetime.datetime.today()
    date_list = []
    for _ in range(5):
        date_list.append(start_date.strftime('%Y-%m-%d'))
        start_date += datetime.timedelta(days=1)
    return date_list
def get_leagua_name():
    endstr=int(time.time())
    cnreq=robust_request(f"https://txt-1-3.speedysurfcdn.net/zh-CN/resource/e/euro-dynamic.js?{endstr}",method="get").text
    enreq=robust_request(f"https://txt-1-3.speedysurfcdn.net/en/resource/e/euro-dynamic.js?{endstr}",method="get").text
    cnreq=eval(cnreq.split("$P.setElement('tournaments',")[1] [:-115])
    enreq=eval(enreq.split("$P.setElement('tournaments',")[1] [:-115])
    #print(cnreq,enreq)
    return cnreq,enreq
def func_match_date(req):
    match_list=[]
    parsed_html = html.fromstring(req.text)
    script_tags = parsed_html.xpath('//script')
    last_script_tag = script_tags[-1]
    script_content = last_script_tag.text_content()
    # print(script_content)
    jstext = script_content.split(";$P.onUpdate")[-1][:-2]
    ctx = execjs.compile("data=" + jstext)
    result = ctx.eval('data')
    for i in result[2][-1][1]:
        leagua_id=i[1]
        match_id=i[2][0]
        home_team=i[2][1]
        away_team=i[2][2]
        match_time=i[2][5]
        for j in i[-2]:
            if type(j[1]) == list and j[1][0] == 5 and j[1][1] == 0 and j[1][2] == 5 and j[1][3] == 0:
                odds=j[-1]
                match_list.append([match_id,leagua_id,match_time,home_team,away_team,odds])
    return match_list

def get_all_matchs():
    print("sbobet 开始了！")
    leaguaname = get_leagua_name()
    matchs_list=[]
    #zh-CN  en
    data_list=listurl()
    for i in data_list:
        enreq=robust_request(f"https://www.sbogogo.com/en/euro/football/{i}",method="get")
        endata=func_match_date(enreq)
        cnreq=robust_request(f"https://www.sbogogo.com/zh-CN/euro/football/{i}",method="get")
        cndata=func_match_date(cnreq)
        matching_items = []
        for item1 in cndata:
            for item2 in endata:
                if item1[0] == item2[0]:
                    matching_items.append((item1, item2))
        for items in matching_items:
            #print(leaguaname)
            for i in leaguaname[0]:
                if i[0]==items[0][1]:
                    leagua_name_cn=i[1]
            for i in leaguaname[1]:
                if i[0]==items[0][1]:
                    leagua_name_en=i[1]

            match_time=datetime.datetime.strptime(items[0][2], "%m/%d/%Y %H:%M")
            if match_time.strftime("%H:%M") == "23:59":
                match_time += datetime.timedelta(minutes=1)
            match_time=int(match_time.timestamp())

            home_team_cn=items[0][3]
            home_team_en=items[1][3]
            away_team_cn=items[0][4]
            away_team_en=items[1][4]
            home=items[0][-1][0]
            draw=items[0][-1][1]
            away=items[0][-1][2]
            match = {"leagua_name_cn": leagua_name_cn, "leagua_name_en": leagua_name_en, "match_time": match_time,
                     "home_team_cn": home_team_cn, "home_team_en": home_team_en,
                     "away_team_cn": away_team_cn, "away_team_en": away_team_en,
                     "odds": [{"company": "sbobet", "home": home, "draw": draw, "away": away}]
                     }
            print(f"发现sbobet比赛:{leagua_name_cn},{leagua_name_en},{datetime.datetime.fromtimestamp(match_time).strftime('%m-%d %H:%M')},{home_team_cn}{home_team_en}:{away_team_cn}{away_team_en},[{home},{draw},{away}]")
            matchs_list.append(match)
    print("sbobet 结束了！")
    return matchs_list

if __name__ == '__main__':
    aaa=get_all_matchs()
    for i in aaa:
        print(i)