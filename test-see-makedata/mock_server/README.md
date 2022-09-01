# test-see-makedata--》mock_server
【介绍】
用于see项目模拟客户服务器端的拉取接口，当收到see的接口导入请求时，返回会话列表信息在see创建拉取数据集
【用法】
与see部署的服务器放在同一内网可达的某一个服务器内，python3 mock_server.py  即可启动server，监听该服务器1769端口，等待see的拉取接口Get请求到来
