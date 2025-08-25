# import streamlit as st
# from prompt_router import handle_user_input
# from utils import intent_classifier
# from Agents import download_agent
# from Agents.title_generator import generate_chat_title
# from Agents.ocrapp import extract_pdf_text_with_vision
# from PyPDF2 import PdfReader
# from io import BytesIO
# import uuid, hashlib, re

# # ---------- page ----------
# st.set_page_config(
#     page_title="PakLaw Judicial Assistant",
#     page_icon="⚖️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ---------- css ----------
# st.markdown(
#     """
# <style>
# /* --- root variables --- */
# :root {
#     --brand: #2E3B55;
#     --brand-light: #3f4f70;
#     --accent: #FFD700;
#     --bg-chat: #fafbfc;
#     --bg-sidebar: #ffffff;
#     --radius: 12px;
#     --shadow: 0 2px 8px rgba(0,0,0,.08);
#     --shadow-hover: 0 4px 16px rgba(0,0,0,.12);
# }

# /* --- global --- */
# html, body, .main {
#     background-color: var(--bg-chat);
# }
# .block-container {
#     padding-top: 3rem;
#     padding-bottom: 8rem;
# }

# /* --- sidebar --- */
# [data-testid="stSidebar"] {
#     background-color: var(--bg-sidebar);
#     border-right: 1px solid #e5e7eb;
# }
# .sidebar-card {
#     background: #ffffff;
#     border-radius: var(--radius);
#     box-shadow: var(--shadow);
#     margin-bottom: .6rem;
#     transition: .25s;
# }
# .sidebar-card:hover {
#     box-shadow: var(--shadow-hover);
#     transform: translateY(-1px);
# }

# /* --- chat bubbles --- */
# .chat-user, .chat-assistant {
#     max-width: 80%;
#     padding: .8rem 1.1rem;
#     border-radius: var(--radius);
#     margin-bottom: .7rem;
#     animation: fadeIn .4s ease-in-out;
#     word-wrap: break-word;
# }

# .chat-user {
#     background: #e6f0fa;
#     border-left: 4px solid var(--accent);
#     margin-left: auto;
# }
# .chat-assistant {
#     background: #f6f8fa;
#     border-left:4px solid var(--brand) ;
#     margin-right: auto;
# }
# @keyframes fadeIn {
#     from {opacity: 0; transform: translateY(8px);}
#     to   {opacity: 1; transform: translateY(0);}
# }

# /* --- sticky bottom bar --- */
# .chat-bar {
#     position: fixed;
#     bottom: 0;
#     left: 0;
#     right: 0;
#     background: #ffffff;
#     border-top: 4px solid var(--brand);
#     box-shadow: 0 -2px 8px rgba(0,0,0,.05);
#     z-index: 1000;
#     padding: .8rem 2rem 1.2rem;
# }
# .chat-bar textarea {
#     border: 2px solid var(--brand);
#     border-radius: var(--radius);
#     font-size: 1rem;
# }
# .chat-bar textarea:focus {
#     border-color: var(--accent);
#     box-shadow: 0 0 0 .15rem rgba(255,215,0,.35);
# }
# .stButton>button {
#     border-radius: var(--radius);
#     font-weight: 600;
#     background: var(--brand);
#     border: none;
#     color: #fff;
#     transition: .25s;
# }
# .stButton>button:hover {
#     background: var(--brand-light);
#     transform: translateY(-1px);
# }
# </style>
# """,
#     unsafe_allow_html=True,
# )

# # ---------- session ----------
# if "chats" not in st.session_state:
#     st.session_state.chats = {}
# if "chat_titles" not in st.session_state:
#     st.session_state.chat_titles = {}
# if "current_chat" not in st.session_state:
#     cid = str(uuid.uuid4())
#     st.session_state.current_chat = cid
#     st.session_state.chats[cid] = []
#     st.session_state.chat_titles[cid] = "New Case"
# if "uploaded_case_text" not in st.session_state:
#     st.session_state.uploaded_case_text = ""
# if "last_uploaded_file_hash" not in st.session_state:
#     st.session_state.last_uploaded_file_hash = None

# # ---------- sidebar ----------
# with st.sidebar:
#     st.markdown("### 📁 Case Files")
#     if st.button("➕ New Case", use_container_width=True):
#         cid = str(uuid.uuid4())
#         st.session_state.current_chat = cid
#         st.session_state.chats[cid] = []
#         st.session_state.chat_titles[cid] = "New Case"
#         st.session_state.uploaded_case_text = ""
#         st.session_state.last_uploaded_file_hash = None
#         st.rerun()

#     for cid in list(st.session_state.chats.keys()):
#         title = st.session_state.chat_titles.get(cid, f"Case {cid[:8]}")
#         if st.button(title, key=f"chat_{cid}", use_container_width=True):
#             st.session_state.current_chat = cid
#             st.rerun()

# # ---------- header ----------
# st.title("⚖️ PakLaw Judicial Assistant")
# st.caption("Interactive legal assistant for Pakistan’s judicial system.")

# # ---------- chat display ----------
# st.markdown("### 📜 Case Discussion & Judgments")

# chat_id = st.session_state.current_chat
# current_chat = st.session_state.chats[chat_id]

# chat_area = st.container()
# with chat_area:
#     for idx, msg in enumerate(current_chat):
#         if msg["role"] == "user":
#             st.markdown(
#                 f'<div class="chat-user"><strong>🧑 Counsel:</strong><br>{msg["message"]}</div>',
#                 unsafe_allow_html=True,
#             )
#         else:
#             html = re.sub(r"(?m)^([A-Z][a-z]+):", r"<strong>\1:</strong>", msg["message"])
#             html = html.replace("\n", "<br>")
#             st.markdown(
#                 f'<div class="chat-assistant"><strong>⚖️ Assistant:</strong><br>{html}</div>',
#                 unsafe_allow_html=True,
#             )
#             download_agent.show_download_if_applicable(idx, current_chat, intent_classifier.classify_prompt_intent)

# # ---------- sticky input ----------
# with st.container():
#     st.markdown('<div class="chat-bar">', unsafe_allow_html=True)

#     with st.form(key="chat_form", clear_on_submit=True):
#         c1, c2 = st.columns([4, 1])

#         with c1:
#             user_input = st.text_area(
#                 "Enter your judicial query:",
#                 key="user_input",
#                 label_visibility="collapsed",
#                 height=100,
#                 placeholder="Type your legal query here or upload a .txt / .pdf case …",
#             )

#             st.markdown(
#             "<small style='color: #666;'>Limit: 10MB per file • Max 30 pages • TXT, PDF</small>",
#             unsafe_allow_html=True
#         )
        
#             uploaded_file = st.file_uploader(
#                     "📎 Upload Case File (.txt or .pdf)",
#                     type=["txt", "pdf"],
#                     label_visibility="collapsed"
#                 )

#             if uploaded_file:
#                 max_mb = 10
#                 if uploaded_file.size > max_mb * 1024 * 1024:
#                     st.error(f"❌ File too large. Max {max_mb} MB allowed.")
#                 else:
#                     file_bytes = uploaded_file.read()
#                     file_hash = hashlib.md5(file_bytes).hexdigest()
#                     if st.session_state.last_uploaded_file_hash != file_hash:
#                         st.session_state.last_uploaded_file_hash = file_hash
#                         try:
#                             if uploaded_file.name.lower().endswith(".txt"):
#                                 st.session_state.uploaded_case_text = file_bytes.decode("utf-8")
#                                 st.success("✅ Text file loaded.")
#                             else:
#                                 reader = PdfReader(BytesIO(file_bytes))
#                                 if len(reader.pages) > 30:
#                                     st.error("❌ PDF too long. Max 30 pages.")
#                                 else:
#                                     txt = extract_pdf_text_with_vision(file_bytes)
#                                     if not txt or len(txt.strip()) < 50:
#                                         st.error("❌ No meaningful text extracted.")
#                                     else:
#                                         st.session_state.uploaded_case_text = txt[:10_000]
#                                         st.success("✅ PDF processed.")

#                         except Exception as e:
#                             st.error(f"❌ Could not read file: {e}")

#         with c2:
#             submitted = st.form_submit_button("Submit", use_container_width=True)

#     st.markdown("</div>", unsafe_allow_html=True)

# # ---------- query handler ----------
# if submitted and (user_input or st.session_state.uploaded_case_text):
#     query = user_input.strip() or "Generate legal judgment"
#     with st.spinner("Processing …"):
#         response = handle_user_input(query)

#     if uploaded_file and uploaded_file.size <= 10 * 1024 * 1024:
#         current_chat.append({"role": "user", "message": f"[📎 Uploaded: {uploaded_file.name}]"})

#     current_chat.append({"role": "user", "message": query})
#     current_chat.append({"role": "assistant", "message": response})

#     st.session_state.chat_titles[chat_id] = generate_chat_title(query) or "Untitled Case"
#     st.rerun()


import streamlit as st
from prompt_router import handle_user_input
from utils import intent_classifier
from Agents import download_agent
from Agents.title_generator import generate_chat_title
from Agents.ocrapp import extract_pdf_text_with_vision
from PyPDF2 import PdfReader
from io import BytesIO
import uuid, hashlib, re

# ==========================
# Page config
# ==========================
st.set_page_config(
    page_title="PakLaw Judicial Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================
# CSS — ChatGPT-style UI
# ==========================
st.markdown(
    """
<style>
:root {
  --gpt-bg: #f7f7f8;
  --gpt-surface: #ffffff;
  --gpt-bubble: #f2f2f2; /* assistant */
  --gpt-text: #111827;
  --gpt-accent: #10a37f; /* OpenAI green */
  --radius: 18px;
}

html, body, .main { background: var(--gpt-bg); }

/* center column like ChatGPT */
.block-container {
  max-width: 860px;
  margin: 0 auto;
  padding-top: 1rem;
  padding-bottom: 7.5rem; /* space for sticky bar */
}

/* Sidebar minimal */
[data-testid="stSidebar"] {
  background: var(--gpt-surface);
  border-right: 1px solid #e5e7eb;
}

/* Header */
h1, h3, h4 { color: var(--gpt-text); }

/* Chat messages */
.chat-wrap { display: flex; flex-direction: column; gap: 12px; }
.msg { padding: .9rem 1.1rem; border-radius: var(--radius); line-height: 1.6; font-size: 0.98rem; }
.msg.assistant { background: var(--gpt-bubble); color: #111; align-self: flex-start; }
.msg.user { background: #fff; border: 1px solid #e5e7eb; align-self: flex-end; }
.msg strong { font-weight: 600; }

/* Sticky bottom input like GPT */
.gpt-input-bar { position: fixed; left: 0; right: 0; bottom: 0; background: linear-gradient(180deg, rgba(247,247,248,0) 0%, var(--gpt-bg) 40%, var(--gpt-bg) 100%); padding: 10px 0 18px; }
.gpt-input-inner { max-width: 860px; margin: 0 auto; display: flex; align-items: flex-end; gap: 10px; padding: 0 16px; }

/* input shell */
.input-shell { flex: 1; background: var(--gpt-surface); border: 1px solid #e5e7eb; border-radius: 24px; display: flex; align-items: flex-end; gap: 8px; padding: 10px; box-shadow: 0 2px 10px rgba(0,0,0,.04); }
.attach-btn { border: none; background: transparent; font-size: 20px; padding: 6px 8px; cursor: pointer; color: #555; border-radius: 10px; }
.attach-btn:hover { background: #f2f2f2; }

/* Streamlit widgets inside shell */
textarea[data-baseweb="textarea"], .stTextArea textarea { width: 100% !important; border: none !important; outline: none !important; resize: none !important; box-shadow: none !important; background: transparent !important; font-size: 1rem !important; min-height: 60px !important; }

/* Send button */
.send-btn { border: none; background: var(--gpt-accent); color: white; padding: 10px 14px; border-radius: 14px; font-weight: 600; cursor: pointer; }
.send-btn:hover { filter: brightness(0.95); }

/* Hide the uploader visually but keep in DOM */
.hidden-uploader [data-testid="stFileUploader"] { height: 0; overflow: hidden; }
.hidden-uploader [data-testid="stFileUploader"] > div { display: none; }

/* File chip */
.file-chip { display: inline-flex; align-items: center; gap: 8px; background: #eef2f7; color: #222; border: 1px solid #e5e7eb; padding: 6px 10px; border-radius: 999px; font-size: .85rem; margin: 0 0 8px 16px; }
.file-chip .x { cursor: pointer; opacity: .7; }
.file-chip .x:hover { opacity: 1; }
</style>
""",
    unsafe_allow_html=True,
)

# ==========================
# Session state
# ==========================
ss = st.session_state
if "chats" not in ss: ss.chats = {}
if "chat_titles" not in ss: ss.chat_titles = {}
if "current_chat" not in ss:
    cid = str(uuid.uuid4())
    ss.current_chat = cid
    ss.chats[cid] = []
    ss.chat_titles[cid] = "New Case"
if "uploaded_case_text" not in ss: ss.uploaded_case_text = ""
if "last_uploaded_file_hash" not in ss: ss.last_uploaded_file_hash = None
if "uploaded_filename" not in ss: ss.uploaded_filename = None
if "pending_text" not in ss: ss.pending_text = ""

# ==========================
# Sidebar
# ==========================
with st.sidebar:
    st.markdown("### 📁 Case Files")
    if st.button("➕ New Case", use_container_width=True):
        cid = str(uuid.uuid4())
        ss.current_chat = cid
        ss.chats[cid] = []
        ss.chat_titles[cid] = "New Case"
        ss.uploaded_case_text = ""
        ss.uploaded_filename = None
        ss.last_uploaded_file_hash = None
        st.rerun()

    for cid in list(ss.chats.keys()):
        title = ss.chat_titles.get(cid, f"Case {cid[:8]}")
        if st.button(title, key=f"chat_{cid}", use_container_width=True):
            ss.current_chat = cid
            st.rerun()

# ==========================
# Header
# ==========================
st.title("⚖️ PakLaw Judicial Assistant")
st.caption("Interactive legal assistant for Pakistan’s judicial system.")
st.markdown("### 📜 Case Discussion & Judgments")

# ==========================
# Chat area
# ==========================
chat_id = ss.current_chat
current_chat = ss.chats[chat_id]

wrap = st.container()
with wrap:
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for idx, msg in enumerate(current_chat):
        if msg["role"] == "user":
            st.markdown(f"<div class='msg user'>{msg['message']}</div>", unsafe_allow_html=True)
        else:
            html = re.sub(r"(?m)^([A-Z][a-z]+):", r"<strong>\\1:</strong>", msg["message"]).replace("\n", "<br>")
            st.markdown(f"<div class='msg assistant'>{html}</div>", unsafe_allow_html=True)
            download_agent.show_download_if_applicable(idx, current_chat, intent_classifier.classify_prompt_intent)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================
# Sticky input bar (GPT-like)
# ==========================
st.markdown('<div class="gpt-input-bar"><div class="gpt-input-inner">', unsafe_allow_html=True)

# Hidden uploader lives in the DOM; we trigger it from the + button via JS
uploader_col, input_col, send_col = st.columns([0.0001, 0.93, 0.07])
with uploader_col:
    st.markdown('<div class="hidden-uploader">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload Case File (.txt or .pdf)",
        type=["txt", "pdf"],
        accept_multiple_files=False,
        label_visibility="collapsed",
        key="case_file",
    )
    st.markdown('</div>', unsafe_allow_html=True)

with input_col:
    # file chip (like GPT shows above input)
    if ss.uploaded_filename:
        st.markdown(
            f"<div class='file-chip'>📎 {ss.uploaded_filename} <span class='x' id='remove-file' title='Remove'>&times;</span></div>",
            unsafe_allow_html=True,
        )
    with st.form("chat_form", clear_on_submit=True):
        ss.pending_text = st.text_area(
            "Type your message",
            value="",
            placeholder="Message PakLaw…",
            label_visibility="collapsed",
            key="chat_textarea",
            height=70,
        )
        submitted = st.form_submit_button("__HIDDEN_SEND__")  # hidden, clicked via JS or Enter

with send_col:
    # Visible Send button (mirrors the hidden submit)
    send_clicked = st.button("Send", key="send_btn_vis", use_container_width=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# ==========================
# JS: map + to file input, Enter to send, remove-chip
# ==========================
st.markdown(
    """
<script>
(function() {
  const root = window.parent.document;
  // Click the first file input when + is pressed
  function wireAttach() {
    const plusBtn = root.querySelector('.attach-btn');
    const fileInputs = root.querySelectorAll('input[type="file"]');
    if (plusBtn && fileInputs.length) {
      plusBtn.addEventListener('click', function() { fileInputs[fileInputs.length-1].click(); });
    }
  }
  // Make our Streamlit Send button behave like GPT: Enter send, Shift+Enter newline
  function wireEnterToSend() {
    const ta = root.querySelector('textarea');
    const visBtn = root.querySelector('button[kind="secondary"]:contains("Send")');
  }

  // A safer generic implementation that doesn't rely on labels:
  function wireGeneric() {
    const textareas = root.querySelectorAll('textarea');
    const sendButtons = Array.from(root.querySelectorAll('button'));
    const hiddenSubmit = sendButtons.find(b => b.innerText === '__HIDDEN_SEND__');
    const visibleSend = sendButtons.find(b => b.innerText.trim() === 'Send');

    const ta = textareas[textareas.length-1];
    if (ta && hiddenSubmit) {
      ta.addEventListener('keydown', function(e){
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          hiddenSubmit.click();
        }
      });
    }
    if (visibleSend && hiddenSubmit) {
      visibleSend.addEventListener('click', function(){ hiddenSubmit.click(); });
    }

    // Remove chip
    const x = root.getElementById('remove-file');
    if (x) {
      x.addEventListener('click', function(){
        window.parent.postMessage({type:'clear-file'}, '*');
      });
    }
  }

  // Inject a + button inside the input shell (left side)
  function ensurePlus() {
    const shells = root.querySelectorAll('.input-shell');
  }

  // Run wiring after small delay to allow Streamlit DOM to mount
  setTimeout(function(){ wireAttach(); wireGeneric(); }, 500);
})();
</script>
""",
    unsafe_allow_html=True,
)

# Note: Streamlit can't directly listen for our postMessage to clear the file.
# We'll just clear via session state on the next run if a flag is set.
if "_clear_file" not in ss: ss._clear_file = False

# Frontend postMessage hook (Streamlit automatically ignores, so emulate via button)
clear_file = st.button("__HIDDEN_CLEAR_FILE__", key="clear_file_hidden", help="internal")
if clear_file or ss._clear_file:
    ss.uploaded_case_text = ""
    ss.uploaded_filename = None
    ss.last_uploaded_file_hash = None
    ss._clear_file = False
    st.experimental_rerun()

# ==========================
# Handle file upload
# ==========================
if uploaded_file is not None:
    max_mb = 10
    if uploaded_file.size > max_mb * 1024 * 1024:
        st.error(f"❌ File too large. Max {max_mb} MB allowed.")
    else:
        file_bytes = uploaded_file.read()
        file_hash = hashlib.md5(file_bytes).hexdigest()
        if ss.last_uploaded_file_hash != file_hash:
            ss.last_uploaded_file_hash = file_hash
            try:
                if uploaded_file.name.lower().endswith(".txt"):
                    ss.uploaded_case_text = file_bytes.decode("utf-8")
                    ss.uploaded_filename = uploaded_file.name
                else:
                    reader = PdfReader(BytesIO(file_bytes))
                    if len(reader.pages) > 30:
                        st.error("❌ PDF too long. Max 30 pages.")
                    else:
                        txt = extract_pdf_text_with_vision(file_bytes)
                        if not txt or len(txt.strip()) < 50:
                            st.error("❌ No meaningful text extracted.")
                        else:
                            ss.uploaded_case_text = txt[:10_000]
                            ss.uploaded_filename = uploaded_file.name
            except Exception as e:
                st.error(f"❌ Could not read file: {e}")

# ==========================
# Submit logic (hidden form button or visible send)
# ==========================
if 'submitted_once' not in ss: ss.submitted_once = False

if submitted or st.session_state.get('send_btn_vis'):
    text = (ss.pending_text or "").strip()
    if text or ss.uploaded_case_text:
        with st.spinner("Processing …"):
            response = handle_user_input(text or "Generate legal judgment")
        if ss.uploaded_filename:
            current_chat.append({"role": "user", "message": f"[📎 Uploaded: {ss.uploaded_filename}]"})
        current_chat.append({"role": "user", "message": text})
        current_chat.append({"role": "assistant", "message": response})
        ss.chat_titles[chat_id] = generate_chat_title(text) or "Untitled Case"
        ss.pending_text = ""
        st.rerun()
