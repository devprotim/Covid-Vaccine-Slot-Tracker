import requests
from datetime import datetime
from requests.sessions import session
base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"

now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
bot_api_key = '...'
api_url = f"https://api.telegram.org/bot{bot_api_key}/sendMessage?chat_id=@__group_id__&text="

group_id = "vaccine_updater"
# this is for district codes and not pincodes it calls the api for districts
district_codes = [725]


def fetch_data_from_cowin(district_id):
    query_params = "?district_id={}&date={}".format(district_id, today_date)
    final_url = base_cowin_url + query_params
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
    response = requests.get(final_url)
    return response


def fetch_data_from_state(district_codes):
    for district_codes in district_codes:
        extract_availability_data(fetch_data_from_cowin(district_codes))


def extract_availability_data(response):
    response_json = response.json()

    for center in response_json["centers"]:
        session = center['sessions'][0]
        if session["available_capacity_dose1"] >= 0 and session["min_age_limit"] == 45:
            message = "Pincode: {}, Name: {}, Slots {}, Minimum Age: {}".format(center["pincode"], center["name"],
                                                                                session["available_capacity_dose1"],
                                                                                session["available_capacity_dose2"],
                                                                                session["min_age_limit"]
                                                                                )
            send_message_telegram(message)


def send_message_telegram(message):
    final_telegram_url = api_url.replace("__group_id__", group_id)
    final_telegram_url = final_telegram_url + message
    response = requests.get(final_telegram_url)
    print(response)


if __name__ == "__main__":
    fetch_data_from_state(district_codes)
