# 🌎 AI Travel Planner

An AI-powered travel planner that generates personalized travel itineraries based on user preferences.

## 🚀 Quick Start

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ai-travel-planner.git
   cd ai-travel-planner
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create your environment file:
   ```bash
   cp .env.example .env
   ```

5. Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   ⚠️ Never commit your .env file to version control!

6. Run the application:
   ```bash
   streamlit run app.py
   ```

## 🔒 Security Notes

- The `.env` file is listed in `.gitignore` and should never be committed
- When deploying to Streamlit Cloud, use their secrets management system
- Keep your API keys private and never share them publicly

## ✨ Features

- 🎯 Personalized travel itinerary generation
- 🎨 Comprehensive preference collection:
  - Destination
  - Duration
  - Budget level
  - Travel style
  - Dietary preferences
  - Mobility preferences
  - Accommodation preferences
- 📥 Downloadable itineraries
- 📱 Responsive design

## 🛠️ Technology Stack

- Python
- Streamlit
- OpenAI GPT-4

## 🚀 Deployment

To deploy on Streamlit Cloud:

1. Push your code to GitHub
2. Connect your repository to Streamlit Cloud
3. Add your OpenAI API key to Streamlit secrets
4. Deploy!

## 📝 License

MIT License 