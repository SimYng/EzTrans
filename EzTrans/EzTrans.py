# encoding=utf-8

import xerox        # 读取剪切板数据
import keyboard     # 获取用户按下的按键
import pyautogui    # 获取鼠标位置

import tkinter      # 自带的GUI库，生成文本框

if __name__ == '__main__':
    from core.trans_api import translators
    from core.utils import re_split
else:
    from .core.trans_api import translators
    from .core.utils import re_split


ch_en_mode = True  # 中英对照模式

translator_i = 0  # 当前翻译器index
translator_num = len(translators)  # 翻译器总数

myTranslate = translators[translator_i]  # 初始化翻译器


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
        current_data = str(get_copy_text())  # 取得当前剪切板数据
        current_data = current_data.replace(
            '- ', '').replace('-\r\n', '').replace('-\n', '').replace('\n', ' ').replace('\r', '').strip()

        # 目前中英对照通过'.'来分割句子。但是会被'Fig. 2'影响
        """ 翻译 """
        print(current_data)
        translate_results = myTranslate(current_data)

        if ch_en_mode:
            temp_current_data = re_split(current_data, '([.?]\s)')

            temp_seg = re_split(translate_results, '(。|？|\?\s)')
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

        """  显示  """
        x, y = pyautogui.position()

        position = "500x400+" + str(x) + "+" + str(y)  # 取得当前鼠标位置
        top = tkinter.Tk()  # 窗口初始化
        top.title("EZ translator by SimYng")
        top.wm_attributes('-topmost', 1)  # 置顶窗口
        top.geometry(position)  # 指定定位生成指定大小窗口
        top.configure(bg=('#%02x%02x%02x' % (199, 237, 204)))
        e = tkinter.Text()  # 生成文本框部件
        e.configure(bg=('#%02x%02x%02x' % (199, 237, 204)))
        e.insert(1.0, translate_results)  # 插入数据
        e.pack()  # 将部件打包进窗口
        top.mainloop()  # 进入消息循环


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
    keyboard.add_hotkey('f', on_press, args=('do_trans',))  # 翻译
    keyboard.add_hotkey('ctrl+e', on_press, args=('zh_en',))  # 中英对照模型切换
    keyboard.add_hotkey('ctrl+r', on_press, args=('translator',))  # 翻译器切换
    # 开始监听
    keyboard.record(until='esc')


if __name__ == '__main__':
    main()
