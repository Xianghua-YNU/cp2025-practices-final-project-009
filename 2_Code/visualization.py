"""
可视化模块 - 创建各种图表和动画
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as colors
import numpy as np
import os

def plot_light_curve(analysis, save_path):
    """绘制光变曲线图"""
    plt.figure(figsize=(10, 6))
    plt.plot(analysis['time_points'], analysis['luminosity'], 'r-', linewidth=2)
    plt.xlabel('时间 (秒)')
    plt.ylabel('光度 (瓦特)')
    plt.title('X射线暴光变曲线 (二维模拟)')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 检测并标记次级脉冲
    if 'secondary_pulse' in analysis:
        sp = analysis['secondary_pulse']
        plt.axvline(x=sp['time'], color='b', linestyle='--', alpha=0.7)
        plt.text(sp['time'], sp['amplitude'], ' 次级脉冲', 
                verticalalignment='bottom', fontsize=10)
    
    file_path = os.path.join(save_path, 'light_curve.png')
    plt.savefig(file_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"光变曲线图保存到: {file_path}")

def create_animation(analysis, save_path):
    """创建并保存燃烧波动画"""
    if len(analysis['snapshots']) < 5:
        print("警告: 捕获的帧数太少，无法创建动画")
        return
    
    print("创建动画...")
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 确定温度范围
    min_temp = min(np.min(snap) for snap in analysis['snapshots'])
    max_temp = max(np.max(snap) for snap in analysis['snapshots'])
    norm = colors.LogNorm(vmin=max(min_temp, 1e7), vmax=min(max_temp, 1e9))
    
    # 创建初始帧
    img = ax.imshow(analysis['snapshots'][0].T, origin='lower', 
                   extent=[0, analysis['params']['Lx']/1000, 
                   0, analysis['params']['Ly']/1000],
                   cmap='inferno', norm=norm, animated=True)
    ax.set_xlabel('x (千米)')
    ax.set_ylabel('y (千米)')
    title = ax.set_title(f'中子星热核燃烧波\n时间 = {analysis["snapshot_times"][0]:.2f} 秒')
    cbar = fig.colorbar(img, ax=ax)
    cbar.set_label('温度 (K)')

    def update(frame):
        """更新动画帧"""
        img.set_array(analysis['snapshots'][frame].T)
        title.set_text(f'中子星热核燃烧波\n时间 = {analysis["snapshot_times"][frame]:.2f} 秒')
        return [img, title]
    
    # 创建动画
    ani = FuncAnimation(fig, update, frames=len(analysis['snapshots']),
                        interval=300, blit=True)
    
    # 保存为GIF
    file_path = os.path.join(save_path, 'burning_wave_2d.gif')
    ani.save(file_path, writer='pillow', fps=5, dpi=120)
    plt.close()
    print(f"动画保存到: {file_path} (共{len(analysis['snapshots'])}帧)")

def plot_final_temperature(analysis, save_path):
    """绘制最终温度分布图"""
    plt.figure(figsize=(8, 6))
    
    # 确定温度范围
    min_temp = np.min(analysis['final_temperature'])
    max_temp = np.max(analysis['final_temperature'])
    norm = colors.LogNorm(vmin=max(min_temp, 1e7), vmax=min(max_temp, 1e9))
    
    plt.imshow(analysis['final_temperature'].T, origin='lower', 
              extent=[0, analysis['params']['Lx']/1000, 
              0, analysis['params']['Ly']/1000],
              cmap='inferno', norm=norm)
    plt.colorbar(label='温度 (K)')
    plt.xlabel('x (千米)')
    plt.ylabel('y (千米)')
    plt.title(f'最终温度分布 (t = {analysis["params"]["total_time"]:.2f} 秒)')
    
    file_path = os.path.join(save_path, 'final_temperature.png')
    plt.savefig(file_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"最终温度图保存到: {file_path}")

def plot_parameter_relations(save_path):
    """绘制参数关系图"""
    print("生成参数关系图...")
    D_values = np.logspace(3, 4, 5) * 1e-4  # 减少数据点数量
    epsilon_values = np.logspace(17, 18, 5) * 1e-4

    # 计算周期和振幅关系
    P_2d = 4.2 / np.sqrt(D_values)
    P_1d = 2.5 / np.sqrt(D_values)
    A_2d = 2.51 * np.log10(epsilon_values) - 10.2
    A_1d = 3.01 * np.log10(epsilon_values) - 12.5

    # 创建图表
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # 周期关系图
    ax1.loglog(D_values*1e4, P_2d, 'ro-', label='二维模型 (P=4.2/√D)')
    ax1.loglog(D_values*1e4, P_1d, 'bo-', label='一维模型 (P=2.5/√D)')
    ax1.set_xlabel('热扩散系数 D (cm²/s)')
    ax1.set_ylabel('振荡周期 P (秒)')
    ax1.set_title('扩散系数对振荡周期的影响')
    ax1.grid(True, which='both', linestyle='--')
    ax1.legend()

    # 振幅关系图
    ax2.semilogx(epsilon_values/1e4, A_2d, 'rs-', label='二维模型 (A=2.51log₁₀ε₀-10.2)')
    ax2.semilogx(epsilon_values/1e4, A_1d, 'bs-', label='一维模型 (A=3.01log₁₀ε₀-12.5)')
    ax2.set_xlabel('反应强度 ε₀ (10¹⁷ erg/g/s)')
    ax2.set_ylabel('振荡振幅 A')
    ax2.set_title('反应强度对振荡振幅的影响')
    ax2.grid(True, which='both', linestyle='--')
    ax2.legend()

    plt.tight_layout()
    
    file_path = os.path.join(save_path, 'parameter_relations.png')
    plt.savefig(file_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"参数关系图保存到: {file_path}")
