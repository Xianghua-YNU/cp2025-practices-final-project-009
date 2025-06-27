"""
工具函数模块 - 通用辅助功能
"""
import os
import getpass

def get_desktop_path():
    """获取当前用户的Windows桌面路径"""
    username = getpass.getuser()
    return os.path.join("C:\\Users", username, "Desktop")

def print_simulation_params(params):
    """打印模拟参数"""
    print("\n=== 模拟参数 ===")
    print(f"计算域尺寸: {params['Lx']/1000:.1f}km × {params['Ly']/1000:.1f}km")
    print(f"网格数: {params['nx']}×{params['ny']}")
    print(f"空间步长: {params['dx']:.1f}m × {params['dy']:.1f}m")
    print(f"热扩散系数: {params['D']:.2e} m²/s")
    print(f"反应强度: {params['epsilon0']:.2e} J/kg/s")
    print(f"活化能/kB: {params['Ea_over_kB']:.2e} K")
    print(f"密度: {params['rho']:.2e} kg/m³")
    print(f"总模拟时间: {params['total_time']}秒")
