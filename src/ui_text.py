class UIVariables:
    def __init__(self):
        self.text={
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
        self.sidebar_text = {
            "title": "Streamlit UI",
            "description": "This is a sidebar for additional options.",
            "input_label": "Enter some text:",
            "button_label": "Click Me",
            "checkbox_label": "label",
            "selectbox_label": "label",
            "download_button_label": "label",
            "form_submit_button_label": "Submit"
        }
    def return_text(self):
        return self.text

    def return_sidebar_text(self):
        return self.sidebar_text
    
    def return_value(self, key):
        return self.text.get(key, None)

    def alter_text(self, key, value):
        if key in self.text:
            self.text[key] = value
        else:
            raise KeyError(f"Key '{key}' not found in text dictionary.")
    
    def alter_sidebar_text(self, key, value):
        if key in self.sidebar_text:
            self.sidebar_text[key] = value
        else:
            raise KeyError(f"Key '{key}' not found in sidebar text dictionary.")
    def reset_text(self):
        self.text = {
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
        self.sidebar_text = {
            "title": "Streamlit UI",
            "description": "This is a sidebar for additional options.",
            "input_label": "Enter some text:",
            "button_label": "Click Me",
            "checkbox_label": "label",
            "selectbox_label": "label",
            "download_button_label": "label",
            "form_submit_button_label": "Submit"
        }