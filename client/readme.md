client
===

# 說明

採集主機硬件資訊至資料庫。


## 安裝

- CentOS


```
yum install -y lshw

```

python3.6
```
pip install request
pip install psutil
```

## 如何設置

**conf/settings.py**

```
# client方式
MODE = 'agent' 

# web 接口
UP_API_URL = "<host>/api/asset_by_hostname/"

# 請求Key 需與backend一致
ASSETKEY = ""
AUTH_KEY_NAME = "auth-key"

# 自定義採集模組
PLUGINS = {
    'disk': 'src.plugins.disk.DiskPlugin',
    'mem': 'src.plugins.mem.MemPlugin',
    'nic': 'src.plugins.nic.NicPlugin',
    'basic': 'src.plugins.basic.BasicPlugin',
    'cpu': 'src.plugins.cpu.CpuPlugin',
}

```

## 如何運行

**main.py**

以當前主機名稱作為唯一，不存在即新增資料庫。

```
python main.py
```
