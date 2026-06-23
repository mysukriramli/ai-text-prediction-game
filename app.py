import streamlit as st

# Set a clean page layout
st.set_page_config(layout="wide")

st.title("📱 The Smartphone Autocomplete Game: How AI Thinks")
st.markdown("""
    **Classroom Activity:** Let's see if you can guess words as fast as an AI! 
    Just like your phone tries to guess the next word when you text your friends, ChatGPT predicts the next word 
    using patterns it has learned. 
    
    We have 'trained' this mini-AI on the patriotic lyrics of **Keranamu Malaysia**. Let's see if your brain matches the phone's math!
""")

# --- THE SIMPLIFIED PUZZLE DATA ---
game_rounds = [
    {
        "context": "Buruh nelayan dan juga",
        "options": {"petani": "92% (High Chance)", "pekerja": "5% (Low Chance)", "pelajar": "3% (Unlikely)"},
        "correct": "petani",
        "explanation": "The phone gives 'petani' a 92% score because it perfectly matches the pattern of the famous song line."
    },
    {
        "context": "Buruh nelayan dan juga petani, Gaya hidup kini dah",
        "options": {"berakhir": "12% (Maybe)", "berubah": "85% (High Chance)", "bermula": "3% (Unlikely)"},
        "correct": "berubah",
        "explanation": "Based on the memory of the rhyme scheme, the autocomplete engine heavily favors 'berubah'."
    },
    {
        "context": "Buruh nelayan dan juga petani, Gaya hidup kini dah berubah, Anak-anak terasuh",
        "options": {"mindanya": "97% (Almost Certain)", "jiwanya": "2% (Low Chance)", "bakatnya": "1% (Unlikely)"},
        "correct": "mindanya",
        "explanation": "A super predictable line! The phone's calculation is nearly 100% sure the next word is 'mindanya'."
    },
    {
        "context": "... Lahir generasi bijak pandai, Pakar IT pakar ekonomi, Jaguh sukan dan juga jutawan, Berkereta jenama",
        "options": {"mewah": "15% (Generic Guess)", "import": "5% (Alternative Word)", "negara": "80% (High Chance)"},
        "correct": "negara",
        "explanation": "A generic phone might guess 'mewah', but a phone trained on Malaysian history knows 'negara' is the exact pattern match here."
    },
    {
        "context": "... Alam cyber teknologi terkini, Kejayaan semakin hampiri, Biar di kota ataupun desa, Kita semua pasti merasa",
        "options": {"gembira": "10% (Plausible)", "bangga": "88% (High Chance)", "selesa": "2% (Rhyme Break)"},
        "correct": "bangga",
        "explanation": "The engine scans the patriotic tone of the entire paragraph to score 'bangga' as the absolute best fit."
    },
    {
        "context": "... Keranamu kami mendakap tuah, Keranamu kami bangsa",
        "options": {"berjaya": "94% (High Chance)", "merdeka": "4% (Valid Word, Wrong Order)", "berdaulat": "2% (Low Chance)"},
        "correct": "berjaya",
        "explanation": "Sequence complete! The prediction engine successfully matched the lyric flow step-by-step."
    }
]

# --- PERSISTENT STORAGE ---
if "current_round" not in st.session_state:
    st.session_state.current_round = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Layout split: 1/2 Left Dashboard, 1/2 Right Inputs
col1, col2 = st.columns([1, 1])

# --- COLUMN 1: THE SMARTPHONE BRAIN ---
with col1:
    st.header("🧠 The Phone's Internal Brain")
    
    if not st.session_state.game_over:
        current_data = game_rounds[st.session_state.current_round]
        
        # Simple Memory Box
        st.markdown("### 📥 1. The Phone's Memory Box")
        st.info(f"\"{current_data['context']} [ ??? ]\"")
        st.caption("This is the exact sentence the phone is allowed to look at to guess the missing word.")
        
        # Simple Chaos Slider
        st.markdown("### 🎛️ 2. The Chaos Slider (Temperature)")
        temperature = st.slider("Set AI Randomness Level:", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
        if temperature <= 0.3:
            st.caption("🟢 **Safe Mode:** The phone is acting normal and will only pick the most predictable words.")
        elif temperature <= 0.7:
            st.caption("🟡 **Balanced Mode:** The phone might try some creative or alternative guesses.")
        else:
            st.caption("🔴 **Chaos Mode:** The phone is acting wild! It might ignore the best answer entirely and create gibberish.")
        
        # Easy Score widget
        st.metric(label="🎯 Your Correct Guesses", value=f"{st.session_state.score} / {len(game_rounds)}")
    else:
        st.balloons()
        st.success("🎉 Phone Prediction Routine Complete!")
        st.metric(label="🏆 Final Class Accuracy Score", value=f"{st.session_state.score} / {len(game_rounds)}")

# --- COLUMN 2: THE STUDENT CHOICE GAME ---
with col2:
    st.header("🧩 The Word Puzzle")
    
    if not st.session_state.game_over:
        current_data = game_rounds[st.session_state.current_round]
        
        st.write("Look at the **Memory Box** on the left. Which word puzzle piece should autocomplete this sentence?")
        
        options_list = list(current_data["options"].keys())
        
        with st.form(key="prediction_form"):
            user_choice = st.radio(
                "Choose a word piece to insert:", 
                options_list, 
                format_func=lambda x: f"'{x}' — Phone's Calculation: {current_data['options'][x]}"
            )
            
            submit_token = st.form_submit_button(label="⚡ Tap to Autocomplete Word")
            
            if submit_token:
                # Custom kid-friendly feedback logs
                if user_choice == current_data["correct"]:
                    st.session_state.score += 1
                    st.success(f"🎯 **Boom! Correct!** You guessed exactly what the phone calculated.")
                else:
                    st.error(f"⚠️ **Phone Hallucination!** The word you picked doesn't fit the expected pattern loop.")
                
                # Fun Phone Explanation logs
                st.markdown("#### 📝 Why did the phone think this?")
                st.help(current_data["explanation"])
                
                # Turn logic management
                if st.session_state.current_round + 1 < len(game_rounds):
                    st.session_state.current_round += 1
                    st.markdown("👇 *Tap the 'Autocomplete' button above one more time to reload the next line!*")
                else:
                    st.session_state.game_over = True
                    st.rerun()
    else:
        st.write("You have successfully helped the phone autocomplete the iconic National Day lyric sequence:")
        st.code("""
        Buruh nelayan dan juga petani
        Gaya hidup kini dah berubah
        Anak-anak terasuh mindanya
        Lahir generasi bijak pandai
        ...
        Berkereta jenama negara
        Megah menyusur di jalan raya
        ...
        Kita semua pasti merasa bangga
        Keranamu kami mendakap tuah
        Keranamu kami bangsa berjaya!
        """)
        
        if st.button("🔄 Restart Game & Clear Phone Memory"):
            st.session_state.current_round = 0
            st.session_state.score = 0
            st.session_state.game_over = False
            st.rerun()
