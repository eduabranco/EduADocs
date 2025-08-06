import streamlit as st
class StreamlitUI:
    def __init__(self):
        st.sidebar.title("Eduadocs")
        self.text = {
            "title": "Welcome to the Streamlit Interface",
            "description": "This is a simple interface built with Streamlit.",
        }
        self.sidebar_text = {
            "title": "Streamlit UI",
            "description": "This is a sidebar for additional options.",
        }
        self.display_interface()
        self.display_elements()
    def display_interface(self):
        st.title(self.text["title"])
        st.write(self.text["description"])
        st.sidebar.write(self.sidebar_text["description"])

    def display_elements(self):
        st.title(self.text["title"])
        st.write(self.text["description"])
        user_input = st.text_input("Enter some text:")
        if user_input:
            st.write(f"You entered: {user_input}")
        
        if st.button("Click Me"):
            st.write("Button clicked!")
        st.checkbox("label")

        st.sidebar.title("Sidebar Menu")


        with st.form("Form Example"):
            st.text_input("Enter some text:")
            st.form_submit_button("Submit")

        st.download_button("label",data="Sample data", file_name="sample.txt")
        st.sidebar.write("This is a sidebar for additional options.")
        with st.form("Form Example3"):
            st.text_input("Enter some text:")
            st.form_submit_button("Submit")
        with st.form("Form Example2"):
            st.text_input("Enter some text:")
            st.form_submit_button("Submit")
        
        st._bottom.selectbox('🗣️🌐', ['English','Português', 'Español', 'Français','日本語','普通话','Русский','हिंदी'])
if __name__ == "__main__":
    StreamlitUI()
