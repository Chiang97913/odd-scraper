from unit.unit import robust_request
import datetime


def add_12_hours_and_convert_to_timestamp(datetime_str):
    date_time_obj = datetime.datetime.fromisoformat(datetime_str) + datetime.timedelta(hours=12)
    return int(date_time_obj.timestamp())
def get_jwt():
    url="https://sports-launch-api.sports-188.com/api/v1/member/login?c=44&u=https://www.1eighty8one8eight1pal8.com&reg=China&q=&tz=480&pid=18802"
    req=robust_request(url,method="get")
    return req.headers["Authorization"]

headerss={"Authorization":get_jwt()}

def get_leagua(dates="prestart"):
    if type(dates)==int:
        dates = datetime.date.today() + datetime.timedelta(days=dates)
    url=f"https://landing-sports-api.sbk-188bet.com/api/v1/zh-cn/ROA/sport/1/competition/date/{dates}/match"
    req =robust_request(url, method="get", header=headerss).json()["d"]
    leagua_list=[]
    for i in req["r"]+req["tr"]:
        for j in i["c"]:
            leagua_list.append({"id":j["id"],"name":j["n"]})
    return leagua_list

def get_matchs_by_leagua_id(leagua_id,dates="prestart"):
    if type(dates)==int:
        dates = datetime.date.today() + datetime.timedelta(days=dates)
    match_list = []
    url1 = f"https://landing-sports-api.sbk-188bet.com/api/v2/zh-cn/ROA/sport/1/mop/date/{dates}/competition/{leagua_id}/premium"
    # url1 = f"https://landing-sports-api.sbk-188bet.com/api/v2/zh-cn/ROA/sport/1/mop/date/{dates}/competition/28491/premium"
    req = robust_request(url1, method="get", header=headerss).json()["d"]
    print(req)
    for i in req["s"]["c"]:

        for j in i["e"]:
           # print(j["isc"])
            leagua_name_cn = req["title"]
            leagua_name_en = req["en"]
            home_team_cn = j["h"]
            home_team_en = j["fn"].split("-vs-")[0].replace("-", " ")
            away_team_cn = j["a"]
            away_team_en = j["fn"].split("-vs-")[1].replace("-", " ")
            match_time = add_12_hours_and_convert_to_timestamp(j["edt"])

            if j["fml"] != {} and  leagua_name_cn!="奇幻赛事" and j["isc"]==False:
                odds = {odds['sx']: odds['v'] for item in j["fml"]["main_markets"] if item.get('t') == 'FT_1X2' for odds
                        in item.get('o', [])}
                if odds!={}:
                    home = float(odds["Home"])
                    draw = float(odds["Draw"])
                    away = float(odds["Away"])
                    match = {"leagua_name_cn": leagua_name_cn, "leagua_name_en": leagua_name_en, "match_time": match_time,
                             "home_team_cn": home_team_cn, "home_team_en": home_team_en, "away_team_cn": away_team_cn,
                             "away_team_en": away_team_en,
                             "odds": [{"company": "188bet", "home": home, "draw": draw, "away": away}]
                             }
                    # {datetime.datetime.fromtimestamp(match_time).strftime('%m-%d %H:%M')}
                    print(
                        f"发现188bet比赛:{leagua_name_cn},{leagua_name_en},{datetime.datetime.fromtimestamp(match_time).strftime('%m-%d %H:%M')},{home_team_cn}{home_team_en}:{away_team_cn}{away_team_en},[{home},{draw},{away}]")
                    match_list.append(match)
    return match_list

def get_all_matchs():
    match_list = []
    print("188bet 开始了！")
    for i in get_leagua():
        match_list=match_list+get_matchs_by_leagua_id(i["id"])
    for i in get_leagua("today"):
        match_list=match_list+get_matchs_by_leagua_id(i["id"],"today")
    print("188bet 结束了！")
    return match_list


if __name__ == '__main__':
    print(get_all_matchs())
