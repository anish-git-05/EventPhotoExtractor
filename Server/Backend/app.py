from flask import Flask,request,jsonify
from flask_cors import CORS
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) 
sys.path.append(parent_dir)
from ML.Pipeline import ImgPipeline
app=Flask(__name__)
CORS(app)

@app.route('/process',methods=['POST'])
def process():
    data=request.get_json()
    input_folder=data.get('inputFolder')
    output_folder=data.get('outputFolder')
    if not input_folder:
        return jsonify({'error':'Input folder is required'}),400
    if not output_folder:
        clean_input_path = os.path.normpath(os.path.abspath(input_folder))
        parent_dir = os.path.dirname(clean_input_path)
        folder_name = os.path.basename(clean_input_path)
        output_folder = os.path.join(parent_dir, f"{folder_name}_curated")
    try:
        ImgPipeline(input_folder,output_folder)
        return jsonify({'message':'Processing complete','outputFolder':output_folder}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500
    
if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port,debug=False)