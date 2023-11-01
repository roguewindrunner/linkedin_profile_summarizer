import os
import requests
from dotenv import load_dotenv
import json

from datetime import datetime, timedelta

load_dotenv()


def scrape_linkedin(linkedin_profile_url: str):
    """
    scrape info from linkedin profiles
    """

    headers = {"Authorization": "Bearer " + os.environ["PROXYCURL_API_KEY"]}
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    timestamp = os.path.getmtime("data.json")
    # Convert timestamp to a datetime object
    last_modified_time = datetime.fromtimestamp(timestamp)

    current_time = datetime.now()

    # Define a time difference of one hour
    one_hour_ago = timedelta(minutes=25)
    if current_time - last_modified_time > one_hour_ago:
        with open("data.json", "w") as file:
            json.dump({}, file)

    with open("data.json", "r") as file:
        data = json.load(file)

    # 'data' now contains the content of the JSON file as a dictionary

    if linkedin_profile_url in data:
        print("dumping from local")
        returned = data[linkedin_profile_url]

        return returned

    else:
        response = requests.get(
            api_endpoint, params={"url": linkedin_profile_url}, headers=headers
        )
        response_temp = response.json()
        response_temp = {
            key: value
            for key, value in response_temp.items()
            if value not in ([], "", "", None)
            and key not in ["people_also_viewed", "certifications"]
        }

        if response_temp.get("groups"):
            for group_dict in response_temp.get("groups"):
                group_dict.pop("profile_pic_url")

        data[linkedin_profile_url] = response_temp
        with open("data.json", "w") as f:
            json.dump(data, f)
        return response_temp
    # gist_response = requests.get(
    #    "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"
    # )


#
# return gist_response
