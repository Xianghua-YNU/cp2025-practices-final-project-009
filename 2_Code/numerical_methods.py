import numpy as np

def compute_laplacian(T, dx, dy):
    """计算二维拉普拉斯算子 (矢量化实现)"""
    laplacian = np.zeros_like(T)
    # x方向二阶导数
    laplacian[1:-1, 1:-1] += (T[2:, 1:-1] - 2*T[1:-1, 1:-1] + T[:-2, 1:-1]) / dx**2
    # y方向二阶导数
    laplacian[1:-1, 1:-1] += (T[1:-1, 2:] - 2*T[1:-1, 1:-1] + T[1:-1, :-2]) / dy**2
    return laplacian

def apply_adiabatic_bc(T):
    """应用绝热边界条件 (优化边界处理)"""
    # 边界处理 (避免单独处理角点)
    T[0, :] = T[1, :]   # 左边界
    T[-1, :] = T[-2, :] # 右边界
    T[:, 0] = T[:, 1]   # 下边界
    T[:, -1] = T[:, -2] # 上边界
    return T

def compute_luminosity(T, epsilon0, Ea_over_kB, dx, dy, rho):
    """计算光变曲线 (简化计算)"""
    # 只计算反应项 (忽略辐射冷却项)
    reaction_term = epsilon0 * np.exp(-Ea_over_kB / np.maximum(T, 1e7))
    return np.sum(reaction_term) * dx * dy * rho

def calculate_time_step(dTdt, dx, dy, D, safety_factor):
    """计算自适应时间步长"""
    max_dTdt = np.max(np.abs(dTdt))
    if max_dTdt > 0:
        return safety_factor * min(dx**2, dy**2) / (4 * D)
    return 0.01  # 默认时间步长
