from es_deldata import Elasticsearch


# busId/hostIp/date 到方法体中更改
if __name__ == '__main__':
    #
    estb_date = Elasticsearch().search_bydate()
    for tb in estb_date:
        print(tb)
        res = Elasticsearch().search_tb(tb).json()['hits']['hits']
        # print(res)
        if res != []:
            type = res[0]['_type']
            res = Elasticsearch().deldata(tb,type)
            print(res)
        else:
            continue


