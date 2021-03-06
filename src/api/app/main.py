import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from tempfile import mkstemp
import shutil

import inference


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def get_root():
  return {
    'name': 'prediction API',
    'version': '1.0'
    }
    
@app.post('/predict')
def predict(image: UploadFile=File(...), diagnostics=False, searchmethod='greedy'):
  fb, name = mkstemp(suffix='.img')
  
  with open(name, 'wb') as file:
    shutil.copyfileobj(image.file, file)
  
  pred = inference.predict(name, searchmethod)
  
  result = {
    'prediction': pred
  }
  
  if(diagnostics):
    result['fileName'] = name
  
  return result
