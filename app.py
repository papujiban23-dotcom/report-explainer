import streamlit as st
import google.generativeai as genai
import pypdf

# Page Config
st.set_page_config(page_title="AI Report Explainer", page_icon="📄", layout="centered")

st.title("📄 Smart AI Report & Document Explainer")
st.write("Koi bhi PDF/Report upload karein aur simple **Hinglish** mein samjhein!")

# Sidebar for API Key
api_key = st.sidebar.text_input("Apni Gemini API Key Yahan Daalein:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # File Uploader
        uploaded_file = st.file_uploader("Apni PDF File Upload Karein", type=["pdf"])
        
        if uploaded_file is not None:
            # Extract Text from PDF
            pdf_reader = pypdf.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
                
            st.success("PDF Upload Ho Gayi!")
            
            # Explain Button
            if st.button("🚀 Report Explain Karo"):
                with st.spinner("AI Report padh raha hai... kripya wait karein..."):
                    # Auto-detect available model supporting generateContent
                    active_model = None
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            active_model = m.name
                            break
                    
                    if not active_model:
                        active_model = 'models/gemini-2.0-flash'
                        
                    model = genai.GenerativeModel(active_model)
                    
                    prompt = f"""
                    You are a helpful AI assistant. Read the following document text and provide a response in simple, clear Hinglish (Hindi written in English script):
                    1. **Document Type:** Auto-detect what kind of report/document this is (e.g., Medical Report, Financial Document, Student Notes, Legal Agreement, etc.).
                    2. **3-Line Summary:** Give a high-level summary in 3 simple sentences.
                    3. **Key Points:** List 5 important key points or findings from the document.
                    4. **Actionable Advice / Important Warnings:** Tell the user what they should do next or if there is any critical warning in simple words.

                    Document Text:
                    {text[:10000]}
                    """
                    
                    response = model.generate_content(prompt)
                    st.markdown("### 📊 Report Ki Simple Explanation:")
                    st.write(response.text)
                    
            st.markdown("---")
            # Ask Question Option
            st.subheader("💬 Report se related koi sawaal poochho")
            user_question = st.text_input("Aapka Sawaal:")
            
            if user_question:
                with st.spinner("Jawab dhoondha ja raha hai..."):
                    active_model = None
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            active_model = m.name
                            break
                    
                    if not active_model:
                        active_model = 'models/gemini-2.0-flash'
                        
                    model = genai.GenerativeModel(active_model)
                    chat_prompt = f"Based on this document text: {text[:10000]}, answer this question in simple Hinglish: {user_question}"
                    chat_response = model.generate_content(chat_prompt)
                    st.write("**AI ka Jawab:**", chat_response.text)

    except Exception as e:
        st.error(f"Error aaya: {e}. Kripya apni API Key check karein.")

else:
    st.warning("Shuru karne ke liye pehle Sidebar mein apni Free Gemini API Key daalein!")
