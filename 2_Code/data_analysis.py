"""
主程序模块 - 设置参数、控制模拟流程、调用其他模块
"""
import numpy as np
from numerical_methods import run_simulation
from visualization import plot_light_curve, create_animation, plot_final_temperature, plot_parameter_relations
from utils import get_desktop_path
import time

def main():
    """主函数，控制整个模拟流程"""
    print("=== 中子星热核燃烧波模拟程序 ===")
    
    # 设置模拟参数
    params = {
        'Lx': 50000.0,       # x方向尺寸 (m)
        'Ly': 50000.0,       # y方向尺寸 (m)
        'nx': 61,            # x方向网格数
        'ny': 61,            # y方向网格数
        'D': 1e4 * 1e-4,     # 热扩散系数 (m²/s)
        'epsilon0': 5e17 * 1e-4,  # 反应强度 (J/kg/s)
        'Ea_over_kB': 7e8,   # 活化能/玻尔兹曼常数 (K)
        'rho': 1e9,          # 密度 (kg/m³)
        'cp': 1e3,           # 比热容 (J/kg·K)
        'total_time': 10.0,  # 总模拟时间 (s)
        'safety_factor': 0.25,  # CFL安全因子
        'T_background': 1e7,  # 背景温度 (K)
        'T_ignition': 2e8,   # 点火温度 (K)
        'ignition_radius_factor': 5,  # 点火半径系数
        'snapshot_interval': 0.2,  # 快照间隔 (s)
        'desktop_path': get_desktop_path()  # 输出文件保存路径
    }
    
    print("\n[1/4] 运行模拟...")
    start_time = time.time()
    results = run_simulation(params)
    sim_time = time.time() - start_time
    print(f"模拟完成! 耗时: {sim_time:.2f}秒")
    
    print("\n[2/4] 分析结果...")
    analysis = {
        'luminosity': results['luminosity'],
        'time_points': results['time_points'],
        'snapshots': results['snapshots'],
        'snapshot_times': results['snapshot_times'],
        'params': params
    }
    
    print("\n[3/4] 生成可视化结果...")
    # 光变曲线图
    plot_light_curve(analysis, params['desktop_path'])
    
    # 燃烧波动画
    create_animation(analysis, params['desktop_path'])
    
    # 最终温度分布
    plot_final_temperature(analysis, params['desktop_path'])
    
    # 参数关系图
    plot_parameter_relations(params['desktop_path'])
    
    print("\n[4/4] 模拟结果摘要:")
    print(f"总模拟时间: {params['total_time']}秒")
    print(f"捕获帧数: {len(results['snapshots'])}")
    print(f"最大光度: {max(results['luminosity']):.2e}瓦特")
    
    # 检测次级脉冲
    if len(results['luminosity']) > 5:
        peak_idx = np.argmax(results['luminosity'])
        if peak_idx < len(results['luminosity']) - 2:
            secondary_peak = max(results['luminosity'][peak_idx+1:])
            if secondary_peak > 0.3 * results['luminosity'][peak_idx]:
                secondary_idx = np.argmax(results['luminosity'][peak_idx+1:]) + peak_idx + 1
                print(f"检测到次级脉冲于 t = {results['time_points'][secondary_idx]:.2f}秒")
    
    print("\n所有结果文件已保存到桌面!")

if __name__ == "__main__":
    main()
