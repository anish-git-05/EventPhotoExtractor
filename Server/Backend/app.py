from flask import Flask,request,jsonify,send_file
from flask_cors import CORS
import os
import sys
import shutil
import gc

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) 
sys.path.append(parent_dir)
from ML.Pipeline import ImgPipeline
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
@app.route('/upload',methods=['POST'])
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

@app.route('/process',methods=['GET'])
def process():
    try:
        os.makedirs(curated_dir,exist_ok=True)
        ImgPipeline(upload_dir,curated_dir)
        curated_photos = os.listdir(curated_dir)
        if len(curated_photos) == 0:
            return jsonify({"error": "No photos met the AI criteria."}), 400
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
        
if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port,debug=False)