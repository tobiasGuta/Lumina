import urllib.request
import urllib.parse
import json
import random
import os
import html
import re
import datetime

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
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

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
    for _ in range(10):
        try:
            word_raw = fetch_data("https://random-word-api.herokuapp.com/word?number=1")
            target_word = word_raw[0]
            dict_data = fetch_data(f"https://api.dictionaryapi.dev/api/v2/entries/en/{target_word}")

            definition = ""
            part_of_speech = "unknown"

            # Just grab the part of speech and the definition, then stop.
            for entry in dict_data:
                for meaning in entry.get('meanings', []):
                    part_of_speech = meaning.get('partOfSpeech', part_of_speech)
                    for d in meaning.get('definitions', []):
                        if not definition:
                            definition = d.get('definition')
                            break
                    if definition:
                        break
                if definition:
                    break

            # Draw the box without the Usage section
            if definition:
                draw_box("Vocabulary Expansion", [
                    f"Word: {target_word.capitalize()} ({part_of_speech})",
                    "", 
                    f"Definition: {definition}"
                ], C['ORANGE'])
                return
        except Exception:
            continue

def run_trivia():
    try:
        data = fetch_data("https://opentdb.com/api.php?amount=1")
        if data['response_code'] == 0:
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
    except Exception: pass

def show_random_report():
    clear()
    topics = ["Cryptography", "Archaeology", "Astrophysics", "Marine_biology", "Ancient_Rome", "Cybersecurity", "Philosophy"]
    wiki_cat = random.choice(topics)
    print(f"{C['PURPLE']}{C['BOLD']}SYNCHRONIZING GLOBAL INTELLIGENCE...{C['RESET']}\n")
    
    # 1. Mission
    try:
        activity = fetch_data("https://bored-api.appbrewery.com/random")
        draw_box("Mission", [f"Action: {activity['activity']}"], C['GREEN'])
    except Exception: pass

    # 2. Watch This (TED Generator)
    draw_box("Watch This (TED)", [
        "Source: Random TED Talk Generator",
        "",
        "Access a new random TED talk from the community archives:",
        "URL: https://omarsinan.github.io/projects/ted/"
    ], C['PINK'])

    # 3. Wikipedia
    try:
        params = {'action': 'query', 'list': 'categorymembers', 'cmtitle': f'Category:{wiki_cat}', 'cmlimit': 20, 'cmnamespace': 0, 'format': 'json'}
        list_data = fetch_data(f"https://en.wikipedia.org/w/api.php?{urllib.parse.urlencode(params)}")
        title = random.choice(list_data['query']['categorymembers'])['title']
        wiki = fetch_data(f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}")
        draw_box(f"Topic: {wiki_cat}", [wiki['title'], "", wiki['extract'], "", f"Link: {wiki['content_urls']['desktop']['page']}"], C['CYAN'])
    except Exception: pass

    # 4. Vocabulary
    get_random_word_definition()

    # 5. Insights
    try:
        advice = fetch_data("https://api.adviceslip.com/advice")['slip']['advice']
        fact = fetch_data("https://uselessfacts.jsph.pl/api/v2/facts/random")['text']
        draw_box("Insights", [f"Advice: {advice}", "", f"Fact: {fact}"], C['YELLOW'])
    except Exception: pass

    # 6. Today in History
    try:
        today = datetime.date.today()
        history_data = fetch_data(
            f"https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/{today.month}/{today.day}"
        )
        events = history_data.get('events', [])
        if events:
            event = random.choice(events[:10])
            draw_box(f"Today in History ({today.strftime('%B %d')})", [
                f"Year: {event.get('year', 'Unknown')}",
                "",
                event.get('text', '')
            ], C['RED'])
    except Exception: pass

    # 7. Quote
    try:
        quote_data = fetch_data("https://zenquotes.io/api/random")
        if quote_data:
            q = quote_data[0]
            draw_box("Inspirational Quote", [
                f'"{q["q"]}"',
                "",
                f"— {q['a']}"
            ], C['PURPLE'])
    except Exception: pass

    # 8. Trivia
    print(f"\n{C['COMMENT']}Preparing Interactive Module...{C['RESET']}")
    run_trivia()
    input(f"\n{C['COMMENT']}Press Enter to return to main frame...{C['RESET']}")

def main():
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
