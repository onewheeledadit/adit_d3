
# coding: utf-8

# In[63]:

from pyspark import SparkConf, SparkContext;
import pyspark.sql as sql;
from pyspark.sql import SQLContext;
import csv;


# In[64]:

sc.stop()


# In[65]:

sc = pyspark.SparkContext()
sql = pyspark.sql.SQLContext(sc)
data = sc.textFile("Crimes_-_2001_to_present.csv").map(lambda x: x.split(",",21))


# In[67]:




# In[66]:

header = data.first() #extract header
data = data.filter(lambda x: x != header)
df = sql.createDataFrame(data, header).cache()


# In[68]:

udfMonth = pyspark.sql.functions.udf(lambda x: x.split("/")[0], pyspark.sql.types.StringType())
df = df.withColumn("Month", udfMonth("Date"))

udfYear = pyspark.sql.functions.udf(lambda x: x.split("/")[2].split(" ")[0], pyspark.sql.types.StringType())
df = df.withColumn("Year", udfYear("Date"))


# In[69]:

df.createOrReplaceTempView("histogram")





# In[70]:

histo = sql.sql('select Month, count(ID) / count(distinct Year) as avg from histogram group by Month');


# In[71]:

histo.collect()


# In[ ]:



