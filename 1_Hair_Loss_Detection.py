import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from google import genai
import os
import base64
from dotenv import load_dotenv

# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Hair Loss Detection",
    page_icon="🧑‍🦱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# LOAD SAME BACKGROUND IMAGE
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BACKGROUND_PATH = os.path.join(
    BASE_DIR,
    "background.png"
)

bg_image = ""

if os.path.exists(BACKGROUND_PATH):

    with open(BACKGROUND_PATH, "rb") as f:
        bg_image = base64.b64encode(
            f.read()
        ).decode()

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    f"""
    <style>

    /* =====================================================
       SAME BACKGROUND / BANNER
       ===================================================== */

    .stApp {{
        background-image:
            url("data:image/png;base64,{bg_image}");

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
       MAIN BANNER
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

        color: white;

        text-shadow:
            2px 2px 8px black;

        margin-top: 5px;

        margin-bottom: 15px;
    }}


    /* =====================================================
       DARK MAIN BOXES
       ===================================================== */

    .st-key-upload_box,
    .st-key-analysis_box,
    .st-key-result_box {{
        background: rgba(0, 0, 0, 0.92) !important;

        border: 2px solid rgba(255, 255, 255, 0.45) !important;

        border-radius: 15px !important;

        padding: 25px !important;

        box-shadow:
            0px 0px 25px rgba(0, 0, 0, 0.9) !important;

        backdrop-filter: blur(12px);

        color: white !important;

        margin-bottom: 20px;
    }}


    /* =====================================================
       BOX HEADINGS
       ===================================================== */

    .box-heading {{
        color: #00E5FF;

        font-size: 29px;

        font-weight: bold;

        text-shadow:
            0px 0px 8px #00E5FF;

        margin-bottom: 15px;
    }}

    .sub-heading {{
        color: #FFD54F;

        font-size: 20px;

        font-weight: bold;

        margin-top: 15px;

        margin-bottom: 8px;
    }}


    /* =====================================================
       NORMAL TEXT
       ===================================================== */

    .box-text {{
        color: white;

        font-size: 16px;

        line-height: 1.6;
    }}


    /* =====================================================
       UPLOAD BOX
       ===================================================== */

    .st-key-upload_box [data-testid="stFileUploader"] {{
        background: rgba(255,255,255,0.05);

        border-radius: 10px;

        padding: 10px;
    }}


    /* =====================================================
       METRIC
       ===================================================== */

    [data-testid="stMetric"] {{
        background: rgba(0, 0, 0, 0.55);

        border: 1px solid rgba(255,255,255,0.25);

        border-radius: 10px;

        padding: 15px;
    }}


    /* =====================================================
       INFO / WARNING / SUCCESS BOXES
       ===================================================== */

    .stAlert {{
        background: rgba(0, 0, 0, 0.65) !important;

        border-radius: 10px !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SAME BANNER
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
# PAGE TITLE
# =========================================================

st.markdown(
    """
    <div class="box-heading">
        🧑‍🦱 Hair Loss Detection & Segmentation
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="box-text">
        Upload a top-view scalp image to generate an
        image-based segmentation estimate.
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# LOAD U-NET MODEL
# =========================================================

@st.cache_resource
def load_model():

    return tf.keras.models.load_model(
        os.path.join(
            BASE_DIR,
            "hair_loss_unet.keras"
        ),
        compile=False
    )


model = load_model()

# =========================================================
# LOAD GEMINI
# =========================================================

@st.cache_resource
def load_gemini_client():

    try:

        if not GEMINI_API_KEY:
            return None

        return genai.Client(
            api_key=GEMINI_API_KEY
        )

    except Exception:

        return None


gemini_client = load_gemini_client()

# =========================================================
# GEMINI GUIDANCE
# =========================================================

def generate_gemini_guidance(
    category,
    percentage
):

    if gemini_client is None:

        return (
            "Gemini AI could not be initialized. "
            "Please check GEMINI_API_KEY in the .env file."
        )

    prompt = f"""
You are an educational hair-care assistant inside a student computer-vision project.

The U-Net model produced an image-based segmented-area estimate:

Estimated category: {category}

Segmented area: {percentage:.2f}%

Important:

- Do NOT diagnose hair loss or any medical condition.
- Do NOT claim that the percentage proves a disease or clinical stage.
- Explain that the result is only a project-defined image segmentation estimate.
- Give practical, general, safe hair/scalp-care suggestions.
- For Moderate and High, recommend discussing persistent, sudden, worsening or concerning changes with a qualified healthcare professional.
- Do not recommend prescription medicines or supplements.
- Keep the response easy to understand.

Return exactly these sections:

1. What the result means
2. Recommended precautions
3. What you can do
4. When to seek professional advice

Use 3-5 concise bullet points under each section.
"""

    try:

        response = gemini_client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return response.text

    except Exception:

        return (
            "Gemini guidance is temporarily unavailable. "
            "The model result above is still available."
        )

# =========================================================
# UPLOAD BOX
# =========================================================

with st.container(border=True, key="upload_box"):

    st.markdown(
        """
        <div class="box-heading">
            📷 Upload Scalp Image
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Choose a scalp image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ]
    )

# =========================================================
# IMAGE PROCESSING
# =========================================================

if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    ).convert("RGB")

    original = np.array(image)

    resized = cv2.resize(
        original,
        (256, 256)
    )

    input_image = (
        resized.astype(
            np.float32
        ) / 255.0
    )

    input_image = np.expand_dims(
        input_image,
        axis=0
    )

    # =====================================================
    # MODEL PREDICTION
    # =====================================================

    with st.spinner(
        "Analyzing image..."
    ):

        prediction = model.predict(
            input_image,
            verbose=0
        )

    mask = (
        prediction[0, :, :, 0] > 0.1
    ).astype(
        np.uint8
    ) * 255

    # =====================================================
    # MORPHOLOGICAL CLEANING
    # =====================================================

    kernel = np.ones(
        (7, 7),
        np.uint8
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    # =====================================================
    # REMOVE SMALL COMPONENTS
    # =====================================================

    num_labels, labels, stats, centroids = (
        cv2.connectedComponentsWithStats(
            mask,
            connectivity=8
        )
    )

    clean_mask = np.zeros_like(
        mask
    )

    for i in range(
        1,
        num_labels
    ):

        area = stats[
            i,
            cv2.CC_STAT_AREA
        ]

        if area > 500:

            clean_mask[
                labels == i
            ] = 255

    mask = clean_mask

    # =====================================================
    # RESIZE MASK
    # =====================================================

    mask_original = cv2.resize(
        mask,
        (
            original.shape[1],
            original.shape[0]
        ),
        interpolation=cv2.INTER_NEAREST
    )

    # =====================================================
    # CREATE OVERLAY
    # =====================================================

    overlay = original.copy()

    overlay[
        mask_original > 0
    ] = (
        255,
        0,
        0
    )

    result = cv2.addWeighted(
        original,
        0.7,
        overlay,
        0.3,
        0
    )

    # =====================================================
    # CALCULATE PERCENTAGE
    # =====================================================

    total_pixels = (
        mask_original.size
    )

    affected_pixels = np.sum(
        mask_original > 0
    )

    percentage = (
        affected_pixels /
        total_pixels
    ) * 100

    # =====================================================
    # CATEGORY
    # =====================================================

    if percentage < 10:

        category = "Low"

    elif percentage < 25:

        category = "Moderate"

    else:

        category = "High"

    # =====================================================
    # IMAGE ANALYSIS BOX
    # =====================================================

    with st.container(
        border=True,
        key="analysis_box"
    ):

        st.markdown(
            """
            <div class="box-heading">
                📊 Image Analysis
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        # -------------------------------------------------
        # ORIGINAL IMAGE
        # -------------------------------------------------

        with col1:

            st.markdown(
                """
                <div class="sub-heading">
                    📷 Original Image
                </div>
                """,
                unsafe_allow_html=True
            )

            st.image(
                original,
                use_container_width=True
            )

        # -------------------------------------------------
        # SEGMENTATION RESULT
        # -------------------------------------------------

        with col2:

            st.markdown(
                """
                <div class="sub-heading">
                    🎯 Segmentation Result
                </div>
                """,
                unsafe_allow_html=True
            )

            st.image(
                result,
                use_container_width=True
            )

        # -------------------------------------------------
        # PREDICTED MASK
        # -------------------------------------------------

        st.markdown(
            """
            <div class="sub-heading">
                🎭 Predicted Mask
            </div>
            """,
            unsafe_allow_html=True
        )

        st.image(
            mask_original,
            width=400
        )

    # =====================================================
    # RESULT BOX
    # =====================================================

    with st.container(
        border=True,
        key="result_box"
    ):

        st.markdown(
            """
            <div class="box-heading">
                📈 Prediction Result
            </div>
            """,
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # SEGMENTED AREA
        # -------------------------------------------------

        st.markdown(
            """
            <div class="sub-heading">
                Estimated Segmented Area
            </div>
            """,
            unsafe_allow_html=True
        )

        st.metric(
            "Segmented Area",
            f"{percentage:.2f}%"
        )

        # -------------------------------------------------
        # CATEGORY
        # -------------------------------------------------

        st.markdown(
            f"""
            <div class="sub-heading">
                📌 Project-Defined Level
            </div>

            <div class="box-text">
                Estimated Level: <b>{category.upper()}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        if category == "Low":

            st.success(
                f"Estimated Level: LOW | "
                f"Segmented Area: "
                f"{percentage:.2f}%"
            )

        elif category == "Moderate":

            st.warning(
                f"Estimated Level: MODERATE | "
                f"Segmented Area: "
                f"{percentage:.2f}%"
            )

        else:

            st.error(
                f"Estimated Level: HIGH | "
                f"Segmented Area: "
                f"{percentage:.2f}%"
            )

        # -------------------------------------------------
        # GEMINI
        # -------------------------------------------------

        st.markdown(
            """
            <div class="sub-heading">
                🤖 Generative AI Guidance
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.spinner(
            "Generating result-based educational guidance..."
        ):

            ai_guidance = generate_gemini_guidance(
                category,
                percentage
            )

        st.markdown(
            ai_guidance
        )

        # -------------------------------------------------
        # DISCLAIMER
        # -------------------------------------------------

        st.info(
            "⚠️ Low, Moderate, and High are "
            "project-defined image-segmentation estimates. "
            "They are not clinically validated hair-loss "
            "stages and should not be treated as a medical diagnosis."
        )