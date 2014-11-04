pyestat
=======

Overview
--------
Python Interface of e-Stat (Japanese Statistics Information)
URL:
http://statdb.nstac.go.jp/system-info/api/

The interface is compativle with version 1.0.

Before you use
--------------
You need to set your api key to an environment variable `PYESTAT_KEY`
You can get it at http://statdb.nstac.go.jp/regist-login/ 

Function1: Search
-----------------
```python
import pyestat

## date 
# find stats on 2010
result = pyestat.find(year=2010)

# find stats on 2010-12
result = pyestat.find(year=2010, month=12)

# find stats from 2010-10 to 2014-10
result = pyestat.find(year=(2010, 2014), month=10)

# find stats from 2010-1 to 2014-10
result = pyestat.find(year=(2010, 2014), month=(1, 10))

# find stats from 2010-1 to 2010-10
result = pyestat.find(year=2010, month=(1, 10))

## statistics code
result = pyestat.find(statsCode="00200521")  # 国勢調査

## keyword 
result = pyestat.find(keyword=u"人口")
result = pyestat.find(keyword=[u"人口", u"住宅"])  # 複数キーワードは AND 
```

* Get Data
```python
import pyestat

statsDataId = "0000032266"
data = pyestat.getData(statsDataId)
```

Dependency
-----------
lxml
