import json

theses = []

languages = ["fi", "en", "sv"]

DEEPL = False
DEEPL_KEY = ""

def get_parties():
    with open("configuration.json", "r") as f:
        data = json.load(f)
    
    parties = data["parties"]
    parties_ids = []
    for party in parties:
        parties_ids.append(party["alias"])
    return data,parties_ids

data, parties_ids = get_parties()

def translate(text, language):
    if DEEPL:
        import deepl

        translator = deepl.Translator(DEEPL_KEY)

        result = translator.translate_text(text, target_lang=language)
        return result.text
    else:
        result = input(f"{text} in {language}: ")
        return result

def these_generator(these, title_fi):
    title = {
        "en": translate(title_fi, "EN"),
        "fi": title_fi,
        "sv": translate(title_fi, "SV")
    }
    statement = {
        "en": translate(these, "EN"),
        "fi": these,
        "sv": translate(these, "SV")
    }
    positions = {
    }
    for party in parties_ids:
        positions[party] = {
            "position": "skip",
            "explanation": {
                "fi": "",
                "en": "",
                "sv": ""
            }
        }
    
    these_json = {
        "title": title,
        "statement": statement,
        "positions": positions
    }
    
    
    theses.append(these_json)

theses_to_run = [('Teesin sisältö', 'Teesin otsikko')]

for these in theses_to_run:
    these_generator(these[0], these[1])

def save():
    with open("configuration.json", "w") as f:
        data["theses"] = theses
        json.dump(data, f)
