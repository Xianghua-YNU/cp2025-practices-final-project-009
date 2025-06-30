import os
import getpass
import numpy as np

def get_desktop_path():
    """获取当前用户的Windows桌面路径"""
    username = getpass.getuser()
    return os.path.join("C:\\Users", username, "Desktop")

def initialize_temperature_field(Lx, Ly, nx, ny, T_background, T_ignition, ignition_radius):
    """初始化温度场"""
    x = np.linspace(0, Lx, nx)
    y = np.linspace(0, Ly, ny)
    X, Y = np.meshgrid(x, y, indexing='ij')
    
    T = np.full((nx, ny), T_background, dtype=np.float64)
    center_x, center_y = Lx/2, Ly/2
    
    for i in range(nx):
        for j in range(ny):
            dist_sq = (x[i] - center_x)**2 + (y[j] - center_y)**2
            if dist_sq <= ignition_radius**2:
                T[i, j] = T_ignition
                
    return T, X, Y
