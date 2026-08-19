import os
import re
import json
import unicodedata
import pymupdf  # PyMuPDF
import docx

def extract_text_from_pdf(file_path):
    doc = pymupdf.open(file_path)
    text = ""
    for page in doc:
        # sort=True maintains reading order across multi-column layouts
        text += page.get_text("text", sort=True) + "\n"
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def route_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    return ""

def clean_cv_text(raw_text):
    # Normalize unicode ligatures (e.g., fi -> fi, fl -> fl, ffi -> ffi)
    text = unicodedata.normalize('NFKD', raw_text)
    
    # Normalize bullet characters and quote marks
    text = re.sub(r'[\u00b7\u2022\u2023\u25E6\u2043\u2219]', '-', text)
    text = re.sub(r'[\u2018\u2019]', "'", text)
    text = re.sub(r'[\u201C\u201D]', '"', text)
    
    # Remove control characters while preserving formatting
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def extract_name(lines):
    for line in lines[:10]:
        line_clean = line.strip()
        if not line_clean:
            continue
        # Skip hash IDs or long single-token metadata tags
        if re.search(r'[0-9]{5,}', line_clean) and len(line_clean) > 15 and " " not in line_clean:
            continue
        # Skip emails, URLs, locations, or standard section headers
        if re.search(r'(@|github\.com|linkedin\.com|http|www\.)', line_clean, re.IGNORECASE):
            continue
        if re.match(r'^(education|skills|experience|projects|course projects|summary)\b', line_clean, re.IGNORECASE):
            continue
        # Match standard 2-4 word capitalized names
        if re.match(r'^[A-Z][a-zA-Z\.\'-]+(?:\s+[A-Z][a-zA-Z\.\'-]+){1,3}$', line_clean):
            return line_clean
        # Fallback for short name lines
        if len(line_clean.split()) <= 4 and len(line_clean) < 40:
            return line_clean
    return "Unknown"

def extract_cv_sections(clean_text):
    cv_data = {
        "Name": "Unknown",
        "Education": [],
        "Skills": [],
        "Experience": []
    }
    
    raw_lines = [line.strip() for line in clean_text.split('\n') if line.strip()]
    if not raw_lines:
        return cv_data

    cv_data["Name"] = extract_name(raw_lines)

    # Expanded headers to capture course/academic projects under Experience
    headers = {
        "Experience": r'^(work experience|professional experience|employment|experience|research experience|project experience|course projects|projects|academic projects)\b',
        "Education": r'^(education|academic background|academics)\b',
        "Skills": r'^(skills|technical skills|technologies|programming languages)\b'
    }

    current_section = None
    section_buffers = {"Experience": [], "Education": [], "Skills": []}

    for line in raw_lines:
        matched_header = None
        for sec_name, pattern in headers.items():
            if re.match(pattern, line, re.IGNORECASE):
                matched_header = sec_name
                break
        
        if matched_header:
            current_section = matched_header
            continue
        
        if current_section:
            section_buffers[current_section].append(line)

    for sec_name in ["Experience", "Education", "Skills"]:
        if section_buffers[sec_name]:
            cv_data[sec_name] = ["\n".join(section_buffers[sec_name])]

    return cv_data

def process_single_file(file_path):
    raw_text = route_file(file_path)
    cleaned = clean_cv_text(raw_text)
    return extract_cv_sections(cleaned)

if __name__ == "__main__":
    test_file = r"E:\downloads\internship\T2\cv\resume_Meyer.pdf"
    if os.path.exists(test_file):
        result = process_single_file(test_file)
        # ensure_ascii=False renders characters without \u escape codes
        print(json.dumps(result, indent=4, ensure_ascii=False))