from io import BytesIO
from fastapi import UploadFile
from pypdf import PdfReader


async def parse_pdf_resume(file: UploadFile) -> str:
    content = await file.read()
    pdf_stream = BytesIO(content)
    reader = PdfReader(pdf_stream)

    pages_text = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            pages_text.append(page_text.strip())

    return "\n\n".join(pages_text).strip()


async def parse_resume_file(file: UploadFile) -> str:
    filename = (file.filename or "").lower()

    if filename.endswith(".pdf"):
        return await parse_pdf_resume(file)

    raise ValueError("Unsupported file type. Only .pdf files are supported.")