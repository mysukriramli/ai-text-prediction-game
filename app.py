import streamlit as st

# Set a clean page layout
st.set_page_config(layout="wide", page_title="AI Next-Token Predictor Game")

st.title("🤖 The Human-GPT Experiment: Next-Token Prediction Game")
st.markdown("""
    **Classroom Concept:** Large Language Models (LLMs) do not understand text; they simply predict the next 
    word (token) based on probability. In this game, **you** are the AI model trained on Malaysian historical text. 
    Can your weights accurately predict the next token?
""")

# --- GAME DATASET (The Training Data) ---
game_rounds = [
    {
        "context": "Buruh nelayan dan juga",
        "options": {"petani": "92% (High Probability)", "pekerja": "5% (Low Probability)", "pelajar": "3% (Rare Token)"},
        "correct": "petani",
        "fact": "The model assigns 92% weight to 'petani' because of strong matching patterns in the training corpus."
    },
    {
        "context": "Buruh nelayan dan juga petani, Gaya hidup kini dah",
        "options": {"berakhir": "12% (Plausible)", "berubah": "85% (High Probability)", "bermula": "3% (Distractor)"},
        "correct": "berubah",
        "fact": "Context window updated. The structural vector shifts heavily toward 'berubah' to preserve the rhyme scheme."
    },
    {
        "context": "Buruh nelayan dan juga petani, Gaya hidup kini dah berubah, Anak-anak terasuh",
        "options": {"mindanya": "97% (Max Probability)", "jiwanya": "2% (Low Probability)", "bakatnya": "1% (Rare Token)"},
        "correct": "mindanya",
        "fact": "A highly predictable token sequence. The model's internal attention mechanism is locked onto semantic harmony."
    },
    {
        "context": "... Mindanya, Lahir generasi bijak pandai, Pakar IT pakar ekonomi, Jaguh sukan dan juga jutawan, Berkereta jenama",
        "options": {"mewah": "15% (Generic Choice)", "import": "5% (Alternative Word)", "negara": "80% (Contextual Match)"},
        "correct": "negara",
        "fact": "Localized training bias! A generic AI might guess 'mewah', but a model trained on Malaysian history strongly weights 'negara'."
    },
    {
        "context": "... Berkereta jenama negara, Megah menyusur di jalan raya, Alam cyber teknologi terkini, Kejayaan semakin hampiri, Biar di kota ataupun desa, Kita semua pasti merasa",
        "options": {"gembira": "10% (Plausible)", "bangga": "88% (High Probability)", "selesa": "2% (Rhyme Break)"},
        "correct": "bangga",
        "fact": "The attention heads evaluate patriotic sentiment across the entire paragraph to score 'bangga' as the optimal next step."
    },
    {
        "context": "... Kita semua pasti merasa bangga, Keranamu kami mendakap tuah, Keranamu kami bangsa",
        "options": {"berjaya": "94% (High Probability)", "merdeka": "4% (Valid but out of order)", "berdaulat": "2% (Low Weight)"},
        "correct": "berjaya",
        "fact": "Sequence completed successfully. The generation weights maximize precision by closing the phrase loops systematically."
    }
]

# --- PERSISTENT GAME STORAGE ---
if "current_round" not in st.session_state:
    st.session_state.current_round = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Layout split
col1, col2 = st.columns([1, 1])

# --- LEFT COLUMN: THE LIVE AI CONTEXT ENGINE ---
with col1:
    st.header("🧠 AI Model Internal State")
    
    if not st.session_state.game_over:
        current_data = game_rounds[st.session_state.current_round]
        
        # Display the prompt context window
        st.markdown("### 📥 Active Context Window (Input Prompt)")
        st.info(f"\"{current_data['context']} ...\"")
        
        # Educational LLM Simulator Settings
        st.markdown("### 🎛️ Hyperparameter Controls")
        temperature = st.slider("Model Temperature (Randomness)", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
        st.caption("Lower temperature makes the AI predictable and deterministic. Higher temperature forces creative, chaotic guesses.")
        
        # Score Tracking widget
        st.metric(label="Model Prediction Accuracy", value=f"{st.session_state.score} / {len(game_rounds)}")
    else:
        st.balloons()
        st.success("🎉 Training Complete! The human model has finalized its parameter weights successfully.")
        st.metric(label="Final Model Accuracy", value=f"{st.session_state.score} / {len(game_rounds)}")

# --- RIGHT COLUMN: NEXT-TOKEN SELECTION PORTAL ---
with col2:
    st.header("🔮 Token Prediction Selector")
    
    if not st.session_state.game_over:
        current_data = game_rounds[st.session_state.current_round]
        
        st.write("Review the context window on the left, then select the absolute best token to continue the sequence:")
        
        # Turn dict keys into button choices for parameters
        options_list = list(current_data["options"].keys())
        
        with st.form(key="prediction_form"):
            user_choice = st.radio("Select the next token vector:", options_list, format_func=lambda x: f"'{x}' — Calculated Confidence: {current_data['options'][x]}")
            submit_token = st.form_submit_button(label="⚡ Execute Next-Token Generation")
            
            if submit_token:
                if user_choice == current_data["correct"]:
                    st.session_state.score += 1
                    st.toast("✅ Target token matched! Attention weights aligned.", icon="🎯")
                else:
                    st.toast("❌ Hallucination! Divergent token selected.", icon="⚠️")
                
                # Show engine logs
                st.markdown("#### 🤖 Execution Logs")
                st.code(f"Selected: '{user_choice}'\nTarget: '{current_data['correct']}'\nLog: {current_data['fact']}")
                
                # Advance round logic
                if st.session_state.current_round + 1 < len(game_rounds):
                    st.session_state.current_round += 1
                    st.markdown("👉 *Click the 'Execute' button above again to feed the new sequence into the context layer.*")
                else:
                    st.session_state.game_over = True
                    st.rerun()
    else:
        st.write("The complete sequence has been compiled by the student cluster network:")
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
        
        if st.button("🔄 Clear Model Memory (Reset Game)"):
            st.session_state.current_round = 0
            st.session_state.score = 0
            st.session_state.game_over = False
            st.rerun()
