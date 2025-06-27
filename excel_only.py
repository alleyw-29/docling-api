# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
# from io import BytesIO
# import pandas as pd

# return {
#     "status": "parsed",
#     "filename": file.filename,
#     "rows": df.shape[0],
#     "columns": df.columns.tolist(),
#     "data": df.replace({np.nan: None}).to_dict(orient="records")
# }