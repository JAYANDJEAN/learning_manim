import numpy as np
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt


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


n_sample = 10
learning_rate = 0.001
num_iterations = 10000
lambda_reg = 0.3

A = get_csr_matrix(n_sample, n_sample, int(n_sample * n_sample / 5))
b = get_csr_matrix(n_sample, 1, n_sample)
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
print(x.toarray() > 0.5)

# 绘制损失函数随迭代次数的变化曲线
plt.plot(range(num_iterations), loss_, label='loss')
plt.plot(range(num_iterations), loss_reg, label='reg')
plt.legend(loc="upper right")
plt.xlabel('num_iter')
plt.ylabel('loss')
plt.title('Loss')
plt.show()
