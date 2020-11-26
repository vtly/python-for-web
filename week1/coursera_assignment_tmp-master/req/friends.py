import requests
import datetime

def calc_age(uid):
    ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'

    payload = {
        "access_token": ACCESS_TOKEN,
        "user_ids": uid,
        }

    r = requests.get("https://api.vk.com/method/users.get?v=5.71", params = payload, verify = False)

    if r.status_code != requests.status_codes.codes.ok:
        raise BaseException

    payload = {
        "access_token": ACCESS_TOKEN,
        "user_id": r.json()['response'][0]['id'],
        "fields": "bdate"
    }

    r = requests.get("https://api.vk.com/method/friends.get?v=5.71", params = payload, verify = False)

    if r.status_code != requests.status_codes.codes.ok:
        raise BaseException

    t = {}
    for i in r.json()['response']['items']:
        if i.get('bdate') is not None:
            try:
                bdy = datetime.datetime.now().year - datetime.datetime.strptime(i['bdate'], '%d.%m.%Y').year
                if t.get(bdy) != None:
                    t[bdy] += 1
                else:
                    t[bdy] = 1
            except ValueError:
                pass    
    
    t = list(t.items())
    t.sort(key = lambda tup: (tup[1], -tup[0]), reverse=True)
    return t

if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
