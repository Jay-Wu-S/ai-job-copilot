from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.parser_service import parse_resume_file

router = APIRouter(tags=["upload"])


@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    filename = file.filename or ""
    lower_name = filename.lower()

    if not lower_name.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only .pdf files are supported."
        )

    try:
        text = await parse_resume_file(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to parse the uploaded resume file."
        )

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="The uploaded PDF does not contain readable text."
        )

    return {
        "filename": filename,
        "resume_text": text
    }