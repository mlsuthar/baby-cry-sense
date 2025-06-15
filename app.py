import os
import numpy as np
import librosa
import joblib
import tensorflow as tf # यह लाइन रहने दें, भले ही आप इसका उपयोग न करें ताकि कोई और एरर न आए
from flask import Flask, request, render_template_string

# ✅ Load Model & Label Encoder (TEMPORARILY COMMENTED OUT FOR TESTING)
# model = tf.keras.models.load_model("best_model.h5")
# label_encoder = joblib.load("label_encoder.pkl")

# ✅ Flask App Setup
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Feature Extraction Function - Keep this, it might be used later or in a dummy prediction
def extract_features(file_path, duration=4, sr=22050, n_mels=128):
    # ... (same as before) ...
    return np.zeros((n_mels, int(sr * duration / 512)), dtype=np.float32) # Return dummy data for testing


# ✅ HTML Template (same as before)
HTML_TEMPLATE = '''
<!doctype html>
<title>Baby Cry Predictor</title>
<h2>Upload a Baby Cry .wav file</h2>
<form method=post enctype=multipart=form-data>
  <input type=file name=file accept=".wav">
  <input type=submit value=Predict>
</form>

{% if predictions %}
  <h3>🔊 Top 3 Predictions (Dummy):</h3>
  <ul>
    {% for label, prob in predictions.items() %}
      <li><strong>{{ label }}</strong>: {{ prob }}%</li>
    {% endfor %}
  </ul>
{% endif %}
'''

# ✅ Routes
@app.route('/', methods=['GET', 'POST'])
def predict():
    predictions = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename.endswith('.wav'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # features = extract_features(filepath) # Keep this for now, but it won't use the model
            # features = np.expand_dims(features, axis=-1)
            # features = np.expand_dims(features, axis=0)

            # preds = model.predict(features)[0] # COMMENT OUT THIS LINE

            # Use dummy predictions for testing
            predictions = {"Dummy Cry 1": 70.0, "Dummy Cry 2": 20.0, "Dummy Cry 3": 10.0}

    return render_template_string(HTML_TEMPLATE, predictions=predictions)

# ✅ Run App
if __name__ == '__main__':
    app.run(debug=True)
