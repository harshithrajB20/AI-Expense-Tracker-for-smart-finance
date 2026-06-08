import streamlit as st
import requests
import json
from datetime import date, datetime
import uuid
import time
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go


from config import API_URL

def mark_notifications_read():
    try:
        token = st.session_state.get("access_token")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        requests.post(
            f"{API_URL}/dashboard/mark-read/",
            headers=headers
        )

    except Exception as e:
        print("Mark read error:", e)
if "notifications_refresh" not in st.session_state:
    st.session_state.notifications_refresh = 0

# Initialize session state for form keys
if 'form_keys' not in st.session_state:
    st.session_state.form_keys = {
        'login': str(time.time()),
        'register': str(time.time() + 1),
        'profile': str(time.time() + 2),
        'budget': str(time.time() + 3),
        'transaction': str(time.time() + 4),
        'ai': str(time.time() + 5)
    }

# This MUST be the first Streamlit command
st.set_page_config(
    page_title="FINALYZE - AI Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="auto"
)

# Update the CSS section (around line 100) with improved metric card styling:

st.markdown("""
<style>
/* =========================== */
/* GLOBAL BACKGROUND FIX */
/* =========================== */

html, body, [data-testid="stApp"] {
    background: var(--background-color) !important;
    color: var(--text-color) !important;
}

/* Center Streamlit tabs */
div[data-baseweb="tab-list"] {
    justify-content: center !important;
}

/* Optional: nicer spacing */
div[data-baseweb="tab"] {
    font-size: 16px;
    font-weight: 600;
    padding: 8px 24px;
}
/* Main content area */
.block-container {
    padding-top: 0.75rem !important;
    padding-bottom: 0.75rem !important;
    background: transparent !important;
}

/* =========================== */
/* METRIC CARDS - FIXED FOR VISIBILITY */
/* =========================== */
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem !important;
    border-radius: 12px;
    margin: 0 !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Target the metric container */
.metric-card [data-testid="stMetric"] {
    background: transparent !important;
    padding: 0 !important;
}

/* Metric label */
.metric-card [data-testid="stMetricLabel"] {
    color: rgba(255, 255, 255, 0.9) !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    margin-bottom: 0.25rem !important;
}

/* Metric value */
.metric-card [data-testid="stMetricValue"] {
    color: white !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    line-height: 1.2 !important;
}

/* Metric delta (arrow and delta value) - FIXED FOR VISIBILITY */
.metric-card [data-testid="stMetricDelta"] {
    color: white !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    background: rgba(255, 255, 255, 0.2) !important;
    padding: 0.2rem 0.5rem !important;
    border-radius: 20px !important;
    display: inline-block !important;
    margin-top: 0.25rem !important;
}

/* Delta icon (arrow) */
.metric-card [data-testid="stMetricDelta"] svg,
.metric-card [data-testid="stMetricDelta"] [data-icon] {
    color: white !important;
    fill: white !important;
    stroke: white !important;
}

/* Delta value text */
.metric-card [data-testid="stMetricDelta"] span {
    color: white !important;
    font-weight: 600 !important;
}

/* Positive delta styling */
.metric-card [data-testid="stMetricDelta"][data-direction="up"] {
    background: rgba(72, 187, 120, 0.3) !important;
}

/* Negative delta styling */
.metric-card [data-testid="stMetricDelta"][data-direction="down"] {
    background: rgba(245, 101, 101, 0.3) !important;
}

/* =========================== */
/* HEADERS */
/* =========================== */
.main-header {
    font-size: 2.5rem;
    font-weight: 700;
    color: #3B82F6;
    margin-bottom: 0.25rem !important;
    padding-bottom: 0.25rem;
    border-bottom: 1px solid rgba(255,255,255,0.2);
}

.sub-header {
    font-size: 1.4rem;
    font-weight: 600;
    color: #CBD5E1;
    margin-bottom: 0.25rem !important;
}

/* =========================== */
/* CARDS */
/* =========================== */
.card {
    background: #FFFFFF;
    padding: 1.25rem;
    border-radius: 12px;
    box-shadow: 0 6px 14px rgba(0, 0, 0, 0.25);
    border: none;
    margin: 0.5rem 0 !important;
}

/* =========================== */
/* BUTTONS */
/* =========================== */
.stButton>button {
    width: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
}

/* =========================== */
/* TABS */
/* =========================== */
.stTabs [data-baseweb="tab-list"] {
    background: #111827;
    padding: 6px;
    border-radius: 10px;
    margin-bottom: 0.25rem !important;
}

.stTabs [data-baseweb="tab"] {
    color: #CBD5E1;
    border-radius: 8px;
}

.stTabs [aria-selected="true"] {
    background: #1F2933;
    color: white;
}

/* =========================== */
/* DATAFRAMES */
/* =========================== */
.dataframe {
    border-radius: 10px;
    overflow: hidden;
}

/* =========================== */
/* SIDEBAR */
/* =========================== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E3A8A 0%, #1E40AF 100%);
}

/* =========================== */
/* HIDE STREAMLIT UI */
/* =========================== */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# Constants
BASE_URL = "http://127.0.0.1:8000/api"
API_URL = BASE_URL

# Currency symbols
CURRENCY_SYMBOLS = {
    "INR": "₹",
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "AUD": "A$",
}


# Session state initialization
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "active_section" not in st.session_state:
    st.session_state.active_section = "dashboard"
if "active_subsection" not in st.session_state:
    st.session_state.active_subsection = None
if "last_notification_id" not in st.session_state:
    st.session_state.last_notification_id = None


def save_token(token):
    st.session_state.access_token = token


def get_headers():
    """
    Attach JWT token to every request
    """
    token = st.session_state.get("access_token")

    if not token:
        return {
            "Content-Type": "application/json"
        }

    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def section_header(title, icon=""):
    st.markdown(
        f"""
        <div style="
            font-size:1.6rem;
            font-weight:700;
            color:#3B82F6;
            margin:0.75rem 0 0.5rem 0;
            padding-bottom:0.25rem;
            border-bottom:1px solid rgba(255,255,255,0.15);
        ">
            {icon} {title}
        </div>
        """,
        unsafe_allow_html=True
    )
# ===============================
# NOTIFICATIONS
# ===============================

def fetch_notifications():
    try:
        token = st.session_state.get("access_token")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(
            f"{API_URL}/dashboard/",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()

            # ✅ IMPORTANT LINE
            return data.get("notifications", [])

        return []

    except Exception as e:
        print("Notification error:", e)
        return []


def notifications_panel():

    # =========================
    # Header + Clear Button
    # =========================
    col1, col2 = st.columns([8, 1])

    with col1:
        section_header("Notifications", "🔔")

    with col2:
        if st.button("🗑", key="open_clear_notifs", help="Clear all notifications"):
            st.session_state.show_clear_confirm = True

    # =========================
    # CLEAR CONFIRM PANEL (ONLY ONCE)
    # =========================
    if st.session_state.get("show_clear_confirm", False):

        st.warning("⚠️ This will permanently delete ALL notifications.")

        confirm = st.checkbox(
            "I understand. Clear all notifications.",
            key="confirm_clear_dashboard"
        )

        if confirm:
            if st.button("🗑 Confirm Clear", use_container_width=True,
                         key="confirm_clear_btn_dashboard"):

                resp = requests.delete(
                    f"{API_URL}/dashboard/notifications/clear/",
                    headers=get_headers(),
                    json={"confirm": True}
                )

                if resp.status_code == 200:
                    st.success("✅ Notifications cleared")

                    # hide confirmation panel
                    st.session_state.show_clear_confirm = False

                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Failed to clear notifications")

    # =========================
    # Fetch Notifications
    # =========================
    notifications = fetch_notifications()

    if not notifications:
        st.info("No notifications yet.")
        return

    # =========================
    # Display Notifications
    # =========================
    for notif in notifications[:10]:

        is_fx = "Foreign Currency" in notif.get("title", "")

        bg = "#FEF3C7" if is_fx else "#F3F4F6"
        border = "#F59E0B" if is_fx else "#3B82F6"

        st.markdown(
            f"""
            <div style="
                background:{bg};
                padding:12px;
                border-radius:10px;
                margin-bottom:8px;
                border-left:5px solid {border};
            ">
                <strong>{notif['title']}</strong><br>
                <span style="font-size:0.9rem;">
                    {notif['message']}
                </span><br>
                <small style="color:gray;">
                    {notif['created_at'][:19].replace('T',' ')}
                </small>
            </div>
            """,
            unsafe_allow_html=True
        )

def clear_notifications():

    st.warning("⚠️ This will permanently delete ALL notifications.")

    confirm = st.checkbox(
        "I understand. Clear all notifications.",
        key="clear_confirm_checkbox_unique"
    )

    if confirm:
        if st.button("🗑 Confirm Clear", use_container_width=True):

            try:
                resp = requests.delete(
                    f"{BASE_URL}/dashboard/notifications/clear/?confirm=true",
                    headers=get_headers(),
                    json={"confirm": True},
                    timeout=10
                )

                st.write("STATUS:", resp.status_code)   # debug
                st.write(resp.text)

                if resp.status_code == 200:
                    st.success("✅ Notifications cleared")
                    st.session_state.show_clear_confirm = False
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Failed to clear notifications")

            except Exception as e:
                st.error(f"Connection error: {e}")

# ============================================
# PROFESSIONAL AUTHENTICATION FUNCTIONS
# ============================================

def login_user():
    """Professional login interface"""
    st.markdown("""
<div style="text-align:center; font-size:2rem; font-weight:700; color:#3B82F6;">
🔐 Sign In
</div>
""", unsafe_allow_html=True)

    st.markdown('<p style="text-align: center; color: #6B7280;">Enter your credentials to access FINALYZE</p>', unsafe_allow_html=True)
    
    # Generate new form key if none exists
    if 'login_form_key' not in st.session_state:
        st.session_state.login_form_key = f"login_form_{time.time()}"
    
    with st.form(key=st.session_state.login_form_key):
        email = st.text_input("Email", key=f"email_{st.session_state.login_form_key}")
        password = st.text_input("Password", type="password", key=f"password_{st.session_state.login_form_key}")
        
        left, center, right = st.columns([2,3,2])
        with center:
            login_btn = st.form_submit_button("🚀 Login", use_container_width=True)
        
        if login_btn:
            payload = {"email": email, "password": password}
            with st.spinner("Authenticating..."):
                response = requests.post(f"{BASE_URL}/auth/login/", json=payload)

            if response.status_code == 200:
                data = response.json()
                save_token(data["access"])
                st.session_state.access_token = data["access"]
                st.session_state.user_email = email
                st.session_state.active_section = "dashboard"
                del st.session_state.login_form_key
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("Login successful!")
                st.markdown('</div>', unsafe_allow_html=True)
                time.sleep(1)
                st.rerun()
            else:
                del st.session_state.login_form_key
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error(f"Login failed: {response.text}")
                st.markdown('</div>', unsafe_allow_html=True)
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def register_user():
    """Professional registration interface"""
    st.markdown("""
<div style="text-align:center; font-size:2rem; font-weight:700; color:#3B82F6;">
🚀 Create Account
</div>
""", unsafe_allow_html=True)

    st.markdown('<p style="text-align: center; color: #6B7280;">Join FINALYZE to manage your finances</p>', unsafe_allow_html=True)
    
    if 'register_form_key' not in st.session_state:
        st.session_state.register_form_key = f"register_form_{time.time()}"
    
    with st.form(key=st.session_state.register_form_key):
        username = st.text_input("Username", key=f"username_{st.session_state.register_form_key}")
        email = st.text_input("Email", key=f"email_{st.session_state.register_form_key}")
        password = st.text_input("Password", type="password", key=f"password_{st.session_state.register_form_key}")
        confirm_password = st.text_input("Confirm Password", type="password", key=f"confirm_{st.session_state.register_form_key}")
        
        password_strength = 0
        password_feedback = []
        
        if password:
            if len(password) >= 8:
                password_strength += 1
            else:
                password_feedback.append("❌ At least 8 characters")
                
            if any(c.isupper() for c in password):
                password_strength += 1
            else:
                password_feedback.append("❌ At least 1 uppercase letter")
                
            if any(c.islower() for c in password):
                password_strength += 1
            else:
                password_feedback.append("❌ At least 1 lowercase letter")
                
            if any(c.isdigit() for c in password):
                password_strength += 1
            else:
                password_feedback.append("❌ At least 1 number")
                
            special_chars = "!@#$%^&*"
            if any(c in special_chars for c in password):
                password_strength += 1
            else:
                password_feedback.append("❌ At least 1 special character (!@#$%^&*)")
            
            strength_colors = ["🔴 Very Weak", "🟠 Weak", "🟡 Fair", "🟢 Good", "✅ Strong"]
            if password_strength < len(strength_colors):
                st.write(f"**Password Strength:** {strength_colors[password_strength]}")
    

        left, center, right = st.columns([2,3,2])
        with center:
            register_btn = st.form_submit_button("✨ Register", use_container_width=True)

        
        if register_btn:
            if password != confirm_password:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error("❌ Passwords do not match!")
                st.markdown('</div>', unsafe_allow_html=True)
                st.stop()
            
            if password_strength < 5:
                if password_feedback:
                    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                    with st.expander("🔒 Password Requirements Not Met", expanded=True):
                        for feedback in password_feedback:
                            st.write(feedback)
                    st.markdown('</div>', unsafe_allow_html=True)
                st.stop()
            
            if "@" not in email or "." not in email:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error("❌ Please enter a valid email address")
                st.markdown('</div>', unsafe_allow_html=True)
                st.stop()
            
            if len(username) < 3:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error("❌ Username must be at least 3 characters")
                st.markdown('</div>', unsafe_allow_html=True)
                st.stop()
            
            payload = {"username": username, "email": email, "password": password}
            
            with st.spinner("Creating your account..."):
                response = requests.post(f"{BASE_URL}/auth/register/", json=payload)

            if response.status_code == 201:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.markdown("""
                <div style="text-align: center;">
                    <h4 style="margin: 0;">✅ Successfully Registered!</h4>
                    <p style="margin: 10px 0 0 0;">You can now login with your credentials.</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.success("Account created successfully! Switch to Login tab to continue.")
                del st.session_state.register_form_key
                st.stop()
                
            else:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                try:
                    error_data = response.json()
                    st.error(f"Registration failed: {error_data}")
                except:
                    st.error(f"Registration failed: {response.text[:200]}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                del st.session_state.register_form_key
                st.stop()
    
    st.markdown('</div>', unsafe_allow_html=True)

def logout():
    """Log out user"""
    st.session_state.access_token = None
    st.session_state.user_email = ""
    st.session_state.active_section = None
    st.session_state.active_subsection = None
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.success("Logged out successfully!")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PROFESSIONAL SIDEBAR NAVIGATION
# ============================================

def sidebar_navigation():
    """Professional sidebar with gradient design"""
    with st.sidebar:
        # Logo and Title
        st.markdown('<div class="sidebar-title">💰 FINALYZE</div>', unsafe_allow_html=True)
        
        # User Info
        if st.session_state.user_email:
            st.markdown(f'<div class="sidebar-user">👤 {st.session_state.user_email}</div>', unsafe_allow_html=True)
        
        # Navigation Menu with Icons
        st.markdown("### 📍 Navigation")
        
        menu_items = [
            ("📊 Dashboard", "dashboard"),
            ("👤 Profile", "profile"),
            ("💰 Budget", "budget"),
            ("💳 Transactions", "transactions"),
            ("🤖 AI Tools", "ai"),
            ("💬 Assistant", "chatbot")
        ]
        
        for icon_text, value in menu_items:
            if st.button(icon_text, key=f"sidebar_{value}_btn", use_container_width=True):
                st.session_state.active_section = value
                st.session_state.active_subsection = None
                st.rerun()
        
        # Logout button
        if st.session_state.access_token:
            if st.button("🚪 Logout", key="sidebar_logout_btn", use_container_width=True):
                logout()
                time.sleep(1)
                st.rerun()

def check_new_fx_notifications():
    if not st.session_state.access_token:
        return

    try:
        resp = requests.get(
            f"{BASE_URL}/finance/notifications/?unread=true",
            headers=get_headers(),
            timeout=5
        )

        if resp.status_code != 200:
            return

        notifications = resp.json()
        if not notifications:
            return

        latest = notifications[0]
        latest_id = latest["id"]

        if st.session_state.last_notification_id == latest_id:
            return

        # 🔔 Toast
        st.toast(
            f"🔔 {latest['title']}\n{latest['message']}",
            icon="💱"
        )

        # ✅ Mark read
        requests.post(
            f"{BASE_URL}/finance/notifications/update/",
            headers=get_headers(),
            json={"ids": [latest_id]},
            timeout=10
        )

        st.session_state.last_notification_id = latest_id

    except Exception as e:
        print("Notification error:", e)

def notification_bell():

    if not st.session_state.access_token:
        return

    try:
        _ = st.session_state.notifications_refresh

        resp = requests.get(
            f"{BASE_URL}/finance/notifications/?unread=true",
            headers=get_headers(),
            timeout=5
        )

        if resp.status_code != 200:
            return

        unread = resp.json()
        count = len(unread)

        col1, col2 = st.columns([9, 1])

        with col2:
            if count > 0:
                st.markdown(
                    f"""
                    <div style="
                        background:red;
                        color:white;
                        border-radius:50%;
                        width:26px;
                        height:26px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-weight:bold;
                        position:relative;
                        top:-10px;
                        right:10px;
                    ">
                        🔔 {count}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown("🔔")

    except Exception as e:
        print("Bell error:", e)

def play_notification_sound():
    st.markdown(
        """
        <audio autoplay>
            <source src="https://www.epidemicsound.com/sound-effects/tracks/29d81738-d260-4981-b4ae-94b3feb57d0c/" type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True
    )


# ============================================
# PROFESSIONAL DASHBOARD VIEW
# ============================================

def dashboard_view():
    notification_bell()       
    check_new_fx_notifications()

    st.markdown('<div class="main-header">📊 Financial Dashboard</div>', unsafe_allow_html=True)
    
    st.markdown(f'<p style="font-size: 1.2rem; color: #9CA3AF; margin-bottom: 1rem;">Welcome back, <strong>{st.session_state.user_email}</strong>! Here\'s your financial overview.</p>', unsafe_allow_html=True)
   
    try:
        response = requests.get(f"{BASE_URL}/dashboard/", headers=get_headers())
        if response.status_code == 200:
            data = response.json()
            
            if "stats" in data:
                cols = st.columns(4)
                
                with cols[0]:
                    balance = data['stats'].get('balance', 0)
                    balance_delta = balance * 0.05
                    st.metric(
                        "Current Balance", 
                        f"₹{balance:,.2f}",
                        delta=f"₹{balance_delta:,.2f}",
                        delta_color="inverse"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with cols[1]:
                    income = data['stats'].get('income', 0)
                    income_delta = income * 0.08
                    st.metric(
                        "Monthly Income", 
                        f"₹{income:,.2f}",
                        delta=f"₹{income_delta:,.2f} (+8%)",
                        delta_color="normal"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with cols[2]:
                    expenses = data['stats'].get('expenses', 0)
                    expenses_delta = expenses * -0.03
                    st.metric(
                        "Monthly Expenses", 
                        f"₹{expenses:,.2f}",
                        delta=f"₹{abs(expenses_delta):,.2f} (-3%)",
                        delta_color="inverse"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with cols[3]:
                    savings_rate = data['stats'].get('savings_rate', 0)
                    savings_delta = savings_rate - 20
                    delta_color = "inverse" if savings_rate < 20 else "normal"
                    st.metric(
                        "Savings Rate", 
                        f"{savings_rate:.1f}%",
                        delta=f"{savings_delta:+.1f}% vs target",
                        delta_color=delta_color
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("### ⚡ Quick Actions")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💸 Add Transaction", key="dash_add_txn", use_container_width=True):
                    st.session_state.active_section = "transactions"
                    st.session_state.active_subsection = "log_transaction"
                    st.rerun()
                if st.button("📊 View Budget", key="dash_view_budget", use_container_width=True):
                    st.session_state.active_section = "budget"
                    st.session_state.active_subsection = "view_budget"
                    st.rerun()
            with col2:
                if st.button("📈 Analysis", key="dash_analysis", use_container_width=True):
                    st.session_state.active_section = "ai"
                    st.session_state.active_subsection = "expense_prediction"
                    st.rerun()
                if st.button("👤 My Profile", key="dash_profile", use_container_width=True):
                    st.session_state.active_section = "profile"
                    st.session_state.active_subsection = "view_profile"
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            notifications_panel()
        else:
            st.error("Failed to load dashboard.")
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Unable to connect to dashboard. Error: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# ENHANCED VIEW FUNCTIONS WITH PROFESSIONAL STYLING
# ============================================

def add_back_button():
    """Add a professional back button"""
    if st.session_state.active_subsection:
        if st.button("← Back to Overview", key=f"back_{st.session_state.active_section}_{st.session_state.active_subsection}"):
            st.session_state.active_subsection = None
            st.rerun()

# ============================================
# YOUR ORIGINAL FUNCTIONS WITH PROFESSIONAL STYLING
# ============================================

def create_user_profile():
    """Create a new user profile with unique form key"""
    section_header("Create Profile", "➕")
    
    if 'create_profile_key' not in st.session_state:
        st.session_state.create_profile_key = f"create_profile_{time.time()}"
    
    with st.form(key=st.session_state.create_profile_key):
        full_name = st.text_input("Full Name", key=f"name_{st.session_state.create_profile_key}")
        email = st.text_input("Email", key=f"email_{st.session_state.create_profile_key}")
        
        if st.form_submit_button("Submit Profile"):
            if not full_name or not email:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error("❌ Please fill in all required fields")
                st.markdown('</div>', unsafe_allow_html=True)
                return
            
            payload = {"full_name": full_name, "email": email}
            
            try:
                response = requests.post(
                    f"{BASE_URL}/dashboard/profile/create/",
                    headers=get_headers(),
                    json=payload
                )
                
                if response.status_code == 201:
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.success("✅ Profile created successfully!")
                    st.markdown('</div>', unsafe_allow_html=True)
                    del st.session_state.create_profile_key
                    st.session_state.active_subsection = None
                    st.rerun()
                else:
                    st.markdown('<div class="error-box">', unsafe_allow_html=True)
                    try:
                        error_details = response.json()
                        st.error(f"❌ Failed to create profile: {error_details.get('detail', response.text)}")
                    except ValueError:
                        st.error(f"❌ Failed to create profile (Status {response.status_code}): {response.text}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    del st.session_state.create_profile_key
                    st.rerun()
                    
            except requests.exceptions.RequestException as e:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error(f"❌ Network error: {str(e)}")
                st.markdown('</div>', unsafe_allow_html=True)
                st.rerun()
            except Exception as e:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error(f"❌ Unexpected error: {str(e)}")
                st.markdown('</div>', unsafe_allow_html=True)
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def view_user_profile():
    """View user profile with styled layout"""
    section_header("View Profile", "👤")

    response = requests.get(f"{BASE_URL}/dashboard/profile/", headers=get_headers())
    
    if response.status_code == 200:
        data = response.json()

        col1, col2 = st.columns([1, 2])
        with col1:
            profile_pic_url = data.get("profile_picture")
            if profile_pic_url:
                st.image(profile_pic_url, width=150, caption="Profile Picture")
            else:
                st.image("https://via.placeholder.com/150", width=150, caption="No Picture")

        with col2:
            st.markdown(f"""
                <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
                    <h4 style="margin-bottom: 0.5rem;">Full Name: <span style="color: #3c4043;">{data.get('full_name', 'N/A')}</span></h4>
                    <p style="margin: 0;">User ID: <strong>{data.get('user', 'N/A')}</strong></p>
                    <p style="margin: 0;">Profile ID: <strong>{data.get('id', 'N/A')}</strong></p>
                </div>
            """, unsafe_allow_html=True)

        if st.button("✏️ Edit Profile"):
            st.session_state.active_subsection = "update_profile"
            st.rerun()

    elif response.status_code == 404:
        st.warning("No profile found. Please create one first.")
    else:
        st.error("Failed to fetch profile.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def update_user_profile():
    """Update existing user profile with unique form key"""
    section_header("Update Profile", "✏️")

    response = requests.get(f"{BASE_URL}/dashboard/profile/", headers=get_headers())
    if response.status_code != 200:
        st.error("Failed to load current profile.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    data = response.json()
    
    if 'update_profile_key' not in st.session_state:
        st.session_state.update_profile_key = f"update_profile_{time.time()}"
    
    with st.form(key=st.session_state.update_profile_key):
        full_name = st.text_input("Full Name", 
                                value=data.get("full_name", ""),
                                key=f"name_{st.session_state.update_profile_key}")
        email = st.text_input("Email", 
                            value=data.get("email", ""),
                            key=f"email_{st.session_state.update_profile_key}")
        profile_picture = st.file_uploader("Upload New Profile Picture", 
                                         type=["jpg", "png"],
                                         key=f"upload_{st.session_state.update_profile_key}")

        if st.form_submit_button("Update Profile"):
            payload = {"full_name": full_name, "email": email}

            if profile_picture:
                files = {"profile_picture": (profile_picture.name, profile_picture, profile_picture.type)}
                response = requests.put(
                    f"{BASE_URL}/dashboard/profile/update/",
                    headers=get_headers(),
                    data=payload,
                    files=files
                )
            else:
                response = requests.put(
                    f"{BASE_URL}/dashboard/profile/update/",
                    headers=get_headers(),
                    json=payload
                )

            if response.status_code == 200:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("✅ Profile updated successfully!")
                st.markdown('</div>', unsafe_allow_html=True)
                del st.session_state.update_profile_key
                st.session_state.active_subsection = None
                st.rerun()
            else:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                del st.session_state.update_profile_key
                st.error(f"❌ Update failed: {response.text}")
                st.markdown('</div>', unsafe_allow_html=True)
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def delete_user_profile():
    """Delete user profile with unique form key"""
    section_header("Delete Profile", "🗑️")

    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.warning("⚠️ This action cannot be undone!")
    st.markdown('</div>', unsafe_allow_html=True)

    if 'delete_profile_key' not in st.session_state:
        st.session_state.delete_profile_key = f"delete_profile_{time.time()}"

    with st.form(key=st.session_state.delete_profile_key):
        confirm = st.checkbox(
            "I understand this will permanently delete my profile",
            key=f"confirm_{st.session_state.delete_profile_key}"
        )
        submitted = st.form_submit_button("🗑️ Delete Profile")

        if confirm and submitted:
            response = requests.delete(f"{BASE_URL}/dashboard/profile/delete/", headers=get_headers())

            if response.status_code == 204:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("🧹 Profile deleted successfully!")
                st.markdown('</div>', unsafe_allow_html=True)
                del st.session_state.delete_profile_key
                st.session_state.active_subsection = None
                st.rerun()
            else:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                del st.session_state.delete_profile_key
                st.error(f"❌ Deletion failed: {response.text}")
                st.markdown('</div>', unsafe_allow_html=True)
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

### ✅ Budget Functions with Professional Styling
def enter_budget():
    """Enter new budget"""
    section_header("Enter Budget", "📊")

    with st.form("enter_budget_form"):
        income = st.number_input("Income")
        savings_goal = st.number_input("Savings Goal")
        month = st.date_input("Budget Month", value=date.today())
        budget_limit = st.number_input("Budget Limit")
        category = st.text_input("Category")

        if st.form_submit_button("Submit Budget"):
            payload = {
                "income": income,
                "savings_goal": savings_goal,
                "month": month.strftime("%Y-%m-%d"),
                "budget_limit": budget_limit,
                "category": category,
            }
            response = requests.post(f"{BASE_URL}/finance/budget/", headers=get_headers(), json=payload)

            if response.status_code == 201:
                budget = response.json()
                st.session_state.budget_id = budget["id"]
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("✅ Budget created successfully!")
                st.markdown('</div>', unsafe_allow_html=True)
                st.session_state.active_subsection = None
            else:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error(f"🚫 Error saving budget: {response.text}")
                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def update_budget():
    """Update existing budget"""
    section_header("Update Budget", "🔄")

    budget_id = st.text_input("Enter Budget ID to update")
    
    if budget_id:
        response = requests.get(f"{BASE_URL}/finance/budget/{budget_id}/", headers=get_headers())
        if response.status_code == 200:
            current_data = response.json()
            
            try:
                current_income = float(current_data.get("income", 0))
                current_savings = float(current_data.get("savings_goal", 0))
                current_limit = float(current_data.get("budget_limit", 0))
            except (ValueError, TypeError):
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error("Invalid number format in budget data")
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                return
            
            with st.form("update_budget_form"):
                income = st.number_input(
                    "New Income", 
                    value=current_income,
                    min_value=0.0,
                    step=1000.0,
                    format="%.2f"
                )
                savings_goal = st.number_input(
                    "New Savings Goal", 
                    value=current_savings,
                    min_value=0.0,
                    step=1000.0,
                    format="%.2f"
                )
                budget_limit = st.number_input(
                    "New Budget Limit", 
                    value=current_limit,
                    min_value=0.0,
                    step=1000.0,
                    format="%.2f"
                )
                category = st.text_input(
                    "New Category", 
                    value=current_data.get("category", "")
                )
                month = st.date_input(
                    "New Budget Month", 
                    value=datetime.strptime(
                        current_data.get("month", str(date.today())), 
                        "%Y-%m-%d"
                    ).date()
                )

                if st.form_submit_button("Update Budget"):
                    payload = {
                        "income": str(income),
                        "savings_goal": str(savings_goal),
                        "month": month.strftime("%Y-%m-%d"),
                        "budget_limit": str(budget_limit),
                        "category": category,
                    }
                    response = requests.put(
                        f"{BASE_URL}/finance/budget/{budget_id}/", 
                        headers=get_headers(), 
                        json=payload
                    )
                    if response.status_code in [200, 202]:
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.success("✅ Budget updated successfully!")
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.session_state.active_subsection = None
                        st.rerun()
                    else:
                        st.markdown('<div class="error-box">', unsafe_allow_html=True)
                        st.error(f"Error updating budget: {response.text}")
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.json(response.json())
        else:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.error(f"Budget not found (Status: {response.status_code})")
            st.markdown('</div>', unsafe_allow_html=True)
            if response.status_code != 404:
                st.json(response.json())
    
    st.markdown('</div>', unsafe_allow_html=True)

def view_budget():
    """View existing budgets"""
    section_header("View Budgets", "💼")

    response = requests.get(f"{BASE_URL}/finance/budget/", headers=get_headers())

    if response.status_code == 200:
        budgets = response.json()

        if not budgets:
            st.info("You don't have any budgets yet.")
        else:
            for budget in budgets:
                with st.expander(f"Budget ID: {budget['id']} - {budget['category']}"):
                    st.markdown(f"""
                        <div style="background-color:#ffffff; color:#000000; padding:20px; 
                                    border-radius:12px; border:1px solid #dcdcdc; 
                                    box-shadow: 0 2px 6px rgba(0,0,0,0.05); font-family:Arial, sans-serif;">
                            <p><strong>💰 Income:</strong> ₹{float(budget['income']):,.2f}</p>
                            <p><strong>🎯 Savings Goal:</strong> ₹{float(budget['savings_goal']):,.2f}</p>
                            <p><strong>🧾 Budget Limit:</strong> ₹{float(budget['budget_limit']):,.2f}</p>
                            <p><strong>🏷️ Category:</strong> {budget['category'].capitalize()}</p>
                            <p><strong>🗓️ Month:</strong> {budget['month']}</p>
                            <p><strong>🕒 Created At:</strong> {datetime.strptime(budget['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%b %d, %Y %I:%M %p")}</p>
                        </div>
                    """, unsafe_allow_html=True)

    elif response.status_code == 401:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.error("❌ Unauthorized: Please check your token or login again.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.error(f"❌ Something went wrong: {response.status_code} - {response.text}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def delete_budget():
    """Delete a budget with confirmation and debug information"""
    section_header("Delete Budget", "🗑️")

    budget_id = st.text_input("Enter Budget ID to delete")
    
    if budget_id:
        try:
            headers = get_headers()
            verify_url = f"{BASE_URL}/finance/budget/{budget_id}/"
            
            with st.spinner("Checking budget..."):
                verify_response = requests.get(verify_url, headers=headers)
            
            if verify_response.status_code == 200:
                budget = verify_response.json()
                
                st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                st.warning(f"""
                **You're about to delete:**
                - Month: {budget['month']}
                - Category: {budget['category']}
                - Income: ₹{float(budget['income']):,.2f}
                """)
                st.markdown('</div>', unsafe_allow_html=True)
                
                if st.checkbox("I understand this cannot be undone", key=f"confirm_del_{budget_id}"):
                    if st.button("Permanently Delete Budget", type="primary"):
                        with st.spinner("Deleting..."):
                            del_response = requests.delete(verify_url, headers=headers)
                        
                        if del_response.status_code == 204:
                            st.markdown('<div class="success-box">', unsafe_allow_html=True)
                            st.success("✅ Budget deleted successfully!")
                            st.markdown('</div>', unsafe_allow_html=True)
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.markdown('<div class="error-box">', unsafe_allow_html=True)
                            st.error(f"""
                            ❌ Deletion failed (Status {del_response.status_code})
                            Response: {del_response.text}
                            """)
                            st.markdown('</div>', unsafe_allow_html=True)
                            st.json(del_response.json())
                
            elif verify_response.status_code == 404:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error("❌ Budget not found. Please check the ID.")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error(f"Verification failed (Status {verify_response.status_code})")
                st.markdown('</div>', unsafe_allow_html=True)
                st.json(verify_response.json())

        except requests.exceptions.RequestException as e:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.error(f"❌ Network error occurred: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("Please check your connection and try again")

        except Exception as e:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.error(f"❌ Unexpected error: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("Please check the console for details")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# TRANSACTION FUNCTIONS WITH PROFESSIONAL STYLING
# ============================================
def log_transaction():
    """Log a new transaction"""
    section_header("Log Transaction", "💳")

    with st.form("log_transaction_form"):
        amount = st.number_input("Amount", min_value=0.0)

        currency = st.selectbox(
            "Currency",
            ["INR", "USD", "EUR", "GBP", "JPY", "AUD"]
        )

        categories = [
            "Rent", "Loan_Repayment", "Insurance", "Groceries", "Transport",
            "Eating_Out", "Entertainment", "Utilities", "Healthcare",
            "Education", "Miscellaneous"
        ]
        category = st.selectbox("Category", categories)

        transaction_date = st.date_input("Transaction Date")
        transaction_time = st.time_input("Transaction Time")
        merchant_name = st.text_input("Merchant Name")

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Cash",
                "UPI",
                "Credit Card",
                "Debit Card",
                "Net Banking",
                "Other"
            ]
        )

        transaction_description = st.text_input("Transaction Description")

        if st.form_submit_button("Submit Transaction"):

            PAYMENT_METHOD_MAP = {
                "CASH": "Cash",
                "UPI": "UPI",
                "CARD": "Credit Card",
                "CREDIT CARD": "Credit Card",
                "NET BANKING": "Net Banking",
                "NET_BANKING": "Net Banking",
            }

            payload = {
                "amount": amount,
                "currency": currency,
                "category": category,
                "transaction_date": transaction_date.strftime("%Y-%m-%d"),
                "transaction_time": transaction_time.strftime("%H:%M"),
                "merchant_name": merchant_name,
                "payment_method": payment_method,
                "transaction_description": transaction_description
            }

            response = requests.post(
                f"{BASE_URL}/finance/transactions/",
                headers=get_headers(),
                json=payload
            )

            if response.status_code == 201:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("✅ Transaction added successfully!")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                try:
                    error_data = response.json()
                    st.error(f"❌ Failed to log transaction: {error_data}")
                except ValueError:
                    st.error(
                        f"❌ Failed to log transaction "
                        f"(Status {response.status_code}): {response.text}"
                    )
                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def recurring_transaction():
    """Log a recurring transaction"""
    st.subheader("🔄 Recurring Transaction")
    
    with st.form("recurring_transaction_form"):
        amount = st.number_input("Amount", min_value=0.0)
        
        categories = [
            "Rent", "Loan_Repayment", "Insurance", "Groceries", "Transport", "Eating_Out", 
            "Entertainment", "Utilities", "Healthcare", "Education", "Miscellaneous"
        ]
        category = st.selectbox("Category", categories)
        
        start_date = st.date_input("Start Date")
        frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly", "Yearly"])
        next_due_date = st.date_input("Next Due Date")
        merchant_name = st.text_input("Merchant Name")
        payment_method = st.selectbox("Payment Method", ["Cash", "UPI", "Card", "Net Banking"])

        if st.form_submit_button("Submit Recurring Transaction"):
            payload = {
                "amount": amount,
                "category": category,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "frequency": frequency,
                "next_due_date": next_due_date.strftime("%Y-%m-%d"),
                "merchant_name": merchant_name,
                "payment_method": payment_method
            }
            response = requests.post(f"{BASE_URL}/finance/recurring-transactions/", headers=get_headers(), json=payload)

            if response.status_code == 201:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("✅ Recurring transaction saved successfully!")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error(f"Failed to save recurring transaction: {response.json()}")
                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def list_transactions():
    """List regular + recurring transactions with currency toggle and totals"""
    section_header("Transaction History", "📜")

    CURRENCY_SYMBOLS = {
        "INR": "₹",
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "AUD": "A$",
    }

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_currency = st.selectbox(
            "Display Currency",
            ["INR", "USD", "EUR", "GBP", "JPY", "AUD"],
            key="txn_currency_filter"
        )

    with col2:
        show_inr = st.toggle("Show INR Column", value=True)

    tx_response = requests.get(
        f"{BASE_URL}/finance/transactions/",
        headers=get_headers()
    )
    rec_response = requests.get(
        f"{BASE_URL}/finance/recurring-transactions/",
        headers=get_headers()
    )

    if tx_response.status_code != 200 or rec_response.status_code != 200:
        st.error("❌ Failed to fetch transactions.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    transactions = tx_response.json()
    recurring_transactions = rec_response.json()

    def convert_amount(inr_amount, rate):
        if selected_currency == "INR":
            return inr_amount
        return inr_amount / rate

    symbol = CURRENCY_SYMBOLS[selected_currency]

    if transactions:
        st.markdown("### 💳 Regular Transactions")

        rows = []
        total_inr = 0.0
        total_selected = 0.0

        for txn in transactions:
            inr_amount = float(txn["amount_in_base_currency"])
            rate = float(txn["exchange_rate"])

            display_amount = convert_amount(inr_amount, rate)

            total_inr += inr_amount
            total_selected += display_amount

            row = {
                "ID": txn["id"],
                "Date": txn["transaction_date"],
                "Time": txn.get("transaction_time", ""),
                f"Amount ({selected_currency})": f"{symbol}{display_amount:,.2f}",
                "Category": txn["category"],
                "Payment Method": txn["payment_method"],
                "Merchant": txn.get("merchant_name", ""),
                "Description": txn.get("transaction_description", "")
            }

            if show_inr:
                row["Amount (INR)"] = f"₹{inr_amount:,.2f}"

            rows.append(row)

        df = pd.DataFrame(rows)

        s1, s2 = st.columns(2)
        s1.metric(f"Total ({selected_currency})", f"{symbol}{total_selected:,.2f}")
        s2.metric("Total (INR)", f"₹{total_inr:,.2f}")

        col_config = {
            "ID": st.column_config.NumberColumn("ID"),
            "Date": st.column_config.DateColumn("Date"),
            "Time": st.column_config.TimeColumn("Time"),
            f"Amount ({selected_currency})": st.column_config.TextColumn(
                f"Amount ({selected_currency})"
            ),
            "Category": "Category",
            "Payment Method": "Payment Method",
            "Merchant": "Merchant",
            "Description": "Description",
        }

        if show_inr:
            col_config["Amount (INR)"] = st.column_config.TextColumn("Amount (INR)")

        st.dataframe(
            df,
            column_config=col_config,
            hide_index=True,
            use_container_width=True
        )

    else:
        st.info("No regular transactions found.")

    if recurring_transactions:
        st.markdown("### 🔁 Recurring Transactions")

        rows = []
        total_inr = 0.0
        total_selected = 0.0

        for txn in recurring_transactions:
            inr_amount = float(txn["amount"])
            rate = float(txn.get("exchange_rate", 1))

            display_amount = convert_amount(inr_amount, rate)

            total_inr += inr_amount
            total_selected += display_amount

            row = {
                "ID": txn["id"],
                "Start Date": txn["start_date"],
                f"Amount ({selected_currency})": f"{symbol}{display_amount:,.2f}",
                "Category": txn["category"],
                "Frequency": txn["frequency"],
                "Next Due": txn["next_due_date"],
            }

            if show_inr:
                row["Amount (INR)"] = f"₹{inr_amount:,.2f}"

            rows.append(row)

        df = pd.DataFrame(rows)

        s1, s2 = st.columns(2)
        s1.metric(f"Recurring Total ({selected_currency})", f"{symbol}{total_selected:,.2f}")
        s2.metric("Recurring Total (INR)", f"₹{total_inr:,.2f}")

        col_config = {
            "ID": st.column_config.NumberColumn("ID"),
            "Start Date": st.column_config.DateColumn("Start Date"),
            f"Amount ({selected_currency})": st.column_config.TextColumn(
                f"Amount ({selected_currency})"
            ),
            "Category": "Category",
            "Frequency": "Frequency",
            "Next Due": st.column_config.DateColumn("Next Due"),
        }

        if show_inr:
            col_config["Amount (INR)"] = st.column_config.TextColumn("Amount (INR)")

        st.dataframe(
            df,
            column_config=col_config,
            hide_index=True,
            use_container_width=True
        )

    else:
        st.info("No recurring transactions found.")

    st.markdown('</div>', unsafe_allow_html=True)


def update_transaction():
    """Update an existing transaction"""
    section_header("Update Transaction", "🔄")

    transaction_id = st.text_input("Enter Transaction ID to update")
    
    if transaction_id:
        response = requests.get(
            f"{BASE_URL}/finance/transactions/{transaction_id}/", 
            headers=get_headers()
        )
        
        if response.status_code == 200:
            current_data = response.json()
            
            with st.form("update_transaction_form"):
                amount = st.number_input(
                    "Amount", 
                    value=float(current_data.get("amount", 0)),
                    min_value=0.0,
                    step=0.01,
                    format="%.2f"
                )
                
                categories = [
                    "General",
                    "Rent", "Loan_Repayment", "Insurance", "Groceries", "Transport", 
                    "Eating_Out", "Entertainment", "Utilities", "Healthcare", 
                    "Education", "Miscellaneous","Shopping"
                ]
                category = st.selectbox(
                    "Category", 
                    categories,
                    index=categories.index(current_data.get("category", "Miscellaneous"))
                )
                
                transaction_date = st.date_input(
                    "Transaction Date",
                    value=datetime.strptime(
                        current_data.get("transaction_date", str(date.today())), 
                        "%Y-%m-%d"
                    ).date()
                )
                
                transaction_time = st.time_input(
                    "Transaction Time",
                    value=datetime.strptime(
                        current_data.get("transaction_time", "12:00:00"), 
                        "%H:%M:%S"
                    ).time()
                )
                
                merchant_name = st.text_input(
                    "Merchant Name", 
                    value=current_data.get("merchant_name", "")
                )
                
                payment_methods = ["Cash", "UPI", "Card", "Net Banking"]

                current_payment_method = current_data.get("payment_method", "Cash")

                if current_payment_method == "Credit Card":
                    current_payment_method = "Card"

                if current_payment_method not in payment_methods:
                    current_payment_method = "Cash"

                payment_method = st.selectbox(
                        "Payment Method",
                        ["Cash", "UPI", "Card", "Net Banking"]
                )

                transaction_description = st.text_input(
                    "Description", 
                    value=current_data.get("transaction_description", "")
                )

                if st.form_submit_button("Update Transaction"):
                    payment_method_map = {
                        "Card": "Credit Card",
                        "Cash": "Cash",
                        "UPI": "UPI",
                        "Net Banking": "Net Banking"
                        }

                    backend_payment_method = payment_method_map.get(payment_method, payment_method)
                    payload = {
                        "amount": str(amount),
                        "category": category,
                        "transaction_date": transaction_date.strftime("%Y-%m-%d"),
                        "transaction_time": transaction_time.strftime("%H:%M"),
                        "merchant_name": merchant_name,
                        "payment_method": backend_payment_method,
                        "transaction_description": transaction_description
                    }
                    
                    response = requests.put(
                        f"{BASE_URL}/finance/transactions/{transaction_id}/", 
                        headers=get_headers(), 
                        json=payload
                    )
                    
                    if response.status_code == 200:
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.success("✅ Transaction updated successfully!")
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown('<div class="error-box">', unsafe_allow_html=True)
                        st.error(f"Error updating transaction: {response.text}")
                        st.markdown('</div>', unsafe_allow_html=True)

        elif response.status_code == 404:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.error("Transaction not found")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.error(f"Error fetching transaction: {response.status_code}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def delete_transaction():
    """Delete a transaction"""
    section_header("Delete Transaction", "🗑️")

    transaction_id = st.text_input("Enter Transaction ID to delete")
    
    if transaction_id:
        response = requests.get(
            f"{BASE_URL}/finance/transactions/{transaction_id}/", 
            headers=get_headers()
        )
        
        if response.status_code == 200:
            transaction = response.json()
            
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.warning(f"""
            **You're about to delete:**
            - Amount: ₹{float(transaction['amount']):,.2f}
            - Category: {transaction['category']}
            - Date: {transaction['transaction_date']} at {transaction['transaction_time']}
            - Merchant: {transaction.get('merchant_name', 'N/A')}
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.checkbox("I confirm I want to delete this transaction"):
                if st.button("Permanently Delete", type="primary"):
                    response = requests.delete(
                        f"{BASE_URL}/finance/transactions/{transaction_id}/", 
                        headers=get_headers()
                    )
                    
                    if response.status_code == 204:
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.success("✅ Transaction deleted successfully!")
                        st.markdown('</div>', unsafe_allow_html=True)
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.markdown('<div class="error-box">', unsafe_allow_html=True)
                        st.error(f"Error deleting transaction: {response.text}")
                        st.markdown('</div>', unsafe_allow_html=True)
        
        elif response.status_code == 404:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.error("Transaction not found")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.error(f"Error fetching transaction: {response.status_code}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def download_reports():
    """Download transaction reports"""
    st.subheader("📥 Download Reports")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Download CSV Report"):
            csv_response = requests.get(f"{BASE_URL}/export/csv/", headers=get_headers())
            if csv_response.status_code == 200:
                st.download_button(
                    label="Click to download",
                    data=csv_response.content,
                    file_name="transactions.csv",
                    mime="text/csv"
                )
            else:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error("Failed to download CSV report.")
                st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("Download PDF Report"):
            pdf_response = requests.get(f"{BASE_URL}/export/pdf/", headers=get_headers())
            if pdf_response.status_code == 200:
                st.download_button(
                    label="Click to download",
                    data=pdf_response.content,
                    file_name="transactions.pdf",
                    mime="application/pdf"
                )
            else:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error("Failed to download PDF report.")
                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# AI PREDICTION FUNCTIONS WITH PROFESSIONAL STYLING
# ============================================

def send_request(endpoint, payload):
    """Helper function to send API requests"""
    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token', '')}",
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}/predict/{endpoint}/"

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.error(f"API Error: {response.status_code}")
            st.write("Response Text:", response.text)
            st.markdown('</div>', unsafe_allow_html=True)
            return None
    except Exception as e:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.error(f"Request failed: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
        return None

def expense_prediction():
    """Expense prediction form"""
    section_header("Expense Prediction", "📊")

    with st.form("expense_prediction_form"):
        st.markdown("### Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            income = st.number_input("Monthly Income (₹)", min_value=0, value=50000)
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            dependents = st.number_input("Number of Dependents", min_value=0, value=0)
        with col2:
            occupation = st.selectbox("Occupation", ["Salaried", "Business", "Professional", "Retired", "Student", "Other"])
            city_tier = st.selectbox("City Tier", [1, 2, 3], index=1)
            savings = st.number_input("Desired Savings (%)", min_value=0, max_value=100, value=20)
        
        st.markdown("### Essential Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            rent = st.number_input("Rent/Mortgage", min_value=0, value=15000)
            groceries = st.number_input("Groceries", min_value=0, value=8000)
            transport = st.number_input("Transport", min_value=0, value=3000)
        with col2:
            loan_repayment = st.number_input("Loan Repayment", min_value=0, value=5000)
            insurance = st.number_input("Insurance", min_value=0, value=2000)
            utilities = st.number_input("Utilities", min_value=0, value=2000)
        
        st.markdown("### Lifestyle Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            eating_out = st.number_input("Dining Out", min_value=0, value=4000)
            entertainment = st.number_input("Entertainment", min_value=0, value=3000)
        with col2:
            healthcare = st.number_input("Healthcare", min_value=0, value=2000)
            education = st.number_input("Education", min_value=0, value=3000)
        
        st.markdown("### Other Expenses (₹)")
        miscellaneous = st.number_input("Miscellaneous", min_value=0, value=2000)
        
        if st.form_submit_button("Predict Expense Breakdown"):
            payload = {
                "Income": income, "Age": age, "Dependents": dependents, "Occupation": occupation,
                "City_Tier": city_tier, "Rent": rent, "Loan_Repayment": loan_repayment,
                "Insurance": insurance, "Groceries": groceries, "Transport": transport,
                "Eating_Out": eating_out, "Entertainment": entertainment, "Utilities": utilities,
                "Healthcare": healthcare, "Education": education, "Miscellaneous": miscellaneous,
                "Desired_Savings_Percentage": savings
            }

            response = send_request("expense", payload)

            if response:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("✅ Prediction successful!")
                st.markdown('</div>', unsafe_allow_html=True)
                prediction = response.get("Expense_Prediction", {})
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Disposable Income", f"₹{prediction.get('Disposable_Income', 0):,.2f}")
                    st.metric("Total Expenses", f"₹{prediction.get('Total_Expenses', 0):,.2f}")
                with col2:
                    st.write("### Category Breakdown")
                    for category, amount in prediction.get("Category_Expenses", {}).items():
                        st.markdown(f"- **{category}:** ₹{amount:,.2f}")

                category_expenses = prediction.get("Category_Expenses", {})
                if category_expenses:
                    labels = list(category_expenses.keys())
                    sizes = list(category_expenses.values())

                    fig, ax = plt.subplots(figsize=(3, 3))
                    fig.patch.set_facecolor('black')
                    ax.set_facecolor('black')
                    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=150,textprops={'fontsize': 6,'color': 'white'})
                    ax.set_title("Expense Breakdown by Category",color='white')
                    st.pyplot(fig)

            else:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error("❌ Failed to get prediction.")
                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def overspending_alert():
    """Overspending alert form"""
    st.subheader("🚨 Overspending Alert")
    
    with st.form("overspending_alert_form"):
        st.markdown("### Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            income = st.number_input("Monthly Income (₹)", min_value=0, value=50000)
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            dependents = st.number_input("Number of Dependents", min_value=0, value=0)
        with col2:
            occupation = st.selectbox("Occupation", ["Salaried", "Business", "Professional", "Retired", "Student", "Other"])
            city_tier = st.selectbox("City Tier", [1, 2, 3], index=1)
            savings = st.number_input("Desired Savings (%)", min_value=0, max_value=100, value=20)
        
        st.markdown("### Essential Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            rent = st.number_input("Rent/Mortgage", min_value=0, value=15000)
            groceries = st.number_input("Groceries", min_value=0, value=8000)
            transport = st.number_input("Transport", min_value=0, value=3000)
        with col2:
            loan_repayment = st.number_input("Loan Repayment", min_value=0, value=5000)
            insurance = st.number_input("Insurance", min_value=0, value=2000)
            utilities = st.number_input("Utilities", min_value=0, value=2000)
        
        st.markdown("### Lifestyle Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            eating_out = st.number_input("Dining Out", min_value=0, value=4000)
            entertainment = st.number_input("Entertainment", min_value=0, value=3000)
        with col2:
            healthcare = st.number_input("Healthcare", min_value=0, value=2000)
            education = st.number_input("Education", min_value=0, value=3000)
        
        st.markdown("### Other Expenses (₹)")
        miscellaneous = st.number_input("Miscellaneous", min_value=0, value=2000)
        
        if st.form_submit_button("Check Overspending Risk"):
            payload = {
                "Income": income, "Age": age, "Dependents": dependents, "Occupation": occupation,
                "City_Tier": city_tier, "Rent": rent, "Loan_Repayment": loan_repayment,
                "Insurance": insurance, "Groceries": groceries, "Transport": transport,
                "Eating_Out": eating_out, "Entertainment": entertainment, "Utilities": utilities,
                "Healthcare": healthcare, "Education": education, "Miscellaneous": miscellaneous,
                "Desired_Savings_Percentage": savings
            }

            response = send_request("overspending", payload)

            if response:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("✅ Analysis completed!")
                st.markdown('</div>', unsafe_allow_html=True)
                alert = response.get("Overspending_Alert", None)
                
                if alert is True:
                    st.markdown('<div class="error-box">', unsafe_allow_html=True)
                    st.error("⚠️ Overspending Detected!")
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown("""
                    ### Recommendations:
                    - Review your discretionary spending (eating out, entertainment)
                    - Consider reducing expenses in high-spend categories
                    - Set up spending alerts for better monitoring
                    """)
                else:
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.success("🎉 Your spending is within healthy limits!")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                categories = ['Rent', 'Groceries', 'Transport', 'Loan Repayment', 'Insurance', 
                              'Utilities', 'Eating Out', 'Entertainment', 'Healthcare', 'Education', 'Miscellaneous']
                values = [rent, groceries, transport, loan_repayment, insurance, utilities, eating_out, 
                          entertainment, healthcare, education, miscellaneous]
                
                if income > 0:
                    percent_spent = [v / income * 100 for v in values]
                else:
                    percent_spent = [0] * len(values)

                df = pd.DataFrame({
                    'Category': categories,
                    'Percent Spent': percent_spent
                }).sort_values('Percent Spent')

                fig, ax = plt.subplots(figsize=(6, 3))
                fig.patch.set_facecolor('black')
                ax.set_facecolor('black')
                bars = ax.barh(df['Category'], df['Percent Spent'], color='cyan')
                ax.set_xlabel('Percentage of Income (%)', color='white')
                ax.set_title('Spending by Category as % of Income', color='white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                for spine in ax.spines.values():
                    spine.set_edgecolor('white')
                for bar in bars:
                    width = bar.get_width()
                    ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, f"{width:.1f}%", va='center', color='white')

                st.pyplot(fig)

            else:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error("❌ Failed to analyze spending.")
                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def anomaly_detection():
    """Anomaly detection with strict financial health checks"""
    st.subheader("🔍 Anomaly Detection")
    
    with st.form("anomaly_detection_form"):
        st.markdown("### Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            income = st.number_input("Monthly Income (₹)", min_value=0, value=50000)
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            dependents = st.number_input("Number of Dependents", min_value=0, value=0)
        with col2:
            occupation = st.selectbox("Occupation", ["Salaried", "Business", "Professional", "Retired", "Student", "Other"])
            city_tier = st.selectbox("City Tier", [1, 2, 3], index=1)
            savings = st.number_input("Desired Savings (%)", min_value=0, max_value=100, value=20)
        
        st.markdown("### Essential Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            rent = st.number_input("Rent/Mortgage", min_value=0, value=15000)
            groceries = st.number_input("Groceries", min_value=0, value=8000)
            transport = st.number_input("Transport", min_value=0, value=3000)
        with col2:
            loan_repayment = st.number_input("Loan Repayment", min_value=0, value=5000)
            insurance = st.number_input("Insurance", min_value=0, value=2000)
            utilities = st.number_input("Utilities", min_value=0, value=2000)
        
        st.markdown("### Lifestyle Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            eating_out = st.number_input("Dining Out", min_value=0, value=4000)
            entertainment = st.number_input("Entertainment", min_value=0, value=3000)
        with col2:
            healthcare = st.number_input("Healthcare", min_value=0, value=2000)
            education = st.number_input("Education", min_value=0, value=3000)
        
        st.markdown("### Other Expenses (₹)")
        miscellaneous = st.number_input("Miscellaneous", min_value=0, value=2000)
        
        if st.form_submit_button("Check for Anomalies"):
            total_expenses = (
                rent + groceries + transport + loan_repayment + 
                insurance + utilities + eating_out + 
                entertainment + healthcare + education + miscellaneous
            )
            actual_savings = income - total_expenses
            savings_percentage = (actual_savings / income) * 100 if income > 0 else 0

            anomalies = []
            
            if actual_savings < 0:
                anomalies.append(("Deficit Spending", f"Expenses exceed income by ₹{abs(actual_savings):,}"))
            
            essential_expenses = rent + groceries + transport + loan_repayment + insurance + utilities
            if essential_expenses > income * 0.6:
                anomalies.append(("High Essentials", f"₹{essential_expenses:,} ({essential_expenses/income*100:.1f}% of income)"))
            
            lifestyle_expenses = eating_out + entertainment + healthcare + education
            if lifestyle_expenses > income * 0.3:
                anomalies.append(("High Lifestyle", f"₹{lifestyle_expenses:,} ({lifestyle_expenses/income*100:.1f}% of income)"))
            
            category_checks = {
                "Rent": rent,
                "Groceries": groceries,
                "Dining Out": eating_out,
                "Entertainment": entertainment,
                "Loan Repayment": loan_repayment
            }
            
            for name, amount in category_checks.items():
                if amount > income * 0.25:
                    anomalies.append((f"Extreme {name}", f"₹{amount:,} ({amount/income*100:.1f}% of income)"))

            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.success("✅ Analysis completed!")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if anomalies:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error(f"⚠️ {len(anomalies)} Financial Anomalies Detected!")
                st.markdown('</div>', unsafe_allow_html=True)
                
                with st.expander("🔍 Anomaly Details", expanded=True):
                    for anomaly in anomalies:
                        st.warning(f"• {anomaly[0]}: {anomaly[1]}")

                st.markdown("### 🚨 Financial Health Alert")
                cols = st.columns(3)
                cols[0].metric("Total Expenses", f"₹{total_expenses:,}", f"{total_expenses/income*100:.1f}% of income")
                cols[1].metric("Actual Savings", f"₹{actual_savings:,}", delta_color="inverse")
                cols[2].metric("Savings vs Goal", f"{savings_percentage:.1f}%", f"{savings_percentage-savings:.1f}%")

                anomaly_types = [a[0] for a in anomalies]
                anomaly_counts = pd.Series(anomaly_types).value_counts().sort_values()

                fig, ax = plt.subplots(figsize=(6, 3))
                fig.patch.set_facecolor('black')
                ax.set_facecolor('black')

                bars = ax.barh(anomaly_counts.index, anomaly_counts.values, color='red', height=0.6)
                ax.set_xlabel('Count', color='white')
                ax.set_title('Detected Financial Anomalies', color='white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                for spine in ax.spines.values():
                    spine.set_edgecolor('white')

                for bar in bars:
                    w = bar.get_width()
                    ax.text(w + 0.1, bar.get_y() + bar.get_height() / 2, str(w), va='center', color='white', fontsize=8)

                st.pyplot(fig)

                st.markdown("### 🛠 Recommended Actions")
                st.write("""
                - Immediately review flagged categories
                - Create emergency budget for deficit
                - Follow the 50/30/20 budget rule:
                  - 50% needs (rent, groceries, utilities)
                  - 30% wants (dining, entertainment)
                  - 20% savings/debt repayment
                - Consider reducing largest expense categories first
                """)
            else:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("✅ No significant anomalies detected")
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("### 💰 Spending Summary")
                cols = st.columns(3)
                cols[0].metric("Total Expenses", f"₹{total_expenses:,}", f"{total_expenses/income*100:.1f}% of income")
                cols[1].metric("Actual Savings", f"₹{actual_savings:,}")
                cols[2].metric("Savings Goal", 
                              f"Met ({savings_percentage:.1f}%)" if savings_percentage >= savings else f"Short by {savings-savings_percentage:.1f}%",
                              delta=f"{savings_percentage-savings:.1f}%")
    
    st.markdown('</div>', unsafe_allow_html=True)

def financial_score_chart_matplotlib(score):
    """Financial score chart using matplotlib (for compatibility)"""
    categories = ['Financial Health Score']
    values = [score]

    fig, ax = plt.subplots(figsize=(6, 6))
    bars = ax.bar(categories, values, color='blue')

    ax.set_ylim(0, 100)
    ax.set_ylabel('Score')
    ax.set_title('Financial Health Score')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height - 10, f'{height:.1f}', ha='center', color='white', fontsize=14, fontweight='bold')

    st.pyplot(fig)

def financial_score():
    """Financial score form"""
    st.subheader("📊 Financial Score")
    
    with st.form("financial_score_form"):
        st.markdown("### Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            income = st.number_input("Monthly Income (₹)", min_value=0, value=50000)
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            dependents = st.number_input("Number of Dependents", min_value=0, value=0)
        with col2:
            occupation = st.selectbox("Occupation", ["Salaried", "Business", "Professional", "Retired", "Student", "Other"])
            city_tier = st.selectbox("City Tier", [1, 2, 3], index=1)
            savings = st.number_input("Desired Savings (%)", min_value=0, max_value=100, value=20)
        
        st.markdown("### Essential Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            rent = st.number_input("Rent/Mortgage", min_value=0, value=15000)
            groceries = st.number_input("Groceries", min_value=0, value=8000)
            transport = st.number_input("Transport", min_value=0, value=3000)
        with col2:
            loan_repayment = st.number_input("Loan Repayment", min_value=0, value=5000)
            insurance = st.number_input("Insurance", min_value=0, value=2000)
            utilities = st.number_input("Utilities", min_value=0, value=2000)
        
        st.markdown("### Lifestyle Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            eating_out = st.number_input("Dining Out", min_value=0, value=4000)
            entertainment = st.number_input("Entertainment", min_value=0, value=3000)
        with col2:
            healthcare = st.number_input("Healthcare", min_value=0, value=2000)
            education = st.number_input("Education", min_value=0, value=3000)
        
        st.markdown("### Other Expenses (₹)")
        miscellaneous = st.number_input("Miscellaneous", min_value=0, value=2000)
        
        if st.form_submit_button("Calculate Financial Score"):
            payload = {
                "Income": income, "Age": age, "Dependents": dependents, "Occupation": occupation,
                "City_Tier": city_tier, "Rent": rent, "Loan_Repayment": loan_repayment,
                "Insurance": insurance, "Groceries": groceries, "Transport": transport,
                "Eating_Out": eating_out, "Entertainment": entertainment, "Utilities": utilities,
                "Healthcare": healthcare, "Education": education, "Miscellaneous": miscellaneous,
                "Desired_Savings_Percentage": savings
            }

            response = send_request("score", payload)

            if response:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("✅ Score calculated successfully!")
                st.markdown('</div>', unsafe_allow_html=True)
                score = response.get("Financial_Health_Score", 0)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Your Financial Health Score", f"{score:.1f}/100")
                    if score >= 75:
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.success("Excellent financial health!")
                        st.markdown('</div>', unsafe_allow_html=True)
                    elif score >= 50:
                        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                        st.warning("Moderate financial health - room for improvement")
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-box">', unsafe_allow_html=True)
                        st.error("Poor financial health - needs attention")
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.write("### Improvement Tips")
                    st.markdown("""
                    - Increase your savings rate
                    - Reduce high-interest debt
                    - Review discretionary spending
                    - Consider additional income streams
                    """)
                    financial_score_chart_matplotlib(score)
            else:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error("❌ Failed to calculate score.")
                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def personalized_recommendations():
    """Personalized recommendations form"""
    st.subheader("💡 Personalized Recommendations")

    with st.form("personalized_recommendation_form"):
        st.markdown("### Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            income = st.number_input("Monthly Income (₹)", min_value=0, value=50000)
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            dependents = st.number_input("Number of Dependents", min_value=0, value=0)
        with col2:
            occupation = st.selectbox("Occupation", ["Salaried", "Business", "Professional", "Retired", "Student", "Other"])
            city_tier = st.selectbox("City Tier", [1, 2, 3], index=1)
            savings = st.number_input("Desired Savings (%)", min_value=0, max_value=100, value=20)

        st.markdown("### Essential Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            rent = st.number_input("Rent/Mortgage", min_value=0, value=15000)
            groceries = st.number_input("Groceries", min_value=0, value=8000)
            transport = st.number_input("Transport", min_value=0, value=3000)
        with col2:
            loan_repayment = st.number_input("Loan Repayment", min_value=0, value=5000)
            insurance = st.number_input("Insurance", min_value=0, value=2000)
            utilities = st.number_input("Utilities", min_value=0, value=2000)

        st.markdown("### Lifestyle Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            eating_out = st.number_input("Dining Out", min_value=0, value=4000)
            entertainment = st.number_input("Entertainment", min_value=0, value=3000)
        with col2:
            healthcare = st.number_input("Healthcare", min_value=0, value=2000)
            education = st.number_input("Education", min_value=0, value=3000)

        st.markdown("### Other Expenses (₹)")
        miscellaneous = st.number_input("Miscellaneous", min_value=0, value=2000)

        if st.form_submit_button("Get Recommendations"):
            payload = {
                "Income": income, "Age": age, "Dependents": dependents, "Occupation": occupation,
                "City_Tier": city_tier, "Rent": rent, "Loan_Repayment": loan_repayment,
                "Insurance": insurance, "Groceries": groceries, "Transport": transport,
                "Eating_Out": eating_out, "Entertainment": entertainment, "Utilities": utilities,
                "Healthcare": healthcare, "Education": education, "Miscellaneous": miscellaneous,
                "Desired_Savings_Percentage": savings
            }

            response = send_request("recommendation", payload)

            if response:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("✅ Recommendations generated successfully!")
                st.markdown('</div>', unsafe_allow_html=True)
                recommendations = response.get("Personalized_Recommendations", {})

                if recommendations:
                    st.write("### 💰 Your Personalized Budget Recommendations")
                    cols = st.columns(2)
                    with cols[0]:
                        st.metric("Recommended Rent", f"₹{recommendations.get('Rent', 0):,.2f}")
                        st.metric("Recommended Groceries", f"₹{recommendations.get('Groceries', 0):,.2f}")
                    with cols[1]:
                        st.metric("Recommended Savings", f"₹{recommendations.get('Savings', 0):,.2f}")
                        st.metric("Discretionary Spending", f"₹{recommendations.get('Discretionary', 0):,.2f}")

                    categories = ['Rent', 'Groceries', 'Savings', 'Discretionary']
                    values = [recommendations.get('Rent', 0), recommendations.get('Groceries', 0),
                              recommendations.get('Savings', 0), recommendations.get('Discretionary', 0)]

                    fig, ax = plt.subplots(figsize=(7, 4))
                    y_pos = range(len(categories))
                    ax.barh(y_pos, values, color='teal')
                    ax.set_yticks(y_pos)
                    ax.set_yticklabels(categories, fontsize=12)
                    ax.invert_yaxis()
                    ax.set_xlabel('Amount (₹)', fontsize=12)
                    ax.set_title('Personalized Budget Recommendations', fontsize=14)

                    max_val = max(values) if values else 0
                    for i, v in enumerate(values):
                        ax.text(v + max_val*0.01, i, f"₹{v:,.2f}", va='center', fontsize=10)

                    st.pyplot(fig)
                else:
                    st.info("No specific recommendations available based on your input.")
            else:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error("❌ Failed to get recommendations.")
                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def savings_efficiency():
    """Savings efficiency analysis form"""
    st.subheader("💰 Savings Efficiency")
    
    with st.form("savings_efficiency_form"):
        st.markdown("### Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            income = st.number_input("Monthly Income (₹)", min_value=0, value=50000)
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            dependents = st.number_input("Number of Dependents", min_value=0, value=0)
        with col2:
            occupation = st.selectbox("Occupation", ["Salaried", "Business", "Professional", "Retired", "Student", "Other"])
            city_tier = st.selectbox("City Tier", [1, 2, 3], index=1)
            savings = st.number_input("Desired Savings (%)", min_value=0, max_value=100, value=20)
        
        st.markdown("### Essential Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            rent = st.number_input("Rent/Mortgage", min_value=0, value=15000)
            groceries = st.number_input("Groceries", min_value=0, value=8000)
            transport = st.number_input("Transport", min_value=0, value=3000)
        with col2:
            loan_repayment = st.number_input("Loan Repayment", min_value=0, value=5000)
            insurance = st.number_input("Insurance", min_value=0, value=2000)
            utilities = st.number_input("Utilities", min_value=0, value=2000)
        
        st.markdown("### Lifestyle Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            eating_out = st.number_input("Dining Out", min_value=0, value=4000)
            entertainment = st.number_input("Entertainment", min_value=0, value=3000)
        with col2:
            healthcare = st.number_input("Healthcare", min_value=0, value=2000)
            education = st.number_input("Education", min_value=0, value=3000)
        
        st.markdown("### Other Expenses (₹)")
        miscellaneous = st.number_input("Miscellaneous", min_value=0, value=2000)
        
        if st.form_submit_button("Analyze Savings Efficiency"):
            total_expenses = (
                rent + groceries + transport + loan_repayment +
                insurance + utilities + eating_out + entertainment +
                healthcare + education + miscellaneous
            )
            actual_savings = income - total_expenses
            actual_savings_percent = (actual_savings / income * 100) if income > 0 else 0
            
            meeting_target = actual_savings_percent >= savings
            
            if meeting_target:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("🎉 You're meeting your savings targets!")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                st.warning("⚠️ You're not meeting your savings targets")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("### Tips to Improve Savings")
            st.markdown("""
                - Review discretionary spending (eating out, entertainment)  
                - Consider refinancing loans for better rates  
                - Automate your savings transfers  
                - Look for cheaper insurance options  
            """)
            
            labels = ['Desired Savings', 'Actual Savings']
            values = [savings, max(0, actual_savings_percent)]
            colors = ['lightgreen', 'steelblue']
            
            fig, ax = plt.subplots(figsize=(6, 3))
            y_pos = range(len(labels))
            ax.barh(y_pos, values, color=colors, alpha=0.7)
            ax.set_yticks(y_pos)
            ax.set_yticklabels(labels, fontsize=12)
            ax.set_xlim(0, max(max(values)*1.1, 100))
            ax.set_xlabel('Savings Percentage (%)', fontsize=12)
            ax.set_title('Savings Efficiency Comparison', fontsize=14)
            
            for i, v in enumerate(values):
                ax.text(v + 1, i, f"{v:.1f}%", va='center', fontsize=11)
            
            st.pyplot(fig)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# VIEW FUNCTIONS WITH PROFESSIONAL STYLING
# ============================================

def profile_view():
    """Professional profile management view"""
    st.markdown('<div class="main-header">👤 Profile Management</div>', unsafe_allow_html=True)
    add_back_button()
    
    if st.session_state.active_subsection == "create_profile":
        create_user_profile()
    elif st.session_state.active_subsection == "update_profile":
        update_user_profile()
    elif st.session_state.active_subsection == "delete_profile":
        delete_user_profile()
    else:
        view_user_profile()
        
        st.markdown("### 🛠 Profile Actions")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("➕ Create Profile", key="profile_create_btn", use_container_width=True):
                st.session_state.active_subsection = "create_profile"
                st.rerun()
        with col2:
            if st.button("✏️ Update Profile", key="profile_update_btn", use_container_width=True):
                st.session_state.active_subsection = "update_profile"
                st.rerun()
        with col3:
            if st.button("🗑️ Delete Profile", key="profile_delete_btn", use_container_width=True):
                st.session_state.active_subsection = "delete_profile"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def budget_view():
    """Professional budget management view"""
    st.markdown('<div class="main-header">💰 Budget Management</div>', unsafe_allow_html=True)
    add_back_button()
    
    if st.session_state.active_subsection == "enter_budget":
        enter_budget()
    elif st.session_state.active_subsection == "update_budget":
        update_budget()
    elif st.session_state.active_subsection == "view_budget":
        view_budget()
    elif st.session_state.active_subsection == "delete_budget":
        delete_budget()
    else:
        st.markdown("### 📋 Budget Operations")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("➕ Enter Budget", key="budget_enter_btn", use_container_width=True):
                st.session_state.active_subsection = "enter_budget"
                st.rerun()
        with col2:
            if st.button("🔄 Update Budget", key="budget_update_btn", use_container_width=True):
                st.session_state.active_subsection = "update_budget"
                st.rerun()
        with col3:
            if st.button("👁️ View Budgets", key="budget_view_btn", use_container_width=True):
                st.session_state.active_subsection = "view_budget"
                st.rerun()
        with col4:
            if st.button("🗑️ Delete Budget", key="budget_delete_btn", use_container_width=True):
                st.session_state.active_subsection = "delete_budget"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def transactions_view():
    """Professional transactions management view"""
    st.markdown('<div class="main-header">💳 Transactions Management</div>', unsafe_allow_html=True)
    add_back_button()
    
    if st.session_state.active_subsection == "log_transaction":
        log_transaction()
    elif st.session_state.active_subsection == "recurring_transaction":
        recurring_transaction()
    elif st.session_state.active_subsection == "list_transactions":
        list_transactions()
    elif st.session_state.active_subsection == "update_transaction":
        update_transaction()
    elif st.session_state.active_subsection == "delete_transaction":
        delete_transaction()        
    elif st.session_state.active_subsection == "download_reports":
        download_reports()
    else:
        st.markdown("### 💼 Transaction Operations")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("➕ Log Transaction", key="txn_log_btn", use_container_width=True):
                st.session_state.active_subsection = "log_transaction"
                st.rerun()
            st.markdown('<div style="height: 10px"></div>', unsafe_allow_html=True)
            if st.button("📜 List Transactions", key="txn_list_btn", use_container_width=True):
                st.session_state.active_subsection = "list_transactions"
                st.rerun()
        
        with col2:
            if st.button("🔄 Recurring Transaction", key="txn_recurring_btn", use_container_width=True):
                st.session_state.active_subsection = "recurring_transaction"
                st.rerun()
            st.markdown('<div style="height: 10px"></div>', unsafe_allow_html=True)
            if st.button("✏️ Update Transaction", key="txn_update_btn", use_container_width=True):
                st.session_state.active_subsection = "update_transaction"
                st.rerun()
        
        with col3:
            if st.button("🗑️ Delete Transaction", key="txn_delete_btn", use_container_width=True):
                st.session_state.active_subsection = "delete_transaction"
                st.rerun()
            st.markdown('<div style="height: 10px"></div>', unsafe_allow_html=True)
            if st.button("📥 Download Reports", key="txn_download_btn", use_container_width=True):
                st.session_state.active_subsection = "download_reports"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def ai_view():
    """Professional AI tools view"""
    st.markdown('<div class="main-header">🤖 AI Financial Tools</div>', unsafe_allow_html=True)
    add_back_button()
    
    if st.session_state.active_subsection == "expense_prediction":
        expense_prediction()
    elif st.session_state.active_subsection == "overspending_alert":
        overspending_alert()
    elif st.session_state.active_subsection == "anomaly_detection":
        anomaly_detection()
    elif st.session_state.active_subsection == "financial_score":
        financial_score()
    elif st.session_state.active_subsection == "personalized_recommendations":
        personalized_recommendations()
    elif st.session_state.active_subsection == "savings_efficiency":
        savings_efficiency()
    else:
        st.markdown("""
        ### 🔮 AI-Powered Financial Insights
        
        Select an AI tool to get personalized financial analysis and recommendations.
        Our machine learning models analyze your financial patterns to provide actionable insights.
        """)
        
        st.markdown("### 🛠 Available Tools")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Expense Prediction", key="ai_expense_btn", use_container_width=True):
                st.session_state.active_subsection = "expense_prediction"
                st.rerun()
            st.caption("Predict your future expenses based on spending patterns")
            
            if st.button("🔍 Anomaly Detection", key="ai_anomaly_btn", use_container_width=True):
                st.session_state.active_subsection = "anomaly_detection"
                st.rerun()
            st.caption("Detect unusual spending patterns and potential issues")
            
            if st.button("💰 Savings Efficiency", key="ai_savings_btn", use_container_width=True):
                st.session_state.active_subsection = "savings_efficiency"
                st.rerun()
            st.caption("Check if you're meeting savings goals efficiently")
        
        with col2:
            if st.button("🚨 Overspending Alert", key="ai_overspending_btn", use_container_width=True):
                st.session_state.active_subsection = "overspending_alert"
                st.rerun()
            st.caption("Get alerts when you're exceeding budget limits")
            
            if st.button("📈 Financial Score", key="ai_score_btn", use_container_width=True):
                st.session_state.active_subsection = "financial_score"
                st.rerun()
            st.caption("Calculate your overall financial health score")
            
            if st.button("💡 Personalized Recs", key="ai_recommendations_btn", use_container_width=True):
                st.session_state.active_subsection = "personalized_recommendations"
                st.rerun()
            st.caption("Get customized budget and saving recommendations")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# INTELLIGENT FINANCIAL CHATBOT
# ============================================

def financial_chatbot():
    """Intelligent Financial Chatbot - Ready to Use"""
    
    st.markdown("### 💬 AI Financial Assistant")
    st.markdown("Ask me anything about personal finance, budgeting, investing, or debt management!")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Hello! I'm your FINALYZE AI Financial Assistant. I can help you with budgeting, saving, investing, debt management, and financial planning. What would you like to know?"}
        ]
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Type your financial question here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                time.sleep(0.5)
                response = get_ai_response(prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    with st.sidebar:
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🧹 Clear Chat", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": "👋 Chat cleared! How can I help you with your finances today?"}
            ]
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 💡 Ask About:")
        
        topics = [
            ("📊 Budgeting", "How to create and stick to a budget?"),
            ("💰 Saving", "Best ways to save money?"),
            ("📈 Investing", "How to start investing?"),
            ("💳 Debt", "How to pay off debt faster?"),
            ("🏠 Home Buying", "Tips for buying a house?"),
            ("🏖️ Retirement", "How to plan for retirement?"),
            ("📱 App Features", "How to use FINALYZE features?")
        ]
        
        for icon, topic in topics:
            if st.button(f"{icon} {topic.split('?')[0]}", key=f"topic_{topic}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": topic})
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


def get_ai_response(user_input):
    """Get intelligent response based on user input"""
    user_input_lower = user_input.lower()
    
    knowledge_base = {
        "budget": {
            "keywords": ["budget", "spend", "expense", "money manage", "save money", "spending"],
            "response": """**📊 Creating a Budget in FINALYZE:**

**Step-by-Step Guide:**
1. **Income Tracking:** Go to Budget → Enter Budget → Set your monthly income
2. **Expense Categories:** Use predefined categories (Rent, Groceries, Transport, etc.)
3. **Set Limits:** Allocate amounts to each category based on 50/30/20 rule
4. **Track Daily:** Use Transactions → Log Transaction for every expense
5. **Weekly Review:** Check Dashboard to see actual vs budgeted spending

**💡 Pro Tips:**
• Start with tracking expenses for 30 days without changing habits
• Use **AI Tools → Expense Prediction** to forecast next month
• Set up **AI Tools → Overspending Alert** for notifications
• Download monthly reports for analysis

**🎯 Budget Rule:** 50% Needs | 30% Wants | 20% Savings/Debt

*What's your biggest budgeting challenge right now?*"""
        },
        
        "saving": {
            "keywords": ["save", "saving", "emergency fund", "rainy day", "how to save"],
            "response": """**💰 Smart Saving Strategies:**

**Priority Order for Saving:**
1. **Emergency Fund:** 3-6 months of essential expenses
2. **High-Interest Debt:** Pay off anything above 7% interest
3. **Retirement:** Max out employer match first
4. **Specific Goals:** House, car, vacation, education

**In FINALYZE:**
• Set **Savings Goal** in Budget section
• Track progress in **Dashboard**
• Use **AI Tools → Savings Efficiency** to analyze rate
• Get **Personalized Recommendations** from AI Tools

**💡 Saving Hacks:**
• Automate transfers (pay yourself first)
• Use high-yield savings accounts (>4% APY)
• Reduce recurring subscriptions
• Implement 24-hour rule for non-essential purchases

*What are you saving for? I can give more specific advice!*"""
        },
        
        "investing": {
            "keywords": ["invest", "stock", "mutual fund", "portfolio", "retirement", "401k", "ira"],
            "response": """**📈 Investment Basics:**

**Getting Started:**
1. **Emergency Fund First:** 3-6 months expenses in savings
2. **Employer Retirement:** Max out 401k match (it's free money!)
3. **IRA Accounts:** Roth IRA if eligible, otherwise Traditional
4. **Low-Cost Funds:** Index funds or ETFs with low expense ratios

**Investment Principles:**
• **Diversify:** Don't put all eggs in one basket
• **Time Horizon:** Match investments to goals
• **Risk Tolerance:** Only invest what you can afford to lose
• **Regular Investing:** Dollar-cost averaging reduces risk

**In FINALYZE:** Track your savings rate in **Dashboard** to ensure you're saving enough to invest.

**⚠️ Important:** I cannot give specific stock recommendations. For personalized advice, consult a certified financial advisor.

*What's your investment time horizon?*"""
        },
        
        "debt": {
            "keywords": ["debt", "loan", "credit card", "pay off", "interest", "borrow"],
            "response": """**💳 Debt Management Plan:**

**Immediate Actions:**
1. **Stop Adding Debt:** Freeze credit cards if necessary
2. **List All Debts:** Amount, interest rate, minimum payment
3. **Contact Creditors:** Ask for lower interest rates or payment plans
4. **Create Repayment Plan** in FINALYZE Transactions

**Repayment Strategies:**
✅ **Snowball Method:** Pay smallest debts first (psychological wins)
✅ **Avalanche Method:** Pay highest interest first (saves money)

**Using FINALYZE:**
1. Log all debts as **Transactions**
2. Set up recurring payments
3. Track progress in **Dashboard**
4. Use **AI Tools → Financial Score** for health check
5. Get **Personalized Recommendations** for payoff plan

**Prevention:**
• Build emergency fund to avoid new debt
• Use cash/debit for daily spending
• Set up **Overspending Alerts** in AI Tools

*Which debts are you currently managing?*"""
        },
        
        "home": {
            "keywords": ["house", "home", "mortgage", "rent", "real estate", "property"],
            "response": """**🏠 Home Buying Guide:**

**Rent vs Buy Analysis:**
• **Rent if:** Staying <5 years, uncertain job, market prices high
• **Buy if:** Staying 5+ years, stable income, building equity

**Home Buying Checklist:**
1. **Credit Score:** 740+ for best rates
2. **Down Payment:** 20% to avoid PMI
3. **Emergency Fund:** Maintain after purchase
4. **Debt-to-Income:** Total debts <36% of income
5. **Housing Costs:** <28% of gross income

**In FINALYZE:**
• Use **Budget** to save for down payment
• Track progress in **Dashboard**
• Use **AI Tools → Expense Prediction** for mortgage planning

**💡 Tips:**
• Get pre-approved before shopping
• Consider all costs (insurance, taxes, maintenance)
• Think long-term (5+ years minimum)

*Are you planning to buy soon or just exploring options?*"""
        },
        
        "retirement": {
            "keywords": ["retire", "retirement", "pension", "old age", "401k", "roth"],
            "response": """**🏖️ Retirement Planning:**

**Retirement Number:** Aim for 25x annual expenses
Example: ₹50,000/month = ₹15,000,000 needed

**Account Priority:**
1. **401k up to employer match** (free money!)
2. **HSA** if available (triple tax advantage)
3. **Roth IRA** (tax-free growth)
4. **Back to 401k** up to limit
5. **Taxable brokerage accounts**

**Using FINALYZE for Retirement:**
• Set retirement savings goal in **Budget**
• Track progress in **Dashboard**
• Use **AI Tools → Expense Prediction** to estimate needs
• Check **Financial Score** for overall health

**💡 Key Factors:**
• Start early (compound interest is powerful)
• Increase contributions with raises
• Consider healthcare costs
• Plan for inflation

*When do you plan to retire and what's your current savings rate?*"""
        },
        
        "app": {
            "keywords": ["app", "finalyze", "feature", "how to use", "tool", "dashboard"],
            "response": """**📱 FINALYZE Features Guide:**

**Main Features Explained:**

**1. 📊 Dashboard**
• View financial overview
• Check key metrics (income, expenses, savings)
• Quick access to all sections

**2. 💰 Budget Management**
• **Enter Budget:** Set monthly income and category limits
• **View Budgets:** See all your budgets
• **Update/Delete:** Modify existing budgets

**3. 💳 Transactions**
• **Log Transaction:** Add new expenses
• **List Transactions:** View all transactions
• **Recurring:** Set up automatic transactions
• **Update/Delete:** Manage existing transactions

**4. 🤖 AI Tools**
• **Expense Prediction:** Forecast future spending
• **Overspending Alert:** Get warnings
• **Anomaly Detection:** Find unusual patterns
• **Financial Score:** Get health score
• **Personalized Recommendations:** Custom advice
• **Savings Efficiency:** Analyze savings rate

**5. 📥 Reports**
• Download CSV or PDF reports
• Export for external analysis

**6. 👤 Profile**
• Manage your account details
• Update personal information

**💡 Tip:** Start with Dashboard for overview, then use AI Tools for insights!

*Which feature would you like to know more about?*"""
        },
        
        "general": {
            "keywords": ["help", "hi", "hello", "hey", "what can you do", "finance"],
            "response": """**🤖 How I Can Help You:**

I'm your FINALYZE AI Financial Assistant! Here's what I can help with:

**📊 Budgeting & Expenses**
• Creating and sticking to budgets
• Expense tracking strategies
• Money management tips

**💰 Saving & Emergency Funds**
• Building emergency savings
• Saving for specific goals
• Optimizing savings rate

**📈 Investing Basics**
• Understanding different investments
• Retirement planning
• Risk management

**💳 Debt Management**
• Credit card debt payoff
• Loan repayment strategies
• Debt consolidation options

**🏠 Major Purchases**
• Home buying guidance
• Car purchase decisions
• Education financing

**📱 Using FINALYZE App**
• Feature explanations
• How-to guides
• Best practices

**🎯 Personalized Advice** based on your specific situation!

*What financial topic would you like to explore today?*"""
        }
    }
    
    best_match = None
    best_score = 0
    
    for category, data in knowledge_base.items():
        score = 0
        for keyword in data["keywords"]:
            if keyword in user_input_lower:
                score += 1
        
        if score > best_score:
            best_score = score
            best_match = category
    
    if best_match and best_score > 0:
        return knowledge_base[best_match]["response"]
    else:
        return """**🤔 I understand you're asking about finances. Let me help!**

Based on your question, I recommend:

**For Personalized Analysis:**
1. Use **AI Tools → Financial Score** for overall health check
2. Try **AI Tools → Personalized Recommendations** for custom advice
3. Check **Dashboard** for your current financial picture

**Common Questions I Can Answer:**
• How to create a budget that works?
• Best strategies for paying off debt?
• How to start investing with little money?
• Planning for big purchases (house, car)?
• Retirement planning at different ages?

**In FINALYZE App:** Most answers can be found by exploring the AI Tools section!

*Could you rephrase your question or tell me which specific area you need help with?*"""


def chatbot_view():
    """Chatbot Interface"""
    st.markdown('<div class="main-header">💬 AI Financial Assistant</div>', unsafe_allow_html=True)
    
    if 'add_back_button' in globals():
        add_back_button()
    
    financial_chatbot()

# ============================================
# MAIN APPLICATION
# ============================================

def show_fx_toast(notification):
    st.toast(
        f"💱 {notification['title']}\n{notification['message']}",
        icon="🔔"
    )


def main():
    """Main application with professional layout"""
    
    if st.session_state.access_token:
        sidebar_navigation()
        
        if st.session_state.active_section == "dashboard":
            dashboard_view()
        elif st.session_state.active_section == "profile":
            profile_view()
        elif st.session_state.active_section == "budget":
            budget_view()
        elif st.session_state.active_section == "transactions":
            transactions_view()
        elif st.session_state.active_section == "ai":
            ai_view()
        elif st.session_state.active_section == "chatbot":
            chatbot_view()
        else:
            dashboard_view()
    else:
        st.markdown('<div class="main-header" style="text-align: center;">🔐 FINALYZE - Sign In</div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🚀 Login", "✨ Register"])
        
        with tab1:
            login_user()
        
        with tab2:
            register_user()

if __name__ == "__main__":
    main()
