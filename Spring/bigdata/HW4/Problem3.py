
# coding: utf-8

# In[112]:

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


# In[114]:

sc.stop()


# In[115]:

sc = SparkContext()

data = sc.textFile('Crimes_-_2001_to_present.csv');
header = data.first()


crimeRDD = data.map(lambda line: re.sub(',(?=[^"]*"[^"]*(?:"[^"]*"[^"]*)*$)',"",line))
lines=crimeRDD.map(lambda line: re.sub('\"',"",line))
crimeRDD = lines.filter(lambda x: x!= header).map(lambda x: x.split(",",21))


# In[105]:

beats = crimeRDD.filter(lambda x: x[10].isdigit()).map(lambda x: (x[10],dt.datetime.strptime(x[2], '%m/%d/%Y %I:%M:%S %p' )))
yearWeeks = weeklycrimeCounts.map( lambda x: ( x[ 0 ][ 1 ], x[ 0 ][ 2 ] ) ).distinct( );
BeatYearWeeks = beats.values( ).cartesian( yearWeeks ).map( lambda x: ( x[ 0 ], x[ 1 ][ 0 ], x[ 1 ][ 1 ] ) );
zeroWeeks = BeatYearWeeks.subtract( weeklycrimeCounts.keys( ) );
totalCrime = weeklycrimeCounts.union(zeroWeeks.map( lambda x: ( x, 0 ) ) );



( training, test ) = totalCrime.randomSplit( ( 0.9, 0.1 ) );
model = RandomForest.trainRegressor( training, categoricalFeaturesInfo = featuresInfo,
                                         numTrees = 20, featureSubsetStrategy = "auto",
                                         impurity = 'variance', maxDepth = 10, maxBins = len( beatsDict ) );
    
    # Measure the model performance on test dataset
prediction = model.predict( test.map( lambda x: x.features ) ); 

    
meanCrimes = test.map( lambda x: x.label ).mean( );
labelsAndPredictions = test.map( lambda x:  x.label ).zip( prediction );
testMSE = labelsAndPredictions.map( lambda ( actual, predicted ): ( actual - predicted ) * ( actual - predicted ) ).sum( ) / float( test.count( ) );
testSSE = labelsAndPredictions.map( lambda ( actual, predicted ): ( actual - predicted ) * ( actual - predicted ) ).sum( );
testSST = labelsAndPredictions.map( lambda ( actual, predicted ): ( actual - meanCrimes ) * ( actual - meanCrimes ) ).sum( );
    
Rsquared = 1 - testSSE / testSST;





# In[106]:


beatsTransform = dict( ( val, key ) for key, val in beatsDict.items( ) );
nextWeek = sc.parallelize( tuple( [ ( beat, weekNum) for beat in range( len( beatsDict ) ) ] ) );
predictionsNextWeek = model.predict( nextWeek ).zip( nextWeek.map( lambda x: beatsTransform[ x[ 0 ] ] ) ).sortByKey( False );



# In[107]:




# In[ ]:




# In[108]:




# In[110]:





