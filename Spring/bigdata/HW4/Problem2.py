
# coding: utf-8

# In[1]:

import findspark
findspark.init()

from pyspark import SparkConf, SparkContext;
import pyspark.sql as sql;
from pyspark.sql import SQLContext;
import csv;
from pyspark.mllib.stat import Statistics
from pyspark.mllib.linalg import Vectors, Matrix, Matrices
import numpy as np
import pandas as pd
from datetime import datetime, date
import math
import re


# In[2]:




# In[3]:

sc = SparkContext()

data = sc.textFile("Crimes_-_2001_to_present.csv")
header = data.first()
crimeRDD = data.filter(lambda x: x!= header).map(lambda x: x.split(",",21))



# In[5]:




# In[4]:

#PART 1



dataP3 = crimeRDD.map(lambda x: (x[3],  x[2].split("/")[2].split(" ")[0])).filter(lambda x: int(x[1]) > 2013);
crimes_by_block = dataP3.map( lambda row: ( row[0], 1 ) ).reduceByKey( lambda x, y: x + y );
sortedblockCrimes = crimes_by_block.takeOrdered(10, key = lambda x: -x[1])

    
    


# In[5]:

sortedblockCrimes


# In[68]:

####Part 2
last5 = crimeRDD.filter(lambda x: x[17] in ['2015', '2014', '2013', '2012', '2011'])
crimes_per_beat = last5.map(lambda x: ((x[17],x[10]),1)).reduceByKey(lambda a,b: a+b)
Year = crimes_per_beat.map(lambda x: x[0][0]).distinct()
beats = crimes_per_beat.map(lambda x: x[0][1]).distinct()
beatsYears = Year.cartesian(beats).map(lambda x: (x,0))
merged = beatsYears.union(crimes_per_beat).map(lambda x: (x[0],x[1]))
merged_final = merged.reduceByKey(lambda x,y : int(x) + int(y))






# In[86]:







# In[88]:

crimes_sorted = merged_final.sortByKey(True).map(lambda x: (x[0][0], (x[0][1], x[1]))).groupByKey().mapValues(list).mapValues(lambda val: sorted(list(val)))


# In[89]:

crimes_pts = crimes_sorted.mapValues(lambda lst: [tup[1] for tup in lst]).map(lambda row: Vectors.dense(row[1:len(row)]))


# In[90]:

corr_matrix = Statistics.corr(crimes_pts)


# In[96]:

corr_matrix.flags[ 'WRITEABLE' ] = True;
np.fill_diagonal(corr_matrix, 0.0 );


# In[124]:

corr_matrix = np.tril(corr_matrix)


# In[100]:

beats = crimes_sorted.mapValues(lambda lst: [tup[0] for tup in lst])
beats_lst = beats.take(1)[0][1]


# In[125]:

corr_df = pd.DataFrame(corr_matrix, index = beats_lst, columns = beats_lst)


# In[127]:

corrs = corr_df.unstack()


# In[129]:

corrs.sort_values(ascending=False)[1:20]


# In[126]:

corr_df


# In[73]:

crimeRDD.take(10)


# In[6]:

mayorcrimes = crimeRDD.map(lambda p: (p[10],datetime.strptime(p[2],'%m/%d/%Y %I:%M:%S %p').date())).filter(lambda x: x[0].isdigit())


# In[7]:

daly = mayorcrimes.filter(lambda x: x[1] < date(2011, 5, 16))
emanuel  = mayorcrimes.filter(lambda x: x[1] >= date(2011,5,16))

daly_pairs = daly.map(lambda x: (x[0],1)) # key is district       
daly_counts = daly_pairs.reduceByKey(lambda x,y: int(x) + int(y))# months Daley in data

emm_pairs = emanuel.map(lambda x: (x[0],1)) # key is district         
emm_counts = emm_pairs.reduceByKey(lambda x,y: int(x) + int(y))




# In[8]:

daly.take(5)


# In[9]:

districtCrimes_Daly = daly.map( lambda x: ( x[ 0 ], 1 ) )                                      .reduceByKey( lambda x, y: int(x) + int(y) )                                      .map( lambda x: ( x[ 0 ], x[ 1 ] / 11) );
districtCrimes_Emmanuel  = emanuel.map(  lambda x: (x[ 0 ], 1 ) )                                     .reduceByKey(  lambda x, y: int(x) + int(y) )                                     .map(  lambda x: (x[ 0 ], x[ 1 ] / 5) );


# In[10]:

joinedDistrictCrimes = districtCrimes_Daly.join( districtCrimes_Emmanuel );
deltaDistrictCrimes = joinedDistrictCrimes.map( lambda x: x[ 1 ][ 0 ] - x[ 1 ][ 1 ] )
                                              



# In[ ]:


meanDiff = deltaDistrictCrimes.mean( );
sdDiff = deltaDistrictCrimes.sampleStdev( );
n = deltaDistrictCrimes.count( );
tstat = meanDiff / ( sdDiff / math.sqrt( n ) );


# In[6]:

sc.stop()





