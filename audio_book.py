# import the required modules
import streamlit as st
from gtts import gTTS
import pdfplumber
import docx
import ebooklib
from ebooklib import epub

# create file uploader widget
st.title("Streamlit AudioBook App")
st.info("Convert your E-book to audiobook")
book = st.file_uploader("Please upload your file", type=['pdf','txt', 'docx', 'epub'])

# Create the function to handle file exttraction based on the extension
def extract_text_from_docx(file):
    doc = docx.Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def extract_text_from_epub(file):
    book = epub.read_epub(file)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return "\n".join(chapters)

# Check if file has been uploaded and extract it
if book:
    if book.type == "application/pdf":
        all_text = ""
        with pdfplumber.open(book) as pdf:
            for text in pdf.pages:
                single_page_text = text.extract_text()
                all_text = all_text + '\n' + single_page_text
    elif book.type == "text/plain":
        all_text = book.read().decode("UTF-8")
    elif book.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        all_text = extract_text_from_docx(book)
    elif book.type == "application/epub+zip":
        all_text = extract_text_from_epub(book)
else:
    all_text = ""

# Check if there is text to convert
if all_text:
    # Convert the extracted text to speech
    tts = gTTS(all_text)
    tts.save("audiobook.mp3")

    # Open and read the content of the file
    audio_file = open('audiobook.mp3', 'rb')
    audio_bytes = audio_file.read()

    # Create an audio player widget
    st.audio(audio_bytes, format="audion/mp3", start_time=0)
else:
    st.warning("No text to convert. Please upload a valid file.")