from django.shortcuts import render
from django.http.request import HttpRequest
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from elasticsearch import Elasticsearch
import urllib3
urllib3.disable_warnings()
# Create your views here.
client = Elasticsearch("https://localhost:9200", basic_auth=("elastic", 'EFUbPM3vK5a2gBiwAW+k'), verify_certs=False)


@require_GET
def info(request: HttpRequest):
    query = request.GET['query']
    rsp = client.search(index="passage", query={
        "multi_match": {
            "query": query,
            "fields": ["belong", "trans", "src"],
            },
    }, highlight={
            "fields": {
                "belong": {},  # 定义高亮显示的字段
                "trans": {},
                "src": {}
        }
    }, size=100)
    with open('example.json', 'w', encoding='utf-8') as f:
        import json
        f.write(json.dumps(rsp.body, ensure_ascii=False, indent=4))
    return JsonResponse(rsp.body, json_dumps_params={"ensure_ascii": False})
    # return JsonResponse({"code": 0, "msg": "ok"})


@require_GET
def info2(request: HttpRequest):
    _id = request.GET['id']
    rsp = client.search(index="passage", query={
        "ids": {
            "values": [_id]
        }
    })
    return JsonResponse(rsp.body, json_dumps_params={"ensure_ascii": False})
