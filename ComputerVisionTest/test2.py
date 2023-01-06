# Import TF and TF Hub libraries.
import tensorflow as tf
import tensorflow_hub as hub
import os.path

# Load the input image.
if os.path.exists("ComputerVisionTest/images/pushup.jpg"):
    print("path exists!!!!!!!!")
image_path = "ComputerVisionTest/images/pushup.jpg"
image = tf.io.read_file(image_path)
image = tf.compat.v1.image.decode_jpeg(image)
image = tf.expand_dims(image, axis=0)
# Resize and pad the image to keep the aspect ratio and fit the expected size.
image = tf.cast(tf.image.resize_with_pad(image, 256, 256), dtype=tf.int32)

# Download the model from TF Hub.
model = hub.load("https://tfhub.dev/google/movenet/singlepose/thunder/4")
movenet = model.signatures['serving_default']

# Run model inference.
outputs = movenet(image)
# Output is a [1, 1, 17, 3] tensor.
keypoints = outputs['output_0']
print(keypoints)