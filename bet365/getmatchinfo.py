import requests
from lxml import etree
import json, urllib, time, random
from generate import generate_dict, generate_X_net_sync_term
from dicttemplate import dict_leagua_1

home_url = "https://www.365-026.com"
useragent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/93.0.4577.78 Mobile/15E148 Safari/604.1'
headers = {
    'User-Agent': useragent,
}


def inits():
    session = requests.Session(headers=headers)
    response = session.get(home_url)
    script_text = etree.fromstring(response.text, parser=etree.HTMLParser()).xpath('//script[@id="bootjs"]')[0].text
    start_marker = 'var ns_weblib_util ='
    start_index = script_text.find(start_marker) + len(start_marker)
    end_index = script_text.find('; var siteFlags=')
    extracted_content = script_text[start_index:end_index].strip()
    configuration_path = json.loads(extracted_content)
    print("configuration", configuration_path["WebsiteConfig"]["SITE_CONFIG_LOCATION"])
    res_configs = session.get(home_url + configuration_path["WebsiteConfig"]["SITE_CONFIG_LOCATION"]).json()
    SST = res_configs['ns_weblib_util']['WebsiteConfig']['SST']
    SESSION_ID = res_configs['flashvars']['SESSION_ID']
    randomnum = random.random()
    fisttime = int(time.time() * 1000)
    return SESSION_ID, SST, randomnum, fisttime, session


SESSION_ID, SST, randomnum, fisttime, session = inits()


def req(webpath, api):
    dicts = generate_dict(dict_leagua_1, randomnum, useragent, fisttime, SESSION_ID, api,
                          f'#{webpath.replace("#", "/")}')
    print(dicts)
    X_net_sync_term = generate_X_net_sync_term(dicts, SST)
    session.headers.update({"X-Net-Sync-Term": X_net_sync_term})
    res = session.get(home_url + api)
    print(res.text)
    return res.text

def get_index_leaguas():
    webpath = "#AS#B1#K^5#"
    api = f"/splashcontentapi/soccertab?lid={langid}&zid=3&pd={urllib.parse.quote(webpath)}&cid=88&cgid=1&ctid=88"
    return req(webpath, api)

def get_leaguas_by_country(PD_country):
    webpath = "#AS#B1#K^5#"
    api = f"/splashcontentapi/soccerpartial?lid={langid}&zid=3&pd=%23AS%23B1%23C1%23D1002%23{PD_country}%23I40%23O2%23&cid=88&cgid=1&ctid=88"
    return req(webpath, api)


def get_matchs_by_leagua(PD_leaguas):
    webpath = f"#AC#B1#C1#D1002#{PD_leaguas}#G40#"
    api = f"/matchmarketscontentapi/markets?lid={langid}&zid=3&pd=%23AC%23B1%23C1%23D1002%23{PD_leaguas}%23G40%23&cid=88&cgid=1&ctid=88"
    return req(webpath, api)

if __name__ == '__main__':
    from parse_res import convert_to_dict
    langid = 10
    aaa=get_index_leaguas()
    print(aaa)
    print(convert_to_dict(aaa))
    aaa = get_leaguas_by_country("D1002")
    print(aaa)
    print(convert_to_dict(aaa))