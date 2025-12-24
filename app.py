import streamlit as st
from github import Github

from agents.agent_a import AgentA
from utils.github_client import init_repo
from config.settings import (
    LLM_PROVIDER,
    LLM_MODEL,
    LLM_TEMPERATURE,
    GITHUB_TOKEN,
    GROQ_API_KEY,
)
from utils.formatting import format_error
from storage.session_cache import clear_cache
from storage.file_cache import clear_file_cache

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------

st.set_page_config(
    page_title="ARES - Agent for Repository Exploration & Structured-analysis",
    layout="wide",
)

st.title("ARES - Agent for Repository Exploration & Structured-analysis")

USER_AVATAR = "assets/user.png"
AGENT_AVATAR = "assets/agent.png"

# -------------------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------------------

st.session_state.setdefault("repo_loaded", False)
st.session_state.setdefault("repo_owner", None)
st.session_state.setdefault("repo_name", None)
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("chat_input", "")

# -------------------------------------------------------------------
# LLM
# -------------------------------------------------------------------

def get_llm():
    if LLM_PROVIDER == "groq":
        from groq import Groq
        client = Groq()

        class GroqLLM:
            def invoke(self, messages):
                response = client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=messages,
                    temperature=LLM_TEMPERATURE,
                )
                return response.choices[0].message

        return GroqLLM()

    raise RuntimeError("Unsupported LLM provider")

# -------------------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------------------

st.sidebar.header("🔧 System Status")

st.sidebar.success(" GROQ_API_KEY detected" if GROQ_API_KEY else "❌ GROQ_API_KEY missing")
st.sidebar.success(" GITHUB_TOKEN detected" if GITHUB_TOKEN else "❌ GITHUB_TOKEN missing")

st.sidebar.divider()
st.sidebar.header("📂 Repository Selection")

owner = st.sidebar.text_input("GitHub Username", value=st.session_state.repo_owner or "")
repo_list = []

if owner:
    try:
        gh = Github(GITHUB_TOKEN)
        repo_list = [r.name for r in gh.get_user(owner).get_repos()]
    except Exception as e:
        st.sidebar.error(str(e))

repo = st.sidebar.selectbox("Select Repository", [""] + repo_list)

if st.sidebar.button("Load Repository"):
    if owner and repo:
        init_repo(owner, repo)
        st.session_state.repo_loaded = True
        st.session_state.repo_owner = owner
        st.session_state.repo_name = repo
        st.sidebar.success(f"Loaded {owner}/{repo}")

st.sidebar.divider()

if st.sidebar.button(" Clear Session "):
    st.session_state.clear()
    clear_cache()
    clear_file_cache()
    st.rerun()

# -------------------------------------------------------------------
# REINIT REPO
# -------------------------------------------------------------------

if st.session_state.repo_loaded:
    init_repo(st.session_state.repo_owner, st.session_state.repo_name)

# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------

if not st.session_state.repo_loaded:
    st.info("Load a repository from the sidebar to begin.")
    st.stop()

llm = get_llm()
agent_a = AgentA(llm)

st.subheader("💬 Chat with the Repository")

# ---- CHAT HISTORY ----
for role, text in st.session_state.chat_history:
    cols = st.columns([1, 12])
    if role == "user":
        cols[0].image(USER_AVATAR, width=32)
        cols[1].markdown(text)
    else:
        cols[0].image(AGENT_AVATAR, width=32)
        cols[1].code(text)

# -------------------------------------------------------------------
# CHAT INPUT (FORM = FIX)
# -------------------------------------------------------------------

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask a question", key="chat_input")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    st.session_state.chat_history.append(("user", user_input))

    try:
        with st.spinner("Processing..."):
            response = agent_a.handle_query(user_input)
        st.session_state.chat_history.append(("agent", response))
    except Exception as e:
        st.session_state.chat_history.append(("agent", format_error(str(e))))

    st.rerun()
