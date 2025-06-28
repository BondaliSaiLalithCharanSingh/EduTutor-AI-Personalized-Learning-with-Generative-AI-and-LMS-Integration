# EduTutor-AI-Personalized-Learning-with-Generative-AI-and-LMS-Integration
EduTutor AI is a next-gen educational platform that empowers students with personalized, AI-driven learning experiences and equips educators with real-time insights into student performance. Built using modern web technologies, LLMs, and vector databases, the platform delivers dynamic quizzes, tailored feedback, and progress tracking — all in one unified system.

💡 Developed as part of a collaborative team project by passionate innovators .

🔍 Project Goals
Simplify access to personalized education using AI.

Generate real-time quizzes based on selected topics and difficulty.

Track learning outcomes and adapt based on user responses.

Enable educators to monitor all students’ progress in a single dashboard.

🧩 Key Features
👩‍🎓 Student Side:
Login with role selection and student name.

Choose topic, difficulty, and number of questions.

AI-powered quiz generation using HuggingFace LLM (google/flan-t5-large).

Instant feedback with correct answers and explanations.

Student Dashboard showing previous quiz attempts.

👨‍🏫 Educator Side:
Login as educator and access the Educator Dashboard.

View all student quiz attempts: name, topic, score, and time.

Dynamically updated data using localStorage (or Pinecone for real deployment).

💾 Backend Intelligence:
FastAPI backend for quiz logic and question generation.

Pinecone Vector Database for storing quiz memories and adaptive learning.

Environment-secured endpoints for AI integration.

🛠️ Tech Stack
Layer	Technology
Frontend	HTML, CSS, JavaScript
Backend	FastAPI (Python)
AI Engine	HuggingFace LLM (google/flan-t5-large)
Database	Pinecone (Vector DB)
Deployment	GitHub, Localhost (dev), IBM Cloud-ready

🚀 Getting Started:
Run backend:
1.git clone https://github.com/BondaliSaiLalithCharanSingh/EduTutor-AI-Personalized-Learning-with-Generative-AI-and-LMS-Integration/tree/main

2.cd backend

3.python -m venv venv
.\venv\Scripts\activate

4.pip install -r requirements.txt

5.uvicorn main:app --reload

Run frontend:
Open frontend/create.html in any browser.

❤️ Acknowledgements
Special thanks to our mentors, peers, and reviewers who supported the development process.

✨ Final Note
EduTutor AI represents more than just a project — it's a collaborative vision to bring intelligent, personalized education to every learner. As a team, we poured our creativity, skills, and dedication into building a solution that is scalable, adaptable, and impactful.

We hope this platform inspires further innovation in the field of EdTech and welcome feedback, contributions, and ideas from the community.

Built with passion, purpose, and teamwork.

