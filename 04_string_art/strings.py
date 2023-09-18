import sys
import numpy as np
import scipy
import scipy.sparse
import scipy.sparse.linalg
from PIL import Image, ImageDraw
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt

import math
from collections import defaultdict
from bresenham import *


# https://github.com/danielvarga/string-art/tree/master

def get_csr_matrix(rows, cols, num_nonzero):
    nonzero_indices = np.random.choice(rows * cols, num_nonzero, replace=False)
    row_indices = nonzero_indices // cols
    col_indices = nonzero_indices % cols
    # data = np.random.uniform(-0.1, 0.1, num_nonzero)
    data = np.random.rand(num_nonzero)
    sparse_matrix = csr_matrix((data, (row_indices, col_indices)), shape=(rows, cols))

    return sparse_matrix


def build_arc_matrix(n, radius):
    hooks = np.array([[math.cos(np.pi * 2 * i / n),
                       math.sin(np.pi * 2 * i / n)] for i in range(n)])
    hooks = (radius * hooks).astype(int)
    edge_codes = []
    row_ind = []
    col_ind = []
    for i, ni in enumerate(hooks):
        for j, nj in enumerate(hooks[i + 1:], start=i + 1):
            edge_codes.append((i, j))
            pixels = bresenham(ni, nj).path
            edge = []
            for pixel in pixels:
                pixel_code = (pixel[1] + radius) * (radius * 2 + 1) + (pixel[0] + radius)
                edge.append(pixel_code)
            row_ind += edge
            col_ind += [len(edge_codes) - 1] * len(edge)
    sparse = csr_matrix(([0.1] * len(row_ind), (row_ind, col_ind)),
                        shape=((2 * radius + 1) * (2 * radius + 1), len(edge_codes)))
    return sparse, hooks, edge_codes


def build_image_vector(input_image_path, radius, width):
    image = Image.open(input_image_path).convert("L")
    image.thumbnail((width, width))
    image.save('original_resize.jpg')
    img = np.array(image)
    img_size = img.shape[0]
    assert img.shape[0] == img.shape[1]
    assert radius <= img_size // 2

    row_ind = []
    col_ind = []
    data = []

    for x in range(-radius, radius):
        for y in range(-radius, radius):
            data.append(float(255 - img[img_size // 2 + y, img_size // 2 + x]) / 255.0)
            pixel_code = (y + radius) * (radius * 2 + 1) + (x + radius)
            row_ind.append(pixel_code)
            col_ind.append(0)
    sparse_b = csr_matrix((data, (row_ind, col_ind)),
                          shape=((2 * radius + 1) * (2 * radius + 1), 1))

    return sparse_b


def fit(A, b, n_sample):
    learning_rate = 0.001
    num_iterations = 1000
    lambda_reg = 0.03
    x = get_csr_matrix(n_sample, 1, n_sample)

    loss_ = []
    loss_reg = []
    for i in range(num_iterations):
        residual = A.dot(x) - b
        gradient_res = 2 * A.T.dot(residual)
        x_array = x.toarray()
        gradient_reg = 2 * lambda_reg * np.where(x_array ** 2 < (x_array - 1) ** 2,
                                                 x_array,
                                                 x_array - 1)
        gradient = gradient_res + gradient_reg
        x = csr_matrix(x - learning_rate * gradient)
        loss_.append(np.linalg.norm(residual.toarray()) ** 2)
        loss_reg.append(lambda_reg * np.sum(np.minimum(x_array ** 2, (x_array - 1) ** 2)))

    print("最终的 x：")
    print(x.toarray())

    # 绘制损失函数随迭代次数的变化曲线
    plt.plot(range(num_iterations), loss_, label='loss')
    plt.plot(range(num_iterations), loss_reg, label='reg')
    plt.legend(loc="upper right")
    plt.xlabel('num_iter')
    plt.ylabel('loss')
    plt.title('Loss')
    plt.savefig('loss.jpg')


# def reconstruct(x, sparse, radius):
#     b_approx = sparse.dot(x)
#     b_image = b_approx.reshape((2 * radius + 1, 2 * radius + 1))
#     b_image = np.clip(b_image, 0, 255)
#     return b_image
#
#
# def reconstruct_and_save(x, sparse, radius, filename):
#     brightness_correction = 1.2
#     b_image = reconstruct(x * brightness_correction, sparse, radius)
#     imsave(filename, b_image)
#

def dump_arcs(solution, hooks, edge_codes, filename):
    f = open(filename, "w")
    n = len(hooks)
    print(n, file=f)
    for i, (x, y) in enumerate(hooks):
        print("%d\t%f\t%f" % (i, x, y), file=f)
    print(file=f)
    assert len(edge_codes) == len(solution)
    for (i, j), value in zip(edge_codes, solution):
        if value == 0:
            continue
        # int values are shown as ints.
        if value == int(value):
            value = int(value)
        print("%d\t%d\t%s" % (i, j, str(value)), file=f)
    f.close()


def main():
    filename, output_prefix = sys.argv[1:]

    n = 180
    radius = 250

    sparse, hooks, edge_codes = build_arc_adjecency_matrix(n, radius)
    # sparse, hooks, edge_codes = build_circle_adjecency_matrix(radius, 10)

    # square image with same center as the circle, sides are 75% of circle diameter.
    shrinkage = 0.75
    img = image(filename, int(radius * 2 * shrinkage))
    sparse_b = build_image_vector(img, radius)
    # imsave(output_prefix+"-original.png", sparse_b.todense().reshape((2*radius+1, 2*radius+1)))

    # finding the solution, a weighting of edges:
    print("solving linear system")
    # note the .todense(). for some reason the sparse version did not work.
    result = scipy.sparse.linalg.lsqr(sparse, np.array(sparse_b.todense()).flatten())
    print("done")
    # x, istop, itn, r1norm, r2norm, anorm, acond, arnorm = result
    x = result[0]

    reconstruct_and_save(x, sparse, radius, output_prefix + "-allow-negative.png")

    # negative values are clipped, they are physically unrealistic.
    x = np.clip(x, 0, 1e6)

    reconstruct_and_save(x, sparse, radius, output_prefix + "-unquantized.png")
    dump_arcs(x, hooks, edge_codes, output_prefix + "-unquantized.txt")

    # quantizing:
    quantization_level = 30  # 50 is already quite good. None means no quantization.
    # clip values larger than clip_factor times maximum.
    # (The long tail does not add too much to percieved quality.)
    clip_factor = 0.3
    if quantization_level is not None:
        max_edge_weight_orig = np.max(x)
        x_quantized = (x / np.max(x) * quantization_level).round()
        x_quantized = np.clip(x_quantized, 0, int(np.max(x_quantized) * clip_factor))
        # scale it back:
        x = x_quantized / quantization_level * max_edge_weight_orig
        dump_arcs(x_quantized, hooks, edge_codes, output_prefix + ".txt")

    reconstruct_and_save(x, sparse, radius, output_prefix + ".png")

    if quantization_level is not None:
        arc_count = 0
        total_distance = 0.0
        hist = defaultdict(int)
        for edge_code, multiplicity in enumerate(x_quantized):
            multiplicity = int(multiplicity)
            hist[multiplicity] += 1
            arc_count += multiplicity
            hook_index1, hook_index2 = edge_codes[edge_code]
            hook1, hook2 = hooks[hook_index1], hooks[hook_index2]
            distance = np.linalg.norm(hook1.astype(float) - hook2.astype(float)) / radius
            total_distance += distance * multiplicity
        for multiplicity in range(max(hist.keys()) + 1):
            print(multiplicity, hist[multiplicity])
        print("total arc count", arc_count)
        print("number of different arcs used", len(x_quantized[x_quantized > 0]))
        print("total distance (assuming a unit diameter circle)", total_distance / 2)  # unit diameter, not unit radius.


def test():
    radius = 200
    width = 500
    num_nail = 100
    filename = 'demo.png'
    sparse_arcs, hooks, edge_codes = build_arc_matrix(num_nail, radius)
    Image.fromarray((sparse_arcs[:, 0].todense() * 255)
                    .astype(np.uint8)
                    .reshape((2 * radius + 1, 2 * radius + 1))) \
        .save('lines.jpg')

    sparse_image = build_image_vector(filename, radius, width)
    Image.fromarray((sparse_image.todense() * 255)
                    .astype(np.uint8)
                    .reshape((2 * radius + 1, 2 * radius + 1))) \
        .save('original_circle.jpg')
    print("sparse_arcs shape:", sparse_arcs.shape)
    print("sparse_image shape:", sparse_image.shape)
    print("hooks shape:", hooks.shape)
    print("edge_codes shape", len(edge_codes))
    fit(sparse_arcs, sparse_image, int(num_nail * (num_nail - 1) / 2))


test()
