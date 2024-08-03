import datetime
from unit.unit import robust_request

def add_12_hours_and_convert_to_timestamp(datetime_str):
    date_time_obj = datetime.datetime.fromisoformat(datetime_str) + datetime.timedelta(hours=0)
    return int(date_time_obj.timestamp())

def get_all_matchs():
    print("dafabet 开始了！")
    url="https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=1&periodIds=100,200&maxMarketsPerMarketType=100&sortMarketsByPriceDifference=true&eventPathIds=240&sortByEventpath=true&sortByEventpathIds=240,227,24158235,22895,23091,22942,102490,22962,22920,35454808,32415090,31938288,25914812,239,226,215,99917500,10199131,10399131,2500,249,250,1,3700,5000,1700,1250,3400,238,2700,22886,22889,3500,1600,237,1100,2100,22881,1300,50,22888,22878,22877,22884,3,1900,10399132,1200,1400,2900,2,10999130,1800,5,3300,10999126,10999125,10999127,4,10999123,6,10999124,10999129,10999128&page=2&eventsPerPage=2270&l=en"
    req=robust_request(url,method="get").json()
    matchs_list=[]
    for i in req:
        if i["eventPaths"][2]["descriptions"].get("zh_CN","").startswith(i["eventPaths"][1]["descriptions"].get("zh_CN","")):
            leagua_name_cn=i["eventPaths"][2]["descriptions"].get("zh_CN","")
        else:
            leagua_name_cn=f'{i["eventPaths"][1]["descriptions"].get("zh_CN","")} {i["eventPaths"][2]["descriptions"].get("zh_CN","")}'
        leagua_name_en=f'{i["eventPaths"][1]["description"]} {i["eventPaths"][2]["description"]}'
        match_time=add_12_hours_and_convert_to_timestamp(i["eventDate"])
        #print(i["eventDate"])
        desired_description = 'Win/Draw/Win'
        desired_dict = next((item for item in i["markets"] if item['description'] == desired_description), None)
        if desired_dict:
            outcomes = desired_dict['outcomes']
            home_team_en=outcomes[0]["description"]
            home_team_cn=outcomes[0]["descriptions"].get("zh_CN",home_team_en)
            away_team_en=outcomes[2]["description"]
            away_team_cn = outcomes[2]["descriptions"].get("zh_CN",away_team_en)
            ####rule
            home=outcomes[0]['consolidatedPrice']['currentPrice']['decimal']
            draw=outcomes[1]['consolidatedPrice']['currentPrice']['decimal']
            away=outcomes[2]['consolidatedPrice']['currentPrice']['decimal']
            match = {"leagua_name_cn": leagua_name_cn, "leagua_name_en": leagua_name_en, "match_time": match_time,
                     "home_team_cn": home_team_cn, "home_team_en": home_team_en,
                     "away_team_cn": away_team_cn, "away_team_en": away_team_en,
                     "odds": [{"company": "dafabet", "home": home, "draw": draw, "away": away}]}

            print( f"发现dafabet比赛:{match['leagua_name_cn']},{match['leagua_name_en']},{datetime.datetime.fromtimestamp(match['match_time']).strftime('%m-%d %H:%M')},{match['home_team_cn']}{match['home_team_en']}:{match['away_team_cn']}{match['away_team_en']},[{home},{draw},{away}]")

            matchs_list.append(match)
    print("dafabet 结束了！")
    return matchs_list



if __name__ == '__main__':
    aaaa=get_all_matchs()
    print(aaaa)
    print(len(aaaa))