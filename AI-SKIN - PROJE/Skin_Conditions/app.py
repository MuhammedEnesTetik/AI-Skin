from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
import numpy as np
import os

app = Flask(__name__)

# Dosya yükleme yolunu ayarla
UPLOAD_FOLDER = r'C:\Users\Vedat\Desktop\skin_type\Skin_Conditions\static\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Modeli yükle
model = load_model(r'C:\Users\Vedat\Desktop\skin_type\trained_tf_model.h5')

# Tahmini yapmak için gerekli fonksiyon
def predict_disease(image_path):
    # Resmi yükle
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    # Tahmin yap
    predictions = model.predict(img_array)
    class_indices = np.argmax(predictions, axis=1)[0]

    # Hastalık isimleri ve bilgileri
    diseases = ["Acne", "Carcinoma", "Eczema", "Keratosis", "Milia", "Rosacea"]
    disease_info = {
        "Acne": "Akne, cilt gözeneklerinin tıkanması sonucu ortaya çıkar.",
        "Carcinoma": "Karsinom, ciltteki kanser türlerinden biridir.",
        "Eczema": "Egzama, ciltte kaşıntı ve döküntülere yol açan bir hastalıktır.",
        "Keratosis": "Keratoz, ciltte kabarık lekelerle karakterize edilir.",
        "Milia": "Milia, cilt altında oluşan küçük beyaz kistlerdir.",
        "Rosacea": "Rozasea, yüz bölgesinde kızarıklık ve şişliklere neden olur."
    }
    
    prediction = diseases[class_indices]
    info = disease_info.get(prediction, "Cilt hastalığı hakkında bilgi bulunamadı.")
    
    return prediction, info

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Tahmin işlemini gerçekleştir
        prediction, disease_info = predict_disease(filepath)
        
        # Sonuç sayfasını render et
        return render_template('result.html', image_filename='uploads/' + filename, prediction=prediction, disease_info=disease_info)

if __name__ == '__main__':
    app.run(debug=True)
