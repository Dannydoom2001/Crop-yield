# importing Flask and other modules
from flask import Flask, request, render_template
import pickle
import joblib
import pandas as pd

RanFor = joblib.load(open('dcc_rf.pkl','rb'))

# dist_list = ['AHMEDNAGAR', 'AKOLA', 'AMRAVATI', 'AURANGABAD', 'BEED', 'BHANDARA', 'BULDHANA', 'CHANDRAPUR', 'DHULE', 'GADCHIROLI', 'GONDIA', 'HINGOLI', 'JALGAON', 'JALNA', 'KOLHAPUR', 'LATUR', 'NAGPUR', 'NANDED', 'NASHIK', 'OSMANABAD', 'PARBHANI', 'PUNE', 'SANGLI', 'SATARA', 'THANE', 'WARDHA', 'WASHIM', 'YAVATMAL']
# crop_list = ['Jowar', 'Bajra', 'Wheat']
# soil_list = ['chalky', 'clay', 'loamy', 'sandy', 'silt', 'silty']
# Flask constructor
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods=["POST"])
def upload():
    if request.method == "POST":
        district = request.form.get("district")
        soil = request.form.get("soil")
        Area = int(request.form.get("area"))
        crop = request.form.get("crop")
        district = "District:_" + district
        Crop = "Crop:_" + crop
        soil_type = "Soil_type:_" + soil
        X = ['Area', 'Soil_type:_chalky', 'Soil_type:_clay', 'Soil_type:_loamy',
             'Soil_type:_peaty', 'Soil_type:_sandy', 'Soil_type:_silt', 'Soil_type:_silty',
             'District:_AHMEDNAGAR', 'District:_AKOLA', 'District:_AMRAVATI',
             'District:_AURANGABAD', 'District:_BEED', 'District:_BHANDARA',
             'District:_BULDHANA', 'District:_CHANDRAPUR', 'District:_DHULE',
             'District:_GADCHIROLI', 'District:_GONDIA', 'District:_HINGOLI',
             'District:_JALGAON', 'District:_JALNA', 'District:_KOLHAPUR',
             'District:_LATUR', 'District:_NAGPUR', 'District:_NANDED',
             'District:_NANDURBAR', 'District:_NASHIK', 'District:_OSMANABAD',
             'District:_PARBHANI', 'District:_PUNE', 'District:_SANGLI',
             'District:_SATARA', 'District:_SOLAPUR', 'District:_THANE',
             'District:_WARDHA', 'District:_WASHIM', 'District:_YAVATMAL',
             'Crop:_Bajra', 'Crop:_Jowar', 'Crop:_Wheat']
        index_dict = dict(zip(X, range(len(X))))

        vect = {}
        for key, val in index_dict.items():
            vect[key] = 0
        try:
            vect[district] = 1
        except Exception as e:
            print("Exception occered for DISTRICT!", e)
        try:
            vect[Crop] = 1
        except Exception as e:
            print("Exception occered for CROP!")
        try:
            vect[soil_type] = 1
        except Exception as e:
            print("Exception occered for SOIL TYPE!")
        try:
            vect['Area'] = Area
        except Exception as e:
            print("Exception occered for AREA!", e)
        df = pd.DataFrame.from_records(vect, index=[0])
        crop_yield = RanFor.predict(df)[0]
        msg = "The predicted YIELD for given attributes is approximately: "+str(crop_yield)+"tons."
        return render_template('home.html', msg=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

