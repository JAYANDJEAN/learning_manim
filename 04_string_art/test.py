import numpy as np
from scipy.sparse import csr_matrix


# 生成均值接近0的10x1矩阵
def get_csr_matrix(rows, cols, num_nonzero):
    # 生成随机非零值的位置
    nonzero_indices = np.random.choice(rows * cols, num_nonzero, replace=False)
    row_indices = nonzero_indices // cols
    col_indices = nonzero_indices % cols

    # 随机生成非零元素的值
    data = np.random.rand(num_nonzero)

    # 创建CSR格式的稀疏矩阵
    sparse_matrix = csr_matrix((data, (row_indices, col_indices)), shape=(rows, cols))

    return sparse_matrix


d = get_csr_matrix(10, 1, 10)
x = np.random.uniform(-0.1, 0.1, (10, 1))
A = get_csr_matrix(20, 10, 10)
b = get_csr_matrix(20, 1, 10)

residual = A.dot(x) - b
print(type(residual))
gradient_reg = np.where(x ** 2 < (x - 1) ** 2, x, x - 1)
# print(gradient_reg)
print(type(gradient_reg))

gradient_res = 2 * A.T.dot(residual)
print(type(gradient_res))
gradient = gradient_res + gradient_reg
print(type(gradient))
x = x - 0.1 * gradient
print(type(x))
# print(type(d))
# print(type(d.toarray()))
# print(type(c))

# print(np.sum(np.minimum(c ** 2, (c - 1) ** 2)))
