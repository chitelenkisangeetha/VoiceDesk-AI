import streamlit as st

from utils.ai import ask_ollama
from utils.voice import listen_to_voice, speak_text
from utils.assistant import check_command


# ==========================================================
# PAGE SETTINGS
# ==========================================================

st.set_page_config(
    page_title="VoiceDesk AI",
    page_icon="🎙️",
    layout="centered"
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef2ff, #f5f3ff, #e0f2fe);
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* HEADER */
.header-card {
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    padding: 35px 25px;
    border-radius: 25px;
    text-align: center;
    color: white;
    box-shadow: 0 15px 35px rgba(79, 70, 229, 0.30);
    margin-bottom: 28px;
}

.header-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 8px;
}

.header-subtitle {
    font-size: 17px;
    opacity: 0.95;
}

/* SECTION TITLES */
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #312e81;
    margin-top: 20px;
    margin-bottom: 10px;
}

/* INPUT */
.stTextInput input {
    border-radius: 14px !important;
    border: 2px solid #c4b5fd !important;
    padding: 14px !important;
    font-size: 16px !important;
    background-color: white !important;
}

/* BUTTONS */
.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: none;
    padding: 13px;
    font-size: 16px;
    font-weight: 700;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    color: white;
    box-shadow: 0 8px 18px rgba(79, 70, 229, 0.20);
    transition: 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 25px rgba(79, 70, 229, 0.30);
}

/* USER MESSAGE */
.user-message {
    background: linear-gradient(135deg, #dbeafe, #ede9fe);
    padding: 16px 18px;
    border-radius: 18px 18px 5px 18px;
    margin-top: 14px;
    margin-left: 40px;
    color: #1e1b4b;
    border: 1px solid #c4b5fd;
}

/* AI MESSAGE */
.ai-message {
    background: white;
    padding: 18px;
    border-radius: 18px 18px 18px 5px;
    margin-top: 10px;
    margin-right: 40px;
    color: #1f2937;
    border: 1px solid #ddd6fe;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.06);
}

/* VOICE CARD */
.voice-card {
    background: linear-gradient(135deg, #ede9fe, #dbeafe);
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    margin-top: 15px;
    border: 1px solid #c4b5fd;
}

/* STATUS */
.status-card {
    background: white;
    padding: 15px;
    border-radius: 16px;
    text-align: center;
    margin-top: 25px;
    border: 1px solid #ddd6fe;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}

/* FOOTER */
.footer {
    text-align: center;
    color: #6366f1;
    font-size: 14px;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    '<div class="header-card">'
    '<div class="header-title">🎙️ VoiceDesk AI</div>'
    '<div class="header-subtitle">'
    'Your Intelligent Voice-Based Personal Assistant'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================================
# LANGUAGE
# ==========================================================

st.markdown(
    '<div class="section-title">🌐 Choose Language</div>',
    unsafe_allow_html=True
)

language = st.selectbox(
    "Language",
    ["English", "Telugu"],
    label_visibility="collapsed"
)

if language == "English":
    speech_language = "en-IN"
else:
    speech_language = "te-IN"


# ==========================================================
# CLEAR CHAT
# ==========================================================

if st.button("🗑️ Clear Conversation"):

    st.session_state.messages = []

    st.rerun()


# ==========================================================
# QUESTION
# ==========================================================

st.markdown(
    '<div class="section-title">💬 Ask VoiceDesk</div>',
    unsafe_allow_html=True
)

question = st.text_input(
    "Question",
    placeholder="Type your question here...",
    label_visibility="collapsed"
)


# ==========================================================
# BUTTONS
# ==========================================================

col1, col2 = st.columns(2)

with col1:
    ask_button = st.button("🤖  Ask AI")

with col2:
    voice_button = st.button("🎤  Speak")


# ==========================================================
# TEXT QUESTION
# ==========================================================

if ask_button:

    if question.strip():

        with st.spinner("✨ VoiceDesk is thinking..."):

            command_answer = check_command(question)

            if command_answer:
                answer = command_answer
            else:
                answer = ask_ollama(question, language)

        st.session_state.messages.append({
            "user": question,
            "ai": answer
        })

        speak_text(answer)

    else:
        st.warning("Please enter a question.")


# ==========================================================
# VOICE QUESTION
# ==========================================================

if voice_button:

    st.markdown(
        '<div class="voice-card">'
        '🎤 <b>Listening...</b><br>'
        'Speak your question now'
        '</div>',
        unsafe_allow_html=True
    )

    voice_question = listen_to_voice(speech_language)

    if voice_question:

        st.markdown("### 🎤 You said")

        st.info(voice_question)

        if not voice_question.startswith(
            ("Sorry", "I couldn't", "Microphone")
        ):

            with st.spinner("✨ VoiceDesk is thinking..."):

                command_answer = check_command(voice_question)

                if command_answer:
                    answer = command_answer
                else:
                    answer = ask_ollama(
                        voice_question,
                        language
                    )

            st.session_state.messages.append({
                "user": voice_question,
                "ai": answer
            })

            speak_text(answer)


# ==========================================================
# CHAT HISTORY
# ==========================================================

if st.session_state.messages:

    st.markdown(
        '<div class="section-title">💬 Conversation</div>',
        unsafe_allow_html=True
    )

    for message in st.session_state.messages:

        st.markdown(
            f'<div class="user-message">'
            f'👤 <b>You</b><br><br>'
            f'{message["user"]}'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="ai-message">'
            f'🤖 <b>VoiceDesk AI</b><br><br>'
            f'{message["ai"]}'
            f'</div>',
            unsafe_allow_html=True
        )


# ==========================================================
# STATUS
# ==========================================================

st.markdown(
    '<div class="status-card">'
    '🟢 <b>VoiceDesk AI is ready</b><br>'
    '🎤 Voice &nbsp; | &nbsp; 🧠 AI &nbsp; | &nbsp; 🔊 Speech'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    '<div class="footer">'
    'Built with Python • Streamlit • Ollama • Llama 3.2'
    '</div>',
    unsafe_allow_html=True
)