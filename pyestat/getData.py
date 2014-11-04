import os

def constructURL(command, params=None):
    """ construct a URL for e-stat """
    base = "http://api.e-stat.go.jp/rest/1.0/app"
    key  = os.environ["PYESTAT_KEY"]

    commandList = {
        "getStatsList": ["surveyYears", "openYears", "statsField", "statsCode",
                         "searchWord", "searchKind", "statsNameList"],
        "getMetaInfo" : ["statsDataId"],
        "getStatsData": ["dataSetId", "statsDataId", "limit"]
    }

    # command check
    if not command in commandList.keys():
        raise ValueError(
            "command must one of " + ", ".join(commandList))

    # argument check
    for param in params.keys():
        if not param in commandList[command]:
            raise ValueError(
                "argument of %s must one of " % (command) \
                + ", ".join(commandList[command]))        

    # construct url
    url = "%s/%s?appId=%s" % (base, command, key)
    if params:
        for key in params.keys():
            url += "&" + key + "=" + params[key]

    print url
    return url


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