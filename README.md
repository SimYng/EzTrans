# EZ Trans

### 简介

* 弹窗翻译pdf英文论文用的小工具，避免换行符的尴尬
* 可以切换多个翻译接口

### TODO

- [ ] 修复百度翻译1022错误
- [ ] 加入Google翻译的支持
- [ ] 挂着梯子的时候，无法访问appi
- [ ] 空格键关闭翻译窗口

## 环境

* 支持Win/MAC/ubuntu，python3

## 安装方法

* 安装前请使用pip安装pywin32、keyboard、brotli、xerox、pyautogui、PyExecJS以及requests库：

```
pip install pywin32
```

``` bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pywin32keyboard brotli xerox pyautogui requests PyExecJS
```

* ~~安装：~~暂时不用这种方式

``` bash
python setup.py build
python setup.py install
```

## 用法

* ~~安装好后，在命令行中输入`chptrans`打开翻译器，复制想翻译的英文（ctrl+c)，复制完后按f键翻译（翻译器会将剪切板中的内容翻译为中文）。~~
* 按`ctrl+e`可以切换中英对照模式。
* 按`ctrl+r`可以切换翻译器。
* 双击`ctrl+c`开始翻译，翻译成功后有弹窗显示

## 使用截图

普通模式：

![](img/show.png)

中英对照模式：

![](img/show2.png)

## 更新日志

* 2021.11.20
  *  Fork from HACHp1/chptrans
  
* 2021.11.21 
  * Fix Bug：'Fig. x'导致中英文对照翻译的断句错误；
  * 将f键开始翻译改成双击`ctrl+c`进行翻译
  
* 2021.11.22

  * 设置弹出的翻译窗口获取焦点。`tkinter`窗口的句柄需要使用`pywintypes.HANDLE()`获取，`pywin32`获取不了

  ```
  hwnd = pywintypes.HANDLE(int(top.frame(), 16))  # 获取窗口句柄,top = tkinter.Tk()
  ```

  - 设置按下空格键，关闭窗口
  - 使用线程显示翻译窗口

## 感谢

- [HACHp1/chptrans](https://github.com/HACHp1/chptrans)
- [ ZCY01/BaiduTranslate ](https://github.com/ZCY01/BaiduTranslate)
