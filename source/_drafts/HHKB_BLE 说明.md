# HHKB_BLE 说明

固件下载及键盘设置：[YDKB](ydkb.io)

教程： [HELP](help.ydkb.io)

2019.6.24 更新

一般现在的左右shift+R按一下应该都行，还有反正拿Adafruit那个连总是更好。



## 刷机方式

刷机方式：
           按住最左上角按键不放(物理位置，一般设置Esc)，插入数据线，电脑会识别出一个U盘名为"HHKB_BLE"，这时可放开Esc了。
           Win: 将下载的"hhkb_ble.bin"复制或拖入U盘，直接覆盖原文件（重点，不要先复制进去再改名）。然后右键弹出U盘或再按一次Esc退出，刷机完成。
           Mac: 先删除原来的"hhkb_ble.bin"，再在废纸篓里也要删除它，然后再将新下载的"hhkb_ble.bin"复制到U盘里，弹出U盘，刷机完成。
           不需要安装任何的驱动和刷机软件。也可以直接上传U盘里的hhkb_ble.bin到网站上，读取键盘的当前设置。
进阶方法：同时按左右shift+b，此时键盘会重启，立即按住Esc不放，这样也可以进入刷机的U盘模式，好处就是整个操作过程不用插拔数据线。
补充说明:Num Lock, Caps Lock, Scroll Lock这些指示灯，在蓝牙模式下并未同步显示电脑的这三者状态。只是按一下按键就切换显示一次对应指示灯。
        如果不同步了，可以使用Shift+对应按键，比如Shift+Capslock，这时CapsLock会生效但是对应指示灯的状态不会变。合理利用这一点也可以在蓝牙下反转指示灯使用，比如numlock指示灯在亮的时候是关，灭的时候是开，可以省电。

[详细方式](http://help.ydkb.io/doku.php?id=bootloader:msd-bootloader)



如果刷完无法使用进入刷机模式：

关掉开关——>按 ESC ——>插线

复制文件的时候 led3 应该快速闪



## 使用 OPTION + COMMAND + DELETE  删除无效



刷完之后 shift + R 刷新重连



## Lock 模式

fn + z 

关闭蓝牙。



F + J 同时按可以唤醒