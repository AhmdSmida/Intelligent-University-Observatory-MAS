# 🔭 Intelligent University Observatory MAS

An intelligent **Multi-Agent System (MAS)** built with Python and the [Mesa](https://mesa.readthedocs.io/) framework. This system autonomously scrapes, classifies, clusters, and recommends AI, Data Science, and Computer Science opportunities (Internships, Scholarships, Certifications, and Research Projects) to university students.

## ✨ Key Features

- **Multi-Agent Architecture:** Powered by a decentralized network of 10 specialized agents working asynchronously.
- **Headless Web Scraping:** Utilizes `Selenium WebDriver` and `BeautifulSoup` to bypass bot protections and extract live data from platforms like LinkedIn, Indeed, Coursera, and ResearchGate.
- **Semantic Recommendation Engine:** Uses TF-IDF, PCA, and Cosine Similarity algorithms to perfectly match students' profiles to relevant opportunities.
- **Continuous Background Worker:** Runs silently 24/7 with smart intervals to prevent IP bans while delivering fresh data.
- **Interactive Dashboard:** Features a beautiful, real-time UI built with `Streamlit` and `Plotly` to visualize metrics, clusters, and personalized recommendations.

## 🤖 The Agent Ecosystem

The pipeline follows the Template Method design pattern, utilizing the following agents:
1. **Scrapers (`Internship`, `Scholarship`, `Certification`, `Project`):** Autonomous agents that fetch and parse HTML from target websites.
2. **`AgentClassifier`:** NLP model that tags raw text into correct opportunity categories.
3. **`AgentCluster`:** Groups similar opportunities together using unsupervised learning (PCA visualization).
4. **`AgentRelevanceMatcher`:** The core recommendation engine comparing student profiles to opportunity requirements.
5. **`AgentAdvisor` & `AgentNotification`:** Dispatch alerts and finalize the recommendation delivery.

## 🚀 Getting Started

### Prerequisites
Ensure you have Python 3.9+ installed. Google Chrome must be installed on your machine for the Headless Scraper to work.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Make sure the required packages such as `mesa`, `streamlit`, `selenium`, `webdriver-manager`, `beautifulsoup4`, `scikit-learn`, `pandas`, and `plotly` are installed.)*

### 2. Run the MAS Worker
To start the background scraping and recommendation engine:
```bash
python run.py
```
*Note: The script initializes an SQLite database (`db/observatory.db`) automatically and seeds 50 mock student profiles.*

### 3. Launch the Dashboard
Open a new terminal window and run:
```bash
streamlit run dashboard/app.py
```
This will open the visual observatory interface in your default web browser.

## ⚙️ Configuration
You can toggle between **Mock Mode** (instant demo data) and **Real Mode** (live Selenium scraping) by modifying `SCRAPER_MOCK_MODE` in `config.py` or `run.py`.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
