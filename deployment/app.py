from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__, template_folder='templates')  # Initialize the flask App
model = pickle.load(open('model/model_linreg.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    distance = float(request.form['distance'])
    surge = float(request.form['surge'])
    cab = str(request.form['cab'])

    val = [distance, surge]

    cab_name = {"UberBlack" : 0,
                "UberBlackSUV" : 1,
                "LyftLux" : 2,
                "LyftLuxBlack": 3,
                "LyftLuxBlackXL" : 4,
                "Lyft" : 5,
                "LyftXL" : 6,
                "LyftShared" : 7,
                "UberTaxi" : 8,
                "UberPool" : 9,
                "UberX": 10,
                "UberXL" : 11,
                "UberWAV" : 12}

    for i in range(0, 13):
        if cab_name[cab] == i:
            val.append(1.0)
        else:
            val.append(0.0)

    prediction = model.predict([val])
    output = round(prediction[0], 2)
    return render_template("index.html", prediction=output, distance=distance, surge=surge, cab=cab)


if __name__ == "__main__":
    app.run(debug=True)