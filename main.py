from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from io import BytesIO
import pandas as pd
from PIL import Image
import pytesseract
import numpy as np
import pdfplumber
import docx
import mimetypes

app = FastAPI()

@app.post("/docling")
async def parse_file(file: UploadFile = File(...)):
    contents = await file.read()
    filename = file.filename.lower()
    mime_type, _ = mimetypes.guess_type(filename)

    try:
        # 1. Handle Image (OCR) — based on MIME type
        if mime_type and mime_type.startswith("image"):
            img = Image.open(BytesIO(contents))
            text = pytesseract.image_to_string(img)
            return {
                "status": "parsed",
                "filename": file.filename,
                "file_type": "image",
                "text": text
            }

        # 2. Handle Excel
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(contents))
            df.replace({np.nan: None}, inplace=True)
            return {
                "status": "parsed",
                "filename": file.filename,
                "file_type": "excel",
                "rows": df.shape[0],
                "columns": df.columns.tolist(),
                "data": df.to_dict(orient="records")
            }

        # 3. Handle CSV
        elif filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(contents))
            df.replace({np.nan: None}, inplace=True)
            return {
                "status": "parsed",
                "filename": file.filename,
                "file_type": "csv",
                "rows": df.shape[0],
                "columns": df.columns.tolist(),
                "data": df.to_dict(orient="records")
            }

        # 4. Handle TXT
        elif filename.endswith(".txt"):
            text = contents.decode("utf-8")
            return {
                "status": "parsed",
                "filename": file.filename,
                "file_type": "text",
                "text": text
            }

        # 5. Handle PDF
        elif filename.endswith(".pdf"):
            text = ""
            with pdfplumber.open(BytesIO(contents)) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return {
                "status": "parsed",
                "filename": file.filename,
                "file_type": "pdf",
                "text": text.strip()
            }

        # 6. Handle DOCX
        elif filename.endswith(".docx"):
            doc = docx.Document(BytesIO(contents))
            text = "\n".join([para.text for para in doc.paragraphs])
            return {
                "status": "parsed",
                "filename": file.filename,
                "file_type": "docx",
                "text": text.strip()
            }

        else:
            raise ValueError("Unsupported file type")

    except Exception as e:
        return JSONResponse(status_code=400, content={
            "error": "Parsing failed",
            "details": str(e)
        })

@app.get("/")
def root():
    return {"message": "Smart parser is live 💡"}
