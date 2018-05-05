# -*-coding:utf-8-*-
import geoip2.database
import os

from flask_babel import gettext
from geoip2.errors import AddressNotFoundError

from apps.core.plug_in.config_process import import_plugin_config

import_plugin_config("geoip_plugin", {})
curren_path = os.path.abspath(os.path.dirname(__file__))
__author__ = "Allen Woo"

def main(*args, **kwargs):

    '''
    插件主函数, 根据ip获取地理位置
    :return:
    '''

    ip = kwargs.get("ip")
    reader = geoip2.database.Reader('{}/GeoLite2-City/GeoLite2-City.mmdb'.format(curren_path))
    geo = {}
    try:
        response = reader.city(ip)
    except AddressNotFoundError:
        geo["continent"] = {"name": gettext("Local")}
        return geo

    geo["continent"] = {}
    geo["continent"]["code"] = response.continent.code
    geo["continent"]["name"] = response.continent.names["es"]
    geo["continent"]["names"] = response.continent.names

    geo["country"] = {}
    geo["country"]["iso_code"] = response.country.iso_code
    geo["country"]["name"] = response.country.name
    geo["country"]["names"] = response.country.names

    geo["subdivisions"] = {}
    geo["subdivisions"]["iso_code"] = response.subdivisions.most_specific.iso_code
    geo["subdivisions"]["name"] = response.subdivisions.most_specific.name
    geo["subdivisions"]["names"] = response.subdivisions.most_specific.names

    geo["coordinates"] = {}
    geo["coordinates"]["lat"] = response.location.latitude
    geo["coordinates"]["lon"] = response.location.longitude
    geo["coordinates"]["accuracy_radius"] = response.location.accuracy_radius
    geo["coordinates"]["time_zone"] = response.location.time_zone

    geo["postal"] = {}
    geo["postal"]["code"] = response.postal.code

    return geo