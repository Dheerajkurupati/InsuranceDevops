from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

# Load the model
import joblib
model = joblib.load('Insurance_Predictor.pkl')

@app.route('/')
def home():
    return render_template('index.html')  # Make sure you have index.html in 'templates/' folder

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form

    age = int(data['age'])
    sex = 1 if data['sex'] == 'male' else 0
    bmi = float(data['bmi'])
    children = int(data['children'])
    smoker = 1 if data['smoker'] == 'yes' else 0
    region = data['region']

    # Encode region
    region_dict = {'northeast': 0, 'northwest': 1, 'southeast': 2, 'southwest': 3}
    region_encoded = region_dict.get(region, 0)

    # Create input array
    input_features = np.array([[age, sex, bmi, children, smoker, region_encoded]])
    prediction = model.predict(input_features)[0]

    return jsonify({'prediction': round(prediction, 2)})

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)

