import gzip

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.signal import convolve2d

f = gzip.open('./MNIST/train-images-idx3-ubyte.gz', 'r')

image_size = 28
num_images = 5

f.read(16)
buf = f.read(image_size * image_size * num_images)
data = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
data = data.reshape(num_images, image_size, image_size, 1)

image = np.asarray(data[1]).squeeze()
plt.imsave('image.png', image, cmap='gray')
plt.imshow(image, cmap='gray')
plt.show()

########################################################
# Load the image and convert it to grayscale
image = Image.open("./images/0_mnist.png").convert('L')
image_array = np.array(image) / 255.

# Define a 3x3 blurring filter (kernel)
# This is a simple average filter
filter = np.array([
    [1 / 15, 1 / 25, 1 / 25, 1 / 25, 1 / 25],
    [1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25],
    [1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25],
    [1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25],
    [1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25]
])

# Apply the filter to the image
# 'boundary' defines how the array borders are handled
# 'mode' defines the size of the output array
# filtered_image_0= convolve2d(image_array[:,:,0], filter, boundary='fill', mode='same')
# filtered_image_1 = convolve2d(image_array[:,:,1], filter, boundary='fill', mode='same')
# filtered_image_2 = convolve2d(image_array[:,:,2], filter, boundary='fill', mode='same')

filtered_image = convolve2d(image_array, filter, boundary='wrap', mode='same')
# filtered_image = np.stack([filtered_image_0, filtered_image_1, filtered_image_2], axis=2)


# Convert the result back to an image
filtered_image = Image.fromarray(np.uint8(filtered_image * 255)).convert('L')

# Save or display the filtered image
filtered_image.save("./images/blur_0_mnist.png")
# filtered_image.show()  # Uncomment to directly display the image


########################################################
# Load the image and convert it to grayscale
image1 = Image.open("./images/mnist_conv1_2.png").convert('L')
image_array1 = np.array(image1) / 255.
image2 = Image.open("./images/mnist_conv2_2.png").convert('L')
image_array2 = np.array(image2) / 255.
image3 = Image.open("./images/mnist_conv3_2.png").convert('L')
image_array3 = np.array(image3) / 255.

res = (image_array1 + image_array2 + image_array3) / 3.0
res = Image.fromarray(np.uint8(res * 255)).convert('L')
res.save("./images/mnist_sum.png")

########################################################
# Load the image and convert it to grayscale
image = Image.open("./images/mnist_conv3.png").convert('L')
image_array = np.array(image) / 255.

# Define a 3x3 blurring filter (kernel)
# This is a simple average filter
filter = np.random.rand(3, 3)

# Apply the filter to the image
# 'boundary' defines how the array borders are handled
# 'mode' defines the size of the output array
# filtered_image_0= convolve2d(image_array[:,:,0], filter, boundary='fill', mode='same')
# filtered_image_1 = convolve2d(image_array[:,:,1], filter, boundary='fill', mode='same')
# filtered_image_2 = convolve2d(image_array[:,:,2], filter, boundary='fill', mode='same')

filtered_image = convolve2d(image_array, filter, boundary='fill', mode='same')
# filtered_image = np.stack([filtered_image_0, filtered_image_1, filtered_image_2], axis=2)


print(np.mean(filtered_image), np.max(filtered_image), np.min(filtered_image))
# Convert the result back to an image
filtered_image = Image.fromarray(np.uint8(filtered_image * 255)).convert('L')

# Save or display the filtered image
filtered_image.save("./images/mnist_conv3_2.png")
# filtered_image.show()  # Uncomment to directly display the image


########################################################
np.random.seed(0)


def relu(x):
    return np.maximum(0, x)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def tanh(x):
    return np.tanh(x)


def leaky_relu(x, alpha=0.3):
    return np.maximum(alpha * x, x)


def elu(x, alpha=1):
    return np.where(x > 0, x, alpha * (np.exp(x) - 1))


# Load the image and convert it to grayscale
image = Image.open("./images/0_mnist.png").convert('L')
image_array = np.array(image) / 255.

# Define a 3x3 blurring filter (kernel)
# This is a simple average filter
filter = np.random.rand(3, 3)

# Apply the filter to the image
# 'boundary' defines how the array borders are handled
# 'mode' defines the size of the output array
# filtered_image_0 = convolve2d(image_array[:,:,0], filter, boundary='fill', mode='same')
# filtered_image_1 = convolve2d(image_array[:,:,1], filter, boundary='fill', mode='same')
# filtered_image_2 = convolve2d(image_array[:,:,2], filter, boundary='fill', mode='same')

filtered_image = convolve2d(image_array, filter, boundary='fill', mode='same')
# filtered_image = np.stack([filtered_image_0, filtered_image_1, filtered_image_2], axis=2)


filtered_image = elu(filtered_image)

# Convert the result back to an image
filtered_image = Image.fromarray(np.uint8(filtered_image * 255)).convert('L')

# Save or display the filtered image
filtered_image.save("./images/mnist_elu.png")
# filtered_image.show()  # Uncomment to directly display the image

########################################################
# Load the image and convert it to grayscale
image = Image.open("./images/0_mnist.png").convert('L')
image_array = np.array(image) / 255.

# Apply average pooling to the image
pool_size = 2
pooled_image = torch.nn.functional.avg_pool2d(torch.tensor(image_array).unsqueeze(0).unsqueeze(0), pool_size)

# Convert the pooled image back to numpy array
pooled_image_array = pooled_image.squeeze().numpy()

# Display the pooled image
pooled_image = Image.fromarray((pooled_image_array * 255).astype(np.uint8))
# Save the pooled image
pooled_image.save("./images/0_mnist_pooled.png")

########################################################
# Load the image and convert it to grayscale
image = Image.open("./images/face.png").convert('L')
image_array = np.array(image) / 255.

# Define a 3x3 blurring filter (kernel)
# This is a simple average filter
filter = np.array([[0, 0, 0],
                   [-1, 0, 1],
                   [0, 0, 0]]) / 9

# Apply the filter to the image
# 'boundary' defines how the array borders are handled
# 'mode' defines the size of the output array
# filtered_image_0= convolve2d(image_array[:,:,0], filter, boundary='fill', mode='same')
# filtered_image_1 = convolve2d(image_array[:,:,1], filter, boundary='fill', mode='same')
# filtered_image_2 = convolve2d(image_array[:,:,2], filter, boundary='fill', mode='same')

filtered_image = convolve2d(image_array, filter, boundary='fill', mode='same')
# filtered_image = np.stack([filtered_image_0, filtered_image_1, filtered_image_2], axis=2)


print(np.mean(filtered_image), np.max(filtered_image), np.min(filtered_image))
# Convert the result back to an image
filtered_image = Image.fromarray(np.uint8(filtered_image * 255)).convert('L')

# Save or display the filtered image
filtered_image.save("./images/face_output.png")
# filtered_image.show()  # Uncomment to directly display the image
