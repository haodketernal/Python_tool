#Author: HaoPV_HPT
#Licene: GPLv3
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import json
from datetime import datetime

es = Elasticsearch([{'host': '10.10.10.23', 'port': '9200'}],http_auth=('elastic', 'vdcVDCmwgMWGxElastic'))

def checkhealth(index_name):
    #set es index
    searchContext = Search(using=es, index=index_name+'*').extra(size=50)
    #set time
    s = searchContext.query().filter('range', **{'@timestamp':{'gte': 'now-25m' , 'lt': 'now'}})

    response = s.execute()
    count = response.hits.total.value
    if (count < 5):
     health_status = 'RED'
    else:
     health_status = 'GREEN'
    print('Health of index '+ index_name+' is: '+health_status+'\n')
    status_to_elastic(index_name,health_status) ##fly to elastic

def status_to_elastic(index_name,health_status):
    es.index(index=datetime.now().strftime('index-health-%Y-%m-%d'),id=datetime.utcnow().isoformat(), body={ "timestamp": datetime.utcnow().isoformat(), "index_patterns": index_name, "health_status": health_status})
    
def main():
    list_index = ['manager-vdc-alert','logs-os-linux']
    #print(list_index[0],list_index[1])
    print('Health check start\n\n')
    for i in range(len(list_index)):
     checkhealth(list_index[i])


    
if __name__ == '__main__':
    main()