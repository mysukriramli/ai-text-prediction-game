import streamlit as st

# Set page layout to centered for a clean mobile-screen feel
st.set_page_config(layout="centered")

# Hide the song title completely to preserve the surprise ending
st.title("📱 Mystery Next-Word Text Engine")
st.markdown("---")

# --- THE AUTOCOMPLETE DICTIONARY LAYER ---
rounds = [
    {
        "prefix": "Buruh nelayan dan juga ",
        "choices": [("petani", "94%"), ("sultan", "4%"), ("influencer", "2%")]
    },
    {
        "prefix": "\nGaya hidup kini dah ",
        "choices": [("berubah", "89%"), ("pusing", "8%"), ("goyang", "3%")]
    },
    {
        "prefix": "\nAnak-anak terasuh ",
        "choices": [("mindanya", "96%"), ("hartanya", "3%"), ("kucingnya", "1%")]
    },
    {
        "prefix": "\nLahir generasi bijak ",
        "choices": [("pandai", "91%"), ("saham", "6%"), ("tiktok", "3%")]
    },
    {
        "prefix": "\nPakar IT pakar ",
        "choices": [("ekonomi", "88%"), ("magic", "9%"), ("tidur", "3%")]
    },
    {
        "prefix": "\nKita semua pasti merasa ",
        "choices": [("bangga", "97%"), ("penat", "2%"), ("bingung", "1%")]
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
    
    # Render the text box simulate a smartphone messaging app screen
    st.markdown("### 💬 Simulated Text Bubble")
    display_text = st.session_state.accumulated_text + current_round["prefix"]
    st.code(display_text + "┃", language="text")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("🤖 Select the next token prediction to continue typing:")
    
    # Create 3 horizontal option columns mimicking the smartphone predictive text strip
    cols = st.columns(3)
    for idx, (word, percentage) in enumerate(current_round["choices"]):
        # The first item in our choices list is always the correct highest percentage line
        is_highest = (idx == 0)
        
        button_label = f"✨ {word}\n{percentage}" if is_highest else f"{word}\n{percentage}"
        
        if cols[idx].button(button_label, key=f"btn_{st.session_state.step}_{idx}", use_container_width=True):
            # If they click anything other than the first option, flag a mutation error
            if not is_highest:
                st.session_state.hallucinated = True
            
            # Save choice and advance internal model index
            st.session_state.accumulated_text = display_text + word
            st.session_state.step += 1
            st.rerun()

# --- THE SURPRISE REVEAL MODE (END GAME) ---
else:
    st.markdown("## 🇲🇾 Surprise Reveal: Keranamu Malaysia!")
    st.markdown("---")
    
    # Case 1: The student fell for a low percentage/wrong choice
    if st.session_state.hallucinated:
        st.error("🚨 **CRITICAL MODEL ERROR: Text Generation Corrupted!**")
        st.markdown("""
            You deviated from the highest probability weights! Because you selected alternative prediction tokens, 
            the AI generated a flawed, hallucinated remix of the lyrics:
        """)
        
        # Display the student's customized wrong lyrics
        st.subheader("📝 The Hallucinated Remix")
        st.code(st.session_state.accumulated_text, language="text")
        
    # Case 2: The student clicked the highest choice perfectly every single time
    else:
        st.success("🎯 **PERFECT GENERATION: Model Weights Fully Aligned!**")
        st.markdown("""
            By strictly choosing the highest probability tokens at every step, your network successfully 
            reproduced the pristine, true historical pattern of the anthem:
        """)
        
        st.subheader("🎵 Perfect Generation Output")
        st.code(st.session_state.accumulated_text + """
Jaguh sukan dan juga jutawan
Berkereta jenama negara
Megah menyusur di jalan raya
Alam cyber teknologi terkini
Kejayaan semakin hampiri
Biar di kota ataupun desa
Kita semua pasti merasa bangga!
        """, language="text")
        
    # Reset button to reload class memory loops
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Wipe Model Cache (Restart Game)", use_container_width=True):
        st.session_state.step = 0
        st.session_state.accumulated_text = ""
        st.session_state.hallucinated = False
        st.rerun()
