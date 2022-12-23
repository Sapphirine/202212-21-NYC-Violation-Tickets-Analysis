from flask import Flask,request, url_for, redirect, render_template, jsonify, session
import pandas as pd
import numpy as np
import pickle



app = Flask(__name__)

#model = pickle.load(open('model3.pkl','rb'))
model = pickle.load(open('rfc_model.pkl','rb'))

url = "https://drive.google.com/file/d/1Ot1TH8vTvXxmJha6RwVRdVR90cjsm0N1/view?usp=sharing"
url='https://drive.google.com/uc?id=' + url.split('/')[-2]

df = pd.read_csv(url)
#df = pd.read_csv('Street_dic3.csv')
dic = dict(zip(df.StreetName, df.StreetCode))

dic2 = {'NY': 4,
 'K': 2,
 'Kings': 3,
 'R': 7,
 'BX': 0,
 'Q': 5,
 'Bronx': 1,
 'Qns': 6}

dic3 = {'Monday': 0,
 'Tuesday': 1,
 'Wednesday': 2,
 'Thursday': 3,
 'Friday': 4,
 'Saturday': 5,
 'Sunday': 6}


dic4 = {1: 'Blocking an Intersection: Obstructing traffic at an intersection also known as "Blocking the Box"',
    2: 'Stopping, standing or parking where a sign, street marking, or traffic control device does not allow stopping',
    3: 'Vehicle idling in a restricted area',
    4: 'General No Parking: No parking where parking is not allowed by sign, street marking or traffic control device',
    5: 'Standing at a commuter van stop, other than temporarily for the purpose of quickly picking up or dropping off passengers',
    6: 'Misuse of agency authorized parking permit',
    7: 'Parking in a meter space for the purpose of displaying, selling, storing, or offering goods for sale',
    8: 'Parking for longer than the maximum time permitted by sign, street marking or traffic control device',
    9: 'Standing of a non-commercial vehicle in a commercial metered zone',
    10: 'Stopping, standing or parking closer than 15 feet of a fire hydrant',
    11: 'Standing or parking in a safety zone, between a safety zone and the nearest curb, or within 30 feet of points on the curb immediately opposite the ends of a safety zone',
    12: 'Standing or parking a vehicle without showing a current New York registration sticker',
    13: 'Fraudulent use of agency authorized parking permit',
    14: 'Parking in order to sell a vehicle by a person who regularly sells vehicles'}


dic5 = {1: '$115',
    2: '$115',
    3: '$115',
    4: '$250',
    5: '$65',
    6: '$65',
    7: '$65',
    8: '$65',
    9: '$50',
    10: '$115',
    11: '$115',
    12: '$65',
    13: '$65',
    14: '$65'}


def PCA_input(input1, input2, input3, input4):
    pca = np.array([[ 0.00285211, -0.92271639,  0.35675341, -0.14599089],
           [ 0.01207291,  0.37399345,  0.73673076, -0.56321483],
           [-0.02380599, -0.0933087 , -0.57393259, -0.81322085]])
    result_input = (np.array([[input1 / 805, input2 / 15, input3 / 7, input4 / 4256]]) * pca).sum(axis=1)
    return result_input

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict',methods=['POST'])
def predict():
    int_features = [x for x in request.form.values()]
    int_features[3] = dic[int_features[3]]
    int_features[2] = dic2[int_features[2]]
    int_features[0] = dic3[int_features[0]]

    final = [np.array(int_features, dtype=int)]
    print(final)
    i1, i2, i3, i4 = final[0]
    
    inp = PCA_input(i1, i2, i3, i4)
    inp = inp.reshape(1,-1)
    #final = [np.array(inp, dtype=int)]
    #final = [np.array(int_features, dtype=int)]
    #final = np.array(int_features)
    #data_unseen = pd.DataFrame([final], columns = cols)
    prediction = model.predict(inp)
    #prediction = predict_model(model, data=data_unseen, round = 0)
    prediction = int(prediction[0])
    return render_template('index.html',pred='Predicted Violation Code: {}'.format(prediction), pred2='Predicted Violation: {}'.format(dic4[prediction]), pred3='Predicted Fine: {}'.format(dic5[prediction]))



if __name__ == '__main__':
    app.run(debug=True)