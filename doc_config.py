class DocConfig:
    def __init__(self):
        self.config_variables = {
            "title": "Welcome to the Streamlit Interface",
            "description": "This is a simple interface built with Streamlit.",
            "input_label": "Enter some text:",
            "button_label": "Click Me",
            "checkbox_label": "label",
            "sidebar_title": "Sidebar Menu",
            "selectbox_label": "label",
            "download_button_label": "label",
            "form_submit_button_label": "Submit",
            "sidebar_description": "This is a sidebar for additional options."
        }

    def get_config_variables(self):
        return self.config_variables

    def get_streamlit_ui(self):
        return self.streamlit_ui
