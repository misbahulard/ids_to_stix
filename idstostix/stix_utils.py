import datetime
import json
import uuid

import stix2

import prototypes
from rdd_utils import _rowify


def to_indicator(r):
    """ Fungsi untuk mengubah rdd menjadi objek stix indicator dan dijadikan rdd indicator"""

    id = str(uuid.uuid4())
    created = datetime.datetime.now()
    modified = created
    valid_from = created
    src_type = r['objects']['0']['type']
    dst_type = r['objects']['1']['type']
    src_ip = r['objects']['0']['value']
    dst_ip = r['objects']['1']['value']

    indicator = stix2.Indicator(
        id="indicator--" + id,
        created=created,
        modified=modified,
        name="Malicious Network Flow",
        description="Malicious IP: " + src_ip + " detected.",
        labels=["malicious-activity"],
        pattern="[network-traffic:src_ref.type = '"
                + src_type + "' AND network-traffic:src_ref.value = '"
                + src_ip + "'] AND [network-traffic:dst_ref.type = '"
                + dst_type + "' AND network-traffic:dst_ref.value = '"
                + dst_ip + "'] REPEATS " + str(r['number_observed']) + " TIMES",
        valid_from=valid_from
    )

    # di jadikan json
    indicator_serialized = indicator.serialize()
    indicator_json = json.loads(indicator_serialized)

    # dijadikan ke row rdd
    return _rowify(indicator_json, prototypes.indicator_prototype)


def to_observable(r):
    """ Fungsi untuk mengubah rdd menjadi objek stix observable dan dijadikan rdd observable"""

    id = str(uuid.uuid4())
    created = datetime.datetime.now()
    modified = created
    protocol = int(r["protocol"])
    first_observed = datetime.datetime.fromtimestamp(float(r["first_observed"]))
    last_observed = datetime.datetime.fromtimestamp(float(r["last_observed"]))
    number_observed = int(r["number_observed"])

    if protocol == 6:
        protocol = "tcp"
    elif protocol == 7:
        protocol = "udp"
    else:
        protocol = "unknown"

    observed = stix2.ObservedData(
        id="observed-data--" + id,
        created=created,
        modified=modified,
        first_observed=first_observed,
        last_observed=last_observed,
        number_observed=number_observed,
        objects=
        {
            "0": {
                "type": "ipv4-addr",
                "value": r["src_ip"]
            },
            "1": {
                "type": "ipv4-addr",
                "value": r["dest_ip"]
            },
            "2": {
                "type": "network-traffic",
                "src_ref": "0",
                "dst_ref": "1",
                "src_port": int(r["src_port"]),
                "dst_port": int(r["dst_port"]),
                "protocols": [
                    "ipv4",
                    protocol
                ],
            }
        }
    )

    # di jadikan json
    observed_serialized = observed.serialize()
    observed_json = json.loads(observed_serialized)

    # dijadikan ke row rdd
    return _rowify(observed_json, prototypes.observable_prototype)
