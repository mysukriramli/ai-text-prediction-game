import streamlit as st

# Set page layout to centered for a clean mobile-screen feel
st.set_page_config(layout="centered")

# Hide the song title completely to preserve the surprise ending
st.title("📱 Mystery Next-Word Text Engine")
st.markdown("---")

# --- THE SCRAMBLED DICTIONARY LAYER ---
# The highest percentage option is intentionally mixed up across different columns
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
if "hallucinated" not in st.session_state:
    st.session_state.hallucinated = False

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
                st.session_state.hallucinated = True
            
            # Save choice and advance internal model index
            st.session_state.accumulated_text = display_text + word
            st.session_state.step += 1
            st.rerun()

# --- THE SURPRISE REVEAL MODE (END GAME) ---
else:
    st.markdown("## 🇲🇾 Surprise Reveal: Keranamu Malaysia!")
    st.markdown("---")
    
    # Render final output text box based on student journey path
    if st.session_state.hallucinated:
        st.error("🚨 **CRITICAL MODEL ERROR: Text Generation Hallucinated!**")
        st.markdown("You selected an alternative prediction token. The output sequence broke pattern sync:")
        st.code(st.session_state.accumulated_text, language="text")
    else:
        st.success("🎯 **PERFECT GENERATION: Model Weights Fully Aligned!**")
        st.markdown("Your choices perfectly matched the maximum statistical expectation of the training set:")
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
    By clicking through this game, you just proved the exact mathematical flaw that makes AI writing easy to spot. 
    Here is what is happening under the hood:
    
    * **The Trap of High Similarity:** Like you, an LLM (Large Language Model) is trained on existing text data. When generating an essay, it constantly looks back at what it just wrote and plays a safe statistical game, picking words with the highest similarity percentages.
    * **The Illusion of Creativity:** AI does not actually 'create' anything brand new. It mirrors paths it has already walked during training. It can only generate combinations of things it has already seen.
    * **The Predictability Footprint:** Because an AI almost always follows maximum probability chains, its text lacks human spontaneity. It produces mathematically perfect, ultra-predictable word patterns.
    """)
    
    st.info("""
    > 🧠 **How AI Detectors Catch It:** Human writers are beautifully chaotic. We mix rare words, sudden structure shifts, and weird metaphors with low statistical probability. 
    > AI detectors look for text that is 'too predictable.' If an essay flows perfectly along the highest probable word tracks—exactly like clicking the maximum percentage buttons in this game—the detector flags it as machine-generated instantly!
    """)
    
    # Reset button to reload class memory loops
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Wipe Model Cache (Restart Game)", use_container_width=True):
        st.session_state.step = 0
        st.session_state.accumulated_text = ""
        st.session_state.hallucinated = False
        st.rerun()
