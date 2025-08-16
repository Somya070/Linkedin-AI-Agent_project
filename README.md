# Linkedin-AI-Agent

An AI-powered LinkedIn content creation and management tool built with **Streamlit**.  
It helps professionals generate personalized LinkedIn posts, research industry trends, optimize engagement, and manage a content calendar — all in one place.

Live demo link: https://linkedin-ai-agentproject-65s4efqisrrgw7wwdq9bpw.streamlit.app/

## 🚀 Features

1. **Profile Analysis**
   - Upload your **LinkedIn profile PDF** or resume.
   - Extracts **skills**, **experience**, and **education**.
   - Displays a clean, structured view of your professional background.

2. **Personalized Post Generation**
   - Select a topic, length, and language (English / Hinglish).
   - Automatically creates LinkedIn-ready posts tailored to your profile.
   - Uses **Few-Shot Learning** to adapt style and tone.

3. **Link Saver & Summarizer**
   - Save useful articles and get an AI-generated summary.
   - Great for curating and sharing content with your network.

4. **Content Calendar**
   - Plan your LinkedIn content in advance.
   - Track post status (Planned / Completed).

5. **Industry Research (Groq API)**
   - AI-assisted industry trends & insights.
   - Ideal for staying ahead in your niche.

6. **Engagement Optimization**
   - Paste an existing LinkedIn post.
   - AI improves hooks, adds hashtags, and optimizes wording for **maximum engagement**.

7. **Performance Analytics**
   - Track and analyze your LinkedIn post performance (planned feature).

---

## 📂 Project Structure

.
├── main.py # Streamlit app entry point
├── few_shot.py # Few-shot post templates & tags
├── post_gen.py # Post generation logic
├── profile_analysis.py # LinkedIn profile API fetch & analysis
├── preprocess.py # Metadata extraction & tag unification
├── db.py # Database functions for saved posts
├── calendar_db.py # Database functions for content calendar
├── llm_helper.py # LLM integration helper
├── utils.py # (Expected) Common utilities like URL summarization
├── scraper.py # (Expected) Web scraping helper for articles
├── summary.py # (Expected) Text summarization logic
├── posts.db # SQLite database for saved posts
├── content_calendar.db # SQLite database for content calendar
├── requirements.txt # Python dependencies
└── README.md # Project documentation


---

## 🛠 Installation

### 1️⃣ Clone the Repository

git clone https://github.com/yourusername/linkedin-ai-agent.git
cd linkedin-ai-agent

pip install -r requirements.txt

### 3️⃣ Set Environment Variables
Create a .env file in the root directory:
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key   # If used in LLM helper

### (Optional) If you use Streamlit secrets:

.streamlit/secrets.toml
GROQ_API_KEY = "your_groq_api_key"

### 4️⃣ Run the App

streamlit run main.py

### 🔑 API Keys Required
Groq API → for Industry Research & Engagement Optimization

(Optional) OpenAI API → if using GPT models in llm_helper.py

(Optional) LinkedIn OAuth API → for direct profile fetching


### 💻 Usage Guide
1. Profile Analysis
Go to Profile Analysis tab.
Upload your LinkedIn PDF/resume.
Click Analyze Profile to see extracted skills, experience, and education.

2. Generate Post
Select a topic, length, and language.
Check "Use analyzed profile data" (optional).
Click Generate Post — your personalized post will appear.

3. Industry Research
Enter your query (e.g., "Latest AI trends in 2025").
Click Get Trends to see insights powered by Groq API.
Engagement Optimization
Paste your LinkedIn post.

4. Link Saver & Summarizer
Save useful article links you find online.
AI automatically fetches and summarizes the content.
Perfect for sharing curated industry news with your network.
Click Optimize for Engagement to get AI-suggested improvements.

5. Engagement Optimization
Paste any LinkedIn post text.
AI rewrites the hook, optimizes language, adds hashtags, and improves flow.
Ensures your post is authentic yet highly shareable.

6. Content Calendar
Plan posts ahead of time with titles, descriptions, and dates.
Keep track of post statuses (Planned / Completed).
Acts as your LinkedIn content pipeline to maintain consistency.

7. Performance Analysis 
Track how your LinkedIn posts perform over time.
See metrics like reach, engagement rate, and top-performing topics.
Identify what works and double down on it.

### 📌 Future Enhancements
1. OAuth-based LinkedIn integration for auto-posting.
2. Schedule posts to auto-publish at set times.
3. Advanced analytics dashboard for post performance.
4. Multi-language post generation.

### ☁ Deployment Options
You can deploy the app using:
Streamlit Cloud (free, easiest)
Docker + AWS/GCP/Azure (requires cloud account; may incur costs)
Heroku or Railway.app (free tier available)

### 📜 License
This project is licensed under the MIT License.

### ✨ Author
Somya Anand — Passionate about AI, self-development, and building tools that empower professionals.
