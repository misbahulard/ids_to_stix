observable_prototype = {
    "type": "observed-data",
    "id": "observed-data--c2552986-5b06-489a-b9af-7bcc25fc991a",
    "created": "2018-04-13T01:03:43.279Z",
    "modified": "2018-04-13T01:03:43.279Z",
    "first_observed": "2018-04-13T01:03:43.279105Z",
    "last_observed": "2018-04-13T01:03:43.279105Z",
    "number_observed": 1,
    "objects": {
        "0": {
            "type": "ipv4-addr",
            "value": "10.0.2.16"
        },
        "1": {
            "type": "ipv4-addr",
            "value": "173.194.70.94"
        },
        "2": {
            "type": "network-traffic",
            "src_ref": "0",
            "dst_ref": "1",
            "src_port": 49165,
            "dst_port": 80,
            "protocols": [
                "ipv4",
                "tcp"
            ]
        }
    }
}

indicator_prototype = {
    "type": "indicator",
    "id": "indicator--d81f86b9-975b-bc0b-775e-810c5ad45a4f",
    "created": "2014-06-29T13:49:37.079Z",
    "modified": "2014-06-29T13:49:37.079Z",
    "name": "Malicious site hosting downloader",
    "description": "Malicious IP 10.252.108.22 detected",
    "labels": [
        "malicious-activity"
    ],
    "pattern": "[url:value = 'http://x4z9arb.cn/4712/']",
    "valid_from": "2014-06-29T13:49:37.079000Z"
}
