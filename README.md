# 密友圈安卓版前置条件说明

### 联系人导入

先将项目目录中的contacts.vcf文件拷贝至手机，您可以通过即时通讯软件（如QQ、微信、和飞信）发送，也可以通过蓝牙、Huawei Share等传输，也可以将手机联接至电脑后手动拷贝，也可以通过以下adb命令传输（专业人员）：
```shell
adb -s XXXXXXX push contacts.vcf /sdcard/contacts.vcf
```
其中，XXXXX代表手机序列号，您可以通过`adb devices`查询您手机的序列号，待文件导入后，在手机端打开此文件，根据手机提示导入即可。
### 设置密友圈软件
用安装有移动电话卡（主卡）并同时安装有项目目录提供版本的密友圈（meetyou_V3.7.1_official_2019-06-20.apk）的安卓手机系统手机登录密友圈，切换至`通讯录`页面，开通`不限时长`业务和`家庭网`业务，待
成功开通后，给`不限时长`业务添加3~5位成员，给`家庭网`业务添加2~3位成员后，就可以运行单机操作的用例了。

### 双机设置
用另一部手机完成单机设置的步骤后，还需要将两台手机互相加入对方的通讯录中，同时需要将两台手机互相加入对方的`不限时长`业务和`家庭网`业务。此时，就可以运行双机操作部分的用例了。


