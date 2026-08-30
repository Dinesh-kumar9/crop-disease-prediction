import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# Load trained model
model = tf.keras.models.load_model("tomato_multiclass_model.h5")

# Class labels (must match training order)
class_names = [
    "Early_blight",
    "Healthy",
    "Late_blight",
    "Leaf_Miner",
    "Magnesium_Deficiency",
    "Nitrogen_Deficiency",
    "Potassium_Deficiency",
    "Spotted_Wilt_Virus"
]

# Image path (put image in same folder)
img_path = "test.jpg"

# Load and preprocess image
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = img_array / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Predict
predictions = model.predict(img_array)[0]

# Get top-2 predictions
top_indices = predictions.argsort()[-2:][::-1]

print("\nTop predictions:")
for idx in top_indices:
    confidence = predictions[idx] * 100
    print(f"{class_names[idx]} : {confidence:.2f}%")
