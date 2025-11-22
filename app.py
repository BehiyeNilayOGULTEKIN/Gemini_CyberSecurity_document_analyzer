import streamlit as st
import os # Ortam değişkenlerini yüklemek için gerekli
import google.generativeai as geneai
# from google.colab import userdata # Render'da çalışmaz, kaldırıldı.

# Configuration and setup
# API anahtarını ortam değişkeninden (Render'da ayarlayacağımız) yükle
api_key = os.getenv('GOOGLE_API_KEY')

if api_key is None:
    # Render'da anahtar yoksa kullanıcıya hata mesajı gösterir
    st.error("GOOGLE_API_KEY bulunamadı. Lütfen Render ortam değişkenlerini kontrol edin.")
    st.stop()

geneai.configure(api_key=api_key)

# Prompt setup
system_prompt=""" Your are cybersecurity document analyzer. You will analyze the exploits that been in document, then separate them into three different levels,low , medium , high risks, then you will explain why they may be occured and how to solve it. """

generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
    "response_mime_type": "text/plain",
}

# Streamlit App Layout
st.set_page_config(page_title="PDF Document Analyzer")
st.title("Cybersecurity Document Analyzer")

# Dosya yükleyici ve buton, Render'da da sorunsuz çalışacaktır.
upload_file = st.file_uploader("Upload a PDF document to analyze", type=["pdf"], width=200)
submit_button = st.button("Analyze Document", width=200)


# Button Function
if submit_button and upload_file is not None:
    st.info("Analysis in progress...")
    try:
        pdf_data = upload_file.getvalue()
        pdf_parts = [{"data": pdf_data, "mime_type": "application/pdf"}]
        prompt_parts = [pdf_parts[0], system_prompt]

        # Initialize model
        model = geneai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=generation_config
        )

        # Generate response
        response = model.generate_content(prompt_parts)
        st.subheader("Analysis Results:")
        st.markdown(response.text)

    except Exception as e:
        st.error(f"An error occurred during content generation: {e}")
elif submit_button and upload_file is None:
    st.warning("Please upload a document to analyze.")
