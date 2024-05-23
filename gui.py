import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import matplotlib
matplotlib.use('TkAgg')
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning)

data = pd.read_csv('fruit_data.csv', sep=',')
fruit_list = [''] + data['品名'].unique().tolist()
location_list = [''] + data['产地'].unique().tolist()

def display_data(fruit=None, location=None):
    if fruit:
        selected_data = data[data['品名'] == fruit]
    elif location:
        selected_data = data[data['产地'] == location]
    else:
        return

    if selected_data.empty:  # 检查是否为空
        print("没有找到匹配的数据，请检查输入的水果和产地是否正确。")
        return

    if fruit:
        selected_data.groupby('产地')['均价'].mean().plot(kind='bar')
    elif location:
        selected_data.groupby('品名')['均价'].mean().plot(kind='bar')

    plt.xticks(rotation=0)  # 设置x轴刻度标签的旋转角度为0
    plt.yticks(rotation=0)  # 设置y轴刻度标签的旋转角度为0
    plt.show()

def analyze_data(fruit=None):
    if not fruit:
        print("请确保已选择水果。")
        return

    selected_data = data[data['品名'] == fruit]

    # 创建一个新的图形，并设置子图的布局为 1 行 2 列
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 在第一个子图上绘制价格波动折线图
    selected_data.pivot_table(index='产地', columns='日期', values='均价').T.plot(ax=axes[0])
    axes[0].set_title("价格波动折线图")

    # 在第二个子图上绘制最高价格的前5个地区的直方图
    selected_data.groupby('产地')['均价'].mean().nlargest(5).plot(kind='bar', ax=axes[1])
    axes[1].set_title("最高价格的前5个地区")

    plt.tight_layout()  # 调整子图之间的间距
    plt.xticks(rotation=0)  # 设置x轴刻度标签的旋转角度为0
    plt.yticks(rotation=0)  # 设置y轴刻度标签的旋转角度为0
    plt.show()

def predict_data(fruit, location):
    if not fruit or not location:
        print("请确保已选择水果和产地。")
        return

    selected_data = data[(data['品名'] == fruit) & (data['产地'] == location)].copy()
    if selected_data.empty:
        print("没有找到匹配的数据，请检查选择的水果和产地是否正确。")
        return

    selected_data.loc[:, '日期'] = pd.to_datetime(selected_data['日期'])
    selected_data.loc[:, '日期'] = selected_data['日期'].map(lambda x: x.toordinal())

    model = LinearRegression()
    model.fit(selected_data[['日期']], selected_data['均价'])

    future_date = pd.to_datetime('2023/4/23')
    future_price = model.predict([[future_date.toordinal()]])
    return future_price[0]

# 创建GUI
window = tk.Tk()
window.title("水果价格分析")

frame1 = tk.Frame(window)
frame1.pack(side=tk.TOP, padx=10, pady=10)

frame2 = tk.Frame(window)
frame2.pack(side=tk.TOP, padx=10, pady=10)

frame3 = tk.Frame(window)
frame3.pack(side=tk.TOP, padx=10, pady=10)

fruit_label = tk.Label(frame1, text="选择水果：")
fruit_label.pack(side=tk.LEFT)

fruit_var = tk.StringVar()
fruit_var.set(fruit_list[0])
fruit_option_menu = tk.OptionMenu(frame1, fruit_var, *fruit_list)
fruit_option_menu.pack(side=tk.LEFT)

location_label = tk.Label(frame1, text="选择产地：")
location_label.pack(side=tk.LEFT)

location_var = tk.StringVar()
location_var.set(location_list[0])
location_option_menu = tk.OptionMenu(frame1, location_var, *location_list)
location_option_menu.pack(side=tk.LEFT)

def update_fruit_options(*args):
    selected_location = location_var.get()
    if selected_location:
        available_fruits = [''] + data[data['产地'] == selected_location]['品名'].unique().tolist()
    else:
        available_fruits = fruit_list

    fruit_option_menu['menu'].delete(0, 'end')
    for fruit in available_fruits:
        fruit_option_menu['menu'].add_command(label=fruit, command=tk._setit(fruit_var, fruit))

def update_location_options(*args):
    selected_fruit = fruit_var.get()
    if selected_fruit:
        available_locations = [''] + data[data['品名'] == selected_fruit]['产地'].unique().tolist()
    else:
        available_locations = location_list

    location_option_menu['menu'].delete(0, 'end')
    for location in available_locations:
        location_option_menu['menu'].add_command(label=location, command=tk._setit(location_var, location))

# 在变量 fruit_var 和 location_var 上设置监听器
fruit_var.trace('w', update_location_options)
location_var.trace('w', update_fruit_options)

display_button = tk.Button(frame2, text="显示数据", command=lambda: display_data(fruit=fruit_var.get(), location=location_var.get()))
display_button.pack(side=tk.LEFT)

analyze_button = tk.Button(frame2, text="分析数据", command=lambda: analyze_data(fruit=fruit_var.get()))
analyze_button.pack(side=tk.LEFT)

predict_button = tk.Button(frame2, text="预测价格", command=lambda: print(predict_data(fruit=fruit_var.get(), location=location_var.get())))
predict_button.pack(side=tk.LEFT)

window.mainloop()
