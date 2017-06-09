
# coding: utf-8

# In[11]:

import findspark
findspark.init()

import os
from pyspark import SparkConf, SparkContext
import datetime as dt
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.util import MLUtils
import pyspark.sql as sql;
from pyspark.sql import SQLContext, Row
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.util import MLUtils
import re


# In[13]:

sc = SparkContext()
sql = sql.SQLContext(sc)
data = sc.textFile('Crimes_-_2001_to_present.csv');
header = data.first()


crimeRDD = data.map(lambda line: re.sub(',(?=[^"]*"[^"]*(?:"[^"]*"[^"]*)*$)',"",line))
lines=crimeRDD.map(lambda line: re.sub('\"',"",line))
crimeRDD = lines.filter(lambda x: x!= header).map(lambda x: x.split(",",21))


# In[15]:

crime_agg = crimeRDD.map(lambda x: Row(ID = x[0], month = x[2].split("/")[0],
                                    day = dt.datetime.strptime(x[2].split(" ")[0], '%m/%d/%Y').strftime('%A'),
                                                             hour = dt.datetime.strptime(x[2],'%m/%d/%Y %I:%M:%S %p').hour))
crime_table = sql.createDataFrame(crime_agg)
crime_table.registerTempTable('arrests')

MonthlyPattern = sql.sql('SELECT month, count(*) as monthly_arrests FROM arrests group by month')



DayPattern = sql.sql('SELECT day, count(*) as daily_arrests FROM arrests group by day')


 
HourPattern = sql.sql('SELECT hour, count(*) as hourly_arrests FROM arrests group by hour')



# In[22]:

for c in DayPattern.collect():
    print(c)


# In[19]:

for c in MonthlyPattern.collect():
    print(c)


# In[ ]:

for c in HourPattern.collect():
    print(c)


# In[ ]:

sc.stop()

