import streamlit as st
class StreamlitUI:
    def __init__(self):
        st.sidebar.title("Streamlit UI")

    def display_interface(self):
        st.title("Welcome to the StreamliStreamlitInterfacet UI")
        st.write("This is a simple interface built with Streamlit.")
        
        user_input = st.text_input("Enter some text:")
        if user_input:
            st.write(f"You entered: {user_input}")
        
        if st.button("Click Me"):
            st.write("Button clicked!")
        st.checkbox("label")

        st.sidebar.title("Sidebar Menu")

        st.selectbox('label')

        st.download_button("label")
        
        st.form_submit_button("Submit")

        st.sidebar.write("This is a sidebar for additional options.")
