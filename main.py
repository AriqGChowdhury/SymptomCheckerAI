import os
from flask import Flask, render_template, url_for, request
import base64
import jsonify
from flask import jsonify
from model import Model


app = Flask(__name__)
secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://project.db'
app.config['SECRET_KEY'] = secret_key
#app.config['SERVER_NAME'] = '127.0.0.1:5000'
port = int(os.environ.get("PORT", 5000))

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.get_json()
    user_input['Blood Pressure'] = user_input['Blood Pressure'][:-2].capitalize()
    user_input['Cholesterol Level'] = user_input['Cholesterol Level'][:-2].capitalize()
    obj = Model()
    prediction = obj.get_user_input(user_input=user_input)
    suggestion = ""
    not_tc = ['Anxiety Disorders', 'Depression', 'Bipolar Disorder', 'Obesessive-Compulsive Disorder', 'Autism Spectrum Disorder (ASD)', 'Schizophrenia']
    if int(user_input['Age']) > 65 and prediction != "['Common Cold']":
        suggestion = "See doctor as soon as possible"
    elif user_input['Blood Pressure'] == 'High' and user_input['Cholesterol Level'] == 'High':
        if user_input['Difficulty Breathing'] == 'Yes':
            suggestion = "Seek medical attention ASAP"
    else:
        if prediction[0] not in not_tc:
            suggestion = "Take over the counter medication if needed, or if preferred create appointment with primary doctor"
    
        
    return jsonify({
        "message": prediction,
        "suggestion":suggestion
                    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)


    
