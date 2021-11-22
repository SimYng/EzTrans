# encoding=utf-8
import threading    # 单独线程显示窗口
import xerox        # 读取剪切板数据
import keyboard     # 获取用户按下的按键
import pyautogui    # 获取鼠标位置
import time         # 获取击键的时间，实现双击ctrl+s开始翻译
import tkinter      # 自带的GUI库，生成文本框
import pywintypes   # 用于获得获取tkinter窗口句柄
import win32gui     # 根据窗口句柄设置焦点


if __name__ == '__main__':
    from core.trans_api import translators
    from core.utils import re_split
else:
    from .core.trans_api import translators
    from .core.utils import re_split

############################### 参数设置 ######################################
ch_en_mode = True  # 中英对照模式
translator_i = 2  # 当前翻译器index
wnd_title = "EzTrans"
wnd_class_name = "TkTopLevel"

############################### 全局变量 ######################################
translator_num = len(translators)  # 翻译器总数
myTranslate = translators[translator_i]  # 初始化翻译器

# 加入双击开始翻译的功能:双击ctrl+c
lastClickTransTime = 0  # 上一次ctrl + c 时间
nowClickTransTime = 0  # 现在ctrl + c 时间
doubleClickInter = 0.5  # 双击的间隔时间


def run(translate_results):
    # 弹出的翻译串口，键盘事件监听器
    def detect_key_press(event):
        # 空格事件触发对应的ASCII码:32
        if event.keycode == 32:
            # print(f"事件触发键盘输入:{event.char},对应的ASCII码:{event.keycode}")
            top.destroy()

    """
    显示翻译结果
    """
    x, y = pyautogui.position()

    position = "500x400+" + str(x) + "+" + str(y)  # 取得当前鼠标位置
    top = tkinter.Tk()  # 窗口初始化
    top.title(wnd_title)
    top.wm_attributes('-topmost', 1)  # 置顶窗口
    top.geometry(position)  # 指定定位生成指定大小窗口
    top.configure(bg=('#%02x%02x%02x' % (199, 237, 204)))
    e = tkinter.Text()  # 生成文本框部件
    e.configure(bg=('#%02x%02x%02x' % (199, 237, 204)))
    e.insert(1.0, translate_results)  # 插入数据
    e.pack()  # 将部件打包进窗口
    e.focus_set()
    e.bind("<Key>", detect_key_press)  # 监听键盘按键事件，按下空格键后关闭窗口
    # tkinter窗口需要用特殊的方式才能获得句柄
    try:
        hwnd = pywintypes.HANDLE(int(top.frame(), 16))  # 获取窗口句柄
        win32gui.SetForegroundWindow(hwnd)              # 根据句柄设置焦点
    except Exception as e:
        print(e)

    top.mainloop()  # 进入消息循环


def get_copy_text():
    """
    获得剪切板数据
    """
    try:
        copy_text = xerox.paste(xsel=True)
    except TypeError:
        copy_text = '请复制一段文字!'
    return copy_text


def on_press(v_cmd):
    """
    监听按键
    """
    global ch_en_mode
    global translator_i
    global myTranslate
    global lastClickTransTime
    global nowClickTransTime

    if v_cmd == 'translator':  # 切换翻译器
        translator_i = (translator_i + 1) % translator_num
        myTranslate = translators[translator_i]
        print('当前翻译器：' + myTranslate.__name__)

    elif v_cmd == 'zh_en':  # 切换中英对照模式
        ch_en_mode = not ch_en_mode
        if ch_en_mode:
            print('当前模式：中英对照')
        else:
            print('当前模式：仅显示翻译')

    elif v_cmd == 'do_trans':  # 按f键翻译
        # 获取本次、上次击键的时间
        lastClickTransTime = nowClickTransTime  # 这里的now其实是这一次的last，上一轮没有更新而已
        nowClickTransTime = time.time()

        # 打印点击的时间差
        # print("lastClickTransTime:", lastClickTransTime)
        # print("nowClickTransTime:", nowClickTransTime)

        # 判断两次双击的时间,若大于时间间隔，则不执行操作
        if nowClickTransTime - lastClickTransTime > doubleClickInter:
            return

        current_data = str(get_copy_text())  # 取得当前剪切板数据
        current_data = current_data.replace(
            '- ', '').replace('-\r\n', '').replace('-\n', '').replace('\n', ' ').replace('\r', '').strip()

        # 目前中英对照通过'.'来分割句子。但是会被'Fig. 2'影响
        current_data = current_data.replace('Fig.', '')

        """ 翻译 """
        # print(current_data)
        translate_results = myTranslate(current_data)

        # 如果开始了中英对照模式
        if ch_en_mode:
            temp_current_data = re_split(current_data, '([.?]\s)')  # 将原句按照'.'进行split
            temp_seg = re_split(translate_results, '(。|？|\?\s)')  # 将译句按照'。'进行split
            if len(temp_seg) > 1:
                if temp_seg[-1] == '':
                    temp_ch = temp_seg[:-1]
                else:
                    temp_ch = temp_seg
            else:
                temp_ch = [translate_results]

            # print(len(temp_current_data), len(temp_ch))
            # assert (len(temp_current_data) == len(temp_ch))

            translate_results = ''
            try:
                for i in range(len(temp_current_data)):
                    translate_results = translate_results + \
                                        temp_ch[i] + '\n' + temp_current_data[i] + \
                                        ' \n------------------------------------\n\n'
            except IndexError:
                translate_results = '【中英分段数量不匹配，对照结果可能有误，请检查中英内容】\n\n' + translate_results

        else:
            translate_results = translate_results.replace('。', '。\n\n')

        """  显示，单独开一个线程  """
        threading.Thread(target=run, args=(translate_results,)).start()
        # run(translate_results)


def main():
    """
    主程序
    """
    print('''
***************************************************************************************
    ███████╗███████╗    ████████╗██████╗  █████╗ ███╗   ██╗███████╗
    ██╔════╝╚══███╔╝    ╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝
    █████╗    ███╔╝        ██║   ██████╔╝███████║██╔██╗ ██║███████╗
    ██╔══╝   ███╔╝         ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║
    ███████╗███████╗       ██║   ██║  ██║██║  ██║██║ ╚████║███████║
    ╚══════╝╚══════╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝
                                                               

    欢迎使用 SimYng's translator
    用法：
        复制想翻译的英文（ctrl+c)，复制完后按f键翻译（翻译器会将剪切板中的内容翻译为中文）
        切换中英对照模式（ctrl+e）：方便进行单句的中英对比
        切换翻译器（ctrl+r）：目前支持百度、Bing、有道
        按Esc键退出
***************************************************************************************
        ''')

    print('当前翻译器：' + myTranslate.__name__)
    print('当前模式：仅显示翻译')

    # 注册按键热键
    keyboard.add_hotkey('ctrl+c', on_press, args=('do_trans',))  # 翻译
    keyboard.add_hotkey('ctrl+e', on_press, args=('zh_en',))  # 中英对照模型切换
    keyboard.add_hotkey('ctrl+r', on_press, args=('translator',))  # 翻译器切换
    # 开始监听
    keyboard.record(until='esc')


if __name__ == '__main__':
    main()
