# ============================================================
# MAILGUARD - SPAM EMAIL DETECTOR
# ============================================================

import streamlit as st
import joblib
import re
import nltk
import time
import math
from nltk.corpus import stopwords


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MailGuard | Email Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       BACKGROUND
    ====================================================== */

    .stApp {

        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(93, 43, 255, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(0, 130, 255, 0.13),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(255, 0, 100, 0.08),
                transparent 35%
            ),
            #020204;

        color: white;

    }


    /* ======================================================
       HIDE STREAMLIT MENU
    ====================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* ======================================================
       MAIN CONTAINER
    ====================================================== */

    .block-container {

        max-width: 1000px;

        padding-top: 30px;

        padding-bottom: 50px;

    }


    /* ======================================================
       LARGE FONTS
    ====================================================== */

    h1 {

        font-size: 48px !important;

        font-weight: 900 !important;

        color: white !important;

    }


    h2 {

        font-size: 32px !important;

        font-weight: 800 !important;

        color: white !important;

    }


    h3 {

        font-size: 25px !important;

        font-weight: 800 !important;

        color: white !important;

    }


    p {

        font-size: 16px !important;

        color: #999 !important;

    }


    /* ======================================================
       TEXT AREA
    ====================================================== */

    textarea {

        background-color:
            #09090d !important;

        color:
            #eeeeee !important;

        border:
            1px solid #292932 !important;

        border-radius:
            16px !important;

        font-size:
            16px !important;

        line-height:
            1.8 !important;

        padding:
            15px !important;

    }


    textarea:focus {

        border-color:
            #7c3aed !important;

        box-shadow:
            0 0 0 1px #7c3aed,
            0 0 30px rgba(124,58,237,.20)
            !important;

    }


    /* ======================================================
       BUTTONS
    ====================================================== */

    .stButton > button {

        width: 100%;

        min-height: 52px;

        border-radius: 13px !important;

        border:
            1px solid #292932 !important;

        background:
            #0b0b10 !important;

        color:
            white !important;

        font-size:
            15px !important;

        font-weight:
            700 !important;

        transition:
            all .25s ease;

    }


    .stButton > button:hover {

        transform:
            translateY(-3px);

        border-color:
            #7c3aed !important;

        background:
            #151020 !important;

        box-shadow:
            0 10px 30px
            rgba(124,58,237,.20);

    }


    /* ======================================================
       CHECK BUTTON
    ====================================================== */

    div.stButton:nth-of-type(4) > button {

        background:
            linear-gradient(
                135deg,
                #7c3aed,
                #2563eb
            ) !important;

        border:
            none !important;

        min-height:
            58px;

        font-size:
            17px !important;

        font-weight:
            800 !important;

        box-shadow:
            0 10px 35px
            rgba(76,29,149,.45);

    }


    div.stButton:nth-of-type(4) > button:hover {

        transform:
            translateY(-4px);

        box-shadow:
            0 18px 50px
            rgba(76,29,149,.65);

    }


    /* ======================================================
       ALERT BASE
    ====================================================== */

    [data-testid="stAlert"] {

        border-radius:
            18px !important;

        font-size:
            17px !important;

        padding:
            18px !important;

    }


    /* ======================================================
       SPAM RED ALERT
    ====================================================== */

    [data-testid="stAlert"][kind="error"] {

        background:
            rgba(127,29,29,.22) !important;

        border:
            2px solid
            rgba(239,68,68,.75) !important;

        box-shadow:
            0 0 40px
            rgba(239,68,68,.25);

        animation:
            spamShake .55s ease-in-out;

    }


    /* ======================================================
       RED SHAKE ANIMATION
    ====================================================== */

    @keyframes spamShake {

        0% {
            transform: translateX(0);
        }

        10% {
            transform: translateX(-10px);
        }

        20% {
            transform: translateX(10px);
        }

        30% {
            transform: translateX(-9px);
        }

        40% {
            transform: translateX(9px);
        }

        50% {
            transform: translateX(-7px);
        }

        60% {
            transform: translateX(7px);
        }

        70% {
            transform: translateX(-5px);
        }

        80% {
            transform: translateX(5px);
        }

        90% {
            transform: translateX(-2px);
        }

        100% {
            transform: translateX(0);
        }

    }


    /* ======================================================
       SAFE GREEN ALERT
    ====================================================== */

    [data-testid="stAlert"][kind="success"] {

        background:
            rgba(6,78,59,.20) !important;

        border:
            2px solid
            rgba(34,197,94,.55) !important;

        box-shadow:
            0 0 40px
            rgba(34,197,94,.18);

        animation:
            safeAppear .7s ease;

    }


    /* ======================================================
       SAFE ANIMATION
    ====================================================== */

    @keyframes safeAppear {

        0% {

            transform:
                scale(.90);

            opacity:
                0;

        }

        60% {

            transform:
                scale(1.04);

            opacity:
                1;

        }

        100% {

            transform:
                scale(1);

            opacity:
                1;

        }

    }


    /* ======================================================
       METRIC CARDS
    ====================================================== */

    [data-testid="stMetric"] {

        background:
            rgba(255,255,255,.025);

        border:
            1px solid
            rgba(255,255,255,.08);

        padding:
            18px;

        border-radius:
            16px;

    }


    [data-testid="stMetricLabel"] {

        color:
            #888 !important;

        font-size:
            14px !important;

    }


    [data-testid="stMetricValue"] {

        color:
            white !important;

        font-size:
            26px !important;

    }


    /* ======================================================
       PROGRESS BAR
    ====================================================== */

    .stProgress > div > div > div > div {

        background:
            linear-gradient(
                90deg,
                #7c3aed,
                #2563eb
            );

    }


    /* ======================================================
       MOBILE
    ====================================================== */

    @media(max-width:700px) {

        .block-container {

            padding-left:
                15px;

            padding-right:
                15px;

            padding-top:
                20px;

        }


        h1 {

            font-size:
                40px !important;

        }


        h2 {

            font-size:
                28px !important;

        }


        h3 {

            font-size:
                22px !important;

        }


        p {

            font-size:
                14px !important;

        }


        textarea {

            font-size:
                14px !important;

        }


        .stButton > button {

            min-height:
                46px;

            font-size:
                13px !important;

        }


        [data-testid="stMetricValue"] {

            font-size:
                20px !important;

        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD STOPWORDS
# ============================================================

@st.cache_resource
def load_stopwords():

    try:

        return set(
            stopwords.words("english")
        )

    except LookupError:

        nltk.download(
            "stopwords",
            quiet=True
        )

        return set(
            stopwords.words("english")
        )


stop_words = load_stopwords()


# ============================================================
# LOAD MODEL AND VECTORIZER
# ============================================================

@st.cache_resource
def load_model():

    model = joblib.load(
        "spam_model.pkl"
    )

    vectorizer = joblib.load(
        "tfidf_vectorizer.pkl"
    )

    return model, vectorizer


model, vectorizer = load_model()


# ============================================================
# CLEAN TEXT FUNCTION
# ============================================================

def clean_text(text):

    text = str(text).lower()


    # Remove HTML
    text = re.sub(
        r"<.*?>",
        " ",
        text
    )


    # Remove URLs
    text = re.sub(
        r"http\S+|www\S+|https\S+",
        " ",
        text
    )


    # Remove email addresses
    text = re.sub(
        r"\S+@\S+",
        " ",
        text
    )


    # Remove special characters
    text = re.sub(
        r"[^a-zA-Z\s]",
        " ",
        text
    )


    # Split words
    words = text.split()


    # Remove stopwords
    words = [
        word
        for word in words
        if word not in stop_words
    ]


    return " ".join(words)


# ============================================================
# SESSION STATE
# ============================================================

if "email" not in st.session_state:

    st.session_state.email = ""


if "result" not in st.session_state:

    st.session_state.result = None


if "confidence" not in st.session_state:

    st.session_state.confidence = None


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns(
    [3, 1]
)


with header_left:

    st.title(
        "🛡️ MailGuard"
    )

    st.caption(
        "EMAIL SECURITY"
    )


with header_right:

    st.success(
        "● Protection Active"
    )


st.divider()


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    "# Keep your inbox **safe & clean.**"
)


st.write(
    "Check suspicious emails instantly and discover "
    "whether a message looks safe or dangerous."
)


# ============================================================
# TRUST FEATURES
# ============================================================

trust1, trust2, trust3, trust4 = st.columns(4)


with trust1:

    st.metric(
        "⚡",
        "Instant",
        "Results"
    )


with trust2:

    st.metric(
        "🔒",
        "Privacy",
        "First"
    )


with trust3:

    st.metric(
        "🧠",
        "Smart",
        "Detection"
    )


with trust4:

    st.metric(
        "✓",
        "Easy",
        "To Use"
    )


st.write("")


# ============================================================
# EMAIL INPUT
# ============================================================

st.subheader(
    "📩 Paste your email"
)


email = st.text_area(
    "Email content",
    value=st.session_state.email,
    height=230,
    placeholder=(
        "Paste the complete email here...\n\n"
        "Example:\n"
        "Subject: Congratulations! You have won a prize...\n\n"
        "Paste the email and click CHECK EMAIL."
    ),
    label_visibility="collapsed"
)


st.session_state.email = email


# ============================================================
# CHARACTER COUNT
# ============================================================

st.caption(
    f"Characters: {len(email):,}"
)


# ============================================================
# SAMPLE EMAILS
# ============================================================

st.caption(
    "TRY A SAMPLE"
)


sample1, sample2, sample3 = st.columns(3)


with sample1:

    suspicious_button = st.button(
        "🚨 Suspicious",
        use_container_width=True
    )


with sample2:

    normal_button = st.button(
        "📩 Normal",
        use_container_width=True
    )


with sample3:

    clear_button = st.button(
        "✨ Clear",
        use_container_width=True
    )


# ============================================================
# SUSPICIOUS SAMPLE
# ============================================================

if suspicious_button:

    st.session_state.email = """Subject: Congratulations! You have won $1,000,000!!!

Dear Winner,

You have been selected to receive an exclusive cash prize of $1,000,000.

Click here immediately to claim your reward.

Send your bank account details and personal information to process the payment.

This offer expires today.

Congratulations!"""


    st.session_state.result = None

    st.session_state.confidence = None

    st.rerun()


# ============================================================
# NORMAL SAMPLE
# ============================================================

if normal_button:

    st.session_state.email = """Subject: Meeting Reminder

Hi Team,

This is a reminder that our project meeting is scheduled for tomorrow at 10 AM.

We will discuss the project progress and the tasks planned for next week.

Regards,
Team Lead"""


    st.session_state.result = None

    st.session_state.confidence = None

    st.rerun()


# ============================================================
# CLEAR
# ============================================================

if clear_button:

    st.session_state.email = ""

    st.session_state.result = None

    st.session_state.confidence = None

    st.rerun()


# ============================================================
# CHECK EMAIL BUTTON
# ============================================================

st.write("")


check_button = st.button(
    "🛡️ CHECK EMAIL",
    use_container_width=True
)


# ============================================================
# EMAIL PREDICTION
# ============================================================

if check_button:

    if not email.strip():

        st.warning(
            "⚠️ Please paste an email before checking."
        )

    else:

        # ----------------------------------------------------
        # SCANNING
        # ----------------------------------------------------

        progress = st.progress(
            0
        )

        status = st.empty()


        scanning_steps = [

            "🔍 Reading email...",

            "🧩 Checking suspicious patterns...",

            "🧠 Analyzing message...",

            "🔐 Finalizing security check..."

        ]


        for index, message in enumerate(
            scanning_steps
        ):

            status.info(
                message
            )

            progress.progress(
                (index + 1) * 25
            )

            time.sleep(
                0.4
            )


        # ----------------------------------------------------
        # CLEAN EMAIL
        # ----------------------------------------------------

        cleaned_email = clean_text(
            email
        )


        # ----------------------------------------------------
        # TRANSFORM EMAIL
        # ----------------------------------------------------

        email_vector = vectorizer.transform(
            [cleaned_email]
        )


        # ----------------------------------------------------
        # PREDICT
        # ----------------------------------------------------

        prediction = model.predict(
            email_vector
        )[0]


        # ----------------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------------

        try:

            decision = model.decision_function(
                email_vector
            )[0]


            confidence = (

                1 /

                (

                    1 +

                    math.exp(
                        -abs(
                            float(decision)
                        )
                    )

                )

            ) * 100


            confidence = min(
                max(
                    confidence,
                    50.0
                ),
                99.9
            )


        except Exception:

            confidence = 90.0


        # ----------------------------------------------------
        # SAVE RESULT
        # ----------------------------------------------------

        st.session_state.result = int(
            prediction
        )

        st.session_state.confidence = confidence


        # Remove scanning UI

        progress.empty()

        status.empty()


        # Rerun so the result animation starts fresh

        st.rerun()


# ============================================================
# RESULT SECTION
# ============================================================

if st.session_state.result is not None:

    prediction = st.session_state.result

    confidence = st.session_state.confidence


    st.divider()


    # ========================================================
    # SPAM
    # ========================================================

    if prediction == 1:

        # BIG RED ALERT
        st.error(
            "🚨  SECURITY ALERT — BE CAREFUL"
        )


        # Extra large warning
        st.markdown(
            "## 🚨 This email looks suspicious"
        )


        st.warning(
            "⚠️ Avoid clicking links or sharing "
            "personal information from this message."
        )


        # Detection strength

        st.markdown(
            "### Detection strength"
        )


        st.progress(
            int(confidence)
        )


        st.caption(
            f"Detection strength: {confidence:.1f}%"
        )


        # Spam information

        result1, result2, result3 = st.columns(3)


        with result1:

            st.metric(
                "Status",
                "🚨 SPAM"
            )


        with result2:

            st.metric(
                "Risk",
                "HIGH"
            )


        with result3:

            st.metric(
                "Action",
                "AVOID"
            )


    # ========================================================
    # SAFE
    # ========================================================

    else:

        # 🎉 Celebration
        st.balloons()


        # GREEN SUCCESS ALERT
        st.success(
            "🛡️  SECURITY CHECK COMPLETE — LOOKS GOOD"
        )


        # Extra large success message
        st.markdown(
            "## 🎉 This email looks safe"
        )


        st.info(
            "Nothing suspicious was detected in this "
            "email based on the current security check."
        )


        # Safety confidence

        st.markdown(
            "### Safety confidence"
        )


        st.progress(
            int(confidence)
        )


        st.caption(
            f"Safety confidence: {confidence:.1f}%"
        )


        # Safe information

        result1, result2, result3 = st.columns(3)


        with result1:

            st.metric(
                "Status",
                "✅ SAFE"
            )


        with result2:

            st.metric(
                "Risk",
                "LOW"
            )


        with result3:

            st.metric(
                "Action",
                "OK"
            )


# ============================================================
# PROTECTION FEATURES
# ============================================================

st.write("")

st.divider()


st.subheader(
    "🛡️ MailGuard Protection"
)


feature1, feature2, feature3 = st.columns(3)


with feature1:

    st.info(
        "⚡ **Instant Detection**\n\n"
        "Get your email safety result within seconds."
    )


with feature2:

    st.info(
        "🔐 **Privacy Focused**\n\n"
        "Email content is processed directly by the application."
    )


with feature3:

    st.info(
        "🎯 **Smart Analysis**\n\n"
        "Automatically checks your email for suspicious patterns."
    )


# ============================================================
# FOOTER
# ============================================================

st.write("")

st.caption(
    "🛡️ MailGuard • Smart Email Protection"
)