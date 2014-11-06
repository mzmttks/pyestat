import os
import lxml.etree


def constructURL(command, params=None):
    """ construct a URL for e-stat """
    base = "http://api.e-stat.go.jp/rest/1.0/app"
    key = os.environ["PYESTAT_KEY"]

    commandList = {
        "getStatsList": ["surveyYears", "openYears", "statsField", "statsCode",
                         "searchWord", "searchKind", "statsNameList"],
        "getMetaInfo": ["statsDataId"],
        "getStatsData": ["dataSetId", "statsDataId", "limit"]
    }

    # command check
    if command not in commandList.keys():
        raise ValueError("command must one of " + ", ".join(commandList))

    # argument check
    for param in params.keys():
        if param not in commandList[command]:
            raise ValueError(
                "argument of %s must one of " % (command)
                + ", ".join(commandList[command]))

    # construct url
    url = "%s/%s?appId=%s" % (base, command, key)
    if params:
        for key in params.keys():
            url += "&" + key + "=" + params[key]

    return url

def xml2obj_sub(xml):
    ret = {}
    for tag in xml.iterchildren():
        ret[tag.tag.lower()] = tag.text
    return ret

def xml2obj_attrib2dict(xml):
    obj = {}
    for attrib in xml.attrib.keys():
        obj[attrib.lower()] = xml.attrib[attrib]
    if xml.text:
        if obj:
            obj["text"] = xml.text
        else:
            obj = xml.text
    return obj

def xml2obj(string):
    """XML response to object"""
    xml = lxml.etree.fromstring(string)
    obj = {}

    if xml.tag == "GET_STATS_LIST":
        obj["result"] = xml2obj_sub(xml.find("RESULT"))
        obj["parameter"] = xml2obj_sub(xml.find("PARAMETER"))
        obj["datalist_inf"] = []
        for tag in xml.find("DATALIST_INF").iterfind("LIST_INF"):
            listinf = xml2obj_attrib2dict(tag)
            for tmp in tag.iterchildren():
                listinf[tmp.tag.lower()] = xml2obj_attrib2dict(tmp)
            obj["datalist_inf"].append(listinf)

        return obj

    if xml.tag == "GET_META_INFO":
        obj["result"] = xml2obj_sub(xml.find("RESULT"))
        obj["parameter"] = xml2obj_sub(xml.find("PARAMETER"))

        obj["metadata_inf"] = {}
        obj["metadata_inf"]["table_inf"] = xml2obj_sub(xml.find("METADATA_INF").find("TABLE_INF"))
        obj["metadata_inf"]["class_inf"] = []
        for tag in xml.find("METADATA_INF").find("CLASS_INF").iterchildren():
            classobj = xml2obj_attrib2dict(tag)
            classobj["class"] = [t.attrib for t in tag.iterchildren()]
            obj["metadata_inf"]["class_inf"].append(classobj)
        return obj

    if xml.tag == "GET_STATS_DATA":
        obj["result"] = xml2obj_sub(xml.find("RESULT"))
        obj["parameter"] = xml2obj_sub(xml.find("PARAMETER"))

        obj["statistical_data"] = {
            "table_inf": {},
            "class_inf": [],
            "data_inf": {"note": [], "value": []}
        }
        obj["statistical_data"]["table_inf"] = xml2obj_sub(xml.find("STATISTICAL_DATA").find("TABLE_INF"))
        for tag in xml.find("STATISTICAL_DATA").find("CLASS_INF").iterchildren():
            classobj = xml2obj_attrib2dict(tag)
            classobj["class"] = [t.attrib for t in tag.iterchildren()]
            obj["statistical_data"]["class_inf"].append(classobj)

        for tag in xml.find("STATISTICAL_DATA").find("DATA_INF").iterfind("NOTE"):
            note = xml2obj_attrib2dict(tag)
            obj["statistical_data"]["data_inf"]["note"].append(note)

        for tag in xml.find("STATISTICAL_DATA").find("DATA_INF").iterfind("VALUE"):
            value = xml2obj_attrib2dict(tag)
            obj["statistical_data"]["data_inf"]["value"].append(value)

        return obj


def find(year=None, month=None, statsCode=None, keyword=None):
    """ find stats id """

    params = {}

    ###
    ## surveyYears
    if type(year) == tuple and month is None:
        raise ValueError("if year is tuple, month must be given")

    if year is not None:
        fr = ""
        to = ""
        if type(year) == tuple and len(year) != 2:
            raise ValueError("year must be integer or 2-length tuple")
        fr = "%4d" % (year[0] if type(year) == tuple else year)
        to = "%4d" % (year[1] if type(year) == tuple else year)

        if month is not None:
            if type(month) == tuple and len(month) != 2:
                raise ValueError("month must be integer or 2-length tuple")
            fr = fr + "%02d" % (month[0] if type(month) == tuple else month)
            to = to + "%02d" % (month[1] if type(month) == tuple else month)

        if fr == to:
            params["surveyYears"] = fr
        else:
            params["surveyYears"] = fr + "-" + to


    url = constructURL("getStatsList", params)

