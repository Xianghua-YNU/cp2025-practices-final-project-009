import numpy as np

def detect_secondary_pulse(luminosity, time_points):
    """检测光变曲线中的次级脉冲"""
    if len(luminosity) > 5:
        peak_idx = np.argmax(luminosity)
        if peak_idx < len(luminosity) - 2:
            # 寻找主峰后的次级峰
            secondary_peak = max(luminosity[peak_idx+1:])
            if secondary_peak > 0.3 * luminosity[peak_idx]:
                secondary_idx = np.argmax(luminosity[peak_idx+1:]) + peak_idx + 1
                return time_points[secondary_idx]
    return None

def calculate_parameter_relations():
    """计算参数关系 (D-P和ε₀-A)"""
    D_values = np.logspace(3, 4, 5) * 1e-4  # 减少数据点数量
    epsilon_values = np.logspace(17, 18, 5) * 1e-4

    # 计算周期和振幅关系
    P_2d = 4.2 / np.sqrt(D_values)
    P_1d = 2.5 / np.sqrt(D_values)
    A_2d = 2.51 * np.log10(epsilon_values) - 10.2
    A_1d = 3.01 * np.log10(epsilon_values) - 12.5
    
    return {
        'D_values': D_values,
        'epsilon_values': epsilon_values,
        'P_2d': P_2d,
        'P_1d': P_1d,
        'A_2d': A_2d,
        'A_1d': A_1d
    }
