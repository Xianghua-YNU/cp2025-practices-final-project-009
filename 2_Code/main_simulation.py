import numpy as np
import time
import os
from utils import get_desktop_path, initialize_temperature_field
from numerical_methods import compute_laplacian, apply_adiabatic_bc, compute_luminosity, calculate_time_step
from data_analysis import detect_secondary_pulse, calculate_parameter_relations
from visualization import plot_light_curve, create_animation, plot_final_temperature, plot_parameter_relations

# ================================================
# 参数设置 (优化缩短运行时间)
# ================================================
# 获取桌面路径
desktop_path = get_desktop_path()
print(f"Windows桌面路径: {desktop_path}")

# 空间参数
Lx = 50000.0   # 计算域x方向尺寸 (m)
Ly = 50000.0   # 计算域y方向尺寸 (m)
nx = 61        # x方向网格点数
ny = 61        # y方向网格点数
dx = Lx / (nx - 1)  # 空间步长 (m)
dy = Ly / (ny - 1)  # 空间步长 (m)

# 物理参数
D = 1e4 * 1e-4    # 热扩散系数 (m²/s)
epsilon0 = 5e17 * 1e-4  # 反应强度 (J/kg/s)
Ea_over_kB = 7e8   # 活化能/玻尔兹曼常数 (K)
rho = 1e9          # 密度 (kg/m³)
cp = 1e3           # 比热容 (J/kg·K)

# 时间参数
dt = 0.01          # 初始时间步长 (s)
total_time = 10.0   # 总模拟时间 (s)
safety_factor = 0.25 # CFL安全因子

# 初始条件参数
T_background = 1e7  # 背景温度 (K)
T_ignition = 2e8    # 点火温度 (K)
ignition_radius = 5 * min(dx, dy)  # 点火半径 (m)
snapshot_interval = 0.2  # 快照间隔 (s)

# ================================================
# 初始化计算域
# ================================================
T, X, Y = initialize_temperature_field(
    Lx, Ly, nx, ny, T_background, T_ignition, ignition_radius
)

# 存储光变曲线
luminosity = []
time_points = []

# 存储快照用于动画
snapshots = []
snapshot_times = []

# ================================================
# 主模拟循环
# ================================================
current_time = 0.0
next_snapshot = 0.0
frame_count = 0

print("Starting optimized simulation...")
start_time = time.time()

while current_time < total_time:
    # 计算拉普拉斯项
    laplacian = compute_laplacian(T, dx, dy)
    
    # 计算反应项
    T_safe = np.maximum(T, 1e7)
    reaction_term = epsilon0 * np.exp(-Ea_over_kB / T_safe)
    
    # 计算时间导数
    dTdt = D * laplacian + reaction_term / cp
    
    # 计算自适应时间步长
    dt = calculate_time_step(dTdt, dx, dy, D, safety_factor)
    
    # 显式欧拉时间推进
    T_new = T + dt * dTdt
    
    # 应用边界条件
    T_new = apply_adiabatic_bc(T_new)
    
    # 更新温度场
    T = T_new
    current_time += dt
    
    # 计算并存储光变曲线
    if current_time >= next_snapshot:
        L = compute_luminosity(T, epsilon0, Ea_over_kB, dx, dy, rho)
        luminosity.append(L)
        time_points.append(current_time)
        snapshots.append(T.copy())
        snapshot_times.append(current_time)
        next_snapshot += snapshot_interval
        frame_count += 1
        print(f"Time: {current_time:.2f}s, Luminosity: {L:.2e} W, Frames: {frame_count}")

# 计算执行时间
end_time = time.time()
print(f"Simulation completed in {end_time - start_time:.2f} seconds")
print(f"Number of frames captured: {len(snapshots)}")

# ================================================
# 结果可视化和分析
# ================================================
# 1. 光变曲线图
light_curve_path = os.path.join(desktop_path, 'light_curve_optimized.png')
plot_light_curve(time_points, luminosity, light_curve_path)

# 2. 燃烧波传播动画
gif_path = os.path.join(desktop_path, 'burning_wave_2d.gif')
create_animation(snapshots, snapshot_times, Lx, Ly, gif_path)

# 3. 最终温度分布图
final_temp_path = os.path.join(desktop_path, 'final_temperature.png')
plot_final_temperature(T, Lx, Ly, current_time, final_temp_path)

# 4. 参数关系图
param_data = calculate_parameter_relations()
param_path = os.path.join(desktop_path, 'parameter_relations_optimized.png')
plot_parameter_relations(param_data, param_path)

# ================================================
# 结果摘要
# ================================================
print("\n=== 模拟结果总结 ===")
print(f"总模拟时间: {current_time:.2f} 秒")
print(f"保存的帧数: {len(snapshots)}")
print(f"最大光度: {max(luminosity):.2e} 瓦特")
print(f"所有输出文件已保存到您的桌面: {desktop_path}")

# 检测次级脉冲
secondary_time = detect_secondary_pulse(luminosity, time_points)
if secondary_time:
    print(f"检测到次级脉冲于 t = {secondary_time:.2f} 秒")

print("模拟完成! 请查看桌面上的GIF动画文件")
