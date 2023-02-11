import requests

import json

def get_parties():
    url = "https://puoluerekisteri.fi/publicapi/party/registered"
    response = requests.request("GET", url).json()
    
    return response

response = get_parties()

languages = ["fi", "en", "sv"]

parties = []

def make_json(party):
    alias = party["id"]
    name = {
        "en": party["name"]["fi"],
        "fi": party["name"]["fi"],
        "sv": party["name"]["sv"]
    }
    short = {
        "en": "",
        "fi": "",
        "sv": "",
    }
    make_shortening(name, short)      
               
    registered = party['siteInfo']['registered']
    description = {
        "fi": f"Rekisteröity {registered}",
        "en": f"Registered {registered}",
        "sv": f"Registrerad {registered}"
    }
    
    party_json = {
        "alias": alias,
        "name": name,
        "short": short,
        "registered": registered,
        "description": description
    }
    
    parties.append(party_json)
    

def make_shortening(name, short):
    for language in languages:
        for word in name[language].split(" "):
            if word == "r.p.":
                continue
            count = 0
            for letter in word:
                if count == 0:
                    short[language] += f"{letter.upper()}"
                    count += 1
                else:
                    count += 1
                    continue


def name_extraction(party, name):
    if "-" in name and not "," in name:
        name = name.split("- ")
        Finnish = name[0]
        Swedish = name[1]
        
    elif "," in name:
        name = name.replace("ruotsiksi ", "").split(",")
        Finnish = name[0]
        Swedish = name[1]
    
    else:
        Finnish = name
        Swedish = name
    
    if Finnish.startswith("Svenska"):
        Finnish1 = Finnish
        Swedish1 = Swedish
        Finnish = Swedish1
        Swedish = Finnish1
        
    
    party["name"] = {
        "fi": Finnish.strip(),
        "sv": Swedish.strip()
    }
    print(Finnish)
    print(Swedish)
count = 0
for party in response:
    count += 1
    party_description = party["siteInfo"]["partyDesc"]
    party_description_sv = party["siteInfo"]["partyDescSv"]
    name_extraction(party, party["name"])
    make_json(party)
    
def add_parties(parties):
    with open("configuration.json", "r") as f:
        data = json.load(f)
        
    data["parties"] = parties
    
    with open("configuration.json", "w") as f:
        
        json.dump(data, f)
        
add_parties(parties)
