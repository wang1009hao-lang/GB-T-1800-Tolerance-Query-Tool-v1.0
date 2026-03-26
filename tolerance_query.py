# -*- coding: utf-8 -*-
"""
国标公差查询工具 (GB/T 1800)
支持孔/轴，基准尺寸，公差等级 IT01~IT18
支持轴孔配合查询
"""

import tkinter as tk
from tkinter import ttk, messagebox

# ============================================================
# 国标公差数据 (GB/T 1800.1-2009)
# 标准公差数值 (单位: μm)
# 尺寸段: (大于, 至] mm
# ============================================================

# 标准公差等级 IT01~IT18 对应各尺寸段的公差值 (μm)
IT_GRADES = {
    'IT01': [0.3, 0.4, 0.4, 0.5, 0.6, 0.6, 0.8, 1.0, 1.2, 2.0, 2.5, 3.0, 4.0],
    'IT0':  [0.5, 0.6, 0.6, 0.8, 1.0, 1.0, 1.2, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0],
    'IT1':  [0.8, 1.0, 1.0, 1.2, 1.5, 1.5, 2.0, 2.5, 3.5, 4.5, 6.0, 7.0, 8.0],
    'IT2':  [1.2, 1.5, 1.5, 2.0, 2.5, 2.5, 3.0, 4.0, 5.0, 7.0, 8.0, 9.0, 10.0],
    'IT3':  [2.0, 2.5, 2.5, 3.0, 4.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 13.0, 15.0],
    'IT4':  [3.0, 4.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0],
    'IT5':  [4.0, 5.0, 6.0, 8.0, 9.0, 11.0, 13.0, 15.0, 18.0, 20.0, 23.0, 25.0, 27.0],
    'IT6':  [6.0, 8.0, 9.0, 11.0, 13.0, 16.0, 19.0, 22.0, 25.0, 29.0, 32.0, 36.0, 40.0],
    'IT7':  [10.0, 12.0, 15.0, 18.0, 21.0, 25.0, 30.0, 35.0, 40.0, 46.0, 52.0, 57.0, 63.0],
    'IT8':  [14.0, 18.0, 22.0, 27.0, 33.0, 39.0, 46.0, 54.0, 63.0, 72.0, 81.0, 89.0, 97.0],
    'IT9':  [25.0, 30.0, 36.0, 43.0, 52.0, 62.0, 74.0, 87.0, 100.0, 115.0, 130.0, 140.0, 155.0],
    'IT10': [40.0, 48.0, 58.0, 70.0, 84.0, 100.0, 120.0, 140.0, 160.0, 185.0, 210.0, 230.0, 250.0],
    'IT11': [60.0, 75.0, 90.0, 110.0, 130.0, 160.0, 190.0, 220.0, 250.0, 290.0, 320.0, 360.0, 400.0],
    'IT12': [100.0, 120.0, 150.0, 180.0, 210.0, 250.0, 300.0, 350.0, 400.0, 460.0, 520.0, 570.0, 630.0],
    'IT13': [140.0, 180.0, 220.0, 270.0, 330.0, 390.0, 460.0, 540.0, 630.0, 720.0, 810.0, 890.0, 970.0],
    'IT14': [250.0, 300.0, 360.0, 430.0, 520.0, 620.0, 740.0, 870.0, 1000.0, 1150.0, 1300.0, 1400.0, 1550.0],
    'IT15': [400.0, 480.0, 580.0, 700.0, 840.0, 1000.0, 1200.0, 1400.0, 1600.0, 1850.0, 2100.0, 2300.0, 2500.0],
    'IT16': [600.0, 750.0, 900.0, 1100.0, 1300.0, 1600.0, 1900.0, 2200.0, 2500.0, 2900.0, 3200.0, 3600.0, 4000.0],
    'IT17': [1000.0, 1200.0, 1500.0, 1800.0, 2100.0, 2500.0, 3000.0, 3500.0, 4000.0, 4600.0, 5200.0, 5700.0, 6300.0],
    'IT18': [1400.0, 1800.0, 2200.0, 2700.0, 3300.0, 3900.0, 4600.0, 5400.0, 6300.0, 7200.0, 8100.0, 8900.0, 9700.0],
}

SIZE_RANGES = [
    (0, 3), (3, 6), (6, 10), (10, 18), (18, 30), (30, 50),
    (50, 80), (80, 120), (120, 180), (180, 250), (250, 315),
    (315, 400), (400, 500)
]

# 轴基本偏差 (es 上偏差, 单位μm) - a到h
SHAFT_ES = {
    'a': [-270, -270, -280, -290, -300, -310, -320, -340, -360, -380, -410, -440, -480],
    'b': [-140, -140, -150, -150, -160, -170, -180, -190, -200, -220, -240, -260, -280],
    'c': [-60, -70, -80, -95, -110, -120, -130, -140, -155, -170, -190, -210, -230],
    'cd': [-34, -46, -56, None, None, None, None, None, None, None, None, None, None],
    'd': [-20, -30, -40, -50, -65, -80, -100, -120, -145, -170, -190, -210, -230],
    'e': [-14, -20, -25, -32, -40, -50, -60, -72, -85, -100, -110, -125, -135],
    'ef': [-10, -14, -18, None, None, None, None, None, None, None, None, None, None],
    'f': [-6, -10, -13, -16, -20, -25, -30, -36, -43, -50, -56, -62, -68],
    'fg': [-4, -6, -8, None, None, None, None, None, None, None, None, None, None],
    'g': [-2, -4, -5, -6, -7, -9, -10, -12, -14, -15, -17, -18, -20],
    'h': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}

SHAFT_EI = {
    'js': None,
    'k': [0, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5],
    'm': [2, 4, 6, 7, 8, 9, 11, 13, 15, 17, 20, 21, 23],
    'n': [4, 8, 10, 12, 15, 17, 20, 23, 27, 31, 34, 37, 40],
    'p': [6, 12, 15, 18, 22, 26, 32, 37, 43, 50, 56, 62, 68],
    'r': [10, 15, 19, 23, 28, 34, 41, 48, 54, 63, 72, 78, 92],
    's': [14, 19, 23, 28, 35, 43, 53, 59, 71, 79, 92, 100, 108],
    't': [18, 23, 28, 33, 41, 48, 66, 75, 91, 104, 122, 134, 146],
    'u': [18, 23, 28, 33, 41, 60, 79, 94, 110, 129, 148, 166, 180],
    'v': [None, None, None, None, None, None, 85, 102, 122, 143, 165, 186, 202],
    'x': [20, 28, 34, 40, 50, 64, 94, 114, 134, 158, 182, 202, 228],
    'y': [None, None, None, None, None, None, 104, 124, 144, 172, 202, 226, 252],
    'z': [26, 35, 42, 50, 60, 80, 122, 146, 172, 202, 226, 252, 284],
}

HOLE_EI = {
    'A': [270, 270, 280, 290, 300, 310, 320, 340, 360, 380, 410, 440, 480],
    'B': [140, 140, 150, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280],
    'C': [60, 70, 80, 95, 110, 120, 130, 140, 155, 170, 190, 210, 230],
    'CD': [34, 46, 56, None, None, None, None, None, None, None, None, None, None],
    'D': [20, 30, 40, 50, 65, 80, 100, 120, 145, 170, 190, 210, 230],
    'E': [14, 20, 25, 32, 40, 50, 60, 72, 85, 100, 110, 125, 135],
    'EF': [10, 14, 18, None, None, None, None, None, None, None, None, None, None],
    'F': [6, 10, 13, 16, 20, 25, 30, 36, 43, 50, 56, 62, 68],
    'FG': [4, 6, 8, None, None, None, None, None, None, None, None, None, None],
    'G': [2, 4, 5, 6, 7, 9, 10, 12, 14, 15, 17, 18, 20],
    'H': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}

HOLE_ES = {
    'JS': None,
    'K': [0, 3, 5, 6, 8, 10, 13, 16, 18, 22, 25, 29, 33],
    'M': [2, 4, 6, 7, 8, 9, 11, 13, 15, 17, 20, 21, 23],
    'N': [4, 8, 10, 12, 15, 17, 20, 23, 27, 31, 34, 37, 40],
    'P': [6, 12, 15, 18, 22, 26, 32, 37, 43, 50, 56, 62, 68],
    'R': [10, 15, 19, 23, 28, 34, 41, 48, 54, 63, 72, 78, 92],
    'S': [14, 19, 23, 28, 35, 43, 53, 59, 71, 79, 92, 100, 108],
    'T': [18, 23, 28, 33, 41, 48, 66, 75, 91, 104, 122, 134, 146],
    'U': [18, 23, 28, 33, 41, 60, 79, 94, 110, 129, 148, 166, 180],
    'X': [20, 28, 34, 40, 50, 64, 94, 114, 134, 158, 182, 202, 228],
    'Z': [26, 35, 42, 50, 60, 80, 122, 146, 172, 202, 226, 252, 284],
}


def get_size_index(size):
    """根据基准尺寸获取尺寸段索引"""
    for i, (lo, hi) in enumerate(SIZE_RANGES):
        if lo < size <= hi:
            return i
    return None


def get_it_value(it_grade, size_idx):
    """获取标准公差值 (μm)"""
    if it_grade not in IT_GRADES:
        return None
    return IT_GRADES[it_grade][size_idx]


def query_shaft(size, deviation_code, it_grade):
    """查询轴公差带"""
    idx = get_size_index(size)
    if idx is None:
        return None, "尺寸超出范围 (0~500mm)"

    it = get_it_value(it_grade, idx)
    if it is None:
        return None, "无效的公差等级"

    code = deviation_code.lower()

    if code in SHAFT_ES:
        es = SHAFT_ES[code][idx]
        if es is None:
            return None, f"该尺寸段不支持偏差代号 {deviation_code}"
        ei = es - it
        return {'es': es, 'ei': ei, 'it': it}, None

    elif code == 'js':
        es = it / 2
        ei = -it / 2
        return {'es': es, 'ei': ei, 'it': it}, None

    elif code in SHAFT_EI:
        ei_val = SHAFT_EI[code]
        if ei_val is None:
            return None, f"偏差代号 {deviation_code} 需特殊处理"
        ei = ei_val[idx]
        if ei is None:
            return None, f"该尺寸段不支持偏差代号 {deviation_code}"
        es = ei + it
        return {'es': es, 'ei': ei, 'it': it}, None

    else:
        return None, f"不支持的偏差代号: {deviation_code}"


def query_hole(size, deviation_code, it_grade):
    """查询孔公差带"""
    idx = get_size_index(size)
    if idx is None:
        return None, "尺寸超出范围 (0~500mm)"

    it = get_it_value(it_grade, idx)
    if it is None:
        return None, "无效的公差等级"

    code = deviation_code.upper()

    if code in HOLE_EI:
        ei = HOLE_EI[code][idx]
        if ei is None:
            return None, f"该尺寸段不支持偏差代号 {deviation_code}"
        es = ei + it
        return {'ES': es, 'EI': ei, 'IT': it}, None

    elif code == 'JS':
        es = it / 2
        ei = -it / 2
        return {'ES': es, 'EI': ei, 'IT': it}, None

    elif code in HOLE_ES:
        es_val = HOLE_ES[code]
        if es_val is None:
            return None, f"偏差代号 {deviation_code} 需特殊处理"
        es = es_val[idx]
        if es is None:
            return None, f"该尺寸段不支持偏差代号 {deviation_code}"
        ei = es - it
        return {'ES': es, 'EI': ei, 'IT': it}, None

    else:
        return None, f"不支持的偏差代号: {deviation_code}"


def format_deviation(value):
    """格式化偏差值显示"""
    if value == 0:
        return "0"
    elif value > 0:
        return f"+{value:.1f}" if value != int(value) else f"+{int(value)}"
    else:
        return f"{value:.1f}" if value != int(value) else f"{int(value)}"


def analyze_fit(size, hole_dev, hole_it, shaft_dev, shaft_it):
    """分析轴孔配合"""
    hole_result, hole_err = query_hole(size, hole_dev, hole_it)
    if hole_err:
        return None, hole_err

    shaft_result, shaft_err = query_shaft(size, shaft_dev, shaft_it)
    if shaft_err:
        return None, shaft_err

    # 孔的极限尺寸
    hole_max = size + hole_result['ES'] / 1000
    hole_min = size + hole_result['EI'] / 1000

    # 轴的极限尺寸
    shaft_max = size + shaft_result['es'] / 1000
    shaft_min = size + shaft_result['ei'] / 1000

    # 计算间隙/过盈
    max_clearance = hole_max - shaft_min  # 最大间隙
    min_clearance = hole_min - shaft_max  # 最小间隙

    # 判断配合类型
    if min_clearance > 0:
        fit_type = "间隙配合"
        max_interference = 0
        min_interference = 0
    elif max_clearance < 0:
        fit_type = "过盈配合"
        max_interference = -min_clearance
        min_interference = -max_clearance
        max_clearance = 0
        min_clearance = 0
    else:
        fit_type = "过渡配合"
        max_interference = -min_clearance if min_clearance < 0 else 0
        min_interference = 0

    return {
        'hole_max': hole_max,
        'hole_min': hole_min,
        'shaft_max': shaft_max,
        'shaft_min': shaft_min,
        'max_clearance': max_clearance,
        'min_clearance': min_clearance,
        'max_interference': max_interference,
        'min_interference': min_interference,
        'fit_type': fit_type,
        'hole_result': hole_result,
        'shaft_result': shaft_result,
    }, None


# ============================================================
# GUI 界面
# ============================================================

class ToleranceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("国标公差查询工具 GB/T 1800")
        self.root.geometry("750x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f4f8')

        self.colors = {
            'bg': '#f0f4f8',
            'card': '#ffffff',
            'primary': '#2563eb',
            'text': '#1e293b',
            'text_light': '#64748b',
            'border': '#e2e8f0',
            'success': '#059669',
            'error': '#dc2626',
            'highlight': '#eff6ff',
            'warning': '#ea580c',
        }

        self.current_tab = 'single'
        self.build_ui()

    def build_ui(self):
        # 标题栏
        title_frame = tk.Frame(self.root, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text="国标公差查询工具",
            font=('Microsoft YaHei', 16, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side='left', padx=20, pady=15)

        tk.Label(
            title_frame,
            text="GB/T 1800.1-2009",
            font=('Microsoft YaHei', 9),
            bg=self.colors['primary'],
            fg='#bfdbfe'
        ).pack(side='right', padx=20, pady=20)

        # 标签页
        tab_frame = tk.Frame(self.root, bg=self.colors['bg'])
        tab_frame.pack(fill='x', padx=20, pady=(10, 0))

        self.tab_single_btn = tk.Button(
            tab_frame,
            text="单个查询",
            font=('Microsoft YaHei', 11),
            bg=self.colors['primary'],
            fg='white',
            relief='flat',
            padx=15, pady=8,
            command=self.switch_to_single
        )
        self.tab_single_btn.pack(side='left', padx=(0, 5))

        self.tab_fit_btn = tk.Button(
            tab_frame,
            text="轴孔配合",
            font=('Microsoft YaHei', 11),
            bg=self.colors['border'],
            fg=self.colors['text'],
            relief='flat',
            padx=15, pady=8,
            command=self.switch_to_fit
        )
        self.tab_fit_btn.pack(side='left')

        # 主内容区
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg'], padx=20, pady=15)
        self.main_frame.pack(fill='both', expand=True)

        self.build_single_tab()
        self.build_fit_tab()
        self.show_single_tab()

    def build_single_tab(self):
        """单个查询标签页"""
        self.single_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])

        # 输入卡片
        input_card = tk.Frame(self.single_frame, bg=self.colors['card'],
                              relief='flat', bd=1,
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        input_card.pack(fill='x', pady=(0, 12))

        tk.Label(input_card, text="查询参数", font=('Microsoft YaHei', 10, 'bold'),
                 bg=self.colors['card'], fg=self.colors['text']).grid(
            row=0, column=0, columnspan=4, sticky='w', padx=15, pady=(12, 8))

        tk.Label(input_card, text="类型:", font=('Microsoft YaHei', 10),
                 bg=self.colors['card'], fg=self.colors['text']).grid(
            row=1, column=0, sticky='w', padx=(15, 5), pady=8)

        self.type_var = tk.StringVar(value='孔')
        type_frame = tk.Frame(input_card, bg=self.colors['card'])
        type_frame.grid(row=1, column=1, sticky='w', padx=5, pady=8)

        tk.Radiobutton(type_frame, text='孔', variable=self.type_var, value='孔',
                       font=('Microsoft YaHei', 10), bg=self.colors['card'],
                       fg=self.colors['text'], activebackground=self.colors['card'],
                       command=self.on_type_change).pack(side='left', padx=(0, 15))

        tk.Radiobutton(type_frame, text='轴', variable=self.type_var, value='轴',
                       font=('Microsoft YaHei', 10), bg=self.colors['card'],
                       fg=self.colors['text'], activebackground=self.colors['card'],
                       command=self.on_type_change).pack(side='left')

        tk.Label(input_card, text="基准尺寸 (mm):", font=('Microsoft YaHei', 10),
                 bg=self.colors['card'], fg=self.colors['text']).grid(
            row=1, column=2, sticky='w', padx=(20, 5), pady=8)

        self.size_var = tk.StringVar()
        tk.Entry(input_card, textvariable=self.size_var,
                 font=('Microsoft YaHei', 11), width=10,
                 relief='solid', bd=1).grid(row=1, column=3, sticky='w', padx=(5, 15), pady=8)

        tk.Label(input_card, text="偏差代号:", font=('Microsoft YaHei', 10),
                 bg=self.colors['card'], fg=self.colors['text']).grid(
            row=2, column=0, sticky='w', padx=(15, 5), pady=8)

        self.deviation_var = tk.StringVar()
        self.deviation_combo = ttk.Combobox(input_card, textvariable=self.deviation_var,
                                             font=('Microsoft YaHei', 10), width=8,
                                             state='readonly')
        self.deviation_combo.grid(row=2, column=1, sticky='w', padx=5, pady=8)

        tk.Label(input_card, text="公差等级:", font=('Microsoft YaHei', 10),
                 bg=self.colors['card'], fg=self.colors['text']).grid(
            row=2, column=2, sticky='w', padx=(20, 5), pady=8)

        self.it_var = tk.StringVar(value='IT7')
        it_grades = ['IT01', 'IT0', 'IT1', 'IT2', 'IT3', 'IT4', 'IT5', 'IT6',
                     'IT7', 'IT8', 'IT9', 'IT10', 'IT11', 'IT12', 'IT13',
                     'IT14', 'IT15', 'IT16', 'IT17', 'IT18']
        ttk.Combobox(input_card, textvariable=self.it_var, values=it_grades,
                     font=('Microsoft YaHei', 10), width=8, state='readonly').grid(
            row=2, column=3, sticky='w', padx=(5, 15), pady=8)

        btn_frame = tk.Frame(input_card, bg=self.colors['card'])
        btn_frame.grid(row=3, column=0, columnspan=4, pady=(5, 15), padx=15)

        tk.Button(btn_frame, text="查询", font=('Microsoft YaHei', 11, 'bold'),
                  bg=self.colors['primary'], fg='white', relief='flat',
                  padx=20, pady=8, cursor='hand2',
                  command=self.query_single).pack(side='left', padx=(0, 10))

        tk.Button(btn_frame, text="清空", font=('Microsoft YaHei', 11),
                  bg=self.colors['border'], fg=self.colors['text'], relief='flat',
                  padx=20, pady=8, cursor='hand2',
                  command=self.clear_single).pack(side='left')

        # 结果卡片
        result_card = tk.Frame(self.single_frame, bg=self.colors['card'],
                               relief='flat', bd=1,
                               highlightbackground=self.colors['border'],
                               highlightthickness=1)
        result_card.pack(fill='both', expand=True)

        tk.Label(result_card, text="查询结果", font=('Microsoft YaHei', 10, 'bold'),
                 bg=self.colors['card'], fg=self.colors['text']).pack(
            anchor='w', padx=15, pady=(12, 5))

        self.result_frame = tk.Frame(result_card, bg=self.colors['highlight'],
                                      relief='flat', bd=0)
        self.result_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        tk.Label(self.result_frame, text="请输入参数后点击查询",
                 font=('Microsoft YaHei', 11), bg=self.colors['highlight'],
                 fg=self.colors['text_light']).pack(padx=20, pady=20, anchor='w')

        self.on_type_change()

    def build_fit_tab(self):
        """轴孔配合标签页"""
        self.fit_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])

        # 孔参数
        hole_card = tk.Frame(self.fit_frame, bg=self.colors['card'],
                             relief='flat', bd=1,
                             highlightbackground=self.colors['border'],
                             highlightthickness=1)
        hole_card.pack(fill='x', pady=(0, 10))

        tk.Label(hole_card, text="孔参数", font=('Microsoft YaHei', 10, 'bold'),
                 bg=self.colors['card'], fg=self.colors['text']).grid(
            row=0, column=0, columnspan=3, sticky='w', padx=15, pady=(12, 8))

        tk.Label(hole_card, text="基准尺寸 (mm):", font=('Microsoft YaHei', 10),
                 bg=self.colors['card'], fg=self.colors['text']).grid(
            row=1, column=0, sticky='w', padx=(15, 5), pady=8)

        self.fit_size_var = tk.StringVar()
        tk.Entry(hole_card, textvariable=self.fit_size_var,
                 font=('Microsoft YaHei', 11), width=10,
                 relief='solid', bd=1).grid(row=1, column=1, sticky='w', padx=5, pady=8)

        tk.Label(hole_card, text="偏差代号:", font=('Microsoft YaHei', 10),
                 bg=self.colors['card'], fg=self.colors['text']).grid(
            row=1, column=2, sticky='w', padx=(15, 5), pady=8)

        self.fit_hole_dev_var = tk.StringVar(value='H')
        self.fit_hole_dev_combo = ttk.Combobox(hole_card, textvariable=self.fit_hole_dev_var,
                                                font=('Microsoft YaHei', 10), width=8,
                                                state='readonly')
        self.fit_hole_dev_combo.grid(row=1, column=3, sticky='w', padx=5, pady=8)

        tk.Label(hole_card, text="公差等级:", font=('Microsoft YaHei', 10),
                 bg=self.colors['card'], fg=self.colors['text']).grid(
            row=2, column=0, sticky='w', padx=(15, 5), pady=8)

        self.fit_hole_it_var = tk.StringVar(value='IT7')
        it_grades = ['IT01', 'IT0', 'IT1', 'IT2', 'IT3', 'IT4', 'IT5', 'IT6',
                     'IT7', 'IT8', 'IT9', 'IT10', 'IT11', 'IT12', 'IT13',
                     'IT14', 'IT15', 'IT16', 'IT17', 'IT18']
        ttk.Combobox(hole_card, textvariable=self.fit_hole_it_var, values=it_grades,
                     font=('Microsoft YaHei', 10), width=8, state='readonly').grid(
            row=2, column=1, sticky='w', padx=5, pady=8)

        # 轴参数
        shaft_card = tk.Frame(self.fit_frame, bg=self.colors['card'],
                              relief='flat', bd=1,
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        shaft_card.pack(fill='x', pady=(0, 10))

        tk.Label(shaft_card, text="轴参数", font=('Microsoft YaHei', 10, 'bold'),
                 bg=self.colors['card'], fg=self.colors['text']).grid(
            row=0, column=0, columnspan=3, sticky='w', padx=15, pady=(12, 8))

        tk.Label(shaft_card, text="偏差代号:", font=('Microsoft YaHei', 10),
                 bg=self.colors['card'], fg=self.colors['text']).grid(
            row=1, column=0, sticky='w', padx=(15, 5), pady=8)

        self.fit_shaft_dev_var = tk.StringVar(value='h')
        self.fit_shaft_dev_combo = ttk.Combobox(shaft_card, textvariable=self.fit_shaft_dev_var,
                                                 font=('Microsoft YaHei', 10), width=8,
                                                 state='readonly')
        self.fit_shaft_dev_combo.grid(row=1, column=1, sticky='w', padx=5, pady=8)

        tk.Label(shaft_card, text="公差等级:", font=('Microsoft YaHei', 10),
                 bg=self.colors['card'], fg=self.colors['text']).grid(
            row=1, column=2, sticky='w', padx=(15, 5), pady=8)

        self.fit_shaft_it_var = tk.StringVar(value='IT6')
        ttk.Combobox(shaft_card, textvariable=self.fit_shaft_it_var, values=it_grades,
                     font=('Microsoft YaHei', 10), width=8, state='readonly').grid(
            row=1, column=3, sticky='w', padx=5, pady=8)

        # 查询按钮
        btn_frame = tk.Frame(shaft_card, bg=self.colors['card'])
        btn_frame.grid(row=2, column=0, columnspan=4, pady=(5, 15), padx=15)

        tk.Button(btn_frame, text="分析配合", font=('Microsoft YaHei', 11, 'bold'),
                  bg=self.colors['primary'], fg='white', relief='flat',
                  padx=20, pady=8, cursor='hand2',
                  command=self.analyze_fit_result).pack(side='left', padx=(0, 10))

        tk.Button(btn_frame, text="清空", font=('Microsoft YaHei', 11),
                  bg=self.colors['border'], fg=self.colors['text'], relief='flat',
                  padx=20, pady=8, cursor='hand2',
                  command=self.clear_fit).pack(side='left')

        # 结果卡片
        result_card = tk.Frame(self.fit_frame, bg=self.colors['card'],
                               relief='flat', bd=1,
                               highlightbackground=self.colors['border'],
                               highlightthickness=1)
        result_card.pack(fill='both', expand=True)

        tk.Label(result_card, text="配合分析结果", font=('Microsoft YaHei', 10, 'bold'),
                 bg=self.colors['card'], fg=self.colors['text']).pack(
            anchor='w', padx=15, pady=(12, 5))

        self.fit_result_frame = tk.Frame(result_card, bg=self.colors['highlight'],
                                          relief='flat', bd=0)
        self.fit_result_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        tk.Label(self.fit_result_frame, text="请输入参数后点击分析配合",
                 font=('Microsoft YaHei', 11), bg=self.colors['highlight'],
                 fg=self.colors['text_light']).pack(padx=20, pady=20, anchor='w')

        # 初始化偏差代号
        self.fit_hole_dev_combo['values'] = ['A', 'B', 'C', 'CD', 'D', 'E', 'EF', 'F', 'FG', 'G', 'H',
                                              'JS', 'K', 'M', 'N', 'P', 'R', 'S', 'T', 'U', 'X', 'Z']
        self.fit_shaft_dev_combo['values'] = ['a', 'b', 'c', 'cd', 'd', 'e', 'ef', 'f', 'fg', 'g', 'h',
                                               'js', 'k', 'm', 'n', 'p', 'r', 's', 't', 'u', 'v', 'x', 'y', 'z']

    def switch_to_single(self):
        """切换到单个查询"""
        self.current_tab = 'single'
        self.fit_frame.pack_forget()
        self.single_frame.pack(fill='both', expand=True)
        self.tab_single_btn.config(bg=self.colors['primary'], fg='white')
        self.tab_fit_btn.config(bg=self.colors['border'], fg=self.colors['text'])

    def switch_to_fit(self):
        """切换到轴孔配合"""
        self.current_tab = 'fit'
        self.single_frame.pack_forget()
        self.fit_frame.pack(fill='both', expand=True)
        self.tab_single_btn.config(bg=self.colors['border'], fg=self.colors['text'])
        self.tab_fit_btn.config(bg=self.colors['primary'], fg='white')

    def show_single_tab(self):
        """显示单个查询标签页"""
        self.fit_frame.pack_forget()
        self.single_frame.pack(fill='both', expand=True)

    def on_type_change(self):
        """切换孔/轴时更新偏差代号列表"""
        t = self.type_var.get()
        if t == '孔':
            codes = ['A', 'B', 'C', 'CD', 'D', 'E', 'EF', 'F', 'FG', 'G', 'H',
                     'JS', 'K', 'M', 'N', 'P', 'R', 'S', 'T', 'U', 'X', 'Z']
            self.deviation_var.set('H')
        else:
            codes = ['a', 'b', 'c', 'cd', 'd', 'e', 'ef', 'f', 'fg', 'g', 'h',
                     'js', 'k', 'm', 'n', 'p', 'r', 's', 't', 'u', 'v', 'x', 'y', 'z']
            self.deviation_var.set('h')
        self.deviation_combo['values'] = codes

    def query_single(self):
        """执行单个查询"""
        size_str = self.size_var.get().strip()
        deviation = self.deviation_var.get().strip()
        it_grade = self.it_var.get().strip()
        part_type = self.type_var.get()

        if not size_str:
            messagebox.showwarning("输入错误", "请输入基准尺寸！")
            return
        try:
            size = float(size_str)
            if size <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("输入错误", "基准尺寸必须为正数！")
            return

        if not deviation:
            messagebox.showwarning("输入错误", "请选择偏差代号！")
            return

        if part_type == '孔':
            result, error = query_hole(size, deviation, it_grade)
        else:
            result, error = query_shaft(size, deviation, it_grade)

        if error:
            self.show_error(error, self.result_frame)
            return

        self.show_result(size, deviation, it_grade, part_type, result)

    def show_result(self, size, deviation, it_grade, part_type, result):
        """显示查询结果"""
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        if part_type == '孔':
            es_key, ei_key = 'ES', 'EI'
            it_key = 'IT'
        else:
            es_key, ei_key = 'es', 'ei'
            it_key = 'it'

        it_val = result[it_key]
        es_val = result[es_key]
        ei_val = result[ei_key]

        tolerance_code = f"{size:.0f}{deviation}{it_grade.replace('IT', '')}"

        tk.Label(self.result_frame, text=f"公差带代号:  {tolerance_code}",
                 font=('Microsoft YaHei', 13, 'bold'), bg=self.colors['highlight'],
                 fg=self.colors['primary']).grid(row=0, column=0, columnspan=4,
                                                  sticky='w', padx=20, pady=(15, 8))

        headers = ['参数', '数值 (um)', '数值 (mm)', '说明']
        for col, h in enumerate(headers):
            tk.Label(self.result_frame, text=h, font=('Microsoft YaHei', 9, 'bold'),
                     bg='#dbeafe', fg=self.colors['text'], width=14, anchor='center',
                     relief='flat', bd=0, padx=5, pady=4).grid(
                row=1, column=col, padx=1, pady=1, sticky='ew')

        rows = [
            (f"标准公差 {it_grade}", f"{it_val:.1f}", f"{it_val/1000:.4f}", "公差带宽度"),
            (f"上偏差 {es_key}", format_deviation(es_val), f"{es_val/1000:+.4f}", "最大极限偏差"),
            (f"下偏差 {ei_key}", format_deviation(ei_val), f"{ei_val/1000:+.4f}", "最小极限偏差"),
        ]

        for r, (label, um, mm, desc) in enumerate(rows):
            bg = '#f8fafc' if r % 2 == 0 else 'white'
            for col, val in enumerate([label, um, mm, desc]):
                tk.Label(self.result_frame, text=val,
                         font=('Consolas', 10) if col in [1, 2] else ('Microsoft YaHei', 9),
                         bg=bg, fg=self.colors['success'] if col in [1, 2] else self.colors['text'],
                         width=14, anchor='center', relief='flat', bd=0,
                         padx=5, pady=5).grid(row=r+2, column=col, padx=1, pady=1, sticky='ew')

        max_size = size + es_val / 1000
        min_size = size + ei_val / 1000
        tk.Label(self.result_frame,
                 text=f"最大极限尺寸: {max_size:.4f} mm    最小极限尺寸: {min_size:.4f} mm",
                 font=('Microsoft YaHei', 10), bg=self.colors['highlight'],
                 fg=self.colors['text']).grid(row=5, column=0, columnspan=4,
                                               sticky='w', padx=20, pady=(10, 15))

    def analyze_fit_result(self):
        """分析轴孔配合"""
        size_str = self.fit_size_var.get().strip()
        hole_dev = self.fit_hole_dev_var.get().strip()
        hole_it = self.fit_hole_it_var.get().strip()
        shaft_dev = self.fit_shaft_dev_var.get().strip()
        shaft_it = self.fit_shaft_it_var.get().strip()

        if not size_str:
            messagebox.showwarning("输入错误", "请输入基准尺寸！")
            return
        try:
            size = float(size_str)
            if size <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("输入错误", "基准尺寸必须为正数！")
            return

        if not hole_dev or not shaft_dev:
            messagebox.showwarning("输入错误", "请选择孔和轴的偏差代号！")
            return

        result, error = analyze_fit(size, hole_dev, hole_it, shaft_dev, shaft_it)
        if error:
            self.show_error(error, self.fit_result_frame)
            return

        self.show_fit_result(size, hole_dev, hole_it, shaft_dev, shaft_it, result)

    def show_fit_result(self, size, hole_dev, hole_it, shaft_dev, shaft_it, result):
        """显示配合分析结果"""
        for widget in self.fit_result_frame.winfo_children():
            widget.destroy()

        fit_type = result['fit_type']
        fit_color = self.colors['success'] if fit_type == "间隙配合" else \
                    self.colors['error'] if fit_type == "过盈配合" else self.colors['warning']

        # 配合代号
        fit_code = f"{size:.0f}{hole_dev}{hole_it.replace('IT', '')}/{shaft_dev}{shaft_it.replace('IT', '')}"
        tk.Label(self.fit_result_frame, text=f"配合代号:  {fit_code}",
                 font=('Microsoft YaHei', 12, 'bold'), bg=self.colors['highlight'],
                 fg=self.colors['primary']).pack(anchor='w', padx=20, pady=(15, 5))

        tk.Label(self.fit_result_frame, text=f"配合类型:  {fit_type}",
                 font=('Microsoft YaHei', 12, 'bold'), bg=self.colors['highlight'],
                 fg=fit_color).pack(anchor='w', padx=20, pady=(0, 15))

        # 详细数据
        info_text = f"""孔尺寸范围:  {result['hole_max']:.4f} ~ {result['hole_min']:.4f} mm
轴尺寸范围:  {result['shaft_max']:.4f} ~ {result['shaft_min']:.4f} mm

"""

        if fit_type == "间隙配合":
            info_text += f"最大间隙:  {result['max_clearance']*1000:.1f} um\n"
            info_text += f"最小间隙:  {result['min_clearance']*1000:.1f} um"
        elif fit_type == "过盈配合":
            info_text += f"最大过盈:  {result['max_interference']*1000:.1f} um\n"
            info_text += f"最小过盈:  {result['min_interference']*1000:.1f} um"
        else:
            info_text += f"最大间隙:  {result['max_clearance']*1000:.1f} um\n"
            info_text += f"最大过盈:  {result['max_interference']*1000:.1f} um"

        tk.Label(self.fit_result_frame, text=info_text,
                 font=('Consolas', 10), bg=self.colors['highlight'],
                 fg=self.colors['text'], justify='left').pack(anchor='w', padx=20, pady=(0, 15))

    def show_error(self, msg, frame):
        """显示错误信息"""
        for widget in frame.winfo_children():
            widget.destroy()
        tk.Label(frame, text=f"错误: {msg}",
                 font=('Microsoft YaHei', 11), bg=self.colors['highlight'],
                 fg=self.colors['error']).pack(padx=20, pady=20, anchor='w')

    def clear_single(self):
        """清空单个查询"""
        self.size_var.set('')
        self.it_var.set('IT7')
        self.on_type_change()
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        tk.Label(self.result_frame, text="请输入参数后点击查询",
                 font=('Microsoft YaHei', 11), bg=self.colors['highlight'],
                 fg=self.colors['text_light']).pack(padx=20, pady=20, anchor='w')

    def clear_fit(self):
        """清空配合查询"""
        self.fit_size_var.set('')
        self.fit_hole_it_var.set('IT7')
        self.fit_shaft_it_var.set('IT6')
        for widget in self.fit_result_frame.winfo_children():
            widget.destroy()
        tk.Label(self.fit_result_frame, text="请输入参数后点击分析配合",
                 font=('Microsoft YaHei', 11), bg=self.colors['highlight'],
                 fg=self.colors['text_light']).pack(padx=20, pady=20, anchor='w')


def main():
    root = tk.Tk()
    app = ToleranceApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
