# 🎓 Student Dropout Prediction System

A machine learning-powered web application that predicts student dropout risk based on multiple academic and demographic factors.

## 🌟 Features

- **Real-time Predictions**: Instantly assess student dropout risk
- **Database Management**: Store and retrieve student records
- **Visual Analytics**: Interactive charts and statistics
- **Multi-factor Analysis**: Considers 7+ key indicators
- **User-friendly Interface**: Clean, intuitive Streamlit interface

## 📊 Prediction Factors

The system evaluates students based on:
- School Satisfaction (1-5)
- Attendance Rate (%)
- Failed Courses
- Commute Time (minutes)
- Disciplinary Incidents
- Homework Completion (%)
- Family Income Level

## 🚀 Local Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/student-dropout-predictor.git
cd student-dropout-predictor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

## 🌐 Live Demo

Access the live application at: [Your Streamlit URL]

## 📦 Project Structure

```
student-dropout-predictor/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── students.db           # SQLite database (auto-created)
```

## 💻 Technology Stack

- **Python 3.8+**
- **Streamlit** - Web framework
- **Pandas** - Data manipulation
- **Scikit-learn** - Machine learning
- **Plotly** - Interactive visualizations
- **SQLite** - Database

## 📈 Usage

1. **Home**: View overall statistics
2. **Predict Dropout**: Enter student data and get predictions
3. **View Database**: Browse all student records
4. **Analytics**: Explore visual insights
5. **About**: Learn more about the system

## 🔒 Data Privacy

All student data is stored locally in SQLite database. No data is shared externally.

## 👥 Credits

**Managed By The Whiskers**

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Contact

For questions or support, please open an issue on GitHub.
