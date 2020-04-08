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


def cluster_centriods(points):
	clusters = points.groupby(['cluster']).mean()
	clusters['size'] = points.groupby(['cluster']).size()
	return clusters

def plot():
	points = pd.read_csv(str(Path().absolute())+'/clusters.csv')
	clusters = points.groupby(['cluster']).mean()
	clusters['size'] = points.groupby(['cluster']).size()
	clusters['geometry'] = [Point(xy) for xy in zip(clusters.LONGITUDE, clusters.LATITUDE)]
	clusters.drop(['LATITUDE','LONGITUDE'], axis = 1, inplace=True)

	montreal_map=gpd.read_file('montreal_boundaries.geojson')
	ax = montreal_map.plot(color='grey')
	max_cluster_size = clusters['size'].max()
	for i in range(410):
  		tmp=clusters[clusters.index==i]
  		spray_locs = gpd.GeoDataFrame(tmp, crs={'init': 'epsg:4326'})
  		alpha=float(tmp.loc[i, 'size'] / max_cluster_size)
  		spray_locs.geometry.plot(color='red', markersize=20, ax=ax , alpha=alpha)
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

	for label in range(len(kmeans.labels_)):
		labels[points[label]]=kmeans.labels_[label]

	with open(str(Path().absolute())+'/clusters.csv','w',newline='') as f:
		thewriter=csv.writer(f)
		thewriter.writerow(['LONGITUDE','LATITUDE','cluster'])
		for i in labels.items():
			thewriter.writerow([i[0][0],i[0][1],i[1]])


if __name__=="__main__":
	clustering(str(Path().absolute())+"/../data/crimes_dataset.csv")
	plot()
