import random
import streamlit as st
from config import LIMIT, DEALER_STAND, SUITS, CARD_RANKS, CARD_VALUES


def _draw_card():
    rank = random.choice(CARD_RANKS)
    suit = random.choice(SUITS)
    return f"{rank}{suit}", CARD_VALUES[rank]


def _calculate_total(values):
    total = sum(values)
    # Ace: 11 -> 1 if bust
    aces = values.count(11)
    while total > LIMIT and aces:
        total -= 10
        aces -= 1
    return total


def player_total():
    return _calculate_total(st.session_state.player_values)


def computer_total():
    return _calculate_total(st.session_state.computer_values)


def _deal_to(target):
    card, value = _draw_card()
    st.session_state[f"{target}_cards"].append(card)
    st.session_state[f"{target}_values"].append(value)
    if target == "player":
        st.session_state.log.append(f"You drew: {card}")
    else:
        st.session_state.log.append("Dealer drew: ???")


def _reveal_dealer_log():
    # Logdaki ??? kartlari gercek kartlarla degistir
    card_idx = 0
    for i, entry in enumerate(st.session_state.log):
        if "Dealer drew: ???" in entry:
            if card_idx < len(st.session_state.computer_cards):
                st.session_state.log[i] = f"Dealer drew: {st.session_state.computer_cards[card_idx]}"
            card_idx += 1


def _end_game(message, result):
    st.session_state.message = message
    st.session_state.game_over = True
    st.session_state.computer_revealed = True
    _reveal_dealer_log()
    bet = st.session_state.get("current_bet", 0)
    if result == "win":
        st.session_state.chips += bet
        st.session_state.wins += 1
    elif result == "lose":
        st.session_state.chips -= bet
        st.session_state.losses += 1
    elif result == "draw":
        st.session_state.draws += 1


def _check_immediate_win():
    p, c = player_total(), computer_total()
    p_bj = p == LIMIT and len(st.session_state.player_values) == 2
    c_bj = c == LIMIT and len(st.session_state.computer_values) == 2

    if p_bj:
        _end_game("Draw! Both have Blackjack!", "draw") if c_bj else _end_game("BLACKJACK! YOU WIN!", "win")
    elif c_bj:
        _end_game("BLACKJACK! Dealer wins. You lose.", "lose")
    elif p > LIMIT:
        _end_game("Bust! You went over 21. You lose.", "lose")
    elif c > LIMIT:
        _end_game("Dealer busted! You win!", "win")


def init_game():
    for key in ["player_cards", "player_values", "computer_cards", "computer_values", "log"]:
        st.session_state[key] = []
    st.session_state.game_over = False
    st.session_state.message = ""
    st.session_state.game_started = True
    st.session_state.computer_revealed = False

    # 2 kart her oyuncuya
    for _ in range(2):
        _deal_to("player")
        _deal_to("computer")
    _check_immediate_win()


def hit():
    _deal_to("player")
    if player_total() > LIMIT:
        _end_game("Bust! You went over 21. You lose.", "lose")
        return
    _deal_to("computer")
    _check_immediate_win()


def stand():
    st.session_state.log.append("--- Dealer is playing... ---")
    while computer_total() < DEALER_STAND:
        _deal_to("computer")

    p, c = player_total(), computer_total()
    if c > LIMIT:
        _end_game("Dealer busted! You win!", "win")
    elif c > p:
        _end_game("Dealer wins. You lose.", "lose")
    elif c == p:
        _end_game("It's a draw!", "draw")
    else:
        _end_game("You win!", "win")
