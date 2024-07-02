import requests as rq
import pwinput as pwi

email = "api@cadreon.com"
print(f"This routine  is designed to check only {email}")
print("Other formatted email addresses should be checked with tdcheck.py instead")
pword = "Cadreon@654"
partnerId = "some value"

while partnerId != "":
    partnerId = input("Please provide a Partner ID to check (blank entry to quit): ")
    if not partnerId:
        exit()

    headers = {"Content-Type": "application/json"}
    data = {"Login": f"{email}", "Password": f"{pword}"}

    base_url = "https://api.thetradedesk.com/v3/"
    url = base_url + "authentication"

    res = rq.post(url=url, headers=headers, json=data)
    if res.status_code != 200:
        print(f"0. The email address {email} is causing a {res.status_code} error")

    tok = res.json()["Token"]
    url = base_url + f"partner/{partnerId}"
    headers = {"Content-Type": "application/json", "TTD-Auth": f"{tok}"}

    res = rq.get(url=url, headers=headers)
    if res.status_code != 200:
        print(f"1. The email address {email} is causing a {res.status_code} error")

    partner_name = res.json()["PartnerName"]
    url = base_url + "advertiser/query/partner"
    headers = {"Content-Type": "application/json", "TTD-Auth": f"{tok}"}
    data = {"PartnerId": f"{partnerId}", "PageStartIndex": 0, "PageSize": 1}

    res = rq.post(url=url, headers=headers, json=data)
    result = res.json()["Result"]
    if res.status_code != 200:
        print(f"2. Problem with {partner_name}: returning a {res.status_code} error")

    total_count = res.json()["TotalUnfilteredCount"]
    if total_count != 0:
        advertiser_id = result[0]["AdvertiserId"]
        advertiser_name = result[0]["AdvertiserName"]
        currency_code = result[0]["CurrencyCode"]
    else:
        advertiser_id = "Not available"
        advertiser_name = "Not available"
        currency_code = "Not available"

    print("\n\nPartner Details")
    print("---------------")
    print(f"  Email Address : {email}")
    print(f"   Partner Name : {partner_name}")
    print(f"     Partner Id : {partnerId}")
    print(f"Advertiser Name : {advertiser_name}")
    print(f"  Advertiser Id : {advertiser_id}")
    print(f"  Currency Code : {currency_code}")
    print("===========================================")
    print(f" Total Running Campaign count: {total_count}\n")
