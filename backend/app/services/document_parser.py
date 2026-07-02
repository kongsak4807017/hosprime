import os
import pypdf
import docx
from typing import List, Dict, Any

class DocumentParser:
    @staticmethod
    def parse_txt(file_path: str) -> List[Dict[str, Any]]:
        """อ่านไฟล์ TXT และจำลองเป็น 1 หน้า"""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        return [{"page_number": 1, "text": text, "section_title": "General"}]

    @staticmethod
    def parse_md(file_path: str) -> List[Dict[str, Any]]:
        """อ่านไฟล์ Markdown และจัดหมวดตามหัวข้อ (Headers)"""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        
        sections = []
        current_section = "Introduction"
        current_text = []
        
        for line in lines:
            if line.startswith("#"):
                if current_text:
                    sections.append({
                        "page_number": 1,
                        "text": "".join(current_text).strip(),
                        "section_title": current_section
                    })
                    current_text = []
                current_section = line.replace("#", "").strip()
            else:
                current_text.append(line)
                
        if current_text or not sections:
            sections.append({
                "page_number": 1,
                "text": "".join(current_text).strip(),
                "section_title": current_section
            })
            
        return sections

    @staticmethod
    def parse_docx(file_path: str) -> List[Dict[str, Any]]:
        """อ่านไฟล์ Word (.docx)"""
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text)
        
        # จัดข้อความเป็นท่อนเดียว จำลองหน้า 1
        text = "\n".join(full_text)
        return [{"page_number": 1, "text": text, "section_title": "Main Document"}]

    @staticmethod
    def parse_pdf(file_path: str) -> List[Dict[str, Any]]:
        """อ่านไฟล์ PDF ทีละหน้า"""
        pages_data = []
        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page_idx, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                pages_data.append({
                    "page_number": page_idx + 1,
                    "text": text,
                    "section_title": f"Page {page_idx + 1}"
                })
        return pages_data

    @classmethod
    def parse_document(cls, file_path: str) -> List[Dict[str, Any]]:
        """วิเคราะห์ประเภทไฟล์และเลือกสกัดข้อความตามรูปแบบ"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".txt":
            return cls.parse_txt(file_path)
        elif ext == ".md":
            return cls.parse_md(file_path)
        elif ext == ".docx":
            return cls.parse_docx(file_path)
        elif ext == ".pdf":
            return cls.parse_pdf(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
