"""
数据分析模块 - 计算统计量、检测特征等
"""
import numpy as np

def detect_secondary_pulse(luminosity, time_points):
    """检测光变曲线中的次级脉冲"""
    if len(luminosity) < 5:
        return None
    
    peak_idx = np.argmax(luminosity)
    if peak_idx >= len(luminosity) - 2:
        return None
    
    # 寻找主峰后的次级峰
    secondary_peak = max(luminosity[peak_idx+1:])
    if secondary_peak > 0.3 * luminosity[peak_idx]:
        secondary_idx = np.argmax(luminosity[peak_idx+1:]) + peak_idx + 1
        return {
            'time': time_points[secondary_idx],
            'amplitude': secondary_peak,
            'relative_amplitude': secondary_peak / luminosity[peak_idx]
        }
    return None

def calculate_statistics(luminosity):
    """计算光变曲线的基本统计量"""
    if not luminosity:
        return {}
    
    return {
        'max_luminosity': max(luminosity),
        'min_luminosity': min(luminosity),
        'mean_luminosity': np.mean(luminosity),
        'std_luminosity': np.std(luminosity)
    }

def analyze_simulation(results):
    """分析模拟结果"""
    analysis = {}
    
    # 计算基本统计量
    analysis['statistics'] = calculate_statistics(results['luminosity'])
    
    # 检测次级脉冲
    secondary_pulse = detect_secondary_pulse(results['luminosity'], results['time_points'])
    if secondary_pulse:
        analysis['secondary_pulse'] = secondary_pulse
    
    return analysis
