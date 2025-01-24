import streamlit as st
import openai
from typing import Dict
from dotenv import load_dotenv
import os

# Page configuration
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# Load environment variables
load_dotenv()

def initialize_openai():
    """Initialize OpenAI client with proper error handling"""
    api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        st.error("⚠️ OpenAI API key not found. Please set it in .env file or Streamlit secrets.")
        st.info("ℹ️ Check the README.md file for setup instructions.")
        st.stop()
    
    try:
        return openai.OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"⚠️ Error initializing OpenAI client: {str(e)}")
        st.stop()

def get_initial_preferences() -> Dict:
    """Get initial travel preferences from user"""
    st.title("✈️ AI Travel Planner")
    st.markdown("### Let's plan your perfect trip! 🌎")
    
    col1, col2 = st.columns(2)
    
    with col1:
        destination = st.text_input("🌍 Where would you like to go?", placeholder="e.g., Paris, France")
        duration = st.number_input("📅 How many days is your trip?", min_value=1, max_value=30, value=3)
        budget = st.selectbox("💰 What's your budget level?", 
                            ["Budget", "Moderate", "Luxury"])
    
    with col2:
        travel_style = st.multiselect("🎨 What's your travel style?",
                                    ["Cultural", "Adventure", "Relaxation", "Food & Dining",
                                     "Shopping", "Nature", "Historical"])
        dietary_prefs = st.multiselect("🍽️ Any dietary preferences?",
                                     ["Vegetarian", "Vegan", "Halal", "Kosher", "None"])
        mobility = st.selectbox("🚶 Walking tolerance?",
                              ["Low (prefer transport)", "Moderate", "High (love walking)"])
    
    accommodation_pref = st.selectbox("🏨 Accommodation preference?",
                                    ["Budget hostel", "Mid-range hotel", "Luxury resort"])
    
    additional_notes = st.text_area("📝 Any additional preferences or notes?", 
                                  placeholder="e.g., interested in local markets, prefer morning activities...")
    
    return {
        "destination": destination,
        "duration": duration,
        "budget": budget,
        "travel_style": travel_style,
        "dietary_prefs": dietary_prefs,
        "mobility": mobility,
        "accommodation": accommodation_pref,
        "notes": additional_notes
    }

def generate_itinerary(client, preferences: Dict) -> str:
    """Generate travel itinerary using OpenAI API"""
    
    system_prompt = """You are an expert travel planner. Generate a detailed day-by-day travel itinerary based on the user's preferences.
    Include:
    - Daily activities with approximate timings
    - Restaurant recommendations considering dietary preferences
    - Transportation suggestions based on mobility preference
    - Estimated costs for activities
    Format the response in markdown with clear headings and bullet points."""
    
    user_prompt = f"""Create a {preferences['duration']}-day itinerary for {preferences['destination']} with these preferences:
    - Budget Level: {preferences['budget']}
    - Travel Style: {', '.join(preferences['travel_style']) if preferences['travel_style'] else 'Any'}
    - Dietary Preferences: {', '.join(preferences['dietary_prefs']) if preferences['dietary_prefs'] else 'None'}
    - Mobility Level: {preferences['mobility']}
    - Accommodation: {preferences['accommodation']}
    Additional Notes: {preferences['notes']}"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating itinerary: {str(e)}"

def main():
    # Initialize OpenAI client
    client = initialize_openai()
    
    # Initialize session state
    if 'itinerary' not in st.session_state:
        st.session_state.itinerary = None
    
    # Get user preferences
    preferences = get_initial_preferences()
    
    # Generate button
    if st.button("🎯 Generate Itinerary"):
        if not preferences["destination"]:
            st.error("⚠️ Please enter a destination")
            return
            
        with st.spinner("🔄 Generating your personalized itinerary..."):
            itinerary = generate_itinerary(client, preferences)
            st.session_state.itinerary = itinerary
    
    # Display itinerary
    if st.session_state.itinerary:
        st.markdown("## 📋 Your Personalized Itinerary")
        st.markdown(st.session_state.itinerary)
        
        # Add download button
        st.download_button(
            label="📥 Download Itinerary",
            data=st.session_state.itinerary,
            file_name=f"travel_itinerary_{preferences['destination'].lower().replace(' ', '_')}.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main() 