from flask import Flask, request, jsonify
import librosa
import numpy as np
import tensorflow as tf  # Replace with your ML library

app = Flask(__name__)

# Load your ML model
model = tf.keras.models.load_model('model/baby_cry_model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    if file and file.filename.endswith('.wav'):
        # Process .wav file (extract features)
        audio, sr = librosa.load(file, sr=22050)
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        mfccs_processed = np.mean(mfccs.T, axis=0)
        mfccs_processed = mfccs_processed.reshape(1, -1)

        # Predict using ML model
        prediction = model.predict(mfccs_processed)
        classes = ["hungry", "sleepy", "bellypain"]
        result = classes[np.argmax(prediction)]

        return jsonify({"prediction": result})
    
    return jsonify({"error": "Invalid file format"}), 400

if __name__ == '__main__':
    app.run(debug=True)
