import datetime
from unit.unit import robust_request

def extract_li_values(data, batch_size=5):
    li_values = [item['LI'] for item in data if 'LI' in item]
    for i in range(0, len(li_values), batch_size):
        yield li_values[i:i + batch_size]
def get_leagua():
    url="https://1xbet.com/LineFeed/GetChampsZip?sport=1&lng=cn&country=57"
    req= robust_request(url,method="get").json()
    if req.get("Success") == True:
        return req["Value"]

def get_match_by_leagua(leaguas):
    url = f"https://1xbet.com/LineFeed/Get1x2_VZip?sports=1&champs={leaguas}&count=100&lng=cn&tz=8&mode=4&country=57&getEmpty=true&gr=54"
    match_list = []
    req = robust_request(url, method="get").json()
    if req.get("Success") == True and req['Value']!= []:
        for i in req['Value']:
            leagua_name_cn = i["L"]
            leagua_name_en = i["LE"]
            home_team_cn = i["O1"]
            home_team_en = i["O1E"]
            away_team_cn = i["O2"]
            away_team_en = i["O2E"]
            match_time = int(i["S"])

            c_values = [d['C'] for d in i["E"] if d['T'] in [1, 2, 3]]
            if c_values!=[] and len(c_values)==3 and i.get("DI")==None and leagua_name_cn not in["MLS+","FIFA 23.业余每日联赛","短款足球 D1","超级联赛","学生联赛"] :

                home = float(c_values[0])
                draw = float(c_values[1])
                away = float(c_values[2])
                match = {"leagua_name_cn": leagua_name_cn, "leagua_name_en": leagua_name_en, "match_time": match_time,
                         "home_team_cn": home_team_cn, "home_team_en": home_team_en,
                         "away_team_cn": away_team_cn, "away_team_en": away_team_en,
                         "odds":[{"company": "1xbet", "home": home, "draw": draw,"away": away}]
                        }
                print(
                    f"发现1xbet比赛:{leagua_name_cn},{leagua_name_en},{datetime.datetime.fromtimestamp(match_time).strftime('%m-%d %H:%M')},{home_team_cn}{home_team_en}:{away_team_cn}{away_team_en},[{home},{draw},{away}]")
                match_list.append(match)
    return match_list

def get_all_matchs():
    print("1xbet 开始了！")
    match_list=[]
    leagua_list=get_leagua() 
    for i in leagua_list:
        #print(i)
        match_list=match_list+get_match_by_leagua(i["LI"])
    print("1xbet 结束！")
    return match_list
if __name__ == '__main__':
    aaaa=get_all_matchs()
    #get_match_by_leagua(88637)