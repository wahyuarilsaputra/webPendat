from flask import Flask,render_template,request
import numpy as np
import pickle
import os
app = Flask(__name__)

@app.route('/',methods = ['POST','GET'])
def web():
    if request.method == 'POST':
        kpr = str(request.form['kpr'])
        inp_rata = int(request.form['inp_rata'])
        pendapatan = float(request.form['pendapatan'])
        durasi = float(request.form['durasi'])
        tanggungan = float(request.form['tanggungan'])
        
        #Kategori KPR
        kpr1 = 0
        kpr2 = 0
        if(kpr == "Ya"):
            kpr1 = 0
            kpr2 = 1
        elif(kpr == "Tidak"):
            kpr1 = 1
            kpr2 = 0

        #Kategori Rata Rata
        rata1 = 0
        rata2 = 0
        rata3 = 0
        rata4 = 0
        rata5 = 0        
        if(inp_rata <= 30):
            rata1 = 1
            rata2 = 0
            rata3 = 0
            rata4 = 0
            rata5 = 0
            
        elif(inp_rata > 30 and inp_rata <= 45):
            #global rata1,rata2,rata3,rata4,rata5
            rata1 = 0
            rata2 = 1
            rata3 = 0
            rata4 = 0
            rata5 = 0

        elif(inp_rata > 45 and inp_rata <= 60):
            rata1 = 0
            rata2 = 0
            rata3 = 1
            rata4 = 0
            rata5 = 0

        elif(inp_rata > 60 and inp_rata <= 90):
            rata1 = 0
            rata2 = 0
            rata3 = 0
            rata4 = 1
            rata5 = 0

        elif(inp_rata > 90):
            rata1 = 0
            rata2 = 0
            rata3 = 0
            rata4 = 0
            rata5 = 1
        model_normalisasi_pendapatan = os.path.join('normalisasiPendapatan')
        model_pendapatan = pickle.load(open(model_normalisasi_pendapatan,'rb'))
        normal_pendapatan = model_pendapatan.transform([[pendapatan]])

        model_normalisasi_durasi = os.path.join('normalisasiDurasi')
        model_durasi = pickle.load(open(model_normalisasi_durasi,'rb'))
        normal_durasi = model_durasi.transform([[durasi]])
        
        model_normalisasi_tanggungan = os.path.join('normalisasiTanggungan')
        model_tanggungan = pickle.load(open(model_normalisasi_tanggungan,'rb'))
        normal_tanggungan = model_tanggungan.transform([[tanggungan]])

        inp = np.array([[kpr1,kpr2,rata1,rata2,rata3,rata4,rata5,normal_pendapatan,normal_durasi,normal_tanggungan]],dtype=object)
        model_path = os.path.join('bayes.pickle')
        model = pickle.load(open(model_path, 'rb'))
        prediksi = model.predict(inp)
        str_prediksi = str(prediksi)
        return render_template('index.html',hasil = str_prediksi)
    return render_template('index.html')

if __name__ == "__main__":
    app.run()



