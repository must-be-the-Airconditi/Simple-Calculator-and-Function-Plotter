import math
import numpy as np
import matplotlib.pyplot as plt
import os
import platform
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re
from ast import literal_eval


def clear_screen():
    """清除屏幕"""
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def safe_eval_math_expr(expr, x_values, **kwargs):
    """
    安全评估数学表达式的函数，替代危险的eval
    """
    # 定义允许使用的函数
    safe_dict = {
        'x': x_values,
        'sin': np.sin,
        'cos': np.cos,
        'tan': np.tan,
        'log': np.log,
        'exp': np.exp,
        'abs': np.abs,
        'sqrt': np.sqrt,
        'pi': np.pi,
        'e': np.e,
        'arcsin': np.arcsin,
        'arccos': np.arccos,
        'arctan': np.arctan,
        'sinh': np.sinh,
        'cosh': np.cosh,
        'tanh': np.tanh,
    }
    
    # 添加额外参数
    safe_dict.update(kwargs)
    
    # 验证表达式是否包含不允许的字符
    allowed_pattern = r'^[a-zA-Z0-9_+\-*/().^, xe\[\]:\s]+$'
    if not re.match(allowed_pattern, expr):
        raise ValueError("表达式包含非法字符")
    
    # 替换表达式中的符号
    processed_expr = expr.replace('^', '**')
    
    # 编译表达式
    compiled_expr = compile(processed_expr, '<string>', 'eval')
    
    # 执行表达式，仅使用安全的命名空间
    return eval(compiled_expr, {"__builtins__": {}}, safe_dict)

def _setup_axes_style(ax):
    """设置坐标轴样式，避免重复代码"""
    ax.set_facecolor('#f8f9fa')
    
    # 绘制网格背景
    ax.grid(True, which='both', linestyle='-', linewidth=0.5, color='#e0e0e0', alpha=0.7)
    ax.minorticks_on()
    ax.grid(True, which='minor', linestyle=':', linewidth=0.3, color='#f0f0f0', alpha=0.5)
    
    # 绘制坐标轴
    ax.axhline(y=0, color='#333333', linestyle='-', linewidth=2)
    ax.axvline(x=0, color='#333333', linestyle='-', linewidth=2)
    
    # 设置边框
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # 添加标签
    ax.set_xlabel('x', fontsize=14, fontweight='bold', color='#333333')
    ax.set_ylabel('y', fontsize=14, fontweight='bold', color='#333333')
    ax.set_title('函数图像', fontsize=16, fontweight='bold', color='#2c3e50', pad=20)

def plot_function_interactive(func_str, x_min, x_max, ax=None, color_idx=0, **kwargs):
    """交互式绘制函数图像（Desmos风格）"""
    try:
        # 生成x值
        x = np.linspace(x_min, x_max, 1000)
        
        # 安全地计算y值 - 使用受限的命名空间和输入验证
        y = safe_eval_math_expr(func_str, x, **kwargs)
        
        # 验证y值的有效性
        if not isinstance(y, np.ndarray):
            raise ValueError("表达式计算结果不是有效的数组")
        if np.any(np.isnan(y)) or np.any(np.isinf(y)):
            raise ValueError("表达式在给定范围内产生无效值(NaN或Inf)")
        
        # 如果没有提供ax，创建新的图表
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')
            _setup_axes_style(ax)
            
        # 清除之前绘制的内容并重新设置样式
        ax.clear()
        _setup_axes_style(ax)
        
        # 绘制函数曲线（使用鲜艳的颜色）
        colors = ['#2d7df6', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22']
        color = colors[color_idx % len(colors)]
        ax.plot(x, y, color=color, linewidth=3, label=f'y = {func_str}', alpha=0.9)
        
        # 添加图例
        ax.legend(fontsize=12, loc='best', framealpha=0.9, edgecolor='#cccccc')
        
        if ax.get.figure() is not None:
            ax.get_figure().canvas.draw()
        
        return True
    except Exception as e:
        print(f"绘图错误: {str(e)}")
        return False

class MultiLanguageSupport:
    """多语言支持类"""
    def __init__(self):
        self.current_language = 'zh'  # 默认中文
        self.translations = {
            'zh': {
                # 窗口标题
                'window_title': '多功能计算器',
                
                # 选项卡名称
                'basic_calculator': '基本计算器',
                'function_plotter': '函数绘图',
                'expression_calculator': '表达式计算',
                
                # 基本计算器部分
                'basic_operations': '基本运算',
                'addition': '加法 (+)',
                'subtraction': '减法 (-)',
                'multiplication': '乘法 (*)',
                'division': '除法 (/)',
                'power': '幂运算 (^)',
                'square_root': '开方 (sqrt)',
                
                'input_numbers': '输入数值',
                'first_number': '第一个数字:',
                'second_number': '第二个数字:',
                
                'result_section': '结果',
                'calculate_button': '计算',
                
                # 函数绘图部分
                'function_plotting': '函数绘图',
                'function_expression': '函数表达式 (使用x作为变量):',
                'x_min': 'x最小值:',
                'x_max': 'x最大值:',
                'parameters': '参数 (格式: a=1,b=2):',
                'real_time_plotting': '实时绘制',
                'plot_function': '绘制函数',
                'stop_plotting': '停止绘制',
                
                # 表达式计算部分
                'math_expression_calculation': '数学表达式计算',
                'enter_expression': '请输入数学表达式:',
                'result_label': '结果:',
                'supported_operators': '支持的运算符: +, -, *, /, **(幂), sqrt(), sin(), cos(), tan(), log(), exp(), abs(), pi, e',
                
                # 提示信息
                'operation_selected': '已选择操作: ',
                'error': '错误',
                'select_operation': '请选择一个操作!',
                'division_by_zero': '除数不能为零!',
                'negative_sqrt': '负数不能开平方根!',
                'unknown_operation': '未知操作!',
                'invalid_number': '请输入有效的数字!',
                'calculation_error': '计算出错: ',
                'xmin_lt_xmax': 'x最小值必须小于最大值!',
                'param_format_error': '参数格式错误，请使用 a=1,b=2 格式',
                'plotting_failed': '绘图失败!',
                'invalid_chars': '表达式包含非法字符！',
                'division_by_zero_error': '除零错误!',
                'calculation_error_msg': '计算错误: ',
                'enter_function_expression': '请输入函数表达式',
                
                # 按钮文本
                'ok': '确定',
                
                # 新增：菜单项
                'language_menu': '语言',
                'chinese': '中文',
                'english': 'English',
                
                # 新增：毛玻璃效果相关
                'frosted_glass_effect': '毛玻璃效果',
                
                # 新增：关于
                'about': '关于',
                'about_message': '多功能计算器 v1.0\n支持基本计算、函数绘图和表达式计算。',
                
                # 新增：菜单栏
                'file_menu': '文件',
                'exit': '退出',
                'help_menu': '帮助',
                'about_calculator': '关于计算器',
            },
            'en': {
                # Window title
                'window_title': 'Multi-Function Calculator',
                
                # Tab names
                'basic_calculator': 'Basic Calculator',
                'function_plotter': 'Function Plotter',
                'expression_calculator': 'Expression Calculator',
                
                # Basic calculator section
                'basic_operations': 'Basic Operations',
                'addition': 'Addition (+)',
                'subtraction': 'Subtraction (-)',
                'multiplication': 'Multiplication (*)',
                'division': 'Division (/)',
                'power': 'Power (^)',
                'square_root': 'Square Root (sqrt)',
                
                'input_numbers': 'Input Numbers',
                'first_number': 'First Number:',
                'second_number': 'Second Number:',
                
                'result_section': 'Result',
                'calculate_button': 'Calculate',
                
                # Function plotting section
                'function_plotting': 'Function Plotting',
                'function_expression': 'Function Expression (use x as variable):',
                'x_min': 'X Min:',
                'x_max': 'X Max:',
                'parameters': 'Parameters (format: a=1,b=2):',
                'real_time_plotting': 'Real-time Plotting',
                'plot_function': 'Plot Function',
                'stop_plotting': 'Stop Plotting',
                
                # Expression calculation section
                'math_expression_calculation': 'Math Expression Calculation',
                'enter_expression': 'Please enter math expression:',
                'result_label': 'Result:',
                'supported_operators': 'Supported operators: +, -, *, /, **(power), sqrt(), sin(), cos(), tan(), log(), exp(), abs(), pi, e',
                
                # Messages
                'operation_selected': 'Operation Selected: ',
                'error': 'Error',
                'select_operation': 'Please select an operation!',
                'division_by_zero': 'Divisor cannot be zero!',
                'negative_sqrt': 'Cannot square root negative numbers!',
                'unknown_operation': 'Unknown operation!',
                'invalid_number': 'Please enter valid numbers!',
                'calculation_error': 'Calculation error: ',
                'xmin_lt_xmax': 'X minimum must be less than X maximum!',
                'param_format_error': 'Parameter format error, please use format like a=1,b=2',
                'plotting_failed': 'Plotting failed!',
                'invalid_chars': 'Expression contains invalid characters!',
                'division_by_zero_error': 'Division by zero error!',
                'calculation_error_msg': 'Calculation error: ',
                'enter_function_expression': 'Please enter function expression',
                
                # Button text
                'ok': 'OK',
                
                # New: Menu items
                'language_menu': 'Language',
                'chinese': '中文',
                'english': 'English',
                
                # New: Frosted glass effect
                'frosted_glass_effect': 'Frosted Glass Effect',
                
                # New: About
                'about': 'About',
                'about_message': 'Multi-Function Calculator v1.0\nSupports basic calculations, function plotting, and expression evaluation.',
                
                # New: Menu bar
                'file_menu': 'File',
                'exit': 'Exit',
                'help_menu': 'Help',
                'about_calculator': 'About Calculator',
            }
        }

    def get_text(self, key):
        """获取指定键的文本"""
        if self.current_language in self.translations:
            if key in self.translations[self.current_language]:
                return self.translations[self.current_language][key]
        # 如果找不到对应语言的翻译，则返回中文默认值
        if key in self.translations['zh']:
            return self.translations['zh'][key]
        # 如果连中文都没有，返回键本身
        return key

    def switch_language(self, lang):
        """切换语言"""
        if lang in self.translations:
            self.current_language = lang
        else:
            self.current_language = 'zh'

    def get_current_language(self):
        """获取当前语言"""
        return self.current_language


class CalculatorGUI:
    def __init__(self, root):
        self.lang_support = MultiLanguageSupport()
        self.root = root
        self.root.title(self.lang_support.get_text('window_title'))
        self.root.geometry("900x700")
        
        # 设置毛玻璃效果
        self.setup_frosted_glass_effect()
        
        # 创建菜单栏 - 确保在最开始就创建
        self.create_menubar()
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置root窗口的行列权重
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # 创建选项卡
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 基本计算器选项卡
        self.basic_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.basic_tab, text=self.lang_support.get_text('basic_calculator'))
        self.create_basic_calculator()
        
        # 函数绘图选项卡
        self.plot_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.plot_tab, text=self.lang_support.get_text('function_plotter'))
        self.create_plot_tab()
        
        # 表达式计算选项卡
        self.expr_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.expr_tab, text=self.lang_support.get_text('expression_calculator'))
        self.create_expression_tab()
        
        # 配置窗口大小调整
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
    def create_menubar(self):
        """创建菜单栏"""
        # 创建主菜单栏
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # 文件菜单
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.lang_support.get_text('file_menu'), menu=file_menu)
        file_menu.add_command(label=self.lang_support.get_text('exit'), command=self.root.quit)
        
        # 语言菜单
        lang_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.lang_support.get_text('language_menu'), menu=lang_menu)
        lang_menu.add_command(label=self.lang_support.get_text('chinese'), command=lambda: self.switch_language('zh'))
        lang_menu.add_command(label=self.lang_support.get_text('english'), command=lambda: self.switch_language('en'))

        # 帮助菜单
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.lang_support.get_text('help_menu'), menu=help_menu)
        help_menu.add_command(label=self.lang_support.get_text('about_calculator'), command=self.show_about)

    def show_about(self):
        """显示关于对话框"""
        messagebox.showinfo(
            self.lang_support.get_text('about'),
            self.lang_support.get_text('about_message')
        )

    def switch_language(self, lang):
        """切换语言"""
        self.lang_support.switch_language(lang)
        self.root.title(self.lang_support.get_text('window_title'))
        
        # 删除旧菜单栏并重新创建以更新语言
        self.root.config(menu=None)  # 先移除旧菜单
        self.create_menubar()  # 重新创建菜单
        
        # 更新选项卡文本
        self.notebook.tab(self.basic_tab, text=self.lang_support.get_text('basic_calculator'))
        self.notebook.tab(self.plot_tab, text=self.lang_support.get_text('function_plotter'))
        self.notebook.tab(self.expr_tab, text=self.lang_support.get_text('expression_calculator'))
        
        # 重新构建各个界面
        self.rebuild_basic_calculator_ui()
        self.rebuild_plot_tab_ui()
        self.rebuild_expression_tab_ui()

    def setup_frosted_glass_effect(self):
        """设置毛玻璃效果"""
        # 尝试应用毛玻璃效果，根据不同操作系统
        try:
            # 对于macOS系统，使用特定的方法实现毛玻璃效果
            if platform.system() == "Darwin":
                # 通过设置窗口属性来模拟毛玻璃效果
                self.root.configure(background="#f0f0f0")  # 设置基础背景色
                self.root.attributes('-transparent', True)
                self.root['background'] = '#f0f0f0'
            # 对于Windows系统
            elif platform.system() == "Windows":
                # Windows毛玻璃效果
                self.root.attributes("-alpha", 0.95)
                self.root.configure(background="#f0f0f0")
            else:
                # Linux或其他系统设置半透明
                self.root.configure(background="#f0f0f0")
                
            # 应用主题以改善整体外观
            style = ttk.Style()
            style.theme_use("clam")  # 使用clam主题，看起来更现代
        except Exception as e:
            # 如果设置失败，使用默认背景
            self.root.configure(background="#f0f0f0")
            print(f"毛玻璃效果设置失败: {str(e)}")
    
    def create_basic_calculator(self):
        # 基本运算按钮
        basic_frame = ttk.LabelFrame(self.basic_tab, text=self.lang_support.get_text('basic_operations'), padding=10)
        basic_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # 设置毛玻璃样式的frame
        basic_frame.configure(relief='raised', borderwidth=2)
        
        operations = [
            (self.lang_support.get_text('addition'), "+"),
            (self.lang_support.get_text('subtraction'), "-"),
            (self.lang_support.get_text('multiplication'), "*"),
            (self.lang_support.get_text('division'), "/"),
            (self.lang_support.get_text('power'), "**"),
            (self.lang_support.get_text('square_root'), "sqrt")
        ]
        
        row_idx = 0
        col_idx = 0
        for op_text, op_cmd in operations:
            btn = ttk.Button(basic_frame, text=op_text, 
                            command=lambda cmd=op_cmd: self.select_operation(cmd))
            btn.grid(row=row_idx, column=col_idx, padx=5, pady=5, sticky=(tk.W, tk.E))
            col_idx += 1
            if col_idx > 2:  # 每行最多3个按钮
                col_idx = 0
                row_idx += 1
        
        # 输入区域
        input_frame = ttk.LabelFrame(self.basic_tab, text=self.lang_support.get_text('input_numbers'), padding=10)
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        input_frame.configure(relief='raised', borderwidth=2)
        
        ttk.Label(input_frame, text=self.lang_support.get_text('first_number')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.num1_entry = ttk.Entry(input_frame, width=20)
        self.num1_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text=self.lang_support.get_text('second_number')).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.num2_entry = ttk.Entry(input_frame, width=20)
        self.num2_entry.grid(row=1, column=1, padx=5, pady=2)
        
        # 结果显示
        result_frame = ttk.LabelFrame(self.basic_tab, text=self.lang_support.get_text('result_section'), padding=10)
        result_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        result_frame.configure(relief='raised', borderwidth=2)
        
        self.result_var = tk.StringVar()
        self.result_label = ttk.Label(result_frame, textvariable=self.result_var, 
                                     font=("Arial", 14, "bold"))
        self.result_label.grid(row=0, column=0, padx=5, pady=5)
        
        # 计算按钮
        calc_btn = ttk.Button(result_frame, text=self.lang_support.get_text('calculate_button'), command=self.calculate)
        calc_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # 当前操作
        self.operation = None
    
    def rebuild_basic_calculator_ui(self):
        """重建基本计算器界面"""
        # 清除现有组件
        for widget in self.basic_tab.winfo_children():
            widget.destroy()
        
        # 重新创建界面
        self.create_basic_calculator()

    def select_operation(self, op):
        self.operation = op
        messagebox.showinfo(self.lang_support.get_text('operation_selected') + op, 
                           self.lang_support.get_text('operation_selected') + op)
        
    def calculate(self):
        try:
            if not self.operation:
                messagebox.showerror(self.lang_support.get_text('error'), self.lang_support.get_text('select_operation'))
                return
                
            num1 = float(self.num1_entry.get())
            if self.operation != "sqrt":
                num2 = float(self.num2_entry.get())
            
            if self.operation == "+":
                result = num1 + num2
            elif self.operation == "-":
                result = num1 - num2
            elif self.operation == "*":
                result = num1 * num2
            elif self.operation == "/":
                if num2 == 0:
                    messagebox.showerror(self.lang_support.get_text('error'), self.lang_support.get_text('division_by_zero'))
                    return
                result = num1 / num2
            elif self.operation == "**":
                result = num1 ** num2
            elif self.operation == "sqrt":
                if num1 < 0:
                    messagebox.showerror(self.lang_support.get_text('error'), self.lang_support.get_text('negative_sqrt'))
                    return
                result = math.sqrt(num1)
            else:
                messagebox.showerror(self.lang_support.get_text('error'), self.lang_support.get_text('unknown_operation'))
                return
                
            self.result_var.set(str(result))
            
        except ValueError:
            messagebox.showerror(self.lang_support.get_text('error'), self.lang_support.get_text('invalid_number'))
        except Exception as e:
            messagebox.showerror(self.lang_support.get_text('error'), self.lang_support.get_text('calculation_error') + str(e))
    
    def create_plot_tab(self):
        # 函数绘图界面
        plot_frame = ttk.LabelFrame(self.plot_tab, text=self.lang_support.get_text('function_plotting'), padding=10)
        plot_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        plot_frame.configure(relief='raised', borderwidth=2)
        
        # 左侧控制面板
        control_frame = ttk.Frame(plot_frame)
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        ttk.Label(control_frame, text=self.lang_support.get_text('function_expression')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.func_entry = ttk.Entry(control_frame, width=30)
        self.func_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(control_frame, text=self.lang_support.get_text('x_min')).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.xmin_entry = ttk.Entry(control_frame, width=15)
        self.xmin_entry.insert(0, "-10")
        self.xmin_entry.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        
        ttk.Label(control_frame, text=self.lang_support.get_text('x_max')).grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.xmax_entry = ttk.Entry(control_frame, width=15)
        self.xmax_entry.insert(0, "10")
        self.xmax_entry.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)
        
        # 参数输入
        ttk.Label(control_frame, text=self.lang_support.get_text('parameters')).grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.params_entry = ttk.Entry(control_frame, width=30)
        self.params_entry.grid(row=3, column=1, padx=5, pady=2)
        
        # 实时绘制复选框
        self.real_time_var = tk.BooleanVar()
        self.real_time_check = ttk.Checkbutton(control_frame, text=self.lang_support.get_text('real_time_plotting'), 
                                              variable=self.real_time_var, 
                                              command=self.toggle_real_time_plotting)
        self.real_time_check.grid(row=4, column=0, columnspan=2, pady=5)
        
        # 绘图按钮
        self.plot_btn = ttk.Button(control_frame, text=self.lang_support.get_text('plot_function'), command=self.plot_function)
        self.plot_btn.grid(row=5, column=0, columnspan=2, pady=10)
        
        # 创建matplotlib图形
        try:
            import matplotlib.backends.backend_tkagg as tkagg
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            from matplotlib.figure import Figure
            
            # 右侧图形显示区域
            self.fig = Figure(figsize=(6, 5), dpi=100, facecolor='#f8f9fa')
            self.ax = self.fig.add_subplot(111)
            self.ax.set_facecolor('#f8f9fa')
            
            # 设置图形样式
            self.ax.grid(True, which='both', linestyle='-', linewidth=0.5, color='#e0e0e0', alpha=0.7)
            self.ax.minorticks_on()
            self.ax.grid(True, which='minor', linestyle=':', linewidth=0.3, color='#f0f0f0', alpha=0.5)
            self.ax.axhline(y=0, color='#333333', linestyle='-', linewidth=2)
            self.ax.axvline(x=0, color='#333333', linestyle='-', linewidth=2)
            
            for spine in self.ax.spines.values():
                spine.set_visible(False)
            
            self.ax.set_xlabel('x', fontsize=14, fontweight='bold', color='#333333')
            self.ax.set_ylabel('y', fontsize=14, fontweight='bold', color='#333333')
            self.ax.set_title(self.lang_support.get_text('function_plotting'), fontsize=16, fontweight='bold', color='#2c3e50', pad=20)
            
            canvas_frame = ttk.Frame(plot_frame)
            canvas_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
            
            self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            
            # 添加matplotlib导航工具栏
            from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
            toolbar_frame = ttk.Frame(canvas_frame)
            toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
            toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
            toolbar.update()
            
        except ImportError:
            messagebox.showwarning("警告", "无法导入matplotlib图形后端，将无法显示实时图形")
            self.canvas = None
        
        # 配置权重以便图形能够缩放
        plot_frame.columnconfigure(1, weight=1)
        plot_frame.rowconfigure(0, weight=1)
        
        # 绑定事件到输入框，实现实时绘制
        self.plot_after_id = None  # 用于存储after方法的ID，以便取消之前的请求
        self.func_entry.bind('<KeyRelease>', self.on_input_change)
        self.xmin_entry.bind('<KeyRelease>', self.on_input_change)
        self.xmax_entry.bind('<KeyRelease>', self.on_input_change)
        self.params_entry.bind('<KeyRelease>', self.on_input_change)
    
    def rebuild_plot_tab_ui(self):
        """重建绘图选项卡界面"""
        # 清除现有组件
        for widget in self.plot_tab.winfo_children():
            widget.destroy()
        
        # 重新创建界面
        self.create_plot_tab()

    def on_input_change(self, event=None):
        """当输入框内容发生变化时调用此方法"""
        if self.real_time_var.get():  # 只有在实时绘制启用时才更新
            # 取消之前的计划绘图任务
            if self.plot_after_id:
                self.root.after_cancel(self.plot_after_id)
            
            # 计划一个新的绘图任务，延迟500毫秒执行，避免过于频繁的更新
            self.plot_after_id = self.root.after(500, self.update_plot)
    
    def toggle_real_time_plotting(self):
        """切换实时绘制状态"""
        if self.real_time_var.get():
            self.plot_btn.config(text=self.lang_support.get_text('stop_plotting'))
            self.update_plot()  # 立即更新一次
        else:
            self.plot_btn.config(text=self.lang_support.get_text('plot_function'))
            # 取消可能存在的待执行的绘图任务
            if self.plot_after_id:
                self.root.after_cancel(self.plot_after_id)
    
    def update_plot(self):
        """更新函数图像"""
        try:
            func_str = self.func_entry.get().strip()
            if not func_str:
                # 如果表达式为空，清空图形
                if self.ax:
                    self.ax.clear()
                    self.ax.set_title(self.lang_support.get_text('enter_function_expression'), fontsize=16, fontweight='bold', color='#2c3e50', pad=20)
                    self.canvas.draw()
                return
                
            x_min = float(self.xmin_entry.get())
            x_max = float(self.xmax_entry.get())
            
            if x_min >= x_max:
                messagebox.showerror(self.lang_support.get_text('error'), self.lang_support.get_text('xmin_lt_xmax'))
                return
            
            # 解析参数
            params = {}
            param_str = self.params_entry.get().strip()
            if param_str:
                try:
                    for item in param_str.split(','):
                        if '=' in item:
                            key, value = item.split('=', 1)  # 分割键值对
                            params[key.strip()] = float(value.strip())
                except ValueError:
                    messagebox.showerror(self.lang_support.get_text('error'), self.lang_support.get_text('param_format_error'))
                    return
            
            # 尝试绘图
            success = plot_function_interactive(func_str, x_min, x_max, ax=self.ax, **params)
            
            if success:
                self.canvas.draw()
            else:
                # 如果绘图失败但处于实时模式下，不显示错误消息框，避免频繁弹窗
                if not self.real_time_var.get():
                    messagebox.showerror(self.lang_support.get_text('error'), self.lang_support.get_text('plotting_failed'))
                
        except ValueError:
            # 如果输入无效值但处于实时模式下，不显示错误消息框，避免频繁弹窗
            if not self.real_time_var.get():
                messagebox.showerror(self.lang_support.get_text('error'), self.lang_support.get_text('invalid_number'))
        except Exception as e:
            # 如果出现其他错误但处于实时模式下，不显示错误消息框，避免频繁弹窗
            if not self.real_time_var.get():
                messagebox.showerror(self.lang_support.get_text('error'), self.lang_support.get_text('calculation_error_msg') + str(e))
    
    def plot_function(self):
        """绘制函数 - 保持原始功能，供非实时模式使用"""
        if self.real_time_var.get():
            # 如果实时绘制被启用，点击按钮应该停止实时绘制
            self.real_time_var.set(False)
            self.plot_btn.config(text=self.lang_support.get_text('plot_function'))
        else:
            # 否则执行单次绘图
            self.update_plot()
                
    def create_expression_tab(self):
        # 表达式计算界面
        expr_frame = ttk.LabelFrame(self.expr_tab, text=self.lang_support.get_text('math_expression_calculation'), padding=10)
        expr_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        expr_frame.configure(relief='raised', borderwidth=2)
        
        ttk.Label(expr_frame, text=self.lang_support.get_text('enter_expression')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.expr_entry = ttk.Entry(expr_frame, width=40)
        self.expr_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        expr_calc_btn = ttk.Button(expr_frame, text=self.lang_support.get_text('calculate_button'), command=self.eval_expression)
        expr_calc_btn.grid(row=2, column=0, padx=5, pady=5)
        
        ttk.Label(expr_frame, text=self.lang_support.get_text('result_label')).grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.expr_result_var = tk.StringVar()
        self.expr_result_label = ttk.Label(expr_frame, textvariable=self.expr_result_var, 
                                          font=("Arial", 12, "bold"), foreground="blue")
        self.expr_result_label.grid(row=3, column=1, padx=5, pady=2)
        
        # 帮助信息
        help_text = self.lang_support.get_text('supported_operators')
        ttk.Label(expr_frame, text=help_text, font=("Arial", 9), foreground="gray").grid(
            row=4, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
    
    def rebuild_expression_tab_ui(self):
        """重建表达式选项卡界面"""
        # 清除现有组件
        for widget in self.expr_tab.winfo_children():
            widget.destroy()
        
        # 重新创建界面
        self.create_expression_tab()

    def eval_expression(self):
        try:
            expression = self.expr_entry.get().strip()
            if not expression:
                messagebox.showerror(self.lang_support.get_text('error'), self.lang_support.get_text('enter_expression'))
                return
            
            # 定义安全的命名空间
            safe_dict = {
                '__builtins__': {},
                'np': np,
                'math': math
            }
            
            # 验证表达式是否包含不允许的字符
            allowed_pattern = r'^[a-zA-Z0-9_+\-*/(). xsincostanlogepabudfhiruqm]+$'
            if not re.match(allowed_pattern, expression):
                messagebox.showerror(self.lang_support.get_text('error'), self.lang_support.get_text('invalid_chars'))
                return
            
            # 替换常用函数名
            expression = expression.replace('sin', 'np.sin')
            expression = expression.replace('cos', 'np.cos')
            expression = expression.replace('tan', 'np.tan')
            expression = expression.replace('log', 'np.log')
            expression = expression.replace('exp', 'np.exp')
            expression = expression.replace('abs', 'np.abs')
            expression = expression.replace('sqrt', 'np.sqrt')
            expression = expression.replace('^', '**')
            expression = expression.replace('pi', 'np.pi')
            expression = expression.replace('e', 'np.e')
            
            # 编译表达式
            compiled_expr = compile(expression, '<string>', 'eval')
            
            # 计算表达式
            result = eval(compiled_expr, safe_dict)
            self.expr_result_var.set(str(result))
            
        except ZeroDivisionError:
            messagebox.showerror(self.lang_support.get_text('error'), self.lang_support.get_text('division_by_zero_error'))
        except Exception as e:
            messagebox.showerror(self.lang_support.get_text('error'), self.lang_support.get_text('calculation_error_msg') + str(e))


def run_gui():
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()


# 主程序入口
if __name__ == "__main__":
    run_gui()
