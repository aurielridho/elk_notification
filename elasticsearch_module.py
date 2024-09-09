from elasticsearch import Elasticsearch

# Konfigurasi Elasticsearch
es = Elasticsearch(
    ['https://localhost:9200'],
    basic_auth=('username', 'password'), #Ganti dengan credential yang valid
    verify_certs=True,
    ca_certs='/root/http_ca.crt' #PATH sertifikat CA untuk SSL
)

def check_alerts():
    rule_details = {}

    query = {
        "size": 10,
        "query": {
            "bool": {
                "filter": [
                    {"range": {"@timestamp": {"gte": "now-1m"}}}
                ]
            }
        },
        "_source": ["kibana.alert.rule.name", "@timestamp", "source.ip"],
        "sort": [{"@timestamp": {"order": "desc"}}]
    }

    response = es.search(index=".internal.alerts-security.alerts-default-*", body=query)

    hits = response['hits']['hits']

    if len(hits) == 0:
        print("No alerts found.")
    else:
        print("Alerts found:")

    for hit in hits:
        alert = hit['_source']
        rule_name = alert.get("kibana.alert.rule.name", "No name")
        timestamp = alert.get("@timestamp", "No timestamp")
        doc_id = hit['_id']
        ip = alert.get("source", {}).get("ip", "No IP")

        if rule_name not in rule_details:
            rule_details[rule_name] = []

        rule_details[rule_name].append({
            "id": doc_id,
            "timestamp": timestamp,
            "ip": ip
        })

    return rule_details
