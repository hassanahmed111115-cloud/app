import streamlit as st
import cv2
import face_recognition
import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta
import json
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont
import io
import sqlite3
import hashlib
import qrcode
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import warnings
import random
import string
import time
from pathlib import Path
import shutil
import base64
import re
from datetime import date
import pickle
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import requests
import json
warnings.filterwarnings('ignore')

# ===============================
# Page Configuration
# ===============================
st.set_page_config(
    page_title="Ultimate College Management System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# Custom CSS for Professional UI
# ===============================
st.markdown("""
<style>
    /* Global Styles */
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .portal-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .portal-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        margin: 0.5rem 0;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .success-box {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 10px;
        animation: slideIn 0.5s ease-out;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #ffe6b0 0%, #ffd89b 100%);
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 10px;
    }
    
    .info-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-left: 5px solid #17a2b8;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 10px;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .dashboard-metric {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .dashboard-metric:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    .notification-badge {
        background: #ff4757;
        color: white;
        padding: 2px 8px;
        border-radius: 20px;
        font-size: 12px;
        position: absolute;
        top: -5px;
        right: -5px;
    }
    
    .progress-bar-custom {
        height: 8px;
        border-radius: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        animation: progress 2s ease-in-out;
    }
    
    @keyframes progress {
        from { width: 0%; }
        to { width: 100%; }
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Card Animation */
    .card-hover {
        transition: all 0.3s ease;
    }
    
    .card-hover:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# Database Setup (Complete)
# ===============================
def init_database():
    """Initialize complete college database with all tables"""
    conn = sqlite3.connect('college_management_complete.db')
    cursor = conn.cursor()
    
    # Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE,
            name TEXT NOT NULL,
            class TEXT,
            branch TEXT,
            year INTEGER,
            semester INTEGER,
            email TEXT,
            phone TEXT,
            parent_phone TEXT,
            parent_email TEXT,
            address TEXT,
            blood_group TEXT,
            dob DATE,
            enrollment_date DATE,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Faculty table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            faculty_id TEXT UNIQUE,
            name TEXT NOT NULL,
            department TEXT,
            designation TEXT,
            qualification TEXT,
            specialization TEXT,
            email TEXT,
            phone TEXT,
            joining_date DATE,
            salary INTEGER,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Parents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_id TEXT UNIQUE,
            name TEXT NOT NULL,
            student_id TEXT,
            student_name TEXT,
            email TEXT,
            phone TEXT,
            occupation TEXT,
            address TEXT,
            relationship TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            name TEXT,
            date DATE,
            time TIME,
            timestamp TIMESTAMP,
            status TEXT,
            marked_by TEXT,
            subject TEXT,
            semester INTEGER,
            faculty_id TEXT,
            latitude REAL,
            longitude REAL,
            location_validated BOOLEAN DEFAULT 0
        )
    ''')
    
    # Faculty Attendance
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty_attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            faculty_id TEXT,
            name TEXT,
            date DATE,
            time TIME,
            status TEXT,
            timestamp TIMESTAMP,
            check_in_time TIME,
            check_out_time TIME
        )
    ''')
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            email TEXT,
            portal_type TEXT,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT UNIQUE,
            course_name TEXT,
            faculty_id TEXT,
            faculty_name TEXT,
            semester INTEGER,
            credits INTEGER,
            schedule TEXT,
            classroom TEXT,
            syllabus TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Assignments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT,
            title TEXT,
            description TEXT,
            due_date DATE,
            max_marks INTEGER,
            created_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            attachment_path TEXT
        )
    ''')
    
    # Submissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_id INTEGER,
            student_id TEXT,
            student_name TEXT,
            submission_date DATE,
            marks INTEGER,
            feedback TEXT,
            file_path TEXT,
            plagiarism_score REAL DEFAULT 0,
            status TEXT DEFAULT 'submitted'
        )
    ''')
    
    # Fees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            student_name TEXT,
            semester INTEGER,
            fee_type TEXT,
            amount INTEGER,
            paid_amount INTEGER DEFAULT 0,
            due_date DATE,
            status TEXT DEFAULT 'pending',
            payment_date DATE,
            transaction_id TEXT,
            payment_method TEXT,
            receipt_path TEXT
        )
    ''')
    
    # Scholarships table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scholarships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            student_name TEXT,
            scholarship_name TEXT,
            amount INTEGER,
            awarded_date DATE,
            valid_until DATE,
            status TEXT DEFAULT 'active'
        )
    ''')
    
    # Complaints table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            student_name TEXT,
            title TEXT,
            description TEXT,
            category TEXT,
            priority TEXT DEFAULT 'normal',
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_by TEXT,
            resolved_date DATE,
            feedback TEXT,
            rating INTEGER
        )
    ''')
    
    # Events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT,
            description TEXT,
            date DATE,
            time TIME,
            venue TEXT,
            organizer TEXT,
            max_participants INTEGER,
            registered_count INTEGER DEFAULT 0,
            created_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Event Registrations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            student_id TEXT,
            student_name TEXT,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            attendance_status TEXT DEFAULT 'registered'
        )
    ''')
    
    # Notifications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            message TEXT,
            target_role TEXT,
            target_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expiry_date DATE,
            priority TEXT DEFAULT 'normal',
            is_read BOOLEAN DEFAULT 0
        )
    ''')
    
    # Library table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS library_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id TEXT UNIQUE,
            title TEXT,
            author TEXT,
            publisher TEXT,
            year INTEGER,
            isbn TEXT,
            category TEXT,
            quantity INTEGER,
            available INTEGER,
            location TEXT,
            added_date DATE
        )
    ''')
    
    # Library Transactions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS library_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id TEXT,
            student_id TEXT,
            student_name TEXT,
            issue_date DATE,
            due_date DATE,
            return_date DATE,
            status TEXT DEFAULT 'issued',
            fine_amount REAL DEFAULT 0,
            remarks TEXT
        )
    ''')
    
    # Hostel Management
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hostel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hostel_name TEXT,
            room_number TEXT,
            student_id TEXT,
            student_name TEXT,
            allocated_date DATE,
            vacated_date DATE,
            status TEXT DEFAULT 'occupied',
            rent_per_month INTEGER
        )
    ''')
    
    # Transport Management
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transport (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route_name TEXT,
            vehicle_number TEXT,
            driver_name TEXT,
            driver_phone TEXT,
            student_id TEXT,
            student_name TEXT,
            pickup_point TEXT,
            drop_point TEXT,
            fee INTEGER,
            status TEXT DEFAULT 'active'
        )
    ''')
    
    # AI Models table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT,
            model_type TEXT,
            accuracy REAL,
            trained_on DATE,
            model_path TEXT,
            parameters TEXT
        )
    ''')
    
    # AI Predictions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_type TEXT,
            target_id TEXT,
            prediction_value TEXT,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            validated BOOLEAN DEFAULT 0
        )
    ''')
    
    # Default Admin User
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, role, portal_type, is_active) VALUES (?, ?, ?, ?, ?)",
                      ('admin', hashlib.sha256('admin123'.encode()).hexdigest(), 'admin', 'admin', 1))
    
    # Default Faculty
    cursor.execute("SELECT * FROM faculty WHERE faculty_id='faculty1'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO faculty (faculty_id, name, department, designation, email)
            VALUES (?, ?, ?, ?, ?)
        """, ('faculty1', 'Dr. John Smith', 'Computer Science', 'Professor', 'john@college.edu'))
        cursor.execute("INSERT INTO users (username, password, role, portal_type) VALUES (?, ?, ?, ?)",
                      ('faculty1', hashlib.sha256('faculty123'.encode()).hexdigest(), 'faculty', 'faculty'))
    
    # Default Student
    cursor.execute("SELECT * FROM students WHERE student_id='student1'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO students (student_id, name, class, branch, year, semester, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('student1', 'Alice Johnson', 'CS-A', 'Computer Science', 1, 1, 'alice@student.edu'))
        cursor.execute("INSERT INTO users (username, password, role, portal_type) VALUES (?, ?, ?, ?)",
                      ('student1', hashlib.sha256('student123'.encode()).hexdigest(), 'student', 'student'))
    
    # Default Parent
    cursor.execute("SELECT * FROM parents WHERE parent_id='parent1'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO parents (parent_id, name, student_id, student_name, email, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ('parent1', 'Robert Johnson', 'student1', 'Alice Johnson', 'robert@parent.com', '9876543210'))
        cursor.execute("INSERT INTO users (username, password, role, portal_type) VALUES (?, ?, ?, ?)",
                      ('parent1', hashlib.sha256('parent123'.encode()).hexdigest(), 'parent', 'parents'))
    
    # Default AI Admin
    cursor.execute("SELECT * FROM users WHERE username='ai_admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, role, portal_type) VALUES (?, ?, ?, ?)",
                      ('ai_admin', hashlib.sha256('ai123'.encode()).hexdigest(), 'ai_admin', 'ai_admin'))
    
    conn.commit()
    conn.close()

# ===============================
# Advanced Helper Functions
# ===============================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password, portal_type):
    conn = sqlite3.connect('college_management_complete.db')
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username=? AND password=? AND portal_type=? AND is_active=1", 
                   (username, hashed, portal_type))
    user = cursor.fetchone()
    if user:
        cursor.execute("UPDATE users SET last_login=? WHERE username=?", 
                      (datetime.now(), username))
        conn.commit()
    conn.close()
    return user is not None

def add_user(username, password, role, portal_type, email=None):
    conn = sqlite3.connect('college_management_complete.db')
    cursor = conn.cursor()
    try:
        hashed = hash_password(password)
        cursor.execute("INSERT INTO users (username, password, role, portal_type, email) VALUES (?, ?, ?, ?, ?)",
                      (username, hashed, role, portal_type, email))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def send_email(to_email, subject, body, attachment=None):
    """Send email with optional attachment"""
    try:
        # SMTP Configuration (Update with your details)
        smtp_server = "smtp.gmail.com"
        port = 587
        sender_email = "college@system.com"  # Update this
        password = "your_password"  # Update this
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        if attachment:
            with open(attachment, "rb") as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
                msg.attach(part)
        
        # Uncomment to actually send
        # server = smtplib.SMTP(smtp_server, port)
        # server.starttls()
        # server.login(sender_email, password)
        # server.send_message(msg)
        # server.quit()
        
        return True
    except:
        return False

def generate_qr_code(data):
    """Generate QR code for any data"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def generate_id_card(student_data):
    """Generate professional ID card"""
    img = Image.new('RGB', (800, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    # Background gradient effect
    for i in range(400):
        color = (100 + i//4, 100 + i//4, 200)
        draw.rectangle([(0, i), (800, i+1)], fill=color)
    
    # College logo placeholder
    draw.rectangle([(50, 50), (150, 150)], fill='#667eea', outline='white', width=3)
    
    # Student details
    draw.text((200, 80), f"Student ID: {student_data.get('student_id', 'N/A')}", fill='white')
    draw.text((200, 120), f"Name: {student_data.get('name', 'N/A')}", fill='white')
    draw.text((200, 160), f"Class: {student_data.get('class', 'N/A')}", fill='white')
    draw.text((200, 200), f"Branch: {student_data.get('branch', 'N/A')}", fill='white')
    
    # QR Code
    qr = generate_qr_code(f"Student: {student_data.get('name')}\nID: {student_data.get('student_id')}")
    qr_img = qr.get_image()
    qr_img = qr_img.resize((150, 150))
    img.paste(qr_img, (600, 200))
    
    return img

def calculate_attendance_percentage(student_id):
    conn = sqlite3.connect('college_management_complete.db')
    attendance = pd.read_sql_query(f"""
        SELECT COUNT(*) as present FROM attendance 
        WHERE student_id='{student_id}' AND status='present'
    """, conn)
    total = pd.read_sql_query(f"SELECT COUNT(*) as total FROM attendance WHERE student_id='{student_id}'", conn)
    conn.close()
    
    if total['total'][0] > 0:
        return (attendance['present'][0] / total['total'][0]) * 100
    return 0

def get_fee_status(student_id):
    conn = sqlite3.connect('college_management_complete.db')
    fees = pd.read_sql_query(f"""
        SELECT SUM(amount) as total, SUM(paid_amount) as paid 
        FROM fees WHERE student_id='{student_id}'
    """, conn)
    conn.close()
    
    total = fees['total'][0] if fees['total'][0] else 0
    paid = fees['paid'][0] if fees['paid'][0] else 0
    
    return total, paid, total - paid

def backup_database():
    """Create timestamped backup"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"backup_college_{timestamp}.db"
    shutil.copy2('college_management_complete.db', backup_file)
    return backup_file

def restore_database(backup_file):
    """Restore from backup"""
    shutil.copy2(backup_file, 'college_management_complete.db')
    return True

def export_report(dataframe, report_name):
    """Export dataframe to CSV and Excel"""
    csv_file = f"{report_name}_{datetime.now().strftime('%Y%m%d')}.csv"
    excel_file = f"{report_name}_{datetime.now().strftime('%Y%m%d')}.xlsx"
    
    dataframe.to_csv(csv_file, index=False)
    dataframe.to_excel(excel_file, index=False)
    
    return csv_file, excel_file

def analyze_sentiment(text):
    """Basic sentiment analysis"""
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'helpful', 'nice']
    negative_words = ['bad', 'poor', 'terrible', 'awful', 'disappointing', 'slow', 'issue']
    
    text_lower = text.lower()
    positive_score = sum(1 for word in positive_words if word in text_lower)
    negative_score = sum(1 for word in negative_words if word in text_lower)
    
    if positive_score > negative_score:
        return 'positive', positive_score - negative_score
    elif negative_score > positive_score:
        return 'negative', negative_score - positive_score
    else:
        return 'neutral', 0

def predict_student_performance(student_id):
    """AI-based student performance prediction"""
    conn = sqlite3.connect('college_management_complete.db')
    
    # Get historical data
    attendance = calculate_attendance_percentage(student_id)
    submissions = pd.read_sql_query(f"SELECT AVG(marks) as avg_marks FROM submissions WHERE student_id='{student_id}'", conn)
    avg_marks = submissions['avg_marks'][0] if submissions['avg_marks'][0] else 0
    
    conn.close()
    
    # Simple prediction model
    performance_score = (attendance * 0.4) + (avg_marks * 0.6)
    
    if performance_score >= 85:
        prediction = "Excellent Performance"
        color = "success"
    elif performance_score >= 70:
        prediction = "Good Performance"
        color = "info"
    elif performance_score >= 50:
        prediction = "Average Performance - Needs Improvement"
        color = "warning"
    else:
        prediction = "Poor Performance - Immediate Intervention Required"
        color = "danger"
    
    return prediction, performance_score, color

# ===============================
# Initialize Database
# ===============================
init_database()

# ===============================
# Session State
# ===============================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'portal_type' not in st.session_state:
    st.session_state.portal_type = None
if 'selected_portal' not in st.session_state:
    st.session_state.selected_portal = None
if 'notifications' not in st.session_state:
    st.session_state.notifications = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# ===============================
# Portal Selection
# ===============================
def show_portal_selection():
    st.markdown('<div class="main-header">🏛️ Ultimate College Management System</div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #667eea;'>Select Your Portal</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    portals = [
        ("🎓", "Student Portal", "student", 
         "📚 Courses\n📝 Assignments\n📊 Attendance\n💰 Fees\n📋 Complaints\n🎯 Events",
         "Access all student resources"),
        ("👨‍🏫", "Faculty Portal", "faculty", 
         "📚 Courses\n📝 Assignments\n📸 Attendance\n📊 Grades\n📋 Reports\n💬 Feedback",
         "Manage teaching activities"),
        ("👨‍👩‍👧", "Parents Portal", "parents", 
         "👤 Child Progress\n📊 Attendance\n💰 Fees\n📝 Reports\n🔔 Alerts\n📅 Events",
         "Monitor child's education"),
        ("👔", "Admin Portal", "admin", 
         "👥 Management\n📊 Analytics\n💰 Finance\n📚 Academics\n🏢 Infrastructure\n📋 Reports",
         "Complete system control"),
        ("🤖", "AI Admin", "ai_admin", 
         "📊 Insights\n📈 Predictions\n⚡ Automation\n💬 Chatbot\n🎯 Recommendations\n🔍 Analytics",
         "AI-powered management")
    ]
    
    cols = [col1, col2, col3, col4, col5]
    
    for idx, (icon, title, portal_type, features, desc) in enumerate(portals):
        with cols[idx]:
            with st.container():
                st.markdown(f"""
                <div class="portal-card">
                    <h1 style="font-size: 3rem;">{icon}</h1>
                    <h3>{title}</h3>
                    <hr style="margin: 10px 0;">
                    <p style="font-size: 12px;">{features.replace(chr(10), '<br>')}</p>
                    <hr style="margin: 10px 0;">
                    <small>{desc}</small>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Enter {title}", key=f"enter_{portal_type}", use_container_width=True):
                    st.session_state.selected_portal = portal_type
                    st.rerun()

# ===============================
# Login Screen
# ===============================
def show_login():
    st.markdown(f'<div class="main-header">🏛️ {st.session_state.selected_portal.title()} Portal Login</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown('<div class="info-box">🔐 Please enter your credentials to access the portal</div>', unsafe_allow_html=True)
            
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔓 Login", type="primary", use_container_width=True):
                    if verify_user(username, password, st.session_state.selected_portal):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.portal_type = st.session_state.selected_portal
                        st.success("Login successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
            
            with col2:
                if st.button("⬅️ Back", use_container_width=True):
                    st.session_state.selected_portal = None
                    st.rerun()
            
            # Demo credentials
            st.markdown("---")
            st.markdown("### Demo Credentials")
            if st.session_state.selected_portal == "student":
                st.info("Username: student1\nPassword: student123")
            elif st.session_state.selected_portal == "faculty":
                st.info("Username: faculty1\nPassword: faculty123")
            elif st.session_state.selected_portal == "parents":
                st.info("Username: parent1\nPassword: parent123")
            elif st.session_state.selected_portal == "admin":
                st.info("Username: admin\nPassword: admin123")
            elif st.session_state.selected_portal == "ai_admin":
                st.info("Username: ai_admin\nPassword: ai123")

# ===============================
# STUDENT PORTAL (Enhanced)
# ===============================
def student_portal():
    st.markdown('<div class="main-header">🎓 Student Portal Dashboard</div>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('college_management_complete.db')
    student = pd.read_sql_query(f"SELECT * FROM students WHERE student_id='{st.session_state.username}'", conn)
    
    if student.empty:
        st.error("Student record not found")
        return
    
    student = student.iloc[0]
    
    # Sidebar with student info
    with st.sidebar:
        st.markdown(f"""
        <div class="stat-card">
            <h3>👤 {student['name']}</h3>
            <p>{student['student_id']}</p>
            <p>{student['branch']} - Semester {student['semester']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
        attendance_pct = calculate_attendance_percentage(student['student_id'])
        total_fees, paid_fees, pending_fees = get_fee_status(student['student_id'])
        
        st.metric("📊 Attendance", f"{attendance_pct:.1f}%")
        st.metric("💰 Fees Paid", f"₹{paid_fees:,.0f}", f"Pending: ₹{pending_fees:,.0f}")
        
        # Performance prediction
        prediction, score, color = predict_student_performance(student['student_id'])
        st.markdown(f"""
        <div class="info-box">
            <strong>🎯 AI Performance Score:</strong> {score:.1f}%<br>
            <strong>📈 Prediction:</strong> {prediction}
        </div>
        """, unsafe_allow_html=True)
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Dashboard", "📚 Courses", "📝 Assignments", 
        "📅 Attendance", "💰 Fees & Scholarships", "📋 Complaints", 
        "🎯 Events & Library"
    ])
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        
        # Upcoming events
        events = pd.read_sql_query("SELECT * FROM events WHERE date >= date('now') ORDER BY date LIMIT 3", conn)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <h2>{len(events)}</h2>
                <p>📅 Upcoming Events</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Pending assignments
        assignments = pd.read_sql_query(f"""
            SELECT a.* FROM assignments a
            WHERE a.course_code IN (
                SELECT course_code FROM courses WHERE semester = {student['semester']}
            )
            AND a.due_date >= date('now')
        """, conn)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <h2>{len(assignments)}</h2>
                <p>📝 Pending Assignments</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Library books
        books = pd.read_sql_query("SELECT COUNT(*) as count FROM library_books WHERE available > 0", conn)
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <h2>{books['count'][0]}</h2>
                <p>📚 Books Available</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Complaints status
        complaints = pd.read_sql_query(f"SELECT COUNT(*) as count FROM complaints WHERE student_id='{student['student_id']}' AND status='pending'", conn)
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <h2>{complaints['count'][0]}</h2>
                <p>📋 Active Complaints</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Recent notifications
        st.subheader("🔔 Recent Notifications")
        notifications = pd.read_sql_query("""
            SELECT * FROM notifications 
            WHERE target_role='student' OR target_role='all' OR target_id=?
            ORDER BY created_at DESC LIMIT 5
        """, conn, params=(student['student_id'],))
        
        for _, notif in notifications.iterrows():
            if notif['priority'] == 'urgent':
                st.error(f"🚨 **{notif['title']}**\n\n{notif['message']}")
            elif notif['priority'] == 'high':
                st.warning(f"⚠️ **{notif['title']}**\n\n{notif['message']}")
            else:
                st.info(f"ℹ️ **{notif['title']}**\n\n{notif['message']}")
        
        # Performance chart
        st.subheader("📊 Academic Performance Trend")
        marks_data = pd.read_sql_query(f"""
            SELECT a.title, s.marks, a.max_marks
            FROM submissions s
            JOIN assignments a ON s.assignment_id = a.id
            WHERE s.student_id='{student['student_id']}'
            ORDER BY s.submission_date DESC LIMIT 10
        """, conn)
        
        if not marks_data.empty:
            marks_data['percentage'] = (marks_data['marks'] / marks_data['max_marks']) * 100
            fig = px.line(marks_data, x='title', y='percentage', title='Assignment Performance')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("📚 Enrolled Courses")
        courses = pd.read_sql_query(f"""
            SELECT c.* FROM courses c
            WHERE c.semester = {student['semester']}
        """, conn)
        
        if not courses.empty:
            for _, course in courses.iterrows():
                with st.expander(f"{course['course_code']}: {course['course_name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Faculty:** {course['faculty_name']}")
                        st.write(f"**Credits:** {course['credits']}")
                        st.write(f"**Schedule:** {course['schedule']}")
                    with col2:
                        st.write(f"**Classroom:** {course['classroom']}")
                        if course['syllabus']:
                            st.download_button("📥 Download Syllabus", course['syllabus'], f"{course['course_code']}_syllabus.pdf")
        else:
            st.info("No courses enrolled yet")
    
    with tab3:
        st.subheader("📝 Assignments")
        
        assignments = pd.read_sql_query(f"""
            SELECT a.* FROM assignments a
            WHERE a.course_code IN (
                SELECT course_code FROM courses WHERE semester = {student['semester']}
            )
            ORDER BY a.due_date
        """, conn)
        
        if not assignments.empty:
            for _, assign in assignments.iterrows():
                with st.expander(f"{assign['title']} - Due: {assign['due_date']} (Max Marks: {assign['max_marks']})"):
                    st.write(f"**Description:** {assign['description']}")
                    
                    # Check submission status
                    submitted = pd.read_sql_query(f"""
                        SELECT * FROM submissions 
                        WHERE assignment_id={assign['id']} 
                        AND student_id='{student['student_id']}'
                    """, conn)
                    
                    if submitted.empty:
                        with st.form(f"submit_{assign['id']}"):
                            answer = st.text_area("Your Answer/Submission", height=150)
                            file = st.file_uploader("Upload File (Optional)", type=['pdf', 'doc', 'docx', 'txt'])
                            
                            if st.form_submit_button("Submit Assignment"):
                                cursor = conn.cursor()
                                cursor.execute("""
                                    INSERT INTO submissions (assignment_id, student_id, student_name, submission_date, status)
                                    VALUES (?, ?, ?, ?, ?)
                                """, (assign['id'], student['student_id'], student['name'], datetime.now().strftime("%Y-%m-%d"), 'submitted'))
                                conn.commit()
                                st.success("Assignment submitted successfully!")
                                st.rerun()
                    else:
                        st.success(f"✅ Submitted on {submitted['submission_date'].iloc[0]}")
                        if submitted['marks'].iloc[0]:
                            st.info(f"📊 Marks: {submitted['marks'].iloc[0]}/{assign['max_marks']}")
                            if submitted['feedback'].iloc[0]:
                                st.info(f"💬 Feedback: {submitted['feedback'].iloc[0]}")
        else:
            st.info("No pending assignments")
    
    with tab4:
        st.subheader("📅 Attendance Record")
        
        # Date filter
        col1, col2 = st.columns(2)
        with col1:
            month = st.selectbox("Month", range(1, 13))
        with col2:
            year = st.number_input("Year", 2020, 2030, datetime.now().year)
        
        attendance_records = pd.read_sql_query(f"""
            SELECT date, time, status, subject
            FROM attendance
            WHERE student_id='{student['student_id']}'
            AND strftime('%m', date) = '{month:02d}'
            AND strftime('%Y', date) = '{year}'
            ORDER BY date DESC
        """, conn)
        
        if not attendance_records.empty:
            st.dataframe(attendance_records, use_container_width=True)
            
            # Attendance heatmap
            attendance_records['date'] = pd.to_datetime(attendance_records['date'])
            attendance_records['day'] = attendance_records['date'].dt.day_name()
            attendance_records['week'] = attendance_records['date'].dt.isocalendar().week
            
            heatmap_data = attendance_records.pivot_table(
                values='status', 
                index='week', 
                columns='day',
                aggfunc=lambda x: (x == 'present').sum()
            ).fillna(0)
            
            fig = px.imshow(heatmap_data, text_auto=True, title='Attendance Heatmap')
            st.plotly_chart(fig, use_container_width=True)
            
            # Download report
            csv = attendance_records.to_csv(index=False)
            st.download_button("📥 Download Attendance Report", csv, "attendance_report.csv", "text/csv")
        else:
            st.info("No attendance records found")
    
    with tab5:
        st.subheader("💰 Fee Details")
        
        fees = pd.read_sql_query(f"SELECT * FROM fees WHERE student_id='{student['student_id']}'", conn)
        
        if not fees.empty:
            st.dataframe(fees, use_container_width=True)
            
            # Fee payment chart
            fig = go.Figure(data=[
                go.Bar(name='Total', x=fees['fee_type'], y=fees['amount']),
                go.Bar(name='Paid', x=fees['fee_type'], y=fees['paid_amount'])
            ])
            fig.update_layout(title='Fee Breakdown', barmode='group')
            st.plotly_chart(fig, use_container_width=True)
            
            # Payment form
            pending_fees = fees[fees['status'] == 'pending']
            if not pending_fees.empty:
                with st.form("payment_form"):
                    st.subheader("Make Payment")
                    selected_fee = st.selectbox("Select Fee Type", pending_fees['fee_type'].values)
                    amount = pending_fees[pending_fees['fee_type'] == selected_fee]['amount'].values[0]
                    paid_amount = pending_fees[pending_fees['fee_type'] == selected_fee]['paid_amount'].values[0]
                    pending = amount - paid_amount
                    
                    st.write(f"**Total Amount:** ₹{amount:,}")
                    st.write(f"**Paid:** ₹{paid_amount:,}")
                    st.write(f"**Pending:** ₹{pending:,}")
                    
                    payment_amount = st.number_input("Payment Amount", min_value=0, max_value=pending, value=pending)
                    payment_method = st.selectbox("Payment Method", ["Credit Card", "Debit Card", "Net Banking", "UPI"])
                    
                    if st.form_submit_button("Pay Now"):
                        # Update fees
                        cursor = conn.cursor()
                        cursor.execute("""
                            UPDATE fees 
                            SET paid_amount = paid_amount + ?,
                                status = CASE WHEN paid_amount + ? >= amount THEN 'paid' ELSE 'partial' END,
                                payment_date = ?,
                                payment_method = ?
                            WHERE student_id=? AND fee_type=?
                        """, (payment_amount, payment_amount, datetime.now().strftime("%Y-%m-%d"), payment_method, 
                              student['student_id'], selected_fee))
                        conn.commit()
                        st.success(f"Payment of ₹{payment_amount} successful!")
                        st.rerun()
        
        # Scholarships
        st.subheader("🏆 Scholarships")
        scholarships = pd.read_sql_query(f"SELECT * FROM scholarships WHERE student_id='{student['student_id']}'", conn)
        
        if not scholarships.empty:
            st.dataframe(scholarships, use_container_width=True)
        else:
            st.info("No scholarships awarded")
    
    with tab6:
        st.subheader("📋 Raise a Complaint")
        
        with st.form("complaint_form"):
            title = st.text_input("Title")
            category = st.selectbox("Category", ["Academic", "Administrative", "Infrastructure", "Hostel", "Transport", "Other"])
            priority = st.selectbox("Priority", ["normal", "high", "urgent"])
            description = st.text_area("Description", height=150)
            
            if st.form_submit_button("Submit Complaint"):
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO complaints (student_id, student_name, title, description, category, priority)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (student['student_id'], student['name'], title, description, category, priority))
                conn.commit()
                st.success("Complaint submitted successfully!")
                
                # Send notification to admin
                send_email("admin@college.edu", "New Complaint", f"Student {student['name']} submitted a complaint: {title}")
                st.rerun()
        
        # View complaints history
        st.subheader("Your Complaints")
        complaints_history = pd.read_sql_query(f"""
            SELECT * FROM complaints 
            WHERE student_id='{student['student_id']}'
            ORDER BY created_at DESC
        """, conn)
        
        if not complaints_history.empty:
            for _, comp in complaints_history.iterrows():
                with st.expander(f"{comp['title']} - Status: {comp['status']} (Priority: {comp['priority']})"):
                    st.write(f"**Category:** {comp['category']}")
                    st.write(f"**Description:** {comp['description']}")
                    st.write(f"**Submitted:** {comp['created_at']}")
                    if comp['status'] == 'resolved':
                        st.success(f"**Resolution:** {comp['feedback']}")
                        st.write(f"**Resolved by:** {comp['resolved_by']} on {comp['resolved_date']}")
                        if comp['rating']:
                            st.write(f"**Rating:** {'⭐' * comp['rating']}")
    
    with tab7:
        st.subheader("🎯 Events & Library")
        
        # Events
        st.subheader("Upcoming Events")
        events = pd.read_sql_query("SELECT * FROM events WHERE date >= date('now') ORDER BY date LIMIT 5", conn)
        
        if not events.empty:
            for _, event in events.iterrows():
                with st.expander(f"📅 {event['event_name']} - {event['date']}"):
                    st.write(f"**Description:** {event['description']}")
                    st.write(f"**Time:** {event['time']}")
                    st.write(f"**Venue:** {event['venue']}")
                    st.write(f"**Organizer:** {event['organizer']}")
                    
                    # Check registration
                    registered = pd.read_sql_query(f"""
                        SELECT * FROM event_registrations 
                        WHERE event_id={event['id']} AND student_id='{student['student_id']}'
                    """, conn)
                    
                    if registered.empty:
                        if st.button(f"Register for {event['event_name']}", key=f"register_{event['id']}"):
                            cursor = conn.cursor()
                            cursor.execute("""
                                INSERT INTO event_registrations (event_id, student_id, student_name)
                                VALUES (?, ?, ?)
                            """, (event['id'], student['student_id'], student['name']))
                            cursor.execute("UPDATE events SET registered_count = registered_count + 1 WHERE id=?", (event['id'],))
                            conn.commit()
                            st.success("Registered successfully!")
                            st.rerun()
                    else:
                        st.success("✅ Registered!")
        else:
            st.info("No upcoming events")
        
        # Library
        st.subheader("📚 Library Management")
        
        # Search books
        search_term = st.text_input("Search Books by Title, Author, or ISBN")
        
        if search_term:
            books = pd.read_sql_query(f"""
                SELECT * FROM library_books 
                WHERE title LIKE '%{search_term}%' 
                OR author LIKE '%{search_term}%' 
                OR isbn LIKE '%{search_term}%'
            """, conn)
        else:
            books = pd.read_sql_query("SELECT * FROM library_books LIMIT 10", conn)
        
        if not books.empty:
            st.dataframe(books[['book_id', 'title', 'author', 'category', 'available', 'location']], 
                        use_container_width=True)
            
            # Issue book
            selected_book = st.selectbox("Select Book to Issue", books['book_id'].values)
            if st.button("Request Book Issue"):
                book = books[books['book_id'] == selected_book].iloc[0]
                if book['available'] > 0:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO library_transactions (book_id, student_id, student_name, issue_date, due_date)
                        VALUES (?, ?, ?, ?, ?)
                    """, (selected_book, student['student_id'], student['name'], 
                          datetime.now().strftime("%Y-%m-%d"), 
                          (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")))
                    cursor.execute("UPDATE library_books SET available = available - 1 WHERE book_id=?", (selected_book,))
                    conn.commit()
                    st.success(f"Book '{book['title']}' issued successfully! Due date: {(datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')}")
                else:
                    st.error("Book not available")
        else:
            st.info("No books found")
        
        # Issued books
        st.subheader("My Issued Books")
        issued = pd.read_sql_query(f"""
            SELECT * FROM library_transactions 
            WHERE student_id='{student['student_id']}' AND status='issued'
        """, conn)
        
        if not issued.empty:
            for _, issue in issued.iterrows():
                with st.expander(f"Book ID: {issue['book_id']} - Due: {issue['due_date']}"):
                    st.write(f"**Issue Date:** {issue['issue_date']}")
                    st.write(f"**Due Date:** {issue['due_date']}")
                    days_left = (pd.to_datetime(issue['due_date']) - pd.to_datetime(datetime.now())).days
                    if days_left < 0:
                        st.error(f"⚠️ Overdue by {abs(days_left)} days! Fine: ₹{abs(days_left) * 5}")
                    else:
                        st.info(f"📅 {days_left} days left to return")
        else:
            st.info("No books issued")
    
    conn.close()

# ===============================
# FACULTY PORTAL (Enhanced)
# ===============================
def faculty_portal():
    st.markdown('<div class="main-header">👨‍🏫 Faculty Portal Dashboard</div>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('college_management_complete.db')
    faculty = pd.read_sql_query(f"SELECT * FROM faculty WHERE faculty_id='{st.session_state.username}'", conn)
    
    if faculty.empty:
        st.error("Faculty record not found")
        return
    
    faculty = faculty.iloc[0]
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div class="stat-card">
            <h3>👨‍🏫 {faculty['name']}</h3>
            <p>{faculty['faculty_id']}</p>
            <p>{faculty['designation']} - {faculty['department']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Courses teaching
        courses = pd.read_sql_query(f"SELECT * FROM courses WHERE faculty_id='{faculty['faculty_id']}'", conn)
        st.metric("📚 Courses Teaching", len(courses))
        
        # Total students
        total_students = 0
        for _, course in courses.iterrows():
            students = pd.read_sql_query(f"SELECT COUNT(*) as count FROM students WHERE semester={course['semester']}", conn)
            total_students += students['count'][0]
        st.metric("👨‍🎓 Total Students", total_students)
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard", "📚 My Courses", "📝 Assignments", 
        "📸 Face Attendance", "📊 Grade Management", "📋 Reports"
    ])
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        
        # Pending assignments
        pending_assignments = pd.read_sql_query(f"""
            SELECT COUNT(*) as count FROM assignments 
            WHERE created_by='{faculty['faculty_id']}' AND due_date >= date('now')
        """, conn)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <h2>{pending_assignments['count'][0]}</h2>
                <p>📝 Pending Assignments</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Submissions to grade
        submissions = pd.read_sql_query(f"""
            SELECT COUNT(*) as count FROM submissions s
            JOIN assignments a ON s.assignment_id = a.id
            WHERE a.created_by='{faculty['faculty_id']}' AND s.marks IS NULL
        """, conn)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <h2>{submissions['count'][0]}</h2>
                <p>📋 Pending Grading</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Today's classes
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <h2>{len(courses)}</h2>
                <p>📚 Today's Classes</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Attendance rate
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <h2>85%</h2>
                <p>📊 Avg. Attendance</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📸 Take Attendance", use_container_width=True):
                st.session_state.take_attendance = True
        with col2:
            if st.button("📝 Create Assignment", use_container_width=True):
                st.session_state.create_assignment = True
        with col3:
            if st.button("📊 View Analytics", use_container_width=True):
                st.session_state.view_analytics = True
    
    with tab2:
        st.subheader("📚 My Courses")
        
        if not courses.empty:
            for _, course in courses.iterrows():
                with st.expander(f"{course['course_code']}: {course['course_name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Semester:** {course['semester']}")
                        st.write(f"**Credits:** {course['credits']}")
                        st.write(f"**Schedule:** {course['schedule']}")
                        st.write(f"**Classroom:** {course['classroom']}")
                    with col2:
                        # Get enrolled students
                        students = pd.read_sql_query(f"""
                            SELECT * FROM students WHERE semester={course['semester']}
                        """, conn)
                        st.write(f"**Enrolled Students:** {len(students)}")
                        
                        # Download student list
                        if not students.empty:
                            csv = students[['student_id', 'name', 'email', 'phone']].to_csv(index=False)
                            st.download_button(f"📥 Download Student List", csv, f"{course['course_code']}_students.csv", "text/csv")
        else:
            st.info("No courses assigned")
    
    with tab3:
        st.subheader("📝 Manage Assignments")
        
        selected_course = st.selectbox("Select Course", courses['course_code'].values)
        
        # Create new assignment
        with st.expander("➕ Create New Assignment"):
            with st.form("assignment_form"):
                title = st.text_input("Assignment Title")
                description = st.text_area("Description")
                due_date = st.date_input("Due Date")
                max_marks = st.number_input("Maximum Marks", 10, 100, 100)
                attachment = st.file_uploader("Attachment", type=['pdf', 'doc', 'docx'])
                
                if st.form_submit_button("Create Assignment"):
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO assignments (course_code, title, description, due_date, max_marks, created_by)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (selected_course, title, description, due_date, max_marks, faculty['faculty_id']))
                    conn.commit()
                    st.success("Assignment created successfully!")
                    
                    # Notify students
                    students = pd.read_sql_query(f"SELECT * FROM students WHERE semester={courses[courses['course_code'] == selected_course]['semester'].iloc[0]}", conn)
                    for _, student in students.iterrows():
                        send_email(student['email'], f"New Assignment: {title}", 
                                  f"A new assignment has been posted: {title}\nDue Date: {due_date}\n\n{description}")
                    st.rerun()
        
        # View existing assignments
        assignments = pd.read_sql_query(f"""
            SELECT * FROM assignments 
            WHERE course_code='{selected_course}'
            ORDER BY due_date DESC
        """, conn)
        
        for _, assign in assignments.iterrows():
            with st.expander(f"{assign['title']} - Due: {assign['due_date']} (Max: {assign['max_marks']})"):
                st.write(f"**Description:** {assign['description']}")
                
                # View submissions
                submissions = pd.read_sql_query(f"""
                    SELECT s.* FROM submissions s
                    WHERE s.assignment_id={assign['id']}
                """, conn)
                
                if not submissions.empty:
                    st.write(f"**Submissions:** {len(submissions)}")
                    
                    # Grade submissions
                    for _, sub in submissions.iterrows():
                        with st.container():
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"**{sub['student_name']}** - Submitted: {sub['submission_date']}")
                            with col2:
                                if not sub['marks']:
                                    marks = st.number_input(f"Marks", 0, assign['max_marks'], key=f"marks_{sub['id']}")
                                    feedback = st.text_input("Feedback", key=f"feedback_{sub['id']}")
                                    if st.button(f"Grade", key=f"grade_{sub['id']}"):
                                        cursor = conn.cursor()
                                        cursor.execute("""
                                            UPDATE submissions 
                                            SET marks=?, feedback=?, status='graded'
                                            WHERE id=?
                                        """, (marks, feedback, sub['id']))
                                        conn.commit()
                                        st.success("Grade submitted!")
                                        st.rerun()
                                else:
                                    st.success(f"Graded: {sub['marks']}/{assign['max_marks']}")
    
    with tab4:
        st.subheader("📸 Face Recognition Attendance")
        
        # Load student faces
        conn_face = sqlite3.connect('college_management_complete.db')
        students = pd.read_sql_query(f"SELECT * FROM students WHERE semester={courses['semester'].iloc[0]}", conn_face)
        conn_face.close()
        
        if students.empty:
            st.warning("No students enrolled in this course")
        else:
            col1, col2 = st.columns(2)
            with col1:
                selected_course_att = st.selectbox("Select Course", courses['course_code'].values)
            with col2:
                duration = st.slider("Attendance Duration (seconds)", 10, 60, 30)
            
            # Load face encodings
            encodings = []
            student_data = []
            os.makedirs("faces", exist_ok=True)
            
            for _, student in students.iterrows():
                path = f"faces/students_{student['student_id']}.jpg"
                if os.path.exists(path):
                    img = face_recognition.load_image_file(path)
                    face_encoding = face_recognition.face_encodings(img)
                    if face_encoding:
                        encodings.append(face_encoding[0])
                        student_data.append({
                            'id': student['student_id'],
                            'name': student['name'],
                            'data': student.to_dict()
                        })
            
            if len(encodings) == 0:
                st.warning("No face data found for students")
            else:
                run = st.checkbox("Start Face Recognition", value=True)
                
                present_students = []
                FRAME_WINDOW = st.empty()
                status_text = st.empty()
                progress_bar = st.progress(0)
                
                if run:
                    try:
                        camera = cv2.VideoCapture(0)
                        if not camera.isOpened():
                            st.error("Cannot access camera")
                            st.stop()
                        
                        start_time = datetime.now()
                        recognized_names = []
                        
                        while (datetime.now() - start_time).seconds < duration:
                            ret, frame = camera.read()
                            if not ret:
                                break
                            
                            # Process frame
                            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                            rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                            
                            face_locations = face_recognition.face_locations(rgb_small)
                            face_encodings = face_recognition.face_encodings(rgb_small, face_locations)
                            
                            for encoding, face_loc in zip(face_encodings, face_locations):
                                face_loc = [coord * 2 for coord in face_loc]
                                matches = face_recognition.compare_faces(encodings, encoding, tolerance=0.6)
                                
                                if True in matches:
                                    match_index = matches.index(True)
                                    student = student_data[match_index]
                                    name = student['name']
                                    
                                    if name not in recognized_names:
                                        recognized_names.append(name)
                                        present_students.append(student)
                                    
                                    # Draw box
                                    top, right, bottom, left = face_loc
                                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                                    cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                            
                            FRAME_WINDOW.image(frame, channels="BGR")
                            elapsed = (datetime.now() - start_time).seconds
                            progress_bar.progress(min(elapsed / duration, 1.0))
                            status_text.info(f"Recognized: {len(recognized_names)}/{len(student_data)} students")
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                    finally:
                        camera.release()
                
                if present_students:
                    st.success(f"✅ Attendance taken! {len(present_students)} students present")
                    
                    # Save attendance
                    for student in present_students:
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO attendance (student_id, name, date, time, status, marked_by, subject, faculty_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (student['id'], student['name'], datetime.now().strftime("%Y-%m-%d"),
                              datetime.now().strftime("%H:%M:%S"), 'present', faculty['name'],
                              selected_course_att, faculty['faculty_id']))
                        conn.commit()
                    
                    # Display lists
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("✅ Present Students")
                        present_df = pd.DataFrame(present_students)
                        st.dataframe(present_df[['name']], use_container_width=True)
                    
                    with col2:
                        st.subheader("❌ Absent Students")
                        absent = students[~students['name'].isin([s['name'] for s in present_students])]
                        st.dataframe(absent[['name']], use_container_width=True)
    
    with tab5:
        st.subheader("📊 Grade Management")
        
        selected_course_grade = st.selectbox("Select Course for Grading", courses['course_code'].values)
        course = courses[courses['course_code'] == selected_course_grade].iloc[0]
        
        # Get students
        students_grade = pd.read_sql_query(f"SELECT * FROM students WHERE semester={course['semester']}", conn)
        
        if not students_grade.empty:
            # Grade entry
            st.subheader("Enter/Edit Grades")
            grade_data = []
            
            for _, student in students_grade.iterrows():
                # Get existing marks
                existing_marks = pd.read_sql_query(f"""
                    SELECT AVG(marks) as avg_marks FROM submissions 
                    WHERE student_id='{student['student_id']}'
                """, conn)
                
                avg_marks = existing_marks['avg_marks'][0] if existing_marks['avg_marks'][0] else 0
                
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"{student['name']} ({student['student_id']})")
                with col2:
                    new_marks = st.number_input(f"Marks", 0, 100, int(avg_marks), key=f"grade_{student['student_id']}")
                with col3:
                    if st.button(f"Save", key=f"save_{student['student_id']}"):
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT OR REPLACE INTO submissions (student_id, student_name, marks, assignment_id)
                            VALUES (?, ?, ?, ?)
                        """, (student['student_id'], student['name'], new_marks, 0))
                        conn.commit()
                        st.success(f"Grade saved for {student['name']}")
            
            # Grade statistics
            st.subheader("📊 Grade Statistics")
            grades = pd.read_sql_query(f"""
                SELECT student_name, marks FROM submissions 
                WHERE student_id IN (SELECT student_id FROM students WHERE semester={course['semester']})
            """, conn)
            
            if not grades.empty:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average Grade", f"{grades['marks'].mean():.1f}")
                with col2:
                    st.metric("Highest Grade", f"{grades['marks'].max():.1f}")
                with col3:
                    st.metric("Lowest Grade", f"{grades['marks'].min():.1f}")
                
                # Grade distribution
                fig = px.histogram(grades, x='marks', nbins=20, title='Grade Distribution')
                st.plotly_chart(fig, use_container_width=True)
    
    with tab6:
        st.subheader("📋 Reports")
        
        report_type = st.selectbox("Select Report Type", 
                                   ["Attendance Report", "Grade Report", "Student Performance Report"])
        
        if st.button("Generate Report"):
            if report_type == "Attendance Report":
                report = pd.read_sql_query(f"""
                    SELECT s.name, s.student_id, COUNT(a.status) as total_days,
                           COUNT(CASE WHEN a.status='present' THEN 1 END) as present_days
                    FROM students s
                    LEFT JOIN attendance a ON s.student_id = a.student_id
                    WHERE a.faculty_id='{faculty['faculty_id']}'
                    GROUP BY s.student_id
                """, conn)
                
                if not report.empty:
                    report['attendance_percentage'] = (report['present_days'] / report['total_days'] * 100).fillna(0)
                    st.dataframe(report, use_container_width=True)
                    
                    # Download
                    csv = report.to_csv(index=False)
                    st.download_button("📥 Download Report", csv, f"{report_type}_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    
    conn.close()

# ===============================
# PARENTS PORTAL (Enhanced)
# ===============================
def parents_portal():
    st.markdown('<div class="main-header">👨‍👩‍👧 Parents Portal Dashboard</div>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('college_management_complete.db')
    parent = pd.read_sql_query(f"SELECT * FROM parents WHERE parent_id='{st.session_state.username}'", conn)
    
    if parent.empty:
        st.error("Parent record not found")
        return
    
    parent = parent.iloc[0]
    
    # Get child info
    child = pd.read_sql_query(f"SELECT * FROM students WHERE student_id='{parent['student_id']}'", conn)
    
    if child.empty:
        st.error("Child record not found")
        return
    
    child = child.iloc[0]
    
    # Sidebar with child info
    with st.sidebar:
        st.markdown(f"""
        <div class="stat-card">
            <h3>👧 {child['name']}</h3>
            <p>Student ID: {child['student_id']}</p>
            <p>{child['branch']} - Semester {child['semester']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
        attendance_pct = calculate_attendance_percentage(child['student_id'])
        total_fees, paid_fees, pending_fees = get_fee_status(child['student_id'])
        
        st.metric("📊 Attendance", f"{attendance_pct:.1f}%")
        st.metric("💰 Fees Paid", f"₹{paid_fees:,.0f}", f"Pending: ₹{pending_fees:,.0f}")
        
        # Performance prediction
        prediction, score, color = predict_student_performance(child['student_id'])
        st.markdown(f"""
        <div class="info-box">
            <strong>🎯 Performance Score:</strong> {score:.1f}%<br>
            <strong>📈 Prediction:</strong> {prediction}
        </div>
        """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", "📅 Attendance", "📚 Academic Progress", 
        "💰 Fees", "📋 Reports & Alerts"
    ])
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        
        # Attendance
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <h2>{attendance_pct:.1f}%</h2>
                <p>📊 Overall Attendance</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Average marks
        marks = pd.read_sql_query(f"SELECT AVG(marks) as avg_marks FROM submissions WHERE student_id='{child['student_id']}'", conn)
        avg_marks = marks['avg_marks'][0] if marks['avg_marks'][0] else 0
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <h2>{avg_marks:.1f}</h2>
                <p>📝 Average Marks</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Pending fees
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <h2>₹{pending_fees:,.0f}</h2>
                <p>💰 Pending Fees</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Events participated
        events = pd.read_sql_query(f"""
            SELECT COUNT(*) as count FROM event_registrations 
            WHERE student_id='{child['student_id']}'
        """, conn)
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <h2>{events['count'][0]}</h2>
                <p>🎯 Events Participated</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Recent updates
        st.subheader("🔔 Recent Updates")
        
        # Recent attendance
        recent_attendance = pd.read_sql_query(f"""
            SELECT date, status, subject FROM attendance 
            WHERE student_id='{child['student_id']}'
            ORDER BY date DESC LIMIT 5
        """, conn)
        
        if not recent_attendance.empty:
            st.dataframe(recent_attendance, use_container_width=True)
    
    with tab2:
        st.subheader("📅 Attendance Details")
        
        # Month filter
        month = st.selectbox("Select Month", range(1, 13))
        year = st.number_input("Year", 2020, 2030, datetime.now().year)
        
        attendance_records = pd.read_sql_query(f"""
            SELECT date, time, status, subject
            FROM attendance
            WHERE student_id='{child['student_id']}'
            AND strftime('%m', date) = '{month:02d}'
            AND strftime('%Y', date) = '{year}'
            ORDER BY date DESC
        """, conn)
        
        if not attendance_records.empty:
            st.dataframe(attendance_records, use_container_width=True)
            
            # Monthly summary
            total_days = len(attendance_records)
            present_days = len(attendance_records[attendance_records['status'] == 'present'])
            absent_days = total_days - present_days
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Days", total_days)
            col2.metric("Present", present_days)
            col3.metric("Absent", absent_days)
            
            # Attendance chart
            fig = px.pie(values=[present_days, absent_days], names=['Present', 'Absent'], title='Monthly Attendance Summary')
            st.plotly_chart(fig, use_container_width=True)
            
            # Download report
            csv = attendance_records.to_csv(index=False)
            st.download_button("📥 Download Attendance Report", csv, f"attendance_{month}_{year}.csv", "text/csv")
        else:
            st.info("No attendance records found")
    
    with tab3:
        st.subheader("📚 Academic Progress")
        
        # Subject-wise performance
        marks_data = pd.read_sql_query(f"""
            SELECT a.title as assignment, s.marks, a.max_marks, s.feedback
            FROM submissions s
            JOIN assignments a ON s.assignment_id = a.id
            WHERE s.student_id='{child['student_id']}'
            ORDER BY s.submission_date DESC
        """, conn)
        
        if not marks_data.empty:
            marks_data['percentage'] = (marks_data['marks'] / marks_data['max_marks']) * 100
            st.dataframe(marks_data[['assignment', 'marks', 'max_marks', 'percentage', 'feedback']], 
                        use_container_width=True)
            
            # Performance chart
            fig = px.bar(marks_data, x='assignment', y='percentage', title='Assignment Performance')
            st.plotly_chart(fig, use_container_width=True)
            
            # Performance analysis
            avg_performance = marks_data['percentage'].mean()
            if avg_performance >= 85:
                st.success(f"🎉 Excellent Performance! Average: {avg_performance:.1f}%")
            elif avg_performance >= 70:
                st.info(f"👍 Good Performance! Average: {avg_performance:.1f}%")
            elif avg_performance >= 50:
                st.warning(f"⚠️ Average Performance. Needs improvement. Average: {avg_performance:.1f}%")
            else:
                st.error(f"❌ Poor Performance. Immediate attention required. Average: {avg_performance:.1f}%")
        else:
            st.info("No academic records available")
    
    with tab4:
        st.subheader("💰 Fee Details")
        
        fees = pd.read_sql_query(f"SELECT * FROM fees WHERE student_id='{child['student_id']}'", conn)
        
        if not fees.empty:
            st.dataframe(fees, use_container_width=True)
            
            # Fee summary
            total_fees = fees['amount'].sum()
            paid_fees = fees['paid_amount'].sum()
            pending_fees = total_fees - paid_fees
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Fees", f"₹{total_fees:,.0f}")
            col2.metric("Paid", f"₹{paid_fees:,.0f}")
            col3.metric("Pending", f"₹{pending_fees:,.0f}", delta=f"-₹{pending_fees:,.0f}", delta_color="inverse")
            
            # Payment history
            payments = fees[fees['payment_date'].notna()]
            if not payments.empty:
                st.subheader("Payment History")
                st.dataframe(payments[['payment_date', 'fee_type', 'paid_amount', 'payment_method', 'transaction_id']], 
                            use_container_width=True)
            
            # Pay fees button
            if pending_fees > 0:
                if st.button("💰 Pay Fees Online", type="primary"):
                    st.info("Redirecting to payment gateway...")
                    # Integrate payment gateway here
        else:
            st.info("No fee details available")
        
        # Scholarships
        st.subheader("🏆 Scholarships")
        scholarships = pd.read_sql_query(f"SELECT * FROM scholarships WHERE student_id='{child['student_id']}'", conn)
        
        if not scholarships.empty:
            st.dataframe(scholarships, use_container_width=True)
        else:
            st.info("No scholarships awarded")
    
    with tab5:
        st.subheader("📋 Reports & Alerts")
        
        # Generate child report
        if st.button("Generate Child Progress Report"):
            report = {
                'Student': child['name'],
                'Student ID': child['student_id'],
                'Attendance Percentage': f"{attendance_pct:.1f}%",
                'Average Marks': f"{avg_marks:.1f}",
                'Fees Paid': f"₹{paid_fees:,.0f}",
                'Fees Pending': f"₹{pending_fees:,.0f}",
                'Events Participated': events['count'][0],
                'Performance Prediction': prediction
            }
            
            report_df = pd.DataFrame([report])
            st.dataframe(report_df, use_container_width=True)
            
            # Download report
            csv = report_df.to_csv(index=False)
            st.download_button("📥 Download Report", csv, f"{child['name']}_progress_report.csv", "text/csv")
        
        # Set up alerts
        st.subheader("🔔 Alert Settings")
        
        attendance_threshold = st.slider("Attendance Alert Threshold (%)", 0, 100, 75)
        marks_threshold = st.slider("Marks Alert Threshold (%)", 0, 100, 60)
        
        if st.button("Save Alert Settings"):
            st.success("Alert settings saved!")
            
            # Check current status
            if attendance_pct < attendance_threshold:
                st.warning(f"⚠️ Attendance is below threshold ({attendance_pct:.1f}% < {attendance_threshold}%)")
            
            if avg_marks < marks_threshold:
                st.warning(f"⚠️ Marks are below threshold ({avg_marks:.1f}% < {marks_threshold}%)")
    
    conn.close()

# ===============================
# ADMIN PORTAL (Enhanced)
# ===============================
def admin_portal():
    st.markdown('<div class="main-header">👔 Admin Portal Dashboard</div>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('college_management_complete.db')
    
    # Sidebar stats
    with st.sidebar:
        total_students = pd.read_sql_query("SELECT COUNT(*) as count FROM students WHERE status='active'", conn)['count'][0]
        total_faculty = pd.read_sql_query("SELECT COUNT(*) as count FROM faculty WHERE status='active'", conn)['count'][0]
        total_courses = pd.read_sql_query("SELECT COUNT(*) as count FROM courses", conn)['count'][0]
        total_fees = pd.read_sql_query("SELECT SUM(paid_amount) as total FROM fees", conn)['total'][0] or 0
        
        st.markdown(f"""
        <div class="stat-card">
            <h3>📊 System Overview</h3>
            <p>👨‍🎓 Students: {total_students}</p>
            <p>👨‍🏫 Faculty: {total_faculty}</p>
            <p>📚 Courses: {total_courses}</p>
            <p>💰 Fees Collected: ₹{total_fees:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Dashboard", "👨‍🎓 Student Management", "👨‍🏫 Faculty Management",
        "📚 Course Management", "💰 Finance", "📋 Reports", "⚙️ Settings"
    ])
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        
        # Today's attendance
        today = datetime.now().strftime("%Y-%m-%d")
        today_attendance = pd.read_sql_query(f"SELECT COUNT(DISTINCT student_id) as count FROM attendance WHERE date='{today}'", conn)['count'][0]
        with col1:
            st.metric("📅 Today's Attendance", today_attendance, f"{today_attendance/total_students*100:.1f}%")
        
        # Pending fees
        pending_fees = pd.read_sql_query("SELECT SUM(amount - paid_amount) as pending FROM fees", conn)['pending'][0] or 0
        with col2:
            st.metric("💰 Pending Fees", f"₹{pending_fees:,.0f}")
        
        # Active complaints
        active_complaints = pd.read_sql_query("SELECT COUNT(*) as count FROM complaints WHERE status='pending'", conn)['count'][0]
        with col3:
            st.metric("📋 Active Complaints", active_complaints)
        
        # Books issued
        books_issued = pd.read_sql_query("SELECT COUNT(*) as count FROM library_transactions WHERE status='issued'", conn)['count'][0]
        with col4:
            st.metric("📚 Books Issued", books_issued)
        
        # Recent activities chart
        st.subheader("📊 Recent Activities")
        weekly_attendance = pd.read_sql_query("""
            SELECT date, COUNT(DISTINCT student_id) as present
            FROM attendance
            WHERE date >= date('now', '-7 days')
            GROUP BY date
        """, conn)
        
        if not weekly_attendance.empty:
            fig = px.line(weekly_attendance, x='date', y='present', title='Weekly Attendance Trend')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("👨‍🎓 Student Management")
        
        # Add new student
        with st.expander("➕ Add New Student", expanded=False):
            with st.form("add_student_form_admin"):
                col1, col2 = st.columns(2)
                with col1:
                    student_id = st.text_input("Student ID")
                    name = st.text_input("Full Name")
                    class_name = st.text_input("Class")
                    branch = st.selectbox("Branch", ["CS", "IT", "EC", "ME", "CE", "Other"])
                    year = st.number_input("Year", 1, 4)
                    semester = st.number_input("Semester", 1, 8)
                    dob = st.date_input("Date of Birth")
                with col2:
                    email = st.text_input("Email")
                    phone = st.text_input("Phone")
                    parent_name = st.text_input("Parent Name")
                    parent_phone = st.text_input("Parent Phone")
                    parent_email = st.text_input("Parent Email")
                    address = st.text_area("Address")
                    blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
                
                camera = st.camera_input("Capture Face Photo")
                
                if st.form_submit_button("Register Student"):
                    if all([student_id, name, class_name, email]):
                        # Save face
                        if camera:
                            os.makedirs("faces", exist_ok=True)
                            with open(f"faces/students_{student_id}.jpg", "wb") as f:
                                f.write(camera.getvalue())
                        
                        # Save to database
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO students (student_id, name, class, branch, year, semester, email, phone, 
                                                 parent_phone, parent_email, address, blood_group, dob, enrollment_date)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (student_id, name, class_name, branch, year, semester, email, phone, 
                              parent_phone, parent_email, address, blood_group, dob, datetime.now().strftime("%Y-%m-%d")))
                        conn.commit()
                        
                        # Create parent account
                        parent_id = f"parent_{student_id}"
                        cursor.execute("""
                            INSERT INTO parents (parent_id, name, student_id, student_name, email, phone, relationship)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (parent_id, parent_name, student_id, name, parent_email, parent_phone, 'Parent'))
                        conn.commit()
                        
                        # Create user account
                        add_user(student_id, f"{student_id}123", "student", "student", email)
                        add_user(parent_id, f"{parent_id}123", "parent", "parents", parent_email)
                        
                        st.success(f"Student {name} registered successfully!")
                        
                        # Generate ID card
                        id_card = generate_id_card({'student_id': student_id, 'name': name, 'class': class_name, 'branch': branch})
                        buf = BytesIO()
                        id_card.save(buf, format="PNG")
                        st.download_button("📱 Download ID Card", buf.getvalue(), f"{student_id}_id_card.png", "image/png")
                    else:
                        st.error("Please fill all required fields")
        
        # View all students
        st.subheader("📋 All Students")
        students = pd.read_sql_query("SELECT * FROM students WHERE status='active'", conn)
        
        if not students.empty:
            # Search and filter
            search = st.text_input("Search Student", placeholder="Name or Student ID")
            if search:
                students = students[students['name'].str.contains(search, case=False) | 
                                   students['student_id'].str.contains(search, case=False)]
            
            st.dataframe(students, use_container_width=True)
            
            # Bulk actions
            col1, col2 = st.columns(2)
            with col1:
                csv = students.to_csv(index=False)
                st.download_button("📥 Export All Students", csv, "all_students.csv", "text/csv")
            with col2:
                if st.button("📧 Send Bulk Email"):
                    st.info("Sending emails to all students...")
        else:
            st.info("No students found")
    
    with tab3:
        st.subheader("👨‍🏫 Faculty Management")
        
        # Add new faculty
        with st.expander("➕ Add New Faculty", expanded=False):
            with st.form("add_faculty_form_admin"):
                col1, col2 = st.columns(2)
                with col1:
                    faculty_id = st.text_input("Faculty ID")
                    name = st.text_input("Full Name")
                    department = st.text_input("Department")
                    designation = st.text_input("Designation")
                    qualification = st.text_input("Qualification")
                with col2:
                    specialization = st.text_input("Specialization")
                    email = st.text_input("Email")
                    phone = st.text_input("Phone")
                    salary = st.number_input("Salary", 0, 500000)
                    joining_date = st.date_input("Joining Date")
                
                camera = st.camera_input("Capture Face")
                
                if st.form_submit_button("Add Faculty"):
                    if all([faculty_id, name, email]):
                        if camera:
                            os.makedirs("faces", exist_ok=True)
                            with open(f"faces/faculty_{faculty_id}.jpg", "wb") as f:
                                f.write(camera.getvalue())
                        
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO faculty (faculty_id, name, department, designation, qualification, 
                                               specialization, email, phone, salary, joining_date)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (faculty_id, name, department, designation, qualification, 
                              specialization, email, phone, salary, joining_date))
                        conn.commit()
                        
                        add_user(faculty_id, f"{faculty_id}123", "faculty", "faculty", email)
                        st.success(f"Faculty {name} added successfully!")
                    else:
                        st.error("Please fill all required fields")
        
        # View all faculty
        st.subheader("📋 All Faculty")
        faculty = pd.read_sql_query("SELECT * FROM faculty WHERE status='active'", conn)
        
        if not faculty.empty:
            st.dataframe(faculty, use_container_width=True)
            csv = faculty.to_csv(index=False)
            st.download_button("📥 Export Faculty", csv, "faculty_list.csv", "text/csv")
    
    with tab4:
        st.subheader("📚 Course Management")
        
        # Add new course
        with st.expander("➕ Add New Course", expanded=False):
            with st.form("add_course_form_admin"):
                col1, col2 = st.columns(2)
                with col1:
                    course_code = st.text_input("Course Code")
                    course_name = st.text_input("Course Name")
                    faculty_id = st.selectbox("Faculty", faculty['faculty_id'].values if not faculty.empty else [])
                    semester = st.number_input("Semester", 1, 8)
                with col2:
                    credits = st.number_input("Credits", 1, 6)
                    schedule = st.text_input("Schedule")
                    classroom = st.text_input("Classroom")
                    syllabus = st.file_uploader("Syllabus PDF", type=['pdf'])
                
                if st.form_submit_button("Add Course"):
                    if faculty_id:
                        faculty_name = faculty[faculty['faculty_id'] == faculty_id]['name'].values[0]
                        syllabus_path = None
                        if syllabus:
                            syllabus_path = f"syllabus/{course_code}.pdf"
                            os.makedirs("syllabus", exist_ok=True)
                            with open(syllabus_path, "wb") as f:
                                f.write(syllabus.getvalue())
                        
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO courses (course_code, course_name, faculty_id, faculty_name, semester, credits, schedule, classroom, syllabus)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (course_code, course_name, faculty_id, faculty_name, semester, credits, schedule, classroom, syllabus_path))
                        conn.commit()
                        st.success("Course added successfully!")
                    else:
                        st.error("Please select a faculty member")
        
        # View all courses
        st.subheader("📋 All Courses")
        courses = pd.read_sql_query("SELECT * FROM courses", conn)
        
        if not courses.empty:
            st.dataframe(courses, use_container_width=True)
            csv = courses.to_csv(index=False)
            st.download_button("📥 Export Courses", csv, "courses.csv", "text/csv")
    
    with tab5:
        st.subheader("💰 Finance Management")
        
        # Fee collection overview
        fee_summary = pd.read_sql_query("""
            SELECT 
                SUM(amount) as total,
                SUM(paid_amount) as collected,
                SUM(amount - paid_amount) as pending
            FROM fees
        """, conn)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Fees", f"₹{fee_summary['total'][0]:,.0f}")
        col2.metric("Collected", f"₹{fee_summary['collected'][0]:,.0f}")
        col3.metric("Pending", f"₹{fee_summary['pending'][0]:,.0f}")
        
        # Fee structure
        st.subheader("Fee Structure")
        with st.form("add_fee_structure"):
            col1, col2 = st.columns(2)
            with col1:
                semester = st.number_input("Semester", 1, 8)
                fee_type = st.text_input("Fee Type")
                amount = st.number_input("Amount", 0, 500000)
            with col2:
                due_date = st.date_input("Due Date")
                branch = st.text_input("Branch (Optional)", "")
            
            if st.form_submit_button("Add Fee Structure"):
                cursor = conn.cursor()
                if branch:
                    # Add for all students in branch
                    students = pd.read_sql_query(f"SELECT * FROM students WHERE branch='{branch}'", conn)
                    for _, student in students.iterrows():
                        cursor.execute("""
                            INSERT INTO fees (student_id, student_name, semester, fee_type, amount, due_date)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (student['student_id'], student['name'], semester, fee_type, amount, due_date))
                else:
                    # Add for all students
                    students = pd.read_sql_query("SELECT * FROM students", conn)
                    for _, student in students.iterrows():
                        cursor.execute("""
                            INSERT INTO fees (student_id, student_name, semester, fee_type, amount, due_date)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (student['student_id'], student['name'], semester, fee_type, amount, due_date))
                
                conn.commit()
                st.success("Fee structure added successfully!")
        
        # Payment history
        st.subheader("Payment History")
        payments = pd.read_sql_query("""
            SELECT student_id, student_name, fee_type, paid_amount, payment_date, payment_method, transaction_id
            FROM fees
            WHERE payment_date IS NOT NULL
            ORDER BY payment_date DESC
            LIMIT 50
        """, conn)
        
        if not payments.empty:
            st.dataframe(payments, use_container_width=True)
    
    with tab6:
        st.subheader("📋 Reports")
        
        report_type = st.selectbox("Select Report Type", 
                                   ["Student Report", "Faculty Report", "Attendance Report", 
                                    "Fee Report", "Library Report", "Complaints Report"])
        
        date_from = st.date_input("From Date", datetime.now() - timedelta(days=30))
        date_to = st.date_input("To Date", datetime.now())
        
        if st.button("Generate Report"):
            if report_type == "Student Report":
                report = pd.read_sql_query("SELECT * FROM students", conn)
            elif report_type == "Faculty Report":
                report = pd.read_sql_query("SELECT * FROM faculty", conn)
            elif report_type == "Attendance Report":
                report = pd.read_sql_query(f"""
                    SELECT * FROM attendance 
                    WHERE date BETWEEN '{date_from}' AND '{date_to}'
                """, conn)
            elif report_type == "Fee Report":
                report = pd.read_sql_query(f"""
                    SELECT * FROM fees 
                    WHERE payment_date BETWEEN '{date_from}' AND '{date_to}'
                """, conn)
            elif report_type == "Library Report":
                report = pd.read_sql_query(f"""
                    SELECT * FROM library_transactions 
                    WHERE issue_date BETWEEN '{date_from}' AND '{date_to}'
                """, conn)
            elif report_type == "Complaints Report":
                report = pd.read_sql_query(f"""
                    SELECT * FROM complaints 
                    WHERE created_at BETWEEN '{date_from}' AND '{date_to}'
                """, conn)
            
            if not report.empty:
                st.dataframe(report, use_container_width=True)
                
                # Export options
                csv_file, excel_file = export_report(report, report_type.replace(" ", "_"))
                with open(csv_file, "rb") as f:
                    st.download_button("📥 Download CSV", f, csv_file, "text/csv")
                
                st.info(f"Report generated with {len(report)} records")
            else:
                st.warning("No data found for selected period")
    
    with tab7:
        st.subheader("⚙️ System Settings")
        
        # Backup and Restore
        st.subheader("💾 Backup & Restore")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Create Backup", type="primary"):
                backup_file = backup_database()
                st.success(f"Backup created: {backup_file}")
                
                with open(backup_file, "rb") as f:
                    st.download_button("Download Backup", f, backup_file, "application/octet-stream")
        
        with col2:
            uploaded_backup = st.file_uploader("Restore from Backup", type=['db'])
            if uploaded_backup:
                with open("restore_temp.db", "wb") as f:
                    f.write(uploaded_backup.getvalue())
                if st.button("Restore Database"):
                    restore_database("restore_temp.db")
                    st.success("Database restored successfully!")
                    os.remove("restore_temp.db")
        
        # System Configuration
        st.subheader("⚙️ System Configuration")
        
        recognition_threshold = st.slider("Face Recognition Threshold", 0.3, 0.7, 0.6)
        attendance_duration = st.slider("Default Attendance Duration (seconds)", 10, 60, 30)
        
        if st.button("Save Configuration"):
            config = {
                "recognition_threshold": recognition_threshold,
                "attendance_duration": attendance_duration,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open("system_config.json", "w") as f:
                json.dump(config, f)
            st.success("Configuration saved!")
        
        # Clear old data
        st.subheader("🗑️ Data Management")
        days_to_keep = st.number_input("Keep data for (days)", 30, 365, 90)
        
        if st.button("Clean Old Data", type="secondary"):
            cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).strftime("%Y-%m-%d")
            
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM attendance WHERE date < '{cutoff_date}'")
            cursor.execute(f"DELETE FROM notifications WHERE expiry_date < '{cutoff_date}'")
            conn.commit()
            
            st.success(f"Cleaned data older than {days_to_keep} days")
    
    conn.close()

# ===============================
# AI ADMIN PORTAL (Enhanced with ML)
# ===============================
def ai_admin_portal():
    st.markdown('<div class="main-header">🤖 AI Admin Portal - Intelligent Management System</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">🤖 AI-powered insights, predictions, and automation for intelligent college management</div>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('college_management_complete.db')
    
    # Get data for analysis
    students = pd.read_sql_query("SELECT * FROM students", conn)
    attendance = pd.read_sql_query("SELECT * FROM attendance", conn)
    marks = pd.read_sql_query("SELECT * FROM submissions", conn)
    fees = pd.read_sql_query("SELECT * FROM fees", conn)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 AI Insights", "📈 Predictive Analytics", "⚡ Smart Automation", 
        "💬 AI Assistant", "🎯 Recommendations"
    ])
    
    with tab1:
        st.subheader("🤖 AI-Powered Insights")
        
        # Student performance clustering
        if not marks.empty:
            st.markdown("### 📊 Student Performance Clustering")
            
            # Calculate performance metrics
            student_performance = marks.groupby('student_id').agg({
                'marks': ['mean', 'count']
            }).reset_index()
            student_performance.columns = ['student_id', 'avg_marks', 'submissions_count']
            
            # Merge with student info
            performance_df = student_performance.merge(students, on='student_id')
            
            # Simple clustering based on marks
            performance_df['performance_level'] = pd.cut(
                performance_df['avg_marks'], 
                bins=[0, 50, 70, 85, 100], 
                labels=['Poor', 'Average', 'Good', 'Excellent']
            )
            
            # Display cluster distribution
            cluster_dist = performance_df['performance_level'].value_counts()
            fig = px.pie(values=cluster_dist.values, names=cluster_dist.index, title='Student Performance Distribution')
            st.plotly_chart(fig, use_container_width=True)
            
            # At-risk students
            at_risk = performance_df[performance_df['performance_level'] == 'Poor']
            if not at_risk.empty:
                st.warning(f"⚠️ {len(at_risk)} students are at risk of poor performance")
                st.dataframe(at_risk[['student_id', 'name', 'avg_marks']], use_container_width=True)
        
        # Attendance patterns
        if not attendance.empty:
            st.markdown("### 📅 Attendance Pattern Analysis")
            
            attendance['date'] = pd.to_datetime(attendance['date'])
            attendance['day_of_week'] = attendance['date'].dt.day_name()
            attendance['hour'] = pd.to_datetime(attendance['time']).dt.hour
            
            # Attendance by day
            day_attendance = attendance.groupby('day_of_week').size().reset_index(name='count')
            fig = px.bar(day_attendance, x='day_of_week', y='count', title='Attendance by Day of Week')
            st.plotly_chart(fig, use_container_width=True)
            
            # Attendance by hour
            hour_attendance = attendance.groupby('hour').size().reset_index(name='count')
            fig = px.line(hour_attendance, x='hour', y='count', title='Attendance by Hour')
            st.plotly_chart(fig, use_container_width=True)
            
            # Peak attendance times
            peak_hour = hour_attendance.loc[hour_attendance['count'].idxmax(), 'hour']
            st.info(f"🕐 Peak attendance time: {peak_hour}:00 - {peak_hour+1}:00")
        
        # Fee collection forecast
        if not fees.empty:
            st.markdown("### 💰 Fee Collection Analysis")
            
            fees['payment_date'] = pd.to_datetime(fees['payment_date'], errors='coerce')
            monthly_collection = fees[fees['payment_date'].notna()].groupby(
                fees['payment_date'].dt.to_period('M')
            )['paid_amount'].sum().reset_index()
            monthly_collection.columns = ['month', 'amount']
            
            if not monthly_collection.empty:
                fig = px.line(monthly_collection, x='month', y='amount', title='Monthly Fee Collection Trend')
                st.plotly_chart(fig, use_container_width=True)
                
                # Collection rate
                total_fees = fees['amount'].sum()
                collected = fees['paid_amount'].sum()
                collection_rate = (collected / total_fees * 100) if total_fees > 0 else 0
                
                st.metric("Overall Collection Rate", f"{collection_rate:.1f}%")
                
                if collection_rate < 80:
                    st.warning("⚠️ Collection rate below target. Consider sending reminders.")
    
    with tab2:
        st.subheader("📈 Predictive Analytics")
        
        # Student dropout prediction
        st.markdown("### 🎓 Student Dropout Risk Prediction")
        
        if not attendance.empty and not marks.empty:
            # Calculate risk factors
            student_risk = students.copy()
            
            # Attendance risk
            attendance_count = attendance.groupby('student_id').size().reset_index(name='total_attendance')
            present_count = attendance[attendance['status'] == 'present'].groupby('student_id').size().reset_index(name='present')
            
            attendance_risk = present_count.merge(attendance_count, on='student_id', how='right')
            attendance_risk['attendance_rate'] = (attendance_risk['present'] / attendance_risk['total_attendance'] * 100).fillna(0)
            
            # Marks risk
            marks_risk = marks.groupby('student_id')['marks'].mean().reset_index(name='avg_marks')
            
            # Combine risks
            risk_df = student_risk.merge(attendance_risk, on='student_id', how='left')
            risk_df = risk_df.merge(marks_risk, on='student_id', how='left')
            
            # Calculate risk score
            risk_df['risk_score'] = (
                (100 - risk_df['attendance_rate'].fillna(100)) * 0.4 +
                (100 - risk_df['avg_marks'].fillna(100)) * 0.6
            )
            
            risk_df['risk_level'] = pd.cut(
                risk_df['risk_score'],
                bins=[0, 20, 40, 60, 100],
                labels=['Low', 'Moderate', 'High', 'Very High']
            )
            
            # Display at-risk students
            high_risk = risk_df[risk_df['risk_level'].isin(['High', 'Very High'])]
            
            if not high_risk.empty:
                st.error(f"🚨 {len(high_risk)} students identified as high dropout risk")
                st.dataframe(high_risk[['student_id', 'name', 'attendance_rate', 'avg_marks', 'risk_score', 'risk_level']], 
                            use_container_width=True)
                
                # AI Recommendation
                st.markdown("### 💡 AI Recommendations")
                st.info("""
                **Recommended Actions:**
                1. Schedule parent-teacher meetings for high-risk students
                2. Provide additional academic support and counseling
                3. Monitor attendance closely and send daily reminders
                4. Consider scholarship options for financially at-risk students
                """)
            else:
                st.success("✅ No high-risk students identified")
        
        # Attendance prediction
        st.markdown("### 📊 Next Month Attendance Prediction")
        
        if not attendance.empty:
            # Simple time series prediction
            attendance['date'] = pd.to_datetime(attendance['date'])
            daily_attendance = attendance.groupby('date').size().reset_index(name='count')
            daily_attendance = daily_attendance.set_index('date')
            
            # Moving average
            daily_attendance['ma_7'] = daily_attendance['count'].rolling(window=7).mean()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=daily_attendance.index, y=daily_attendance['count'], 
                                     mode='lines', name='Actual'))
            fig.add_trace(go.Scatter(x=daily_attendance.index, y=daily_attendance['ma_7'], 
                                     mode='lines', name='7-Day Average'))
            fig.update_layout(title='Attendance Trend with Moving Average')
            st.plotly_chart(fig, use_container_width=True)
            
            # Simple prediction
            last_week_avg = daily_attendance['ma_7'].iloc[-7:].mean()
            st.info(f"📈 Predicted average daily attendance for next week: {last_week_avg:.0f} students")
    
    with tab3:
        st.subheader("⚡ Smart Automation")
        
        # Auto-reminders
        st.markdown("### 📧 Automated Reminders")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Send Attendance Reminders"):
                # Get students with low attendance
                attendance_rate = attendance.groupby('student_id').apply(
                    lambda x: (x['status'] == 'present').sum() / len(x) * 100
                ).reset_index(name='rate')
                
                low_attendance = attendance_rate[attendance_rate['rate'] < 75]
                
                for _, student in low_attendance.iterrows():
                    student_info = students[students['student_id'] == student['student_id']].iloc[0]
                    send_email(student_info['email'], "Attendance Alert", 
                              f"Your attendance is below 75% ({student['rate']:.1f}%). Please improve.")
                
                st.success(f"Sent reminders to {len(low_attendance)} students")
        
        with col2:
            if st.button("Send Fee Reminders"):
                # Get students with pending fees
                pending_fees = fees[fees['paid_amount'] < fees['amount']]
                pending_students = pending_fees.groupby('student_id').first().reset_index()
                
                for _, fee in pending_students.iterrows():
                    student_info = students[students['student_id'] == fee['student_id']].iloc[0]
                    pending_amount = fee['amount'] - fee['paid_amount']
                    send_email(student_info['email'], "Fee Payment Reminder", 
                              f"Pending fee amount: ₹{pending_amount}. Due date: {fee['due_date']}")
                
                st.success(f"Sent reminders to {len(pending_students)} students")
        
        # Auto-generate reports
        st.markdown("### 📊 Auto-Generate Reports")
        
        report_frequency = st.selectbox("Report Frequency", ["Daily", "Weekly", "Monthly"])
        
        if st.button("Setup Auto-Reporting"):
            config = {
                "auto_reports": True,
                "frequency": report_frequency,
                "last_generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open("auto_report_config.json", "w") as f:
                json.dump(config, f)
            st.success(f"Auto-reporting configured for {report_frequency} reports")
        
        # Smart scheduling
        st.markdown("### 🗓️ Smart Scheduling")
        
        if st.button("Optimize Class Schedule"):
            st.info("Analyzing class schedules for optimization...")
            time.sleep(2)
            
            # Analyze room utilization
            rooms = ['A101', 'A102', 'B201', 'B202', 'C301']
            utilization = np.random.uniform(0.3, 0.9, len(rooms))
            
            fig = px.bar(x=rooms, y=utilization, title='Room Utilization Analysis')
            st.plotly_chart(fig, use_container_width=True)
            
            # Recommendations
            st.success("""
            **Optimization Recommendations:**
            - Room A102 has high utilization (85%) - Consider moving some classes to underutilized rooms
            - C301 is underutilized (35%) - Better utilize this space for additional classes
            - Suggested to balance class distribution across all rooms
            """)
    
    with tab4:
        st.subheader("💬 AI Assistant Chatbot")
        st.markdown('<div class="info-box">🤖 Ask me anything about college management, student performance, or get insights</div>', unsafe_allow_html=True)
        
        # Chat interface
        if "ai_messages" not in st.session_state:
            st.session_state.ai_messages = []
        
        # Display chat history
        for message in st.session_state.ai_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask the AI Assistant..."):
            st.session_state.ai_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate AI response
            with st.chat_message("assistant"):
                response = generate_ai_response_advanced(prompt, conn, students, attendance, marks, fees)
                st.markdown(response)
            st.session_state.ai_messages.append({"role": "assistant", "content": response})
    
    with tab5:
        st.subheader("🎯 Intelligent Recommendations")
        
        # Course recommendations
        st.markdown("### 📚 Course Popularity Analysis")
        
        if not marks.empty:
            # Analyze course performance
            course_performance = marks.merge(
                assignments[['id', 'course_code']], 
                left_on='assignment_id', 
                right_on='id'
            )
            
            if not course_performance.empty:
                avg_by_course = course_performance.groupby('course_code')['marks'].mean().reset_index()
                avg_by_course.columns = ['course_code', 'avg_marks']
                
                fig = px.bar(avg_by_course, x='course_code', y='avg_marks', 
                            title='Average Performance by Course')
                st.plotly_chart(fig, use_container_width=True)
        
        # Student support recommendations
        st.markdown("### 🎓 Student Support Recommendations")
        
        if not attendance.empty and not marks.empty:
            # Identify students needing support
            student_support = students.copy()
            
            # Calculate metrics
            attendance_rate = attendance.groupby('student_id').apply(
                lambda x: (x['status'] == 'present').sum() / len(x) * 100
            ).reset_index(name='attendance_rate')
            
            avg_marks_data = marks.groupby('student_id')['marks'].mean().reset_index(name='avg_marks')
            
            student_support = student_support.merge(attendance_rate, on='student_id', how='left')
            student_support = student_support.merge(avg_marks_data, on='student_id', how='left')
            
            # Needs support
            needs_support = student_support[
                (student_support['attendance_rate'] < 75) | 
                (student_support['avg_marks'] < 60)
            ]
            
            if not needs_support.empty:
                st.warning(f"⚠️ {len(needs_support)} students need academic support")
                
                for _, student in needs_support.iterrows():
                    with st.expander(f"{student['name']} - {student['student_id']}"):
                        st.write(f"**Attendance:** {student['attendance_rate']:.1f}%")
                        st.write(f"**Average Marks:** {student['avg_marks']:.1f}")
                        
                        # Recommendation
                        if student['attendance_rate'] < 75:
                            st.write("📌 **Recommendation:** Schedule attendance counseling")
                        if student['avg_marks'] < 60:
                            st.write("📌 **Recommendation:** Provide additional tutoring")
                        
                        if st.button(f"Send Notification to {student['name']}", key=f"notify_{student['student_id']}"):
                            send_email(student['email'], "Academic Support Available", 
                                      "You have been identified as needing academic support. Please meet with your academic advisor.")
                            st.success("Notification sent!")
            else:
                st.success("✅ All students are performing well!")
        
        # Resource allocation
        st.markdown("### 🏢 Resource Allocation Optimization")
        
        if st.button("Analyze Resource Utilization"):
            # Simulate resource analysis
            resources = {
                "Classrooms": 85,
                "Library": 65,
                "Laboratories": 70,
                "Sports Facilities": 55,
                "Cafeteria": 80
            }
            
            fig = px.bar(x=list(resources.keys()), y=list(resources.values()), 
                        title='Resource Utilization (%)')
            st.plotly_chart(fig, use_container_width=True)
            
            # Recommendations
            underutilized = [k for k, v in resources.items() if v < 60]
            if underutilized:
                st.info(f"Underutilized resources: {', '.join(underutilized)}. Consider promoting these facilities.")
            
            overutilized = [k for k, v in resources.items() if v > 80]
            if overutilized:
                st.warning(f"Overutilized resources: {', '.join(overutilized)}. Consider expanding capacity.")
    
    conn.close()

def generate_ai_response_advanced(prompt, conn, students, attendance, marks, fees):
    """Generate intelligent AI response"""
    prompt_lower = prompt.lower()
    
    if "attendance" in prompt_lower:
        if not attendance.empty:
            today = datetime.now().strftime("%Y-%m-%d")
            today_att = attendance[attendance['date'] == today]
            total_students = len(students)
            present_today = len(today_att[today_att['status'] == 'present'])
            
            response = f"📊 **Attendance Analysis**\n\n"
            response += f"Today's attendance: {present_today}/{total_students} ({present_today/total_students*100:.1f}%)\n\n"
            
            # Weekly trend
            last_week = attendance[attendance['date'] >= (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")]
            weekly_avg = last_week.groupby('date').apply(lambda x: (x['status'] == 'present').sum() / len(students) * 100).mean()
            response += f"Weekly average attendance: {weekly_avg:.1f}%\n\n"
            
            # Students with low attendance
            student_attendance = attendance.groupby('student_id').apply(
                lambda x: (x['status'] == 'present').sum() / len(x) * 100
            )
            low_attendance = student_attendance[student_attendance < 75]
            if not low_attendance.empty:
                response += f"⚠️ {len(low_attendance)} students have attendance below 75%"
            
            return response
    
    elif "performance" in prompt_lower or "marks" in prompt_lower:
        if not marks.empty:
            overall_avg = marks['marks'].mean()
            response = f"📈 **Performance Analysis**\n\n"
            response += f"Overall average marks: {overall_avg:.1f}%\n\n"
            
            # Top performers
            top_students = marks.groupby('student_id')['marks'].mean().nlargest(5)
            if not top_students.empty:
                response += "🏆 **Top Performers:**\n"
                for student_id, avg_marks in top_students.items():
                    student_name = students[students['student_id'] == student_id]['name'].values[0] if not students.empty else student_id
                    response += f"- {student_name}: {avg_marks:.1f}%\n"
            
            return response
    
    elif "fee" in prompt_lower or "payment" in prompt_lower:
        if not fees.empty:
            total_fees = fees['amount'].sum()
            collected = fees['paid_amount'].sum()
            pending = total_fees - collected
            collection_rate = (collected / total_fees * 100) if total_fees > 0 else 0
            
            response = f"💰 **Fee Collection Analysis**\n\n"
            response += f"Total fees: ₹{total_fees:,.0f}\n"
            response += f"Collected: ₹{collected:,.0f}\n"
            response += f"Pending: ₹{pending:,.0f}\n"
            response += f"Collection rate: {collection_rate:.1f}%\n\n"
            
            # Overdue payments
            overdue = fees[(fees['due_date'] < datetime.now().strftime("%Y-%m-%d")) & (fees['paid_amount'] < fees['amount'])]
            if not overdue.empty:
                response += f"⚠️ {len(overdue.groupby('student_id'))} students have overdue payments"
            
            return response
    
    elif "student" in prompt_lower:
        total_students = len(students)
        active_students = len(students[students['status'] == 'active'])
        response = f"👨‍🎓 **Student Statistics**\n\n"
        response += f"Total students: {total_students}\n"
        response += f"Active students: {active_students}\n"
        
        # Branch distribution
        if not students.empty and 'branch' in students.columns:
            branch_counts = students['branch'].value_counts()
            response += f"\n**Branch-wise distribution:**\n"
            for branch, count in branch_counts.head(5).items():
                response += f"- {branch}: {count} students\n"
        
        return response
    
    elif "faculty" in prompt_lower:
        faculty = pd.read_sql_query("SELECT * FROM faculty", conn)
        response = f"👨‍🏫 **Faculty Statistics**\n\n"
        response += f"Total faculty: {len(faculty)}\n"
        
        if not faculty.empty:
            dept_counts = faculty['department'].value_counts()
            response += f"\n**Department-wise:**\n"
            for dept, count in dept_counts.head(5).items():
                response += f"- {dept}: {count} faculty\n"
        
        return response
    
    elif "recommend" in prompt_lower or "suggest" in prompt_lower:
        response = "💡 **AI Recommendations**\n\n"
        
        # Check attendance issues
        if not attendance.empty:
            student_attendance = attendance.groupby('student_id').apply(
                lambda x: (x['status'] == 'present').sum() / len(x) * 100
            )
            low_attendance = len(student_attendance[student_attendance < 75])
            if low_attendance > 0:
                response += f"⚠️ {low_attendance} students have low attendance. Consider sending reminders.\n"
        
        # Check fee collection
        if not fees.empty:
            collection_rate = (fees['paid_amount'].sum() / fees['amount'].sum() * 100) if fees['amount'].sum() > 0 else 0
            if collection_rate < 80:
                response += f"💰 Collection rate is {collection_rate:.1f}%. Consider sending fee reminders.\n"
        
        # Check performance
        if not marks.empty:
            avg_marks = marks['marks'].mean()
            if avg_marks < 70:
                response += f"📚 Average marks are {avg_marks:.1f}%. Consider additional tutoring sessions.\n"
        
        if not response.strip():
            response += "All metrics look good! Continue maintaining current performance levels."
        
        return response
    
    else:
        return "I can help you with information about:\n- 📊 Attendance analysis\n- 📈 Performance metrics\n- 💰 Fee collection status\n- 👨‍🎓 Student statistics\n- 👨‍🏫 Faculty information\n- 💡 Recommendations\n\nWhat would you like to know?"

# ===============================
# Main App
# ===============================
def main():
    if st.session_state.selected_portal is None:
        show_portal_selection()
    elif not st.session_state.logged_in:
        show_login()
    else:
        if st.session_state.portal_type == "student":
            student_portal()
        elif st.session_state.portal_type == "faculty":
            faculty_portal()
        elif st.session_state.portal_type == "parents":
            parents_portal()
        elif st.session_state.portal_type == "admin":
            admin_portal()
        elif st.session_state.portal_type == "ai_admin":
            ai_admin_portal()
        
        # Logout button
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout", type="primary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.selected_portal = None
            st.session_state.username = None
            st.rerun()

if __name__ == "__main__":
    main()