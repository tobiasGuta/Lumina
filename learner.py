import urllib.request
import urllib.parse
import json
import random
import os
import html
import re

# --- DRACULA THEME COLORS ---
C = {
    "BG": "\033[48;2;40;42;54m", "FG": "\033[38;2;248;248;242m",
    "CYAN": "\033[38;2;139;233;253m", "PURPLE": "\033[38;2;189;147;249m",
    "GREEN": "\033[38;2;80;250;123m", "ORANGE": "\033[38;2;255;184;108m",
    "YELLOW": "\033[38;2;241;250;140m", "PINK": "\033[38;2;255;121;198m",
    "COMMENT": "\033[38;2;98;114;164m", "RED": "\033[38;2;255;85;85m",
    "RESET": "\033[0m", "BOLD": "\033[1m"
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def fetch_data(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except:
        return None

# ==========================================
# TERMINAL UI FUNCTIONS (For Local Use)
# ==========================================
def draw_box(title, content, color):
    width = 70
    print(f"{color}┌─ {C['BOLD']}{title.upper()} {'─' * (width - len(title) - 4)}┐{C['RESET']}")
    for line in content:
        words = str(line).split()
        current_line = ""
        for word in words:
            if len(current_line + word) + 1 <= width - 4:
                current_line += (word + " ")
            else:
                print(f"{color}│ {C['FG']}{current_line.ljust(width-4)} {color}│{C['RESET']}")
                current_line = word + " "
        print(f"{color}│ {C['FG']}{current_line.ljust(width-4)} {color}│{C['RESET']}")
    print(f"{color}└{'─' * (width - 2)}┘{C['RESET']}")

def get_random_word_definition():
    found_valid_word = False
    retries = 0
    while not found_valid_word and retries < 5:
        retries += 1
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
                draw_box("Vocabulary Expansion", [
                    f"Word: {target_word.capitalize()} ({part_of_speech})",
                    "", 
                    f"Definition: {definition}"
                ], C['ORANGE'])
                found_valid_word = True
        except: 
            continue

def run_trivia():
    try:
        data = fetch_data("https://opentdb.com/api.php?amount=1")
        if data and data['response_code'] == 0:
            item = data['results'][0]
            question = html.unescape(item['question'])
            correct = html.unescape(item['correct_answer'])
            options = [html.unescape(ans) for ans in item['incorrect_answers']] + [correct]
            random.shuffle(options)

            content = [f"Category: {item['category']}", f"Difficulty: {item['difficulty'].upper()}", "", question, ""]
            for i, opt in enumerate(options):
                content.append(f"{i+1}. {opt}")
            draw_box("Interactive Challenge", content, C['PURPLE'])
            
            ans = input(f"\n{C['YELLOW']}Select Option (1-{len(options)}): {C['FG']}")
            if options[int(ans)-1] == correct:
                print(f"\n{C['GREEN']}CORRECT: Access Granted.{C['RESET']}")
            else:
                print(f"\n{C['RED']}FAILED: Correct answer was {correct}.{C['RESET']}")
    except: pass

def show_random_report():
    clear()
    topics = ["Cryptography", "Archaeology", "Astrophysics", "Marine_biology", "Ancient_Rome", "Cybersecurity", "Philosophy"]
    wiki_cat = random.choice(topics)
    print(f"{C['PURPLE']}{C['BOLD']}SYNCHRONIZING GLOBAL INTELLIGENCE...{C['RESET']}\n")
    
    activity = fetch_data("https://bored-api.appbrewery.com/random")
    if activity: draw_box("Mission", [f"Action: {activity['activity']}"], C['GREEN'])

    draw_box("Watch This (TED)", [
        "Source: Random TED Talk Generator", "",
        "Access a new random TED talk from the community archives:",
        "URL: https://omarsinan.github.io/projects/ted/"
    ], C['PINK'])

    try:
        params = {'action': 'query', 'list': 'categorymembers', 'cmtitle': f'Category:{wiki_cat}', 'cmlimit': 20, 'cmnamespace': 0, 'format': 'json'}
        list_data = fetch_data(f"https://en.wikipedia.org/w/api.php?{urllib.parse.urlencode(params)}")
        title = random.choice(list_data['query']['categorymembers'])['title']
        wiki = fetch_data(f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}")
        draw_box(f"Topic: {wiki_cat}", [wiki['title'], "", wiki['extract'], "", f"Link: {wiki['content_urls']['desktop']['page']}"], C['CYAN'])
    except: pass

    get_random_word_definition()

    try:
        advice = fetch_data("https://api.adviceslip.com/advice")['slip']['advice']
        fact = fetch_data("https://uselessfacts.jsph.pl/api/v2/facts/random")['text']
        draw_box("Insights", [f"Advice: {advice}", "", f"Fact: {fact}"], C['YELLOW'])
    except: pass

    print(f"\n{C['COMMENT']}Preparing Interactive Module...{C['RESET']}")
    run_trivia()
    input(f"\n{C['COMMENT']}Press Enter to return to main frame...{C['RESET']}")


# ==========================================
# DISCORD WEBHOOK FUNCTIONS (For GitHub)
# ==========================================
def run_discord_sync(webhook_url):
    print("Gathering data for Discord...")
    embeds = []
    
    # Main Embed
    main_embed = {
        "title": "Zero-Paywall Knowledge Sync",
        "description": "Daily global intelligence gathered successfully.",
        "color": 9169363, # Cyan
        "fields": []
    }

    # Mission
    activity = fetch_data("https://bored-api.appbrewery.com/random")
    if activity and 'activity' in activity:
        main_embed["fields"].append({"name": "Mission", "value": activity['activity'], "inline": False})

    # Wikipedia
    topics = ["Cryptography", "Archaeology", "Astrophysics", "Marine_biology", "Ancient_Rome", "Cybersecurity", "Philosophy"]
    wiki_cat = random.choice(topics)
    try:
        params = {'action': 'query', 'list': 'categorymembers', 'cmtitle': f'Category:{wiki_cat}', 'cmlimit': 20, 'cmnamespace': 0, 'format': 'json'}
        list_data = fetch_data(f"https://en.wikipedia.org/w/api.php?{urllib.parse.urlencode(params)}")
        title = random.choice(list_data['query']['categorymembers'])['title']
        wiki = fetch_data(f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}")
        main_embed["fields"].append({
            "name": f"Wiki: {wiki['title']} ({wiki_cat})", 
            "value": f"{wiki['extract']}\n[Read More]({wiki['content_urls']['desktop']['page']})", 
            "inline": False
        })
    except: pass

    # Insights
    advice_data = fetch_data("https://api.adviceslip.com/advice")
    fact_data = fetch_data("https://uselessfacts.jsph.pl/api/v2/facts/random")
    if advice_data and fact_data:
        main_embed["fields"].append({
            "name": "Insights", 
            "value": f"**Advice:** {advice_data['slip']['advice']}\n**Fact:** {fact_data['text']}", 
            "inline": False
        })

    embeds.append(main_embed)

    # Trivia Embed
    trivia_data = fetch_data("https://opentdb.com/api.php?amount=1")
    if trivia_data and trivia_data.get('response_code') == 0:
        item = trivia_data['results'][0]
        correct = html.unescape(item['correct_answer'])
        options = [html.unescape(ans) for ans in item['incorrect_answers']] + [correct]
        random.shuffle(options)
        options_text = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])
        
        embeds.append({
            "title": "Interactive Challenge (Trivia)",
            "color": 12424185, # Purple
            "fields": [
                {"name": "Category & Difficulty", "value": f"{item['category']} | {item['difficulty'].upper()}", "inline": False},
                {"name": "Question", "value": html.unescape(item['question']), "inline": False},
                {"name": "Options", "value": options_text, "inline": False},
                {"name": "Answer", "value": f"||{correct}||", "inline": False}
            ]
        })

    # Send to Discord
    payload = {"username": "Lumina", "embeds": embeds}
    req = urllib.request.Request(
        webhook_url, 
        data=json.dumps(payload).encode('utf-8'), 
        headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    )
    urllib.request.urlopen(req)
    print("Successfully sent to Discord!")

# ==========================================
# MAIN ROUTER
# ==========================================
def main():
    # 1. Check if running on GitHub Actions (Webhook exists)
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if webhook_url:
        print("GitHub Actions detected. Running automated Discord sync...")
        run_discord_sync(webhook_url)
        return # End script so it doesn't try to open the terminal menu
    
    # 2. If no Webhook, run original interactive terminal UI
    while True:
        clear()
        print(f"""{C['PURPLE']}
██╗     ██╗   ██╗███╗   ███╗██╗███╗   ██╗ █████╗ 
██║     ██║   ██║████╗ ████║██║████╗  ██║██╔══██╗
██║     ██║   ██║██╔████╔██║██║██╔██╗ ██║███████║
██║     ██║   ██║██║╚██╔╝██║██║██║╚██╗██║██╔══██║
███████╗╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║  ██║
╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
        {C['COMMENT']}ZERO-PAYWALL KNOWLEDGE{C['RESET']}
        """)

        print(f"{C['FG']}┌{'─'*68}┐")
        print(f"│  {C['CYAN']}1. {C['FG']}{'START RANDOM SYNC'.ljust(25)} {C['COMMENT']}{'All APIs Combined Discovery'.ljust(35)} {C['FG']}│")
        print(f"│  {C['PINK']}2. {C['FG']}{'TERMINATE SESSION'.ljust(25)} {C['COMMENT']}{'Power Down'.ljust(35)} {C['FG']}│")
        print(f"└{'─'*68}┘")

        choice = input(f"\n{C['PINK']}root@learner{C['FG']}:{C['PURPLE']}~{C['FG']}$ ")
        if choice == '1': show_random_report()
        elif choice == '2': break
        else:
            print(f"{C['RED']}Invalid Command.{C['RESET']}"); import time; time.sleep(0.5)

if __name__ == "__main__":
    main()
