# aliyun_exposed
通过ack查询阿里云环境暴露公网资产，可用于安全暴露面管理

## 使用方式
1. 导入依赖
```
pip3 install openpyxl
pip3 install pandas
pip3 install aliyun-python-sdk-core-v3
```
2. 修改脚本中AccessKeylist为目标阿里云环境的ack，可适用与多个阿里云账号ack批量查询
```
AccessKeylist = [
	['asadsafsdfdsfsdfds', 'dsvsdcsdvsdvfdvdffd'],
	['fdvdfbfgdsfvdfvdsd',  'dgrtbdfjsjsvvfddfbfd'],
	]
```
3. 执行后在执行路径下保存结果为aliyun_exposed.xlsx
