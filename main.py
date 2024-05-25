import requests

def bust():
    pass

def calculate_total(hand, isPrint):
    ace_count = 0
    total = 0
    
    for card in hand:
        if card["value"] == "ACE":
            total += 11
            ace_count += 1
        elif card["value"] == "KING" or card["value"] == "QUEEN" or card["value"] == "JACK":
            total += 10
        else:
            total += int(card["value"])
    
    while total > 21:
        if total > 21 and ace_count > 1:
            total -= 10
            ace_count -= 1
        else:
            break

    if total > 21:
        bust()

    if isPrint:
        print("    TOTAL: " + str(total) + "\n")

    return total

def stand():
    pass

def draw_card(deck_id, hand):
    response = requests.get("https://www.deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=1")
    data = response.json()
    card = data["cards"][0]

    hand.append(card)
    print("YOU DREW A: " + card["value"] + " of " + hand[0]["suit"] + "!")

def main():
    response = requests.get("https://www.deckofcardsapi.com/api/deck/new/draw/?count=4")
    data = response.json()
    deck_id = data["deck_id"]
    cards = data["cards"]

    dealers_hand, gamblers_hand = [cards[0], cards[1]], [cards[2], cards[3]]
    
    print("YOUR HAND: " + "\n    " + gamblers_hand[0]["value"] + " of " + gamblers_hand[0]["suit"] + "\n    " + gamblers_hand[1]["value"] + " of " + gamblers_hand[1]["suit"])
    calculate_total(gamblers_hand, isPrint=True)

    print("DEALER'S HAND: " + "\n    " + dealers_hand[0]["value"] + " of " + dealers_hand[0]["suit"] + "\n    " + dealers_hand[1]["value"] + " of " + dealers_hand[1]["suit"])
    calculate_total(dealers_hand, isPrint=True)

    action = input("HIT or STAND:\n")

    if action.lower() == "hit":
        draw_card(deck_id, gamblers_hand)
        calculate_total(gamblers_hand, isPrint=True)
    if action.lower() == "stand":
        stand()

main()