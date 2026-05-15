from flask import Flask,request,jsonify,send_file
from flask_cors import CORS
import os
import sys
import shutil
import gc
import requests
from dotenv import load_dotenv

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) 
sys.path.append(parent_dir)
from ML.Pipeline import ImgPipeline
from ML.ImgQuality import tune_quality
from ML.ImgCluster import tune_eps
app=Flask(__name__)
CORS(app)

upload_dir="uploads"
curated_dir="curated"
zip_curated="curated_album"
if os.path.exists(upload_dir):
    shutil.rmtree(upload_dir)
if os.path.exists(curated_dir):
    shutil.rmtree(curated_dir)
os.makedirs(upload_dir)
os.makedirs(curated_dir)
@app.route('/upload/files',methods=['POST'])
def upload():
    os.makedirs(upload_dir,exist_ok=True)
    data=request.files
    if 'images' not in data:
        return jsonify({'error':'No images uploaded'}),400
    files=data.getlist('images')
    for img in files:
        if img.filename:
            img.save(os.path.join(upload_dir,img.filename))
    return jsonify({'message':'Images uploaded succesfully'}),200
topk_value=8
@app.route('/upload/topk',methods=['POST'])
def upload_topk():
    data=request.json
    if not data:
        return jsonify({'message':'User did not enter topk value.'}),200
    try:
        global topk_value
        topk_value=int(data.get('topk'))
        return jsonify({'message':'topk value recieved'}),200
    except Exception as e:
        return jsonify({'error':f'Server error in recieving the top k value:\n{str(e)}'})


JSON_BIN_URL="https://api.jsonbin.io/v3/b"
BIN_ID=os.environ.get("BIN_ID")
API_KEY=os.environ.get("API_KEY")
default_hParams={"eps":0.15,"isBlurry":800,"isDark":60}
def get_hParams():
    if not BIN_ID or not API_KEY:
        return default_hParams
    try:
        headers={'X-Master-Key':API_KEY}
        response=requests.get(f"{JSON_BIN_URL}/{BIN_ID}/latest",headers=headers)
        if response.status_code==200:
            hParams={}
            hParams['eps']=response.json().get('record', {}).get('hyperparameters', {}).get('eps', 0.15)
            hParams['isBlurry']=response.json().get('record', {}).get('hyperparameters', {}).get('isBlurry', 800)
            hParams['isDark']=response.json().get('record', {}).get('hyperparameters', {}).get('isDark', 60)
            return hParams
        return default_hParams  
    except:
        return default_hParams

def save_hParams(new_hParams):
    old_hParams=get_hParams()
    if not BIN_ID or not API_KEY:
        return
    try:
        headers = {
            'Content-Type': 'application/json',
            'X-Master-Key': API_KEY
        }
        if 'eps' not in new_hParams:
            new_eps=old_hParams['eps']
        else:
            new_eps=new_hParams['eps']
        if 'isBlurry' not in new_hParams:
            new_isBlurry=old_hParams['isBlurry']
        else:
            new_isBlurry=new_hParams['isBlurry']
        if 'isDark' not in new_hParams:
            new_isDark=old_hParams['isDark']
        else:
            new_isDark=new_hParams['isDark']
        requests.put(f"{JSON_BIN_URL}/{BIN_ID}", json={"hyperparameters": {"eps": round(new_eps, 4),"isBlurry": round(new_isBlurry, 4),"isDark": round(new_isDark, 4)}}, headers=headers)
    except Exception as e:
        print(f"Cloud Save Error: {e}")

@app.route('/process',methods=['GET'])
def process():
    try:
        os.makedirs(curated_dir,exist_ok=True)
        ImgPipeline(upload_dir,curated_dir,get_hParams(),topk_value)
        curated_photos = os.listdir(curated_dir)
        if len(curated_photos) == 0:
            return jsonify({"error": "No photos met the AI criteria."}), 400
        gc.collect()
        zip_path = shutil.make_archive(zip_curated, 'zip', curated_dir)
        return send_file(
            zip_path, 
            as_attachment=True, 
            download_name='curated_album.zip',
            mimetype='application/zip'
        )
    except Exception as e:
        return jsonify({'error':str(e)}),500
    finally:
        if os.path.exists(upload_dir): shutil.rmtree(upload_dir)
        if os.path.exists(curated_dir): shutil.rmtree(curated_dir)
        os.makedirs(upload_dir,exist_ok=True)
        os.makedirs(curated_dir,exist_ok=True)
        gc.collect()

@app.route('/ping',methods=['GET'])
def ping():
    return jsonify({'Server is awake':True}),200

qualityFeedback=0
uniqueFeedback=0
@app.route('/feedback',methods=['POST'])
def handleFeedback():
    data=request.json
    global qualityFeedback
    global uniqueFeedback
    try:
        if not data:
            return jsonify({"message":"Feedback not submitted by the user"}),200
        raw_quality = data.get('quality')
        qualityFeedback = int(raw_quality) if raw_quality is not None else None
        raw_unique = data.get('uniqueness')
        uniqueFeedback = int(raw_unique) if raw_unique is not None else None
        hParamsval=get_hParams()
        old_eps=hParamsval['eps']
        old_isBlurry=hParamsval['isBlurry']
        old_isDark=hParamsval['isDark']
        if qualityFeedback is None:
            new_quality={"isBlurry":old_isBlurry,"isDark":old_isDark}
        else:
            new_quality=tune_quality(old_isBlurry=old_isBlurry,old_isDark=old_isDark,Feedback_quality=qualityFeedback)
        if uniqueFeedback is None:
            new_eps=old_eps
        else:
            new_eps=tune_eps(old_eps=old_eps,Feedback_uniqueness=uniqueFeedback)
        new_quality['eps']=new_eps
        new_hParams=new_quality
        save_hParams(new_hParams=new_hParams)
        return jsonify({"message":"Feedback recieved succesfully!"}),200
    except Exception as e:
        return jsonify({"error":f"Server error in feedback submission: {str(e)}"}),400
    

if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port,debug=False)