import streamlit as st

# Set page configuration
st.set_page_config(page_title="Twitter-Themed App", page_icon="🐦")

# Load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Define functions for each page
def url_page():
    st.title("URL Page")
    st.write("You entered a URL!")

def video_page():
    st.title("Video Page")
    st.write("You uploaded a video!")

# Initialize session state
if "input_provided" not in st.session_state:
    st.session_state.input_provided = False

# Main app logic
def main():
    # Add a header with a title and description
    st.header("Twitter-Themed App")
    st.subheader("Navigate seamlessly based on your input")

    # Check if input has already been provided
    if st.session_state.input_provided:
        # User has provided input, display appropriate page
        if st.session_state.page == "URL Page":
            url_page()
        elif st.session_state.page == "Video Page":
            video_page()
    else:
        # Create a sidebar for navigation
        st.sidebar.title("Navigation")

        # Add a file uploader and URL input with improved prompts
        st.write("Please provide an input to proceed:")
        file = st.file_uploader("Upload a video file (mp4, avi, mov)")
        url = st.text_input("Or enter a URL")

        # Navigate based on user input
        if file:
            st.session_state.input_provided = True
            st.session_state.page = "Video Page"
            video_page()
        elif url:
            st.session_state.input_provided = True
            st.session_state.page = "URL Page"
            url_page()
        else:
            st.sidebar.write("Awaiting your input")

if __name__ == "__main__":
    main()
