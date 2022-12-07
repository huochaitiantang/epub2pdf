# epub2pdf
网上的其他开源项目，一般使用模拟浏览器将`epub`文件打开，再打印成`pdf`，如借助`wkhtmltopdf`等工具，容易出现字体、图片、链接错误。

本项目直接解析`epub`中的`html`，提取其中的目录、文字、图片、引用关系等，然后使用`reportLab`工具自定义排版，并生成`pdf`。

### 环境
* python3
* `pip3 install beautifulSoup4`
* `pip3 install reportLab`

### 特性
* 支持不同字体：宋体（SimSun）, 黑体（SimHei）, 楷体（SimKai）
* 支持内部超链接跳转
* 支持图片
* 支持左侧大纲（书签）显示

### 使用
处理某一个`epub`文件：
```
python main.py ${epub_path}
```
批量处理文件夹内所有`epub`文件：
```
python main.py ${epub_dir}
```
