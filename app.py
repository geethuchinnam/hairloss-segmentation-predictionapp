import streamlit as st
import base64
import os

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Artificial Intelligence Career for Women",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# LOAD BACKGROUND IMAGE
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKGROUND_PATH = os.path.join(BASE_DIR, "background.png")

bg_image = ""

if os.path.exists(BACKGROUND_PATH):
    with open(BACKGROUND_PATH, "rb") as f:
        bg_image = base64.b64encode(f.read()).decode()

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    f"""
    <style>

    /* =====================================================
       BACKGROUND
       ===================================================== */

    .stApp {{
        background-image: url("data:image/png;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* =====================================================
       HIDE SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {{
        display: none !important;
    }}

    div[data-testid="stSidebarNav"] {{
        display: none !important;
    }}

    button[data-testid="collapsedControl"] {{
        display: none !important;
    }}

    /* =====================================================
       MAIN HEADING
       ===================================================== */

    .main-title {{
        text-align: center;
        font-size: 44px;
        font-weight: bold;
        color: #FFFFFF;
        text-shadow:
            0px 0px 8px #00E5FF,
            0px 0px 18px #00E5FF;
        margin-top: 10px;
    }}

    .capstone {{
        text-align: center;
        font-size: 25px;
        font-weight: bold;
        color: #FFFFFF;
        text-shadow: 2px 2px 8px black;
        margin-top: 5px;
        margin-bottom: 15px;
    }}

    /* =====================================================
       DARK BOXES
       ===================================================== */

    .st-key-left_box,
    .st-key-right_box {{
        background: rgba(0, 0, 0, 0.94) !important;
        border: 2px solid rgba(255, 255, 255, 0.50) !important;
        border-radius: 15px !important;
        padding: 25px !important;
        min-height: 540px !important;
        box-shadow: 0px 0px 25px rgba(0, 0, 0, 0.95) !important;
        backdrop-filter: blur(12px);
    }}

    /* =====================================================
       BOX HEADINGS
       ===================================================== */

    .box-heading {{
        color: #00E5FF;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
        text-shadow: 0px 0px 8px #00E5FF;
    }}

    .sub-heading {{
        color: #FFD54F;
        font-size: 20px;
        font-weight: bold;
        margin-top: 18px;
        margin-bottom: 8px;
    }}

    .project-title {{
        color: white;
        font-size: 21px;
        font-weight: bold;
        line-height: 1.4;
    }}

    /* =====================================================
       TEXT
       ===================================================== */

    .box-text {{
        color: white;
        font-size: 15px;
        line-height: 1.6;
    }}

    /* =====================================================
       PREDICTION BUTTON
       ===================================================== */

    .stButton > button {{
        background-color: #111111 !important;
        color: white !important;
        border: 2px solid #00E5FF !important;
        border-radius: 10px !important;
        font-size: 17px !important;
        font-weight: bold !important;
        width: 100% !important;
        min-height: 48px !important;
        transition: 0.3s !important;
    }}

    .stButton > button:hover {{
        background-color: #00E5FF !important;
        color: black !important;
        box-shadow: 0px 0px 15px #00E5FF !important;
    }}

    /* =====================================================
       NOTE BOX
       ===================================================== */

    .note-box {{
        margin-top: 18px;
        padding: 12px;
        border-radius: 8px;
        background: rgba(255, 193, 7, 0.12);
        border: 1px solid rgba(255, 193, 7, 0.5);
        color: white;
        font-size: 13px;
        line-height: 1.5;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# TITLE
# =========================================================

st.markdown(
    """
    <div class="main-title">
        ARTIFICIAL INTELLIGENCE CAREER FOR WOMEN (AICW)
    </div>

    <div class="capstone">
        Capstone Project
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# =========================================================
# TWO COLUMNS
# =========================================================

left, right = st.columns(2, gap="large")

# =========================================================
# LEFT BOX
# =========================================================

with left:

    with st.container(border=True, key="left_box"):

        st.markdown(
            """
            <div class="box-heading">
                👥 Team Members
            </div>

            <div class="box-text">

            <p>
            <b>1. Chinnam Navya Sri Geethika</b><br>
            Team Leader<br>
            📧 geetuchinnam3699@gmail.com
            </p>

            <p>
            <b>2. Kona Ramya</b><br>
            📧 ramyakona20@gmail.com
            </p>

            <p>
            <b>3. Pasalapudi Sri Jyothi</b><br>
            📧 jyothipasalapudi69@gmail.com
            </p>

            </div>

            <div class="sub-heading">
                🏫 College
            </div>

            <div class="box-text">
                VSM College of Engineering
            </div>

            <div class="sub-heading">
                👨‍🏫 Guide
            </div>

            <div class="box-text">
                Mr. Abdul Aziz Md<br>
                Co-Lead (AICW)
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# RIGHT BOX
# =========================================================

with right:

    with st.container(border=True, key="right_box"):

        st.markdown(
            """
            <div class="box-heading">
                📌 Project Details
            </div>

            <div class="sub-heading">
                Project Title
            </div>

            <div class="project-title">
                TrichoVision AI – Intelligent Hair & Scalp Analysis
            </div>

            <div class="sub-heading">
                Project Description
            </div>

            <div class="box-text">

            <p>
            TrichoVision AI is an intelligent hair and scalp analysis
            system that uses a U-Net deep learning model to analyze
            a top-view scalp image and generate an image-based
            segmentation estimate.
            </p>

            <p>
            The system segments the affected region, calculates the
            segmented area percentage, and classifies the result into
            Low, Moderate, or High project-defined levels.
            </p>

            <p>
            Gemini Generative AI is integrated to provide result-based
            educational guidance, precautions, and general hair-care
            suggestions.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        # =====================================================
        # PREDICTION LINK
        # THIS BUTTON IS INSIDE THE RIGHT BOX
        # =====================================================

        st.markdown(
            """
            <div style="
                margin-top: 25px;
                margin-bottom: 12px;
                color: #00E5FF;
                font-size: 18px;
                font-weight: bold;
            ">
                🔍 Ready to analyze your image?
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "🔗 Prediction Link",
            use_container_width=True
        ):
            st.switch_page(
                "pages/1_Hair_Loss_Detection.py"
            )

        # =====================================================
        # NOTE
        # =====================================================

        st.markdown(
            """
            <div class="note-box">
                <b>Note:</b> These are project-defined image
                segmentation estimates and not a medical diagnosis.
            </div>
            """,
            unsafe_allow_html=True
        )