# 📧 Email Spam Detector

A Machine Learning-based **Email Spam Detector** built with Python and Scikit-learn. This project classifies emails as **Spam** or **Ham (Not Spam)** using Natural Language Processing (NLP) and TF-IDF feature extraction.

---

## 🚀 Features

- 📄 Loads and preprocesses email datasets
- 🧹 Cleans and prepares text data
- 🔤 Converts text into numerical features using TF-IDF
- 🤖 Trains multiple Machine Learning models
- ⚖️ Uses GridSearchCV for hyperparameter tuning
- 🗳️ Implements a Voting Classifier ensemble
- 📊 Evaluates model performance using accuracy and classification metrics
- 💾 Saves the trained model for future predictions

---

## 🛠️ Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- Seaborn
- NLTK
- Scikit-learn
- Pickle

---

## 📂 Project Structure

```
Email-Spam-Detector/
│
├── spamdetector.ipynb      # Main Jupyter Notebook
├── spam.csv                # Dataset
├── model/
│   ├── spam_classifier.pkl
│   └── vectorizer.pkl
├── README.md
└── requirements.txt
```

---

## 📊 Machine Learning Pipeline

1. Load the dataset
2. Data preprocessing
3. Train-Test Split
4. Text Vectorization using TF-IDF
5. Hyperparameter tuning with GridSearchCV
6. Train multiple models:
   - Logistic Regression
   - Multinomial Naive Bayes
   - Linear SVM
7. Voting Classifier Ensemble
8. Model Evaluation
9. Save trained model

---

## 📈 Models Used

- Logistic Regression
- Multinomial Naive Bayes
- Linear Support Vector Machine (SVM)
- Voting Classifier (Ensemble)

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Email-Spam-Detector.git
```

### 2. Move into the project

```bash
cd Email-Spam-Detector
```

### 3. Create a virtual environment (Optional)

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Project

Open Jupyter Notebook

```bash
jupyter notebook
```

or

```bash
jupyter lab
```

Then open:

```
spamdetector.ipynb
```

Run all cells.

---

## 📝 Dataset

The project uses the **SMS Spam Collection Dataset** (`spam.csv`) containing two columns:

- **v1** → Label (spam/ham)
- **v2** → Email/SMS text

---

## 📊 Evaluation Metrics

The notebook evaluates the trained model using:

- Accuracy
- Precision
- Recall
- F1-Score
- Classification Report
- Confusion Matrix

---

## 💾 Model Saving

The trained model and TF-IDF vectorizer are saved inside the **model/** directory and can be reused without retraining.

---

## 🔮 Future Improvements

- Deploy using Streamlit
- Flask/FastAPI API
- Deep Learning (LSTM/BERT)
- Email attachment analysis
- Real-time Gmail integration

---

## 👨‍💻 Author

**Sayam Suri**

B.Tech Information Technology

---
