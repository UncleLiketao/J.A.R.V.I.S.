tool 文件夹下有 adb 与airtest文件夹 需要把本机的adb 跟 airtest 的exe文件拷贝一份到这
 adb 可以到python包 或者airtest安装包下有个 ...\airtest\core\android\static\adb\windows\

airtest 是python 命令包下有个  Scripts\airtest.exe


测试文件随便放在哪里可以单独选择一个测试文本 但文件名必须是BC开始的

Air的报错输出还是只能显示在黑色框框中
UPR是屏蔽状态


2021.03.23
新增： ui支持停止按钮 ：可能停止有问题
           输出unity日志，本地保存一份：输出白色 log窗口： 警告绿色： 其他红色
修正： 选取文件
          循环失败
            
2021.03.25
新增： 测试录像功能，日志按测试名称存储
修正： 修改文件调用方式，adblog只有打开的时候调用一次
屏蔽： 输出等级为I的不刷屏


Q&A:
1.Device Unauthorized 设备未授权
adb devices -l  
手机上的开发人员选项，然后单击“撤销USB调试授权”