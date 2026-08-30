import tensorflow as tf
print(f"TensorFlow Version: {tf.__version__}")
try:
    print(f"Tensor calculation result: {tf.reduce_sum(tf.random.normal([1000, 1000]))}")
    print("SUCCESS: TensorFlow is working.")
except Exception as e:
    print(f"FAILURE: {e}")
