import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Student Dropout Predictor",
    page_icon="🎓",
    layout="wide"
)

# Database setup
DATABASE_FILE = 'students.db'

def initialize_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        school_satisfaction REAL,
        attendance_rate REAL,
        failed_courses INTEGER,
        commute_time INTEGER,
        disciplinary_incidents INTEGER,
        homework_completion REAL,
        family_income TEXT,
        promotion_status TEXT,
        prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    conn.commit()
    conn.close()

def predict_promotion(satisfaction, attendance, failed_courses, commute, disciplinary, homework, income):
    """Simple rule-based prediction"""
    if (satisfaction > 3 and attendance > 70 and failed_courses <= 2 and
        commute <= 40 and disciplinary <= 2 and homework > 80):
        return "Promoted"
    else:
        return "At Risk of Dropout"

def insert_student_data(student_id, satisfaction, attendance, failed_courses, 
                       commute, disciplinary, homework, family_income, promotion_status):
    """Insert student data into database"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO students (
                student_id, school_satisfaction, attendance_rate, failed_courses, 
                commute_time, disciplinary_incidents, homework_completion, 
                family_income, promotion_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (student_id, satisfaction, attendance, failed_courses, commute,
              disciplinary, homework, family_income, promotion_status))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Database error: {e}")
        return False

def get_all_students():
    """Retrieve all students from database"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        df = pd.read_sql_query("SELECT * FROM students ORDER BY prediction_date DESC", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error retrieving data: {e}")
        return pd.DataFrame()

def delete_student(student_id):
    """Delete student record"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error deleting record: {e}")
        return False

# Initialize database
initialize_database()

# Sidebar navigation
st.sidebar.title("🎓 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Predict Dropout", "View Database", "Analytics", "About"])

# Main content based on page selection
if page == "Home":
    st.title("🎓 Student Dropout Prediction System")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Students", len(get_all_students()))
    
    with col2:
        df = get_all_students()
        if not df.empty:
            at_risk = len(df[df['promotion_status'] == 'At Risk of Dropout'])
            st.metric("At Risk Students", at_risk)
    
    with col3:
        if not df.empty:
            promoted = len(df[df['promotion_status'] == 'Promoted'])
            st.metric("Promoted Students", promoted)
    
    st.markdown("---")
    st.subheader("📊 About This System")
    st.write("""
    This system helps predict student dropout risk based on multiple factors:
    - School satisfaction levels
    - Attendance rates
    - Academic performance (failed courses)
    - Commute time
    - Disciplinary incidents
    - Homework completion rates
    - Family income levels
    
    Use the sidebar to navigate between different features.
    """)

elif page == "Predict Dropout":
    st.title("🔮 Student Dropout Prediction")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        student_id = st.number_input("Student ID", min_value=1, step=1, value=1)
        satisfaction = st.slider("School Satisfaction (1-5)", 1.0, 5.0, 3.0, 0.1)
        attendance = st.slider("Attendance Rate (%)", 0.0, 100.0, 75.0, 1.0)
        failed_courses = st.number_input("Failed Courses", min_value=0, max_value=10, value=0)
    
    with col2:
        commute = st.slider("Commute Time (minutes)", 1, 120, 30, 1)
        disciplinary = st.number_input("Disciplinary Incidents", min_value=0, max_value=10, value=0)
        homework = st.slider("Homework Completion (%)", 0.0, 100.0, 85.0, 1.0)
        family_income = st.selectbox("Family Income Level", ["low", "medium", "high"])
    
    st.markdown("---")
    
    if st.button("🎯 Predict & Save", type="primary", use_container_width=True):
        # Make prediction
        promotion_status = predict_promotion(
            satisfaction, attendance, failed_courses, 
            commute, disciplinary, homework, family_income
        )
        
        # Insert into database
        if insert_student_data(student_id, satisfaction, attendance, failed_courses,
                              commute, disciplinary, homework, family_income, promotion_status):
            
            # Display result
            if promotion_status == "Promoted":
                st.success(f"✅ Student {student_id} is predicted to be **{promotion_status}**")
            else:
                st.error(f"⚠️ Student {student_id} is **{promotion_status}**")
            
            # Show factors
            st.subheader("📈 Contributing Factors")
            factors = {
                "School Satisfaction": f"{satisfaction}/5 {'✅' if satisfaction > 3 else '❌'}",
                "Attendance Rate": f"{attendance}% {'✅' if attendance > 70 else '❌'}",
                "Failed Courses": f"{failed_courses} {'✅' if failed_courses <= 2 else '❌'}",
                "Commute Time": f"{commute} min {'✅' if commute <= 40 else '❌'}",
                "Disciplinary Cases": f"{disciplinary} {'✅' if disciplinary <= 2 else '❌'}",
                "Homework Completion": f"{homework}% {'✅' if homework > 80 else '❌'}"
            }
            
            for factor, value in factors.items():
                st.write(f"**{factor}:** {value}")

elif page == "View Database":
    st.title("📁 Student Database")
    st.markdown("---")
    
    # Get all students
    df = get_all_students()
    
    if df.empty:
        st.info("No student records found. Add predictions to see data here.")
    else:
        # Display statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            avg_attendance = df['attendance_rate'].mean()
            st.metric("Avg Attendance", f"{avg_attendance:.1f}%")
        with col3:
            at_risk = len(df[df['promotion_status'] == 'At Risk of Dropout'])
            st.metric("At Risk", at_risk)
        with col4:
            avg_satisfaction = df['school_satisfaction'].mean()
            st.metric("Avg Satisfaction", f"{avg_satisfaction:.1f}/5")
        
        st.markdown("---")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=df['promotion_status'].unique(),
                default=df['promotion_status'].unique()
            )
        with col2:
            income_filter = st.multiselect(
                "Filter by Income",
                options=df['family_income'].unique(),
                default=df['family_income'].unique()
            )
        
        # Apply filters
        filtered_df = df[
            (df['promotion_status'].isin(status_filter)) &
            (df['family_income'].isin(income_filter))
        ]
        
        # Display dataframe
        st.dataframe(filtered_df, use_container_width=True)
        
        # Delete student option
        st.markdown("---")
        st.subheader("🗑️ Delete Student Record")
        col1, col2 = st.columns([3, 1])
        with col1:
            delete_id = st.number_input("Enter Student ID to Delete", min_value=1, step=1)
        with col2:
            if st.button("Delete", type="secondary"):
                if delete_student(delete_id):
                    st.success(f"Student {delete_id} deleted successfully!")
                    st.rerun()

elif page == "Analytics":
    st.title("📊 Analytics Dashboard")
    st.markdown("---")
    
    df = get_all_students()
    
    if df.empty:
        st.info("No data available for analytics. Add student predictions first.")
    else:
        # Status distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Promotion Status Distribution")
            status_counts = df['promotion_status'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index,
                        color_discrete_sequence=['#00509e', '#d9534f'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Income Level Distribution")
            income_counts = df['family_income'].value_counts()
            fig = px.bar(x=income_counts.index, y=income_counts.values,
                        labels={'x': 'Income Level', 'y': 'Count'},
                        color=income_counts.index)
            st.plotly_chart(fig, use_container_width=True)
        
        # Correlation analysis
        st.subheader("📈 Factor Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            # Attendance vs Satisfaction
            fig = px.scatter(df, x='attendance_rate', y='school_satisfaction',
                           color='promotion_status',
                           labels={'attendance_rate': 'Attendance Rate (%)',
                                  'school_satisfaction': 'School Satisfaction'},
                           title='Attendance vs Satisfaction')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Failed courses distribution
            fig = px.histogram(df, x='failed_courses', color='promotion_status',
                             labels={'failed_courses': 'Number of Failed Courses'},
                             title='Failed Courses Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        # Average metrics by status
        st.subheader("📊 Average Metrics by Status")
        avg_by_status = df.groupby('promotion_status').agg({
            'school_satisfaction': 'mean',
            'attendance_rate': 'mean',
            'failed_courses': 'mean',
            'homework_completion': 'mean'
        }).round(2)
        st.dataframe(avg_by_status, use_container_width=True)

else:  # About page
    st.title("ℹ️ About This Project")
    st.markdown("---")
    
    st.subheader("🎯 Project Overview")
    st.write("""
    The Student Dropout Prediction System uses machine learning and statistical analysis 
    to identify students at risk of dropping out. This early warning system helps educators 
    intervene proactively.
    """)
    
    st.subheader("🔍 Prediction Criteria")
    st.write("""
    A student is considered **Promoted** if they meet ALL of the following criteria:
    - School Satisfaction > 3 (out of 5)
    - Attendance Rate > 70%
    - Failed Courses ≤ 2
    - Commute Time ≤ 40 minutes
    - Disciplinary Incidents ≤ 2
    - Homework Completion > 80%
    """)
    
    st.subheader("🛠️ Technology Stack")
    st.write("""
    - **Frontend:** Streamlit
    - **Database:** SQLite
    - **Machine Learning:** Scikit-learn
    - **Visualization:** Plotly
    - **Deployment:** Streamlit Cloud
    """)
    
    st.subheader("👥 Credits")
    st.write("**Managed By The Whiskers**")
    st.write("Powered by Python & Streamlit")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("🎓 Student Dropout Predictor v1.0")
st.sidebar.write("Managed By The Whiskers")
