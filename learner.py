import urllib.request
import urllib.parse
import json
import random
import os
import html

# Discord requires integer color codes. Here are the Dracula colors converted.
COLORS = {
    "PURPLE": 12424185, "GREEN": 5307011, "CYAN": 9169363, 
    "ORANGE": 16758892, "YELLOW": 15858316, "PINK": 16742854, "RED": 16733525
}

def fetch_data(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except:
        return None

def get_random_word_definition():
    for _ in range(5):  # Added retry limit to prevent infinite loops
        try:
            word_raw = fetch_data("https://random-word-api.herokuapp.com/word?number=1")
            target_word = word_raw[0]
            dict_data = fetch_data(f"https://api.dictionaryapi.dev/api/v2/entries/en/{target_word}")

            definition = ""
            part_of_speech = "unknown"

            for entry in dict_data:
                for meaning in entry.get('meanings', []):
                    part_of_speech = meaning.get('partOfSpeech', part_of_speech)
                    for d in meaning.get('definitions', []):
                        if not definition:
                            definition = d.get('definition')
                            break
                    if definition: break
                if definition: break

            if definition:
                return {"name": f"Vocabulary: {target_word.capitalize()} ({part_of_speech})", "value": definition, "inline": False}
        except:
            continue
    return None

def run_trivia():
    try:
        data = fetch_data("https://opentdb.com/api.php?amount=1")
        if data and data.get('response_code') == 0:
            item = data['results'][0]
            question = html.unescape(item['question'])
            correct = html.unescape(item['correct_answer'])
            options = [html.unescape(ans) for ans in item['incorrect_answers']] + [correct]
            random.shuffle(options)

            options_text = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])
            
            return {
                "title": "Interactive Challenge (Trivia)",
                "color": COLORS["PURPLE"],
                "fields": [
                    {"name": "Category & Difficulty", "value": f"{item['category']} | {item['difficulty'].upper()}", "inline": False},
                    {"name": "Question", "value": question, "inline": False},
                    {"name": "Options", "value": options_text, "inline": False},
                    {"name": "Answer", "value": f"||{correct}||", "inline": False} # Hidden in spoiler tag
                ]
            }
    except:
        return None

def generate_discord_payload():
    embeds = []
    
    # 1. Main Knowledge Embed
    main_embed = {
        "title": "Zero-Paywall Knowledge Sync",
        "description": "Daily global intelligence gathered successfully.",
        "color": COLORS["CYAN"],
        "fields": []
    }

    # Mission
    activity = fetch_data("https://bored-api.appbrewery.com/random")
    if activity:
        main_embed["fields"].append({"name": "Mission", "value": activity.get('activity', 'N/A'), "inline": False})

    # Wikipedia
    topics = ["Cryptography", "Archaeology", "Astrophysics", "Marine_biology", "Ancient_Rome", "Cybersecurity", "Philosophy"]
    wiki_cat = random.choice(topics)
    try:
        params = {'action': 'query', 'list': 'categorymembers', 'cmtitle': f'Category:{wiki_cat}', 'cmlimit': 20, 'cmnamespace': 0, 'format': 'json'}
        list_data = fetch_data(f"https://en.wikipedia.org/w/api.php?{urllib.parse.urlencode(params)}")
        if list_data:
            title = random.choice(list_data['query']['categorymembers'])['title']
            wiki = fetch_data(f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}")
            if wiki:
                main_embed["fields"].append({
                    "name": f"Wiki: {wiki['title']} ({wiki_cat})", 
                    "value": f"{wiki['extract']}\n[Read More]({wiki['content_urls']['desktop']['page']})", 
                    "inline": False
                })
    except: pass

    # Vocabulary
    vocab_field = get_random_word_definition()
    if vocab_field:
        main_embed["fields"].append(vocab_field)

    # Insights
    advice = fetch_data("https://api.adviceslip.com/advice")
    fact = fetch_data("https://uselessfacts.jsph.pl/api/v2/facts/random")
    if advice and fact:
        main_embed["fields"].append({
            "name": "Insights", 
            "value": f"**Advice:** {advice['slip']['advice']}\n**Fact:** {fact['text']}", 
            "inline": False
        })

    embeds.append(main_embed)

    # 2. Trivia Embed
    trivia_embed = run_trivia()
    if trivia_embed:
        embeds.append(trivia_embed)

    return {"username": "Lumina", "embeds": embeds}

def main():
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Error: DISCORD_WEBHOOK_URL environment variable not set.")
        return

    payload = generate_discord_payload()
    
    # Send to Discord
    req = urllib.request.Request(
        webhook_url, 
        data=json.dumps(payload).encode('utf-8'), 
        headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    )
    
    try:
        urllib.request.urlopen(req)
        print("Payload sent to Discord successfully.")
    except Exception as e:
        print(f"Failed to send to Discord: {e}")

if __name__ == "__main__":
    main()
