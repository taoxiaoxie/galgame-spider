# galgame-spider
- galgame 爬虫
- json文件路径：
https://huggingface.co/datasets/alpindale/visual-novels
- 数据集路径：https://vndb.org/c51034

1. 安装依赖
```bash
pip3 install -r requirements.txt
```

2. 下载huggingface 项目
```bash
git clone https://huggingface.co/datasets/alpindale/visual-novels
```

3. 运行爬虫项目
```bash
python3 main.py
```
> 注； 信号量设置为10，间隔时间为0.3s，(`config.py`)可根据自己的需求进行修改。
> 太快会被封ip。
```bash
pip install -r requirements.txt
```