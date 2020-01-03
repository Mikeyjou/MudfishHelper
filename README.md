# MudfishHelper
提供快速連線Mudfish VPN的小工具(參考Kazaf的連線教學)

**需要安裝Python3**

# 安裝
首先，clone專案並安裝套件

	$ pip install -r requirements.txt

在config.ini裡，設置Mudfsih帳號密碼

```ini
[account]
username= 帳號
password= 密碼
``` 

# 執行
1. 手動執行Mudfish控制面板

2. 執行.py程式

```sh
$ pip install -r requirements.txt
```

3. 成功登入後，手動選擇物品

```sh
使用者有以下物品:
(1) 5e
(2)  :
選擇物品:1
```

4. 輸入遊戲ip

```sh
遊戲IP: xxx.xxx.xxx.xxx
```

5. 選擇節點

```sh
開始找尋合適節點..
有以下合適節點:
(1) TW Asia (Taiwan - HostingInside 2) Avg:38.89
(2) TW Asia (Taiwan - HostingInside 14) Avg:39.09
(3) TW Asia (Taiwan - HostingInside 11) Avg:40.29
(4) TW Asia (Taiwan - Google) Avg:41.55
(5) TW Asia (Taiwan - HostingInside 15) Avg:42.50
(6) TW Asia (Taiwan - HostingInside 1) Avg:43.23
(7) TW Asia (Taiwan - HostingInside 10) Avg:43.31
(8) TW Asia (Taiwan - ESTNOC) Avg:43.80
(9) TW Asia (Taiwan - Google 5) Avg:43.95
(10) TW Asia (Taiwan - HostingInside 9) Avg:44.16
(11) TW Asia (Taiwan - Google 6) Avg:47.70
(12) TW Asia (Taiwan - HostingInside 4) Avg:47.95
(13) TW Asia (Taiwan - Google 4) Avg:59.82
選擇節點: 1
```

6. 成功連線

7. 選擇後續操作

```sh
(1)新連線 (新遊戲重新輸入IP並選節點)
(2)更換節點 (同一遊戲更換節點)
(3)關閉連線 (切斷當前VPN)
(4)結束程式
選擇操作: 1
```

8. 至Mudfish控制面板，F5重新整理畫面，確定連線成功
