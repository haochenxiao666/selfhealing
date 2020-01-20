#SelfHealing#
    基于zabbix 报警信息去定义处理动作。自动化处理报警。

# 环境要求:
    python 2.7 版本
    mysql 5.6以上

# 安装依赖库:
    pip install -r requirements.txt

# 使用方法：

1. **zabbix报警模板**
    ```
    告警主机:{HOST.NAME}
    告警IP:{HOST.IP}
    告警时间:{EVENT.DATE}{EVENT.TIME}
    告警等级:{TRIGGER.SEVERITY}
    告警信息: {TRIGGER.NAME}
    告警项目:{TRIGGER.KEY1}
    问题详情:{ITEM.NAME}:{ITEM.VALUE}
    当前状态:{TRIGGER.STATUS}:{ITEM.VALUE1}
    事件ID:{EVENT.ID}
    ```

2. **cp db.conf.demo db.conf**。
    ```
    你的cmdb 资产数据库连接信息，本项目基于jumpserver 资产采集信息去匹配。
    [dbconfig]
    db = jumpserver
    host = ip
    user = user
    passwd = password
    charset = utf8
    timeout = 600

    [DingURL]
    DingURL1 = your dingding
    DingURL2 = your dingding
    ```


3. **密钥文件**
      ```
      在keys 目录下面,如果没有其在项目更目录创建keys 目录，然后把连接主机的私钥文件方到这个目录，命名为id_rsa并授权600。必须授权为600 否则会无法连接远程主机。
      ```

4. **supervisor**

      参考supervisor 目录下面配置文件去启动程序。

5. **动作定义**
    ```
     接口文件 SelfHealing.py
     可以二改此文件获取定义动作,后续会基于playbook去完善动作流
    ```

5. **测试运行**
    ```
     python AutoPlay.py
    ```





