# fastopen

# 说明
通过终端连接到linux服务器后，如果想要通过samba在本地打开服务器上的文件或者文件夹，以往做法是现在本地打开服务器的文件夹，然后一级一级进入，直到需要打开的文件夹或者文件，在这个过程重存在两个问题：
1、把终端切换到文件夹浏览器，并打开指定服务器的根目录
2、需要一级一级打开，如果文件隐藏的比较深，会非常麻烦费时
然而通过此工具，可以在终端输入一条指令，就可以快速打开指定的文件或者文件夹

当然不止于此，我们还可以扩展其他更多命令，比如通过vscode打开指定的文件或者文件夹

# 工作原理：
服务器端和本地端通过MQTT通信，在服务器输入命令后，通过MQTT发送到本地，本地负责执行命令
