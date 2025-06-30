import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as colors
import numpy as np
import os

def plot_light_curve(time_points, luminosity, save_path):
    """绘制光变曲线图"""
    plt.figure(figsize=(10, 6))
    plt.plot(time_points, luminosity, 'r-', linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Luminosity (W)')
    plt.title('X-ray Burst Light Curve (Optimized 2D Simulation)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"光变曲线图保存到: {save_path}")

def create_animation(snapshots, snapshot_times, Lx, Ly, save_path):
    """创建燃烧波传播动画 (GIF格式)"""
    print("Creating animation...")
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 确定温度范围
    min_temp = min(np.min(snap) for snap in snapshots)
    max_temp = max(np.max(snap) for snap in snapshots)
    norm = colors.LogNorm(vmin=max(min_temp, 1e7), vmax=min(max_temp, 1e9))
    
    # 创建初始帧
    img = ax.imshow(snapshots[0].T, origin='lower', extent=[0, Lx/1000, 0, Ly/1000],
                   cmap='inferno', norm=norm, animated=True)
    ax.set_xlabel('x (km)')
    ax.set_ylabel('y (km)')
    title = ax.set_title(f'Thermonuclear Burning Wave\nTime = {snapshot_times[0]:.2f} s')
    cbar = fig.colorbar(img, ax=ax)
    cbar.set_label('Temperature (K)')
    
    def update(frame):
        img.set_array(snapshots[frame].T)
        title.set_text(f'Thermonuclear Burning Wave\nTime = {snapshot_times[frame]:.2f} s')
        return [img, title]
    
    # 确保有足够的帧创建动画
    if len(snapshots) < 10:
        print("警告: 捕获的帧数太少，无法创建流畅动画")
        print("建议: 增加总模拟时间或减少快照间隔")
    
    # 创建动画 - 使用所有帧
    ani = FuncAnimation(fig, update, frames=len(snapshots),
                        interval=300, blit=True)
    
    # 保存为GIF
    print(f"保存动画到: {save_path} (共{len(snapshots)}帧)")
    ani.save(save_path, writer='pillow', fps=5, dpi=120)
    plt.close()
    print(f"动画保存完成: {save_path}")

def plot_final_temperature(T, Lx, Ly, current_time, save_path):
    """显示最后温度分布"""
    plt.figure(figsize=(8, 6))
    
    # 确定温度范围
    min_temp = np.min(T)
    max_temp = np.max(T)
    norm = colors.LogNorm(vmin=max(min_temp, 1e7), vmax=min(max_temp, 1e9))
    
    plt.imshow(T.T, origin='lower', extent=[0, Lx/1000, 0, Ly/1000],
              cmap='inferno', norm=norm)
    plt.colorbar(label='Temperature (K)')
    plt.xlabel('x (km)')
    plt.ylabel('y (km)')
    plt.title(f'Final Temperature Distribution (t = {current_time:.2f} s)')
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"最终温度图保存到: {save_path}")

def plot_parameter_relations(param_data, save_path):
    """绘制参数关系图"""
    print("Generating parameter relations plot...")
    
    # 解包参数数据
    D_values = param_data['D_values']
    epsilon_values = param_data['epsilon_values']
    P_2d = param_data['P_2d']
    P_1d = param_data['P_1d']
    A_2d = param_data['A_2d']
    A_1d = param_data['A_1d']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 周期关系图
    ax1.loglog(D_values*1e4, P_2d, 'ro-', label='2D Model (P=4.2/√D)')
    ax1.loglog(D_values*1e4, P_1d, 'bo-', label='1D Model (P=2.5/√D)')
    ax1.set_xlabel('Thermal Diffusivity D (cm²/s)')
    ax1.set_ylabel('Oscillation Period P (s)')
    ax1.set_title('Effect of Diffusivity on Period')
    ax1.grid(True, which='both', linestyle='--')
    ax1.legend()
    
    # 振幅关系图
    ax2.semilogx(epsilon_values/1e4, A_2d, 'rs-', label='2D Model (A=2.51log₁₀ε₀-10.2)')
    ax2.semilogx(epsilon_values/1e4, A_1d, 'bs-', label='1D Model (A=3.01log₁₀ε₀-12.5)')
    ax2.set_xlabel('Reaction Strength ε₀ (10¹⁷ erg/g/s)')
    ax2.set_ylabel('Oscillation Amplitude A')
    ax2.set_title('Effect of Reaction Strength on Amplitude')
    ax2.grid(True, which='both', linestyle='--')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"参数关系图保存到: {save_path}")
