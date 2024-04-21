from fastapi import APIRouter, Response, UploadFile, Form, File
from fastapi import FastAPI, HTTPException, Body, status, Depends
from connection import itemdb, db2
from models import Book
import hashlib
from gridfs import GridFS
from bson import ObjectId
from fastapi.responses import StreamingResponse, FileResponse
import os

fs = GridFS(db2, collection="credentials")
router = APIRouter(prefix="/items", tags=['Books'])
chunkdb = db2.credentials.chunks

def calculate_hash(content):
    md5 = hashlib.md5()
    md5.update(content)
    return md5.hexdigest()

def get_file_extension(file_path):
    return os.path.splitext(file_path)[1][1:]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = None)
async def upload_book(input_file: UploadFile = File(...), book_title : str = Form(...), author : str = Form(...), genre : str = Form(...)):
    try:
        content = await input_file.read()
        file_hash = calculate_hash(content)

        if itemdb.find_one({"hash" : file_hash}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate file detected.")
        
        file_id = fs.put(content, filename=input_file.filename)
        file_id_str = str(file_id)

        metadata = {
            'filename': input_file.filename,
            'book_title' : book_title,
            'author' : author,
            'genre' : genre,
            'hash': file_hash,
            'file_id': file_id_str
        }

        itemdb.insert_one(metadata)

        return {"message": "File uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Book])
async def retrieve_books():
    all_items = itemdb.find({}, {"_id" : 0 ,"book_title": 1, "author": 1, "genre": 1, "file_id" : 1})  # Retrieve only specific fields
    return [Book(**item) for item in all_items]

@router.get("/{id}", status_code=status.HTTP_200_OK, response_description = "Retrieve a single item", response_model=None)
async def retrieve_book(id: str):
    
    retrieved_item = itemdb.find_one({"file_id": id})
    # Check if the item exists
    if retrieved_item:
        # Extract the filename from the retrieved item
        filename = retrieved_item.get("filename", "UnknownFilename")

    extension = get_file_extension(filename)

    #we will transform the id back into objectid type so that we can query it in the chunks db
    convert_id = ObjectId(id)

    output_data = fs.get(convert_id).read()
    if not output_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    if extension == "pdf":
        return StreamingResponse(iter([output_data]), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={filename}"})
    elif extension =="epub":
        return StreamingResponse(iter([output_data]), media_type="application/epub+zip", headers={"Content-Disposition": f"attachment; filename={filename}"})
    else:
        return { "detail" : "oopsie, wrong extension ayy lmao" }