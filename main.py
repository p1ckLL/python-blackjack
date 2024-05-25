import requests
import time

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
        if ace_count > 0:
            total -= 10
            ace_count -= 1
        else:
            break

    if isPrint:
        print("    TOTAL: " + str(total) + "\n")

    return total

def check_player_bust(gambler_total):
  if gambler_total > 21:
    print("YOU BUST. YOU LOSE!")
    time.sleep(4)
    main()

def check_winners(gamblers_hand, dealers_hand):
    gambler_total = calculate_total(gamblers_hand, isPrint=False)
    dealer_total = calculate_total(dealers_hand, isPrint=False)

    # Check for ties
    if gambler_total == dealer_total:
      print("PUSH")
      time.sleep(4)
      main()

    # Check for blackjacks
    if gambler_total == 21:
      print("YOU WIN!")
      time.sleep(4)
      main()
    if dealer_total == 21:
      print("YOU LOSE!")
      time.sleep(4)
      main()

    # Check for dealer busts
    if dealer_total > 21:
      print("DEALER BUSTS. YOU WIN!")
      time.sleep(4)
      main()

    # Check for closest to 21
    if 21 - gambler_total < 21 - dealer_total:
      print("YOU WIN!")
      time.sleep(4)
      main()
    else:
      print("YOU LOSE!")
      time.sleep(4)
      main()  
    


def draw_card(deck_id, hand, player_type):
    response = requests.get("https://www.deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=1")
    data = response.json()
    card = data["cards"][0]

    hand.append(card)
    print(f"{player_type} DREW " + card["value"] + " of " + hand[0]["suit"] + "!")

def stand(deck_id, gamblers_hand, dealers_hand):
    while calculate_total(dealers_hand, isPrint=False) < 17:
      draw_card(deck_id, dealers_hand, "DEALER")
    check_winners(gamblers_hand, dealers_hand)

def main():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

    is_bust = False

    deck = requests.get("https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6").json()
    cards = requests.get("https://www.deckofcardsapi.com/api/deck/" + deck["deck_id"] + "/draw/?count=4").json()["cards"]

    dealers_hand, gamblers_hand = [cards[0], cards[1]], [cards[2], cards[3]]

    while not is_bust:
      print("YOUR HAND:")
      for card in gamblers_hand:
          print(card["value"] + " of " + card["suit"])
      calculate_total(gamblers_hand, isPrint=True)
      if calculate_total(gamblers_hand, isPrint=False) == 21:
        print("BLACKJACK!")
        time.sleep(4)
        main()

      print("DEALER'S HAND:")
      for card in dealers_hand:
        print(card["value"] + " of " + card["suit"])
      calculate_total(dealers_hand, isPrint=True)
      if calculate_total(gamblers_hand, isPrint=False) == 21:
        print("DEALER BLACKJACK. YOU LOSE!")
        time.sleep(4)
        main()

      action = input("HIT or STAND:\n")

      if action.lower() == "hit":
          print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
          draw_card(deck["deck_id"], gamblers_hand, "YOU")
          check_player_bust(calculate_total(gamblers_hand, isPrint=False))
      if action.lower() == "stand":
          stand(deck["deck_id"], gamblers_hand, dealers_hand)

main()