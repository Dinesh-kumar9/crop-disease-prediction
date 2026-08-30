
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import os

# Configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 10

# Directory Setup
BASE_DIR = "dataset_banana"
TRAIN_DIR = os.path.join(BASE_DIR, "train")

def check_structure():
    if not os.path.exists(TRAIN_DIR):
        print(f"Error: Dataset not found at {TRAIN_DIR}")
        print("Please ensure you have 'dataset_banana/train' folder populated with images.")
        return False

    
    # Check if classes exist
    classes = os.listdir(TRAIN_DIR)
    if not classes:
        print("Error: No class folders found in train directory.")
        return False
        
    print(f"Found {len(classes)} classes: {classes}")
    return True

def train_model():
    if not check_structure():
        return

    # Data Generators with Automatic Validation Split
    train_gen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2  # Use 20% of data for validation
    )

    try:
        print(f"Loading training data from {TRAIN_DIR}...")
        train_data = train_gen.flow_from_directory(
            TRAIN_DIR,
            target_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            class_mode="categorical",
            subset='training'  # Set as training data
        )

        print(f"Loading validation data from {TRAIN_DIR}...")
        val_data = train_gen.flow_from_directory(
            TRAIN_DIR,  # Use same directory
            target_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            class_mode="categorical",
            subset='validation'  # Set as validation data
        )

    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Model Architecture
    base_model = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_shape=(224, 224, 3)
    )
    
    base_model.trainable = False  # Freeze base layers for transfer learning

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    output = Dense(train_data.num_classes, activation="softmax")(x)

    model = Model(inputs=base_model.input, outputs=output)

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    print("\nStarting Training...")
    history = model.fit(
        train_data,
        validation_data=val_data,
        epochs=EPOCHS
    )

    print("\nSaving Model...")
    model.save("banana_multiclass_model.h5")
    print("Model saved as 'banana_multiclass_model.h5'")

if __name__ == "__main__":
    train_model()
