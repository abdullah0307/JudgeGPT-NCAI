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

# ---------- page ----------
st.set_page_config(
    page_title="PakLaw Judicial Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- css ----------
st.markdown(
    """
<style>
:root {
    --brand: #2E3B55;
    --accent: #10a37f;
    --bg-chat: #f9f9f9;
    --bg-sidebar: #ffffff;
    --radius: 18px;
}

html, body, .main {
    background-color: var(--bg-chat);
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 7rem;
    max-width: 820px;
    margin: auto;
}

[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar);
    border-right: 1px solid #e5e7eb;
}

.chat-user, .chat-assistant {
    max-width: 85%;
    padding: .9rem 1.2rem;
    border-radius: var(--radius);
    margin: 0.8rem 0;
    line-height: 1.5;
    word-wrap: break-word;
    font-size: 0.95rem;
}
.chat-user {
    background: #ffffff;
    border: 1px solid #ddd;
    margin-left: auto;
}
.chat-assistant {
    background: #f0f2f5;
    border: 1px solid #ddd;
    margin-right: auto;
}

/* Sticky input bar */
.chat-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #fff;
    border-top: 1px solid #ddd;
    padding: .8rem 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    z-index: 1000;
}
.chat-input {
    flex: 1;
    resize: none;
    border-radius: var(--radius);
    border: 1px solid #ccc;
    padding: .7rem 1rem;
    font-size: 1rem;
    height: 70px;
}
.chat-input:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 .15rem rgba(16,163,127,.35);
}
.icon-btn {
    border: none;
    background: transparent;
    font-size: 1.4rem;
    cursor: pointer;
    color: #555;
}
.icon-btn:hover {
    color: var(--accent);
}
.send-btn {
    border-radius: var(--radius);
    font-weight: 600;
    background: var(--accent);
    border: none;
    color: #fff;
    padding: .6rem 1.2rem;
    cursor: pointer;
}
.send-btn:hover {
    background: #0e8f6e;
}
.uploaded-file {
    font-size: 0.85rem;
    color: #444;
    margin-bottom: 0.4rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- session ----------
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "chat_titles" not in st.session_state:
    st.session_state.chat_titles = {}
if "current_chat" not in st.session_state:
    cid = str(uuid.uuid4())
    st.session_state.current_chat = cid
    st.session_state.chats[cid] = []
    st.session_state.chat_titles[cid] = "New Case"
if "uploaded_case_text" not in st.session_state:
    st.session_state.uploaded_case_text = ""
if "last_uploaded_file_hash" not in st.session_state:
    st.session_state.last_uploaded_file_hash = None
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None

# ---------- sidebar ----------
with st.sidebar:
    st.markdown("### 📁 Case Files")
    if st.button("➕ New Case", use_container_width=True):
        cid = str(uuid.uuid4())
        st.session_state.current_chat = cid
        st.session_state.chats[cid] = []
        st.session_state.chat_titles[cid] = "New Case"
        st.session_state.uploaded_case_text = ""
        st.session_state.last_uploaded_file_hash = None
        st.session_state.uploaded_filename = None
        st.rerun()

    for cid in list(st.session_state.chats.keys()):
        title = st.session_state.chat_titles.get(cid, f"Case {cid[:8]}")
        if st.button(title, key=f"chat_{cid}", use_container_width=True):
            st.session_state.current_chat = cid
            st.rerun()

# ---------- header ----------
st.title("⚖️ PakLaw Judicial Assistant")
st.caption("Interactive legal assistant for Pakistan’s judicial system.")

# ---------- chat display ----------
chat_id = st.session_state.current_chat
current_chat = st.session_state.chats[chat_id]

chat_area = st.container()
with chat_area:
    for idx, msg in enumerate(current_chat):
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">{msg["message"]}</div>', unsafe_allow_html=True)
        else:
            html = re.sub(r"(?m)^([A-Z][a-z]+):", r"<strong>\\1:</strong>", msg["message"])
            html = html.replace("\\n", "<br>")
            st.markdown(f'<div class="chat-assistant">{html}</div>', unsafe_allow_html=True)
            download_agent.show_download_if_applicable(idx, current_chat, intent_classifier.classify_prompt_intent)

# ---------- sticky input ----------
st.markdown('<div class="chat-bar">', unsafe_allow_html=True)

# File uploader (hidden, triggered by + button)
uploaded_file = st.file_uploader(
    "Upload Case File (.txt or .pdf)",
    type=["txt", "pdf"],
    label_visibility="collapsed",
    key="file_upload",
)

col1, col2, col3 = st.columns([0.5, 6, 1])
with col1:
    st.markdown('<button class="icon-btn">➕</button>', unsafe_allow_html=True)

with col2:
    user_input = st.text_area(
        "Enter your judicial query:",
        key="user_input",
        label_visibility="collapsed",
        placeholder="Type your legal query...",
    )

with col3:
    submitted = st.button("Send", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Show uploaded file name
if uploaded_file:
    max_mb = 10
    if uploaded_file.size > max_mb * 1024 * 1024:
        st.error(f"❌ File too large. Max {max_mb} MB allowed.")
    else:
        file_bytes = uploaded_file.read()
        file_hash = hashlib.md5(file_bytes).hexdigest()
        if st.session_state.last_uploaded_file_hash != file_hash:
            st.session_state.last_uploaded_file_hash = file_hash
            try:
                if uploaded_file.name.lower().endswith(".txt"):
                    st.session_state.uploaded_case_text = file_bytes.decode("utf-8")
                    st.session_state.uploaded_filename = uploaded_file.name
                else:
                    reader = PdfReader(BytesIO(file_bytes))
                    if len(reader.pages) > 30:
                        st.error("❌ PDF too long. Max 30 pages.")
                    else:
                        txt = extract_pdf_text_with_vision(file_bytes)
                        if not txt or len(txt.strip()) < 50:
                            st.error("❌ No meaningful text extracted.")
                        else:
                            st.session_state.uploaded_case_text = txt[:10_000]
                            st.session_state.uploaded_filename = uploaded_file.name
            except Exception as e:
                st.error(f"❌ Could not read file: {e}")

if st.session_state.uploaded_filename:
    st.markdown(f"<div class='uploaded-file'>📎 {st.session_state.uploaded_filename}</div>", unsafe_allow_html=True)

# ---------- query handler ----------
if submitted and (user_input or st.session_state.uploaded_case_text):
    query = user_input.strip() or "Generate legal judgment"
    with st.spinner("Processing …"):
        response = handle_user_input(query)

    if st.session_state.uploaded_filename:
        current_chat.append({"role": "user", "message": f"[📎 Uploaded: {st.session_state.uploaded_filename}]"})

    current_chat.append({"role": "user", "message": query})
    current_chat.append({"role": "assistant", "message": response})

    st.session_state.chat_titles[chat_id] = generate_chat_title(query) or "Untitled Case"
    st.rerun()
