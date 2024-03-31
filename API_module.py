#this fastapi module needs package called 'uvicorn' to run the server on localhost. So first do 'pip install uvicorn'
from DLA_OCR_module import DLA_OCR
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image, PpmImagePlugin
import io
from pdf2image import convert_from_bytes
import numpy as np
from OCRmodule import OCR
import glob

#to run this fastAPI server on localhost run this API_module.py or go to terminal and inside pwc folder run 'python -m uvicorn API_module:app --host 127.0.0.1 --port 5000' and your fastAPI server will run on localhost:8000
#after running the server on localhost:8000 go to 'http://localhost:8000/docs#/' to see the swagger api docs of all written apis.


app = FastAPI()



@app.post('/upload/dla_ocr_output')
async def get_DLA_OCR_output(file: bytes = File(...)):
    input_image = Image.open(io.BytesIO(file)).convert("RGB")
    input_image = np.asarray(input_image)
    dla_ocr_obj = DLA_OCR()
    result = dla_ocr_obj.generate_extracted_json_file(input_image)
    response = JSONResponse(status_code=200, content=result)
    return response


@app.post('/upload/ocr_output')
async def get_OCR_output(file: UploadFile = File(...)):
    file1 = await file.read()
    pages = convert_from_bytes(file1, 100)
    texts = ""
    for pageNum, page in enumerate(pages):
        result = OCR.get_texts(OCR(), np.array(page))
        texts += result + '\n'
    result_dict = {'ocr_output': texts}
    response = JSONResponse(status_code=200, content=result_dict)
    return response




@app.post('/upload/doc_classification')
async def get_classification_output(file: UploadFile = File(...)):
    file1 = await file.read()
    pages = convert_from_bytes(file1, 100)
    texts = ""
    for pageNum, page in enumerate(pages):
        result = OCR.get_texts(OCR(), np.array(page))
        texts += result
    texts = texts.lower()
    wordList = texts.split(' ')
    output= doc_classifier(wordList)
    response = JSONResponse(status_code=200, content={'doc_type': output})
    return response


def doc_classifier(doc_words):
    key_word_lookup = {'agreement':['agreement'],
                       'allotment':['allotment']
                       }
    class_lookup = {'agreement':'Builder-Buyer Agreement',
                    'allotment':'Allotment Letter',
                    'invalid':'Invalid Document'
                    }
    lookup_keys = key_word_lookup.keys()
    result = 'invalid'
    for word in doc_words:
        for lookup_key in lookup_keys:
            if word in key_word_lookup[lookup_key]:
                result = lookup_key
                break
        if result!='invalid':
            break
    return class_lookup[result]





if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)



