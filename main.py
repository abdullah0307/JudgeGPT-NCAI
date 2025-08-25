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

# app.py
import streamlit as st
from prompt_router import handle_user_input
from utils import intent_classifier
from Agents import download_agent
from Agents.title_generator import generate_chat_title
from Agents.ocrapp import extract_pdf_text_with_vision
from PyPDF2 import PdfReader
from io import BytesIO
import uuid, hashlib, re

# ---- page config ----
st.set_page_config(page_title="PakLaw Judicial Assistant", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

# ---- CSS (ChatGPT-like) ----
st.markdown(
    """
<style>
:root{
  --bg: #f7f7f8;
  --surface: #ffffff;
  --assistant-bubble: #f2f2f2;
  --text: #0b1221;
  --muted: #6b7280;
  --accent: #10a37f; /* kept accent but not used on send button */
  --radius: 18px;
}

/* page background and center column */
html, body, .main { background: var(--bg); }
.block-container { max-width: 880px; margin: 0 auto; padding-top: 14px; padding-bottom: 120px; }

/* Sidebar style (neutral like GPT) */
[data-testid="stSidebar"] { background: var(--surface); border-right: 1px solid #e6e6e9; }
.stButton>button, .stMarkdown { font-family: inherit; }

/* chat area */
.chat-wrap { display:flex; flex-direction:column; gap:12px; padding: 8px 14px 40px 14px; }
.msg { padding: 12px 16px; border-radius: 14px; max-width: 78%; line-height:1.5; font-size: 15px; box-shadow: 0 1px 0 rgba(16,24,40,0.03); }
.msg.assistant { background: var(--assistant-bubble); color: var(--text); align-self: flex-start; }
.msg.user { background: var(--surface); border: 1px solid #ececec; color: var(--text); align-self: flex-end; }

/* input bar wrapper like GPT */
.gpt-input-bar { position: fixed; left: 0; right: 0; bottom: 0; padding: 14px 0; background: linear-gradient(transparent, var(--bg)); z-index: 999; }
.gpt-inner { max-width: 880px; margin: 0 auto; display:flex; gap:12px; align-items:flex-end; padding: 0 16px; }

/* input shell */
.input-shell { flex: 1; background: var(--surface); border: 1px solid #e8eaed; border-radius: 24px; padding: 10px; display:flex; gap:8px; align-items:flex-end; box-shadow: 0 6px 16px rgba(15,23,42,0.04); }

/* left attach button */
#gpt-attach-btn { width:36px; height:36px; border-radius:10px; display:inline-flex; align-items:center; justify-content:center; border:none; background:transparent; cursor:pointer; color:#444; font-size:18px; }
#gpt-attach-btn:hover { background:#f2f2f2; }

/* textarea look inside streamlit */
textarea[role="textbox"], .stTextArea textarea { width:100% !important; height: 64px !important; resize:none; border:none !important; outline:none !important; background:transparent !important; font-size:15px !important; padding:6px 0 !important; }

/* send circular gray button (paper plane) */
#gpt-send-btn { width:44px; height:44px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; border:none; cursor:pointer; background:#eef1f3; color:#111; box-shadow: 0 1px 0 rgba(16,24,40,0.03); }
#gpt-send-btn:hover { background:#e2e6e9; transform: translateY(-1px); }

/* file chip displayed above input area */
.file-chip { display:inline-flex; align-items:center; gap:8px; background:#eef2f7; padding:6px 10px; border-radius:999px; font-size:13px; margin-bottom:8px; color:#111; border:1px solid #e6eef7; }
.file-chip .x { cursor:pointer; opacity:0.7; }
.file-chip .x:hover { opacity:1; }

/* hide the internal/hidden control buttons (we hide them via JS too) */
.hidden-btn { display:none !important; }

/* small helpers for spacing near header */
.title-row { display:flex; align-items:center; gap:12px; }
</style>
""",
    unsafe_allow_html=True,
)

# ---- session state ----
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
if "chat_input_temp" not in ss: ss.chat_input_temp = ""

# ---- sidebar ----
with st.sidebar:
    st.markdown("### 📁 Case Files")
    # neutral card-like new case button
    if st.button("➕ New Case", use_container_width=True):
        cid = str(uuid.uuid4())
        ss.current_chat = cid
        ss.chats[cid] = []
        ss.chat_titles[cid] = "New Case"
        ss.uploaded_case_text = ""
        ss.uploaded_filename = None
        ss.last_uploaded_file_hash = None
        st.experimental_rerun()

    # existing cases
    for cid in list(ss.chats.keys()):
        title = ss.chat_titles.get(cid, f"Case {cid[:8]}")
        if st.button(title, key=f"chat_{cid}", use_container_width=True):
            ss.current_chat = cid
            st.experimental_rerun()

# ---- header ----
st.markdown('<div class="title-row"><h1 style="margin:0">⚖️ PakLaw Judicial Assistant</h1></div>', unsafe_allow_html=True)
st.caption("Interactive legal assistant for Pakistan’s judicial system.")
st.markdown("### 📜 Case Discussion & Judgments")

# ---- chat area ----
chat_id = ss.current_chat
current_chat = ss.chats[chat_id]

chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    # initial placeholder if empty
    if not current_chat:
        intro = "Hello! I’m the PakLaw assistant — ask me about cases, generate judgments, or upload a case file using the + button below."
        current_chat.append({"role": "assistant", "message": intro})
    for idx, msg in enumerate(current_chat):
        if msg["role"] == "user":
            # user bubble (right)
            st.markdown(f'<div class="msg user">{msg["message"]}</div>', unsafe_allow_html=True)
        else:
            # assistant bubble (left), keep any "Judge:" labels bold etc.
            html = re.sub(r"(?m)^([A-Z][a-z]+):", r"<strong>\1:</strong>", msg["message"])
            html = html.replace("\n", "<br>")
            st.markdown(f'<div class="msg assistant">{html}</div>', unsafe_allow_html=True)
            # show download if applicable (keeps your existing functionality)
            try:
                download_agent.show_download_if_applicable(idx, current_chat, intent_classifier.classify_prompt_intent)
            except Exception:
                pass
    st.markdown('</div>', unsafe_allow_html=True)

# ---- sticky GPT-like input bar ----
# We'll put a hidden file_uploader in DOM, trigger it from the + button using JS.
st.markdown('<div class="gpt-input-bar"><div class="gpt-inner">', unsafe_allow_html=True)

# Columns layout for attach / input / send (visual)
col_attach, col_input, col_send = st.columns([0.06, 0.88, 0.06])

with col_attach:
    # visible attach button (HTML) — triggers file input via JS
    st.markdown('<button id="gpt-attach-btn" title="Attach file">+</button>', unsafe_allow_html=True)

with col_input:
    # file chip area (shows uploaded file name and remove X)
    if ss.uploaded_filename:
        st.markdown(f'<div class="file-chip">📎 {ss.uploaded_filename}<span class="x" id="remove-file" title="Remove">&times;</span></div>', unsafe_allow_html=True)

    # hidden file_uploader element (kept in DOM)
    # place it here so its input is present; we'll keep it visually hidden via CSS (but not necessary)
    uploaded_file = st.file_uploader("Upload Case File (.txt or .pdf)", type=["txt", "pdf"], key="case_file", label_visibility="collapsed")

    # the main form: text_area + hidden submit
    with st.form("chat_form", clear_on_submit=True):
        ss.chat_input_temp = st.text_area("Message", value="", placeholder="Message PakLaw…", key="chat_textarea", label_visibility="collapsed", height=64)
        # hidden submit button (we will hide it via JS immediately)
        hidden_submit = st.form_submit_button("__SEND_HIDDEN__")

with col_send:
    # visible send circular button (HTML) with paper plane SVG => triggers hidden_submit via JS
    send_html = """
    <button id="gpt-send-btn" title="Send">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" 
           stroke-linecap="round" stroke-linejoin="round" style="display:block">
        <path d="M22 2L11 13"></path>
        <path d="M22 2L15 22L11 13L2 9L22 2Z"></path>
      </svg>
    </button>
    """
    st.markdown(send_html, unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# Hidden clear button to remove uploaded file (server side)
clear_clicked = st.button("__CLEAR_FILE__", key="__clear_file_hidden__", help="internal", visible=False) if hasattr(st, 'button') else False
# Note: some Streamlit versions don't support visible=False; we include button and hide it via JS style anyway.
# We'll handle actual clearing below based on file uploader changes or clear button.

# ---- JS wiring: attach + enter-to-send + hide hidden submit + connect visible send to hidden submit + remove chip ----
st.markdown(
    """
<script>
(function(){
  // operate on parent document (Streamlit renders in an iframe)
  const root = window.parent.document;

  function findHiddenSubmit() {
    const buttons = Array.from(root.querySelectorAll('button'));
    return buttons.find(b => b.innerText && b.innerText.trim() === '__SEND_HIDDEN__');
  }
  function findClearBtn() {
    const buttons = Array.from(root.querySelectorAll('button'));
    return buttons.find(b => b.innerText && b.innerText.trim() === '__CLEAR_FILE__');
  }

  setTimeout(()=> {
    try {
      const attachBtn = root.getElementById('gpt-attach-btn');
      const sendBtn = root.getElementById('gpt-send-btn');
      const hiddenSubmit = findHiddenSubmit();
      const clearBtn = findClearBtn();

      // hide the hidden submit (it exists inside the form)
      if (hiddenSubmit) { hiddenSubmit.style.display = 'none'; }

      // wire visible send to hidden submit
      if (sendBtn && hiddenSubmit) {
        sendBtn.addEventListener('click', function(e){ hiddenSubmit.click(); });
      }

      // wire Enter (no Shift) inside the last textarea to submit
      const textareas = root.querySelectorAll('textarea');
      if (textareas && textareas.length) {
        const ta = textareas[textareas.length - 1];
        ta.addEventListener('keydown', function(e){
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (hiddenSubmit) hiddenSubmit.click();
          }
        });
      }

      // wire attach button to last file input in DOM
      if (attachBtn) {
        const fileInputs = root.querySelectorAll('input[type=file]');
        if (fileInputs && fileInputs.length) {
          const fileInput = fileInputs[fileInputs.length - 1];
          attachBtn.addEventListener('click', function(){ fileInput.click(); });
        }
      }

      // wire remove-file chip: trigger server-side clear button
      const rem = root.getElementById('remove-file');
      if (rem) {
        rem.addEventListener('click', function(){
          // find hidden "__CLEAR_FILE__" button and click it
          if (clearBtn) { clearBtn.click(); } else {
            // fallback: try to clear by clicking a button with that text
            const btns = Array.from(root.querySelectorAll('button')).filter(b => b.innerText && b.innerText.trim() === '__CLEAR_FILE__');
            if (btns.length) btns[0].click();
          }
        });
      }
    } catch(err) {
      console.warn("GPT UI wiring error:", err);
    }
  }, 600);
})();
</script>
""",
    unsafe_allow_html=True,
)

# ---- handle clear file server-side if that hidden button was clicked ----
# Some Streamlit versions will set the clicked button True; check state key too.
if st.session_state.get("__clear_file_hidden__", False):
    ss.uploaded_case_text = ""
    ss.uploaded_filename = None
    ss.last_uploaded_file_hash = None
    # Clear the st.file_uploader value by resetting the key
    try:
        st.session_state["case_file"] = None
    except Exception:
        pass
    st.experimental_rerun()

# ---- file processing when user chooses a file ----
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

# ---- sending messages: hidden_submit triggers this block because we used st.form_submit_button ----
# hidden_submit will be True only during the run where it was clicked (or when visible send triggered it)
if hidden_submit:
    # retrieve text content from the text area key
    text = (st.session_state.get("chat_textarea", "") or "").strip()
    # if there's attached file content but no text, still allow (we use a default instruction)
    if not text and ss.uploaded_case_text:
        text = "Please summarize and generate a judgment based on the attached case."
    if text or ss.uploaded_case_text:
        with st.spinner("Processing …"):
            response = handle_user_input(text)
        # append upload note if present
        if ss.uploaded_filename:
            current_chat.append({"role": "user", "message": f"[📎 Uploaded: {ss.uploaded_filename}]"})
        # append user and assistant messages
        current_chat.append({"role": "user", "message": text})
        current_chat.append({"role": "assistant", "message": response})
        # update conversation title
        ss.chat_titles[chat_id] = generate_chat_title(text) or "Untitled Case"
        # clear textarea (form clear_on_submit True already cleared it)
        st.experimental_rerun()

# ---- fallback: if visible send HTML button was clicked it triggers hidden_submit via JS so above handles it ----
# ---- end of app ----
