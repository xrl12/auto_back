# 使用pyqt5做到一个自动备份的小软件

选定一个源目录和一个备份目录，会实时监听源目录，并把源码目录的内容拷贝的备份目录

## 启动方法
```pip
pip3 install -r requrests.txt
```
由于一些懂得都懂的原因，可能会导致下载进度比较慢。可以试一下下面这个命令，这个命令会使用清华源去下载
```pip
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requrests.txt
```
## 启动命令
注意，这里要保证实在项目的根目录里面
```cmd
python main.py
```

## 使用方法
![image](https://github.com/xrl12/auto_back/assets/53255548/af8b3cc1-ca0a-4cdb-af12-0d0420cd9fa0)

出现这个页面就表示运行成功了。
然后我们去选择源目录和目标目录就会自动运行了。


https://github.com/xrl12/auto_back/assets/53255548/26cc1594-9147-495e-b903-37d35060348b

## 打包成桌面软件
找到bulid.sh 文件
```sh
pyinstaller --onefile --noconsole  -p "C:\Users\29966\PycharmProjects\auto_back\.venv;" "C:\Users\29966\PycharmProjects\auto_back\main.py"  -d all -F -n alexxu --clean
```
C:\Users\29966\PycharmProjects\auto_back\.venv;  python虚拟环境路径

C:\Users\29966\PycharmProjects\auto_back\main.py 项目路径

把这两个路劲换成自己对应的路劲。

-n 是打包后文件的名字，可以随便修改。

## todo
- [x] 监听源目录，并自动拷贝到目标目录
- [ ] 用户自己设置轮询时间（多久备份一次）
- [ ] 开始监听的时候，自动把源目录所有的文件备份到目标盘

## 结束
感谢[watchdog](https://github.com/gorakhargosh/watchdog)。

有任何问题都欢迎大家提issue讨论

邮箱：mrxu<mrxr_000824@163.com
