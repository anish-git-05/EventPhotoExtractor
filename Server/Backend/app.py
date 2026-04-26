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
        parent_dir=os.path.dirname(os.path.abspath(input_folder))
        output_folder=os.path.join(parent_dir,'curated_album')
    try:
        ImgPipeline(input_folder,output_folder)
        return jsonify({'message':'Processing complete','outputFolder':output_folder}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500
    
if __name__=="__main__":
    app.run(debug=True,port=5000)