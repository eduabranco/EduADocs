import streamlit as st
import json
from enum import Enum

class DocumentType(Enum):
    SUMMARY = "Summary"
    EXERCISES = "Exercise List"
    CORRECTION = "Exercise Correction"

class LLMProvider(Enum):
    OPENAI = "OpenAI"
    GOOGLE = "Google (Gemini)"
    HUGGINGFACE = "HuggingFace"
    OLLAMA = "Ollama"

class StreamlitUI:
    def __init__(self):
        self.initialize_session_state()
        self.setup_page_config()
        self.display_interface()

    def setup_page_config(self):
        st.set_page_config(
            page_title="EduADocs - AI Educational Content Generator",
            page_icon="📚",
            layout="wide",
            initial_sidebar_state="expanded"
        )

    def initialize_session_state(self):
        if 'generated_draft' not in st.session_state:
            st.session_state.generated_draft = ""
        if 'approved_content' not in st.session_state:
            st.session_state.approved_content = ""
        if 'generation_step' not in st.session_state:
            st.session_state.generation_step = "input"  # input, draft, approved, final

    def display_interface(self):
        # Sidebar configuration
        self.display_sidebar()
        
        # Main content area
        st.title("📚 EduADocs - AI Educational Content Generator")
        st.markdown("Generate summaries, exercises, and corrections with AI-powered assistance")
        
        # Display different views based on current step
        if st.session_state.generation_step == "input":
            self.display_input_form()
        elif st.session_state.generation_step == "draft":
            self.display_draft_review()
        elif st.session_state.generation_step == "approved":
            self.display_approved_content()
        elif st.session_state.generation_step == "final":
            self.display_final_document()

    def display_sidebar(self):
        st.sidebar.title("⚙️ Configuration")
        
        # LLM Provider Selection
        st.sidebar.subheader("🤖 AI Provider")
        provider = st.sidebar.selectbox(
            "Choose LLM Provider:",
            [provider.value for provider in LLMProvider],
            key="llm_provider"
        )
        
        # Provider-specific settings
        if provider == LLMProvider.OPENAI.value:
            st.sidebar.text_input("OpenAI API Key:", type="password", key="openai_key")
            st.sidebar.selectbox("Model:", ["gpt-4", "gpt-3.5-turbo"], key="openai_model")
        elif provider == LLMProvider.GOOGLE.value:
            st.sidebar.text_input("Google API Key:", type="password", key="google_key")
            st.sidebar.selectbox("Model:", ["gemini-pro", "gemini-pro-vision"], key="google_model")
        elif provider == LLMProvider.HUGGINGFACE.value:
            st.sidebar.text_input("HuggingFace API Key:", type="password", key="hf_key")
            st.sidebar.text_input("Model Name:", placeholder="microsoft/DialoGPT-medium", key="hf_model")
        elif provider == LLMProvider.OLLAMA.value:
            st.sidebar.text_input("Ollama Endpoint:", value="http://localhost:11434", key="ollama_endpoint")
            st.sidebar.text_input("Model Name:", placeholder="llama2", key="ollama_model")
        
        st.sidebar.divider()
        
        # Language Selection
        st.sidebar.subheader("🌐 Language")
        st.sidebar.selectbox(
            'Output Language:',
            ['English', 'Português', 'Español', 'Français', '日本語', '普通话', 'Русский', 'हिंदी'],
            key="output_language"
        )
        
        st.sidebar.divider()
        
        # Progress indicator
        st.sidebar.subheader("📊 Progress")
        progress_steps = ["Input", "Draft", "Review", "Final"]
        current_step_index = progress_steps.index(st.session_state.generation_step.title()) if st.session_state.generation_step.title() in progress_steps else 0
        st.sidebar.progress((current_step_index + 1) / len(progress_steps))
        st.sidebar.write(f"Current Step: {progress_steps[current_step_index]}")

    def display_input_form(self):
        st.header("📝 Content Specification")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("content_specification"):
                # Document type selection
                doc_type = st.selectbox(
                    "📄 Document Type:",
                    [dtype.value for dtype in DocumentType],
                    key="document_type"
                )
                
                # Subject and topic
                subject = st.text_input("📚 Subject:", placeholder="e.g., Mathematics, History, Biology")
                topic = st.text_input("🎯 Topic:", placeholder="e.g., Quadratic Equations, World War II, Cell Division")
                
                # Additional details
                st.subheader("📋 Additional Details")
                
                if doc_type == DocumentType.SUMMARY.value:
                    details = st.text_area(
                        "Summary Requirements:",
                        placeholder="Specify the depth of coverage, target audience level, key points to include...",
                        height=150
                    )
                elif doc_type == DocumentType.EXERCISES.value:
                    col_ex1, col_ex2 = st.columns(2)
                    with col_ex1:
                        num_exercises = st.number_input("Number of Exercises:", min_value=1, max_value=50, value=10)
                        difficulty = st.selectbox("Difficulty Level:", ["Beginner", "Intermediate", "Advanced"])
                    with col_ex2:
                        exercise_types = st.multiselect(
                            "Exercise Types:",
                            ["Multiple Choice", "Short Answer", "Essay", "Problem Solving", "True/False"]
                        )
                    details = st.text_area(
                        "Additional Requirements:",
                        placeholder="Specific topics to focus on, learning objectives, special instructions...",
                        height=100
                    )
                elif doc_type == DocumentType.CORRECTION.value:
                    st.info("📤 Upload student submissions for correction")
                    uploaded_files = st.file_uploader(
                        "Student Submissions:",
                        accept_multiple_files=True,
                        type=['txt', 'pdf', 'docx']
                    )
                    grading_criteria = st.text_area(
                        "Grading Criteria:",
                        placeholder="Rubric, point distribution, specific areas to focus on...",
                        height=100
                    )
                    details = f"Grading Criteria: {grading_criteria}"
                
                # Target audience
                audience = st.selectbox(
                    "🎓 Target Audience:",
                    ["Elementary School", "Middle School", "High School", "Undergraduate", "Graduate", "Professional"]
                )
                
                # Additional context
                context = st.text_area(
                    "📝 Additional Context:",
                    placeholder="Any other relevant information, constraints, or special requirements...",
                    height=100
                )
                
                submitted = st.form_submit_button("🚀 Generate Draft", type="primary")
                
                if submitted and subject and topic:
                    # Store form data in session state
                    st.session_state.form_data = {
                        'document_type': doc_type,
                        'subject': subject,
                        'topic': topic,
                        'details': details,
                        'audience': audience,
                        'context': context,
                        'language': st.session_state.output_language,
                        'llm_provider': st.session_state.llm_provider
                    }
                    
                    # TODO: Call CrewAI here to generate draft
                    st.session_state.generated_draft = self.simulate_draft_generation()
                    st.session_state.generation_step = "draft"
                    st.rerun()
                elif submitted:
                    st.error("Please fill in at least the Subject and Topic fields.")
        
        with col2:
            st.subheader("💡 Tips")
            st.info("""
            **For better results:**
            - Be specific about the topic
            - Include learning objectives
            - Specify the complexity level
            - Mention any curriculum standards
            """)
            
            st.subheader("📖 Examples")
            with st.expander("Summary Example"):
                st.code("""
                Subject: Biology
                Topic: Photosynthesis
                Details: Include light and dark reactions, 
                         focus on molecular processes
                """)
            
            with st.expander("Exercise Example"):
                st.code("""
                Subject: Mathematics  
                Topic: Derivatives
                Details: Mix of computational and 
                         conceptual problems
                """)

    def display_draft_review(self):
        st.header("📋 Draft Review")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader("Generated Draft (Markdown)")
            
            # Display the generated draft
            draft_container = st.container()
            with draft_container:
                st.markdown("**Preview:**")
                st.markdown(st.session_state.generated_draft)
            
            st.divider()
            
            # Editable version
            st.subheader("✏️ Edit Draft")
            edited_draft = st.text_area(
                "Make your modifications:",
                value=st.session_state.generated_draft,
                height=400,
                key="edited_draft"
            )
            
            # Action buttons
            col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
            
            with col_btn1:
                if st.button("🔄 Regenerate", type="secondary"):
                    st.session_state.generated_draft = self.simulate_draft_generation()
                    st.rerun()
            
            with col_btn2:
                if st.button("💾 Save Changes", type="secondary"):
                    st.session_state.generated_draft = edited_draft
                    st.success("Changes saved!")
            
            with col_btn3:
                if st.button("✅ Approve Draft", type="primary"):
                    st.session_state.approved_content = edited_draft
                    st.session_state.generation_step = "approved"
                    st.rerun()
            
            with col_btn4:
                if st.button("⬅️ Back to Input", type="secondary"):
                    st.session_state.generation_step = "input"
                    st.rerun()
        
        with col2:
            st.subheader("📊 Content Analysis")
            st.metric("Word Count", len(st.session_state.generated_draft.split()))
            st.metric("Characters", len(st.session_state.generated_draft))
            
            st.subheader("🎯 Original Request")
            if 'form_data' in st.session_state:
                st.write(f"**Type:** {st.session_state.form_data['document_type']}")
                st.write(f"**Subject:** {st.session_state.form_data['subject']}")
                st.write(f"**Topic:** {st.session_state.form_data['topic']}")

    def display_approved_content(self):
        st.header("✅ Content Approved")
        st.success("Your content has been approved and is ready for document generation!")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader("📄 Final Content Preview")
            st.markdown(st.session_state.approved_content)
            
            st.divider()
            
            # Document format options
            st.subheader("📤 Document Generation Options")
            
            col_fmt1, col_fmt2 = st.columns(2)
            with col_fmt1:
                output_format = st.selectbox(
                    "Output Format:",
                    ["DOCX (Word Document)", "PDF", "HTML"],
                    key="output_format"
                )
                
                include_header = st.checkbox("Include Header with Metadata", value=True)
                include_footer = st.checkbox("Include Footer with Page Numbers", value=True)
            
            with col_fmt2:
                template_style = st.selectbox(
                    "Document Style:",
                    ["Academic", "Professional", "Casual", "Custom"],
                    key="template_style"
                )
                
                font_size = st.selectbox("Font Size:", ["10pt", "11pt", "12pt", "14pt"], index=2)
        
        with col2:
            st.subheader("🚀 Actions")
            
            if st.button("📄 Generate Document", type="primary"):
                # TODO: Call CrewAI to generate final document
                st.session_state.generation_step = "final"
                st.rerun()
            
            if st.button("✏️ Edit Content", type="secondary"):
                st.session_state.generation_step = "draft"
                st.rerun()
            
            if st.button("🔄 Start Over", type="secondary"):
                self.reset_session()
                st.rerun()

    def display_final_document(self):
        st.header("🎉 Document Generated Successfully!")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.success("Your document has been generated and is ready for download!")
            
            # Simulate document download
            document_data = self.simulate_document_generation()
            
            st.download_button(
                label="📥 Download Document",
                data=document_data,
                file_name=f"eduadocs_{st.session_state.form_data['subject']}_{st.session_state.form_data['topic']}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                type="primary"
            )
            
            st.subheader("📋 Generation Summary")
            if 'form_data' in st.session_state:
                st.write(f"**Document Type:** {st.session_state.form_data['document_type']}")
                st.write(f"**Subject:** {st.session_state.form_data['subject']}")
                st.write(f"**Topic:** {st.session_state.form_data['topic']}")
                st.write(f"**Target Audience:** {st.session_state.form_data['audience']}")
                st.write(f"**Language:** {st.session_state.form_data['language']}")
                st.write(f"**LLM Provider:** {st.session_state.form_data['llm_provider']}")
        
        with col2:
            st.subheader("🔄 Next Steps")
            
            if st.button("📝 Create New Document", type="primary"):
                self.reset_session()
                st.rerun()
            
            if st.button("🔍 View Content", type="secondary"):
                st.session_state.generation_step = "approved"
                st.rerun()
            
            st.subheader("📊 Statistics")
            st.metric("Documents Created", "1")
            st.metric("Success Rate", "100%")

    def simulate_draft_generation(self):
        """Simulate draft generation - replace with actual CrewAI call"""
        form_data = st.session_state.form_data
        return f"""# {form_data['subject']}: {form_data['topic']}

## Introduction
This is a simulated draft for {form_data['document_type'].lower()} on {form_data['topic']} in {form_data['subject']}.

## Main Content
Generated content would appear here based on the specified requirements:
- **Target Audience:** {form_data['audience']}
- **Additional Details:** {form_data['details']}

## Conclusion
This concludes the simulated draft content.

*Generated using {form_data['llm_provider']} in {form_data['language']}*
"""

    def simulate_document_generation(self):
        """Simulate document generation - replace with actual document creation"""
        return b"Simulated DOCX content - replace with actual python-docx generated document"

    def reset_session(self):
        """Reset session state to start over"""
        for key in ['generated_draft', 'approved_content', 'form_data']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.generation_step = "input"

if __name__ == "__main__":
    StreamlitUI()
