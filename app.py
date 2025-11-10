
import streamlit as st
import asyncio
import pathlib
from pathlib import Path

from agent import root_agent
import config
from helper import load_env

# Imports for Runner are done inside the function to avoid issues if not available

# Load environment variables
load_env()

# Set page config
st.set_page_config(
    page_title="AI News Podcast Generator",
    page_icon="🎙️",
    layout="wide"
)

# Initialize session state
if 'report_generated' not in st.session_state:
    st.session_state.report_generated = False
if 'audio_generated' not in st.session_state:
    st.session_state.audio_generated = False


def check_api_key():
    if config.GEMINI_API_KEY == "your-gemini-api-key-here" or not config.GEMINI_API_KEY:
        return False
    return True


async def run_agent_async(user_input: str):
    try:
        # Use Runner class - this is the proper way according to ADK docs
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        from google.genai import types
        import uuid
        
        # Set up session management
        session_service = InMemorySessionService()
        app_name = "agents"
        user_id = "streamlit_user"
        session_id = str(uuid.uuid4())  # Generate unique session ID
        
        # Create runner with the agent
        runner = Runner(
            agent=root_agent,
            app_name=app_name,
            session_service=session_service
        )
        
        # Create the session
        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        
        # Create user message content
        user_content = types.Content(
            role='user',
            parts=[types.Part(text=user_input)]
        )
        
        # Run the agent and collect responses
        final_response = None
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_content
        ):
            # Check if this is the final response
            if event.is_final_response() and event.content and event.content.parts:
                final_response = event.content.parts[0].text
        
        return final_response
    except Exception as e:
        error_msg = str(e)
        import traceback
        full_traceback = traceback.format_exc()
        
        # Check if it's the function calling error
        if "Tool use with function calling is unsupported" in str(e):
            error_msg += "\n\n⚠️ This error suggests the model or API doesn't support function calling."
            error_msg += "\nPossible solutions:"
            error_msg += "\n1. Try a different Gemini 2.0 model (check sidebar for available models)"
            error_msg += "\n2. Verify your API key has access to function calling features"
            error_msg += "\n3. Check if there's an API version mismatch"
        
        error_msg += f"\n\nFull Traceback:\n{full_traceback}"
        return f"Error running agent: {error_msg}"


def run_agent(user_input: str):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(run_agent_async(user_input))
            return response
        finally:
            loop.close()
    except Exception as e:
        error_msg = str(e)
        import traceback
        error_msg += f"\n\nTraceback: {traceback.format_exc()}"
        return f"Error running agent: {error_msg}"


def main():
    st.title("🎙️ AI News Podcast Generator")
    st.markdown("Generate AI news reports and podcast audio for NASDAQ-listed companies")
    
    # Check API key
    if not check_api_key():
        st.error("⚠️ Please configure your Gemini API key in `config.py` before using this app.")
        st.info("Edit `config.py` and set `GEMINI_API_KEY` to your API key.")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Whitelisted Domains")
        st.caption("The agent only trusts news from these sources during Google search.")
        for domain in config.WHITELIST_DOMAINS:
            st.text(f"• {domain}")
    
    # Main content
    st.markdown("---")
    
    # User input
    user_input = st.text_input(
        "Enter your request:",
        value="Generate a research report and podcast about the latest AI news for NASDAQ-listed US companies.",
        help="The agent will search for news, compile a report, and generate a podcast."
    )
    
    # Generate button
    col1, col2 = st.columns([1, 4])
    with col1:
        generate_button = st.button("🚀 Generate Report & Podcast", type="primary", use_container_width=True)
    
    if generate_button:
        if not user_input.strip():
            st.warning("Please enter a request.")
        else:
            # Show progress
            with st.spinner("🔄 Processing your request... This may take 1-2 minutes."):
                status_placeholder = st.empty()
                status_placeholder.info("⏳ Starting research...")
                
                try:
                    # Run the agent
                    run_agent(user_input)
                    st.session_state.report_generated = True
                    
                    status_placeholder.success("✅ Report and podcast generated successfully!")
                    
                except Exception as e:
                    status_placeholder.error(f"❌ Error: {str(e)}")
                    st.session_state.report_generated = False
    
    # Display results
    if st.session_state.report_generated:
        st.markdown("---")
        st.header("📊 Results")
        
        # Check if report file exists
        report_path = Path(config.REPORT_FILENAME)
        if report_path.exists():
            st.success(f"✅ Report saved: `{config.REPORT_FILENAME}`")
            
            # Display report
            with st.expander("📄 View Research Report", expanded=True):
                try:
                    with open(report_path, 'r', encoding='utf-8') as f:
                        report_content = f.read()
                    st.markdown(report_content)
                except Exception as e:
                    st.error(f"Error reading report: {str(e)}")
            
            # Download report button
            with open(report_path, 'r', encoding='utf-8') as f:
                st.download_button(
                    label="📥 Download Report",
                    data=f.read(),
                    file_name=config.REPORT_FILENAME,
                    mime="text/markdown"
                )
        else:
            st.warning(f"⚠️ Report file `{config.REPORT_FILENAME}` not found yet. Please wait...")
        
        # Check if audio file exists
        audio_path = Path(config.PODCAST_FILENAME)
        if audio_path.exists():
            st.success(f"✅ Podcast audio saved: `{config.PODCAST_FILENAME}`")
            
            # Audio player
            st.subheader("🎧 Podcast Audio")
            try:
                audio_file = open(audio_path, 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/wav')
                audio_file.close()
            except Exception as e:
                st.error(f"Error loading audio: {str(e)}")
            
            # Download audio button
            with open(audio_path, 'rb') as f:
                st.download_button(
                    label="📥 Download Podcast Audio",
                    data=f.read(),
                    file_name=config.PODCAST_FILENAME,
                    mime="audio/wav"
                )
        else:
            st.info(f"⏳ Podcast audio file `{config.PODCAST_FILENAME}` is being generated. Please wait...")
        
    # Instructions
    st.markdown("---")
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        1. **Configure API Key**: Edit `config.py` and set your `GEMINI_API_KEY`
        2. **Enter Request**: Type your request or use the default one
        3. **Generate**: Click the "Generate Report & Podcast" button
        4. **Wait**: The process takes about 1-2 minutes:
           - ~30 seconds for research report
           - ~1 minute for podcast audio generation
        5. **View Results**: The report and audio will appear below
        
        **Note**: The agent searches whitelisted tech news domains and focuses on NASDAQ-listed US companies.
        """)


if __name__ == "__main__":
    main()

