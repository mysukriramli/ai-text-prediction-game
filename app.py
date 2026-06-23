import streamlit as st

# Set page layout to centered for a clean mobile-screen feel
st.set_page_config(layout="centered")

# Hide the song title completely to preserve the surprise ending
st.title("📱 Mystery Next-Word Text Engine")
st.markdown("---")

# --- THE SCRAMBLED DICTIONARY LAYER ---
# The highest percentage option is mixed up across different columns each round
rounds = [
    {
        "prefix": "Buruh nelayan dan juga ",
        "choices": [("sultan", "4%"), ("petani", "94%"), ("influencer", "2%")],
        "correct_word": "petani"
    },
    {
        "prefix": "\nGaya hidup kini dah ",
        "choices": [("berubah", "89%"), ("pusing", "8%"), ("goyang", "3%")],
        "correct_word": "berubah"
    },
    {
        "prefix": "\nAnak-anak terasuh ",
        "choices": [("hartanya", "3%"), ("kucingnya", "1%"), ("mindanya", "96%")],
        "correct_word": "mindanya"
    },
    {
        "prefix": "\nLahir generasi bijak ",
        "choices": [("tiktok", "3%"), ("pandai", "91%"), ("saham", "6%")],
        "correct_word": "pandai"
    },
    {
        "prefix": "\nPakar IT pakar ",
        "choices": [("ekonomi", "88%"), ("magic", "9%"), ("tidur", "3%")],
        "correct_word": "ekonomi"
    },
    {
        "prefix": "\nKita semua pasti merasa ",
        "choices": [("penat", "2%"), ("bangga", "97%"), ("bingung", "1%")],
        "correct_word": "bangga"
    }
]

# --- PARAMETER MEMORY STATES ---
if "step" not in st.session_state:
    st.session_state.step = 0
if "accumulated_text" not in st.session_state:
    st.session_state.accumulated_text = ""
if "low_prob_chosen" not in st.session_state:
    st.session_state.low_prob_chosen = False

# --- GAME ACTIVE MODE ---
if st.session_state.step < len(rounds):
    current_round = rounds[st.session_state.step]
    
    # Render the text box simulating a smartphone messaging app screen
    st.markdown("### 💬 Simulated Text Bubble")
    display_text = st.session_state.accumulated_text + current_round["prefix"]
    st.code(display_text + "┃", language="text")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("🤖 Select the next token prediction to continue typing:")
    
    # Create 3 horizontal option columns mimicking the smartphone predictive text strip
    cols = st.columns(3)
    for idx, (word, percentage) in enumerate(current_round["choices"]):
        button_label = f"{word}\n{percentage}"
        
        if cols[idx].button(button_label, key=f"btn_{st.session_state.step}_{idx}", use_container_width=True):
            # Track if the student clicks anything other than the mathematically highest word
            if word != current_round["correct_word"]:
                st.session_state.low_prob_chosen = True
            
            # Save choice and advance internal model index
            st.session_state.accumulated_text = display_text + word
            st.session_state.step += 1
            st.rerun()

# --- THE SURPRISE REVEAL MODE (END GAME) ---
else:
    st.markdown("## 🇲🇾 Surprise Reveal: Keranamu Malaysia!")
    st.markdown("---")
    
    # Render final output text box based on student choices
    if st.session_state.low_prob_chosen:
        st.warning("⚠️ **Low Probability Path Selected**")
        st.markdown("""
            An AI usually avoids these low-percentage paths because they are completely **unfamiliar**. It has never 
            learned those specific word combinations before during its training phase. 
            
            Because the AI doesn't actually understand the whole context—it doesn't know that this is an iconic patriotic 
            lyric song about **Keranamu Malaysia**—it just follows math. By veering off the high-probability track, 
            the text pattern broke and generated an alternative version:
        """)
        st.code(st.session_state.accumulated_text, language="text")
    else:
        st.success("🎯 **PERFECT GENERATION: Maximum Probability Path**")
        st.markdown("Your choices perfectly matched the highest statistical expectations of the training data:")
        st.code(st.session_state.accumulated_text + """
Jaguh sukan dan juga jutawan
Berkereta jenama negara
Megah menyusur di jalan raya
Alam cyber teknologi terkini
Kejayaan semakin hampiri
Biar di kota ataupun desa
Kita semua pasti merasa bangga!
        """, language="text")
        
    st.markdown("---")
    
    # --- DEEP AI EXPLANATION LESSON SECTION ---
    st.header("💡 Why are AI Essays So Easily Detected?")
    
    st.markdown("""
    By clicking through this game, you just demonstrated the exact mathematical reason why AI writing detectors work so well:
    
    * **The Trap of High Similarity:** An LLM (Large Language Model) always plays a safe statistical game. It constantly picks words with the highest similarity percentages based on what it learned in training.
    * **No Real Understanding:** AI doesn't know what a 'national anthem' or 'emotion' is. It just connects words that frequently sit next to each other in its memory database.
    * **The Predictability Footprint:** Because an AI almost always follows the maximum probability chains to avoid unfamiliar territory, its writing lacks natural human randomness. It produces word patterns that are statistically 'too perfect.'
    """)
    
    st.info("""
    > 🧠 **The Catch:** Human writers are beautifully unpredictable. We mix rare vocabulary, sudden structure shifts, and unique metaphors that an AI's math would score as 'low probability.' 
    > If a student's essay flows perfectly along the highest probable word tracks—exactly like clicking the maximum percentage buttons in this game—detection algorithms spot the machine-like consistency instantly!
    """)
    
    # Reset button to reload class memory loops
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Wipe Model Cache (Restart Game)", use_container_width=True):
        st.session_state.step = 0
        st.session_state.accumulated_text = ""
        st.session_state.low_prob_chosen = False
        st.rerun()
