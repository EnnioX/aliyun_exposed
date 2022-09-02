import pandas as pd
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.request import CommonRequest
import json

# pip3 install openpyxl
# pip3 install pandas
# pip3 install aliyun-python-sdk-core-v3

AccessKeylist = [
	['afdsfsdfsdfsdfsdf', 'fhgynjythnfdgthbesrfrgregteght'],
	]


def aliyun_info():
	df_all = pd.DataFrame()
	for x in range(len(AccessKeylist)):
		df = get_exposed_instance(x)
		df_all = df_all.append(df, ignore_index=True)
		df_all.index = df_all.index + 1
	return df_all


# 查询云安全中心暴露资产 返回df
def get_exposed_instance(x):
    def get_exposed_instance_page(page):  # DescribeExposedInstanceList
        credentials = AccessKeyCredential(AccessKeylist[x][0], AccessKeylist[x][1])
        client = AcsClient(region_id='cn-hangzhou', credential=credentials)
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('tds.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')
        request.set_version('2018-12-03')
        request.set_action_name('DescribeExposedInstanceList')
        request.add_query_param('PageSize', "200")  # 每次查询200条数据
        request.add_query_param('CurrentPage', page)
        response = client.do_action(request)
        data = json.loads(response)
        return data
    total = get_exposed_instance_page(1)['PageInfo']['TotalCount']
    rounds = total // 200 + 1  # 查询轮数,每页查询200条数据
    df = pd.DataFrame()  # 建立空df
    for i in range(1, rounds + 1):
        df = df.append(pd.DataFrame(get_exposed_instance_page(i)['ExposedInstances']), ignore_index=True)
    # 选取指定列，调整列顺序，重新命名列名
    before_list = ['InstanceId', 'InstanceName', 'InternetIp', 'IntranetIp', 'ExposureType', 'ExposureIp', 'ExposureTypeId', 'ExposureComponent', 'ExposurePort']
    after_list = ['InstanceId', 'InstanceName', 'InternetIp', 'IntranetIp', 'ExposureType', 'ExposureIp', 'ExposureTypeId', 'ExposureComponent', 'ExposurePort']
    # after_list = ['实例id', '实例名称', '公网IP', '内网IP', '暴露方式', '暴露IP', '暴露方式实例id', '暴露组件', '暴露端口']
    df = change_columns(df, before_list, after_list)
    return df


# 从df中选取特定的字段并排列、重命名
def change_columns(df, before_list, after_list):
    df = df[before_list]  # 选取特定的字段并排列
    for i in range(len(before_list)):
        df = df.rename({before_list[i]: after_list[i]}, axis='columns')  # 重命名字段
    return df


def main():
    with pd.ExcelWriter('aliyun_exposed.xlsx') as writer:
        aliyun_info().to_excel(writer, sheet_name="暴露资产")


if __name__ == '__main__':
	main()
