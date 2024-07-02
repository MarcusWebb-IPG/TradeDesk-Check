from datetime import datetime
from typing import Any
import requests as rq
import json
import csv
import time


def post_URL(pwd, email, token=None, part_Id=None) -> json:
    if not token:
        urladd = "authentication"
        headers = {"Content-Type": "application/json"}
        data = {"Login": f"{email}", "Password": f"{pwd}"}
    else:
        urladd = "advertiser/query/partner"
        headers = {"Content-Type": "application/json", "TTD-Auth": f"{token}"}
        data = {"PartnerId": f"{part_Id}", "PageStartIndex": 0, "PageSize": 1}

    base_url = "https://api.thetradedesk.com/v3/"
    url = base_url + urladd

    '''
    print(f"Calling URL: {url}")
    print(f"Headers : {headers}")
    print(f"Data: {data}")
'''
    return rq.post(url=url, headers=headers, json=data)


def get_URL(part_Id, token=None) -> Any:
    base_url = "https://api.thetradedesk.com/v3/"
    url = base_url + f"partner/{part_Id}"
    headers = {"Content-Type": "application/json", "TTD-Auth": f"{token}"}

    res = rq.get(url=url, headers=headers)
    partner_name = res.json()["PartnerName"]
    return partner_name


now = datetime.now()

with open(f"OK-{now.strftime("%Y-%m-%d-%H%M%S")}.csv", "a", encoding='utf-8-sig') as dest_file:
    writer = csv.writer(dest_file, delimiter=",")

    with open("BadCredentials.csv", "a", encoding="utf-8-sig") as bad_file:
        bad_writer = csv.writer(bad_file, delimiter=",")

        with open("known-good.csv", "r", encoding='utf-8-sig') as source_file:
            reader = csv.reader(source_file, delimiter=",")

            for i, line in enumerate(reader):
                pwd = line[3]
                email = line[2]
                part_Id = line[1]

                result = post_URL(pwd, email)
                if result.status_code != 200:
                    print(f"\n\tOops - {email} authentication error:")
                    print(f">>>   {result}")
                    print("Writing to BadCredentials.csv")
                    line_to_write = ",".join(map(str, line))
                    bad_file.write(line_to_write + '\n')
                    continue

                token = result.json()["Token"]
                part_name = get_URL(part_Id, token)
                result = post_URL(pwd, email, token, part_Id)
                if result.status_code != 200:
                    print(f"\n\n\t[{email}] - got an error: {result.json()}")
                    print("Writing to BadCredentials.csv")
                    line_to_write = ",".join(map(str, line))
                    bad_file.write(line_to_write + '\n')
                    continue

                resultlist = result.json()["Result"]

                tufc = result.json()["TotalUnfilteredCount"]

                if result.json()["TotalUnfilteredCount"] == 0:
                    msge = '[WARNING] - No Campaigns running for '
                    msge += f' {part_name} - storing previous good credentials'
                    print(f'>>>    {msge}')
                else:
                    advert_id = resultlist[0]["AdvertiserId"]
                    advert_name = resultlist[0]["AdvertiserName"]
                    curr_code = resultlist[0]["CurrencyCode"]
                    total_count = result.json()["TotalUnfilteredCount"]

                row = (line[0], part_Id, email, pwd, curr_code, part_name)
                line_to_write = ','.join(map(str, row))

                print(f"\nValid: {part_name} / {advert_name}({advert_id})")
                print(f"\t(Currently running {total_count} campaigns)\n")

                dest_file.write(line_to_write + '\n')
                print("Sleep for 5 seconds - stop API flooding at TradeDesk")
                time.sleep(5)

source_file.close()
dest_file.close()
