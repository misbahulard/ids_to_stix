import datetime
import json
import re
import uuid

import geoip2.database
import stix2
from geoip2.errors import AddressNotFoundError

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
    # protocol = int(r["protocol"])
    temp_first = float(r["first_observed"])
    temp_last = float(r["last_observed"])
    first_observed = datetime.datetime.fromtimestamp(temp_first)
    last_observed = datetime.datetime.fromtimestamp(temp_last)
    number_observed = int(r["number_observed"])

    # if protocol == 6:
    #     protocol = "tcp"
    # elif protocol == 7:
    #     protocol = "udp"
    # else:
    #     protocol = "unknown"

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
                "src_port": r["src_port"],
                "dst_port": r["dest_port"],
                "protocols": [
                    "ipv4",
                    r["protocol"]
                ],
            }
        }
    )

    # di jadikan json
    observed_serialized = observed.serialize()
    observed_json = json.loads(observed_serialized)

    # dijadikan ke row rdd
    return _rowify(observed_json, prototypes.observable_prototype)


def to_identity(r):
    """ Fungsi untuk mengubah rdd menjadi objek stix identity dengan cara lookup ip ke geoip maxmind"""

    id = str(uuid.uuid4())
    created = datetime.datetime.now()
    modified = created

    ip = r['objects']['0']['value']
    geoip = lookup_ip(ip)
    name = geoip['country'] + ' generic'
    desc = 'Individual identity from ' + geoip['city'] + ', ' + geoip['country']

    identity = stix2.Identity(
        id="identity--" + id,
        created=created,
        modified=modified,
        name=name,
        description=desc,
        identity_class="individual"
    )

    # di jadikan json
    identity_serialized = identity.serialize()
    identity_json = json.loads(identity_serialized)

    # dijadikan ke row rdd
    return _rowify(identity_json, prototypes.identity_prototype)


def lookup_ip(ip):
    """ Fungsi untuk lookup ip ke datavase geoip maxmind """
    geo_dict = {}
    reader = geoip2.database.Reader('data/GeoLite2-City.mmdb')
    try:
        result = reader.city(ip)
        name = result.country.name
        city = result.city.name

        if city is None:
            city = "UNDEFINED"

        geo_dict['country'] = name
        geo_dict['city'] = city

    except AddressNotFoundError:
        if is_private(ip):
            geo_dict['country'] = 'PRIVATE'
            geo_dict['city'] = 'PRIVATE'
        else:
            geo_dict['country'] = 'UNDEFINED'
            geo_dict['city'] = 'UNDEFINED'

    return geo_dict


def is_private(ip):
    """ Fungsi untuk melakukan pengecekan apakah ip tersebut private """
    regex = r"(^127\.)|(^192\.168\.)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)"

    if re.search(regex, ip):
        return True
    else:
        return False
