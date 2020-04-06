import csv
import os
import sys
from pathlib import Path
# Spark imports
from pyspark.rdd import RDD
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import math


# ploting
import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd 
from shapely.geometry import Point,Polygon


def plot():
	spray_df = pd.read_csv(str(Path().absolute())+'/test.csv')
	geometry = [Point(xy) for xy in zip(spray_df.LONGITUDE, spray_df.LATITUDE)]

	spray_df['geometry'] = geometry
	spray_df.drop(['LATITUDE','LONGITUDE'], axis = 1, inplace=True)
	crs = {'init': 'epsg:4326'}
	street_map=gpd.read_file(str(Path().absolute())+"/get_geojson.txt")
	ax = street_map.plot(color='grey',figsize=(15,15))
	allofthem=spray_df.cluster
	allofthem=allofthem.count()
	for i in range(410):
  		tmp=spray_df[spray_df.cluster==i]
  		spray_locs = gpd.GeoDataFrame(tmp, crs=crs)
  		alpha=tmp.cluster
  		alpha=alpha.count()
  		alpha=float(alpha/allofthem)*100
  		spray_locs.geometry.plot(marker='d', color='r', markersize=1, ax=ax , alpha=alpha)
	plt.title('Montreal crimes')
	plt.show()



def init_spark():
    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL basic example") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()
    return spark


def distnaces(points,threshold):
	for point1 in points:
		for point2 in points:
			(a,b)=point2
			tmp=math.sqrt(sum([(float(a) - float(b)) ** 2 for a, b in zip(point1, point2)]))
			if tmp>threshold:
				return False
	return True


def clustering(filename):
	spark = init_spark()
	rdd=spark.sparkContext.textFile(filename)
	header = rdd.first()
	rdd=rdd.filter(lambda x:x!=header)
	rdd=rdd.mapPartitions(lambda x: csv.reader(x))
	rdd=rdd.filter(lambda x: x[6] != '1' and x[7] != '1')
	rddprim=rdd.map(lambda x:(x[6],x[7]))
	rdd=rdd.map(lambda x:(float(x[6])*100000,float(x[7])*100000))
	rdd=rdd.map(lambda x:[int(x[0]),int(x[1])])
	locations=rdd.collect()
	X=np.array(locations)
	kmeans = KMeans(n_clusters=410, random_state=0).fit(X)
	labels={}
	points=rddprim.collect()

	# x = (45.488568, 73.643122)
	# y = (45.484567, 73.646684)
	# threshold = math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))


	for label in range(len(kmeans.labels_)):
		labels[points[label]]=kmeans.labels_[label]

	# clusters={cluster:[] for cluster in kmeans.labels_}
	# for key in labels.keys():
	# 	clusters[labels[key]].append(key)
	# for cluster in clusters.keys():
	# 	clusters[cluster]=len(clusters[cluster])
	# rdd=spark.sparkContext.parallelize(clusters.items())
	# rdd=rdd.sortBy(lambda x:x[1],ascending=False)
	# rdd=rdd.map(lambda x:x[0])
	# clusters=


	# for cluster in clusters.keys():
	# 	if distnaces(clusters[cluster],7*threshold)==False:
	# 		print(cluster)
	# 		return False
	# return True




	with open(str(Path().absolute())+'/test.csv','w',newline='') as f:
		thewriter=csv.writer(f)
		thewriter.writerow(['LONGITUDE','LATITUDE','cluster'])
		for i in labels.items():
			thewriter.writerow([i[0][0],i[0][1],i[1]])

	
		

	


if __name__=="__main__":
	clustering(str(Path().absolute())+"../data/crimes_dataset.csv")
	plot()






