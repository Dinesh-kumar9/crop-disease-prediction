"""
scripts/train_tomato.py
Training script for the Tomato multi-class disease classifier (MobileNetV2).

Run from the project root:
    python scripts/train_tomato.py

Output: models/tomato_multiclass_model.h5
"""
import sys
from pathlib import Path

# Ensure imports resolve from project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

IMG_SIZE = (224, 224)
BATCH_SIZE = 16

train_dir = str(PROJECT_ROOT / "dataset" / "train")
val_dir   = str(PROJECT_ROOT / "dataset" / "val")
test_dir  = str(PROJECT_ROOT / "dataset" / "test")

train_gen = ImageDataGenerator(rescale=1./255)
val_gen   = ImageDataGenerator(rescale=1./255)

train_data = train_gen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

val_data = val_gen.flow_from_directory(
    val_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224,224,3)
)

base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
output = Dense(train_data.num_classes, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

model.fit(
    train_data,
    validation_data=val_data,
    epochs=5
)

model.save(str(PROJECT_ROOT / "models" / "tomato_multiclass_model.h5"))
print("Model saved to models/tomato_multiclass_model.h5")
