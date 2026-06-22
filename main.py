import streamlit as st
import streamlit.components.v1 as components
from art import logo
from config import LIMIT, STARTING_CHIPS, STATS
from game import init_game, hit, stand, player_total, computer_total
from ui import CARD_CSS, FIREWORKS_JS, render_hand, render_stat_card

st.set_page_config(page_title="Blackjack", page_icon="🃏")

# ── SESSION STATE INIT ───────────────────────────────────────────────────────

for key, default in [("chips", STARTING_CHIPS), ("wins", 0), ("losses", 0), ("draws", 0)]:
    st.session_state.setdefault(key, default)

# ── UI ───────────────────────────────────────────────────────────────────────

st.html(CARD_CSS)
st.code(logo, language=None)

# Skor paneli
for col, (label, key, color) in zip(st.columns(4), STATS):
    with col:
        st.html(render_stat_card(label, st.session_state[key], color))

st.divider()

if "game_started" not in st.session_state:
    if st.session_state.chips <= 0:
        st.error("You're out of chips! Game over.")
        if st.button("Restart", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    else:
        st.subheader("Place Your Bet")
        max_bet = st.session_state.chips
        if max_bet <= 10:
            bet = max_bet
            st.info(f"Bet: {bet} chips (only option)")
        else:
            bet = st.slider("Bet", min_value=10, max_value=max_bet, value=min(100, max_bet), step=10)
        if st.button("Start Game", use_container_width=True):
            st.session_state.current_bet = bet
            init_game()
            st.rerun()
else:
    p_total = player_total()
    c_total = computer_total()
    revealed = st.session_state.computer_revealed

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Your Hand")
        st.html(render_hand(st.session_state.player_cards))
        st.metric("Total", p_total)
    with col2:
        st.subheader("Dealer's Hand")
        st.html(render_hand(st.session_state.computer_cards, revealed))
        st.metric("Total", c_total if revealed else "?")

    st.caption(f"Current Bet: {st.session_state.get('current_bet', 0)} chips")

    with st.expander("Game Log"):
        for entry in st.session_state.log:
            st.write(entry)

    if st.session_state.game_over:
        msg = st.session_state.message
        msg_lower = msg.lower()

        won = "you win" in msg_lower

        if won:
            st.success(msg)
            st.balloons()
        elif "you lose" in msg_lower or "bust" in msg_lower:
            st.error(msg)
        else:
            st.info(msg)

        if st.button("Play Again", use_container_width=True):
            saved = {k: st.session_state[k] for k in ["chips", "wins", "losses", "draws"]}
            st.session_state.clear()
            st.session_state.update(saved)
            st.rerun()

        if won:
            components.html(FIREWORKS_JS, height=420)
    else:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Hit", use_container_width=True, disabled=p_total == LIMIT):
                hit()
                st.rerun()
        with c2:
            if st.button("Stand", use_container_width=True):
                stand()
                st.rerun()
