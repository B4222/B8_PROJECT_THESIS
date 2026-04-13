import os

def clean_text(text):
    if not text:
        return ""
    return " ".join(text.replace("\n", " ").replace("\r", " ").split())


def extract_text_from_pdf(file_path):
    from pdfminer.high_level import extract_text

    return extract_text(file_path)


def extract_text_from_docx(file_path):
    import docx

    document = docx.Document(file_path)
    return "\n".join([paragraph.text for paragraph in document.paragraphs])


def extract_resume_text(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    if extension == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif extension == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Only PDF and DOCX files are supported.")

    cleaned = clean_text(text)
    if not cleaned:
        raise ValueError("No readable text found in resume.")
    return cleaned
