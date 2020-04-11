# Analyzing Criminal Acts In The City of Montreal

Yashar Dabiran(@yshrdbrn), Shiva Shamloo(@sshamlo)

## Abstract
In this report, we focus on finding spatial and temporal criminal hotspots. We analyze the dataset from the city of Montreal and our goal is to find criminal patterns and predict potential criminal types. We are going to use Random Forest classifier to predict potential crime types and K-means to detect criminal hotspots. This report would help the people living in Montreal to be more aware of criminal activities in different neighbourhoods and would help the police to predict future crimes in a specific location within a particular time therefore  helping them to put more/less patrol in certain areas of the city at a particular time.

## Introduction
Crimes can affect the economic growth of a city by different means, including the prvention of people moving to that city or affecting the travelers. However these factors can be controlled by knowing the fact that crimes usually happen in some neighborhoods more than others since criminals normally commit the same crimes at a same location. Mining the Montreal crime dataset will provide information about which blocks and streets crimes happen more frequently. When presented demographically, the result can help civilians to know which neighborhoods to buy houses in or help _SPVM_ relocate forces to fight crimes more efficiently.

### Problem Statement
Our project tries to spot different criminal zones in the Montreal city and predicts different crime types given specific requirements. Some of the problems we are faced include incomplete datasets and finding good measurements to classify neighborhoods' safety. To overcome some of these obstacles, we define new features that are independant from the missing values.

### Related Work
lots of research has been done on criminal acts around the world. Works ranging from utilizing spacial data to predict different crime types [3] to exploring relationships between the criminal activity and social values including education and ethnicity. There is a similar research to this project that works with the criminal acts datasets of Denver and Los Angeles [2]. Despite all the existing work done, we could not find any report that analyzes the dataset of the city of Montreal.

## Materials and Methods

### Dataset
Our dataset is the criminal acts recorded by the Montreal Police Service [1]. The dataset is consisted of 8 columns:

* **Category:** Type of the crime that can either be:
  * “Introduction” which means breaking and entering a public establishment or a private residence, theft of a firearm from a residence.
  * “Vol dans / sur véhicule à moteur” that is a theft of the contents of a motor vehicle (car, truck, motorcycle, etc.) or of a vehicle part (wheel, bumper, etc.).
  * “Méfait” which is a graffiti and damage to religious property, vehicle or general damage and all other types of mischief.
  * “Vol qualifié” that corresponds to a robbery accompanied by commercial violence, financial institution, person, handbag, armored vehicle, vehicle, firearm, 	and all other types of robbery.
  * “Infraction entraînant la mort” that means a first degree murder, second degree murder, manslaughter, infanticide, criminal negligence, and all other types of offenses resulting in death.

* **Date:** the date that the event was reported to the police.

* **Quart:** the time of the reported event.

* **PDQ:** Neighbourhood station number covering the territory where the event took place. For finding the territories we use another dataset that shows the territory assigned to each station.

* **X and Y:** Geospatial position. The value 0 means no geographic position was provided when entering the information.

* **Latitude and longitude:** geographic position of the event after obfuscation at an intersection. The value 1 means no geographic position was provided when entering the information.

### Data Preparation
In order to be able to use to the dataset in later stages, we needed to modify it. We were faced with two challenges:

**Missing Coordinates:** 

About 18% of the records were missing latitude and longitude. Since both of the algorithms use coordinates as hyper-parameters, reasonable-enough coordinates had to be added to each record or the record had to be deleted. The proposed substitute coordinates were the police station's coordinates that the crime was reported it. Since this approach was going to be applied to about 1/5th of the records, it would introduce considerable amount of bias so we decided to delete the incomplete records.

**Compound date format:**

The date column is in the format `YYYY-MM-DD`. In order to have more relevant hyper-parameters the date column is replaced with 3 columns: _Year_, _Month_ and _Day of the week_.

The processed dataset is in [data/crimes_dataset_processed.csv](data/crimes_dataset_processed.csv).

### Methods and Algorithms

In this project we used K-means in order to detect crime hotspots In order to do so, we defined the location of each crime as the feature vector. Assuming to be in euclidean space, we tried to tune out hyper parameter which is the number of clusters by defining a max distance and by putting a constraint on each cluster that every point in a cluster should have no more than the max distance. As a result we’ve reached k=410 for the maximum distance of 35 blocks.
On the other hand, we used Random forest to predict a crime category. In this case there are many hyperparameters. To find the best hyper parameters we used Grid Search for different number of decision trees, different depths etc.

We use _PySpark_ for data preprocessing and extracting the new features. We also use _scikit-learn_ python library in order to build our model, make predictions and compute the accuracy.

## Results

The final result of the K-means shows that most of the crimes, regardless of their categories, happen in the east side of the city. Figure **** shows the centroid of each cluster with respect to its points abundance. Furthermore, we were able to achieve 43% accuracy for predicting the crime category based on the location, date and time. We also computed other measurements such as precision and recall with one versus the other algorithm.

## Discussion

The results of our crime prediction model and the clustering method can be combined and used by the police department to better allocate their resources. One possible application is to use the crime prediction model on the criminal hotspots obtained to figure out what kind of forces to dispatch to those areas.

One of the limitations we faced was the relatively small size of the dataset. There are a total of 160,000 records in the dataset, with about 20% of them missing coordinates. The records date back to 2015. More accurate results would have been obtained if the crime reports before 2015 were also included.

We see two possible areas of expansion over this project. One is to find an alternative approach on the missing coordinates data issue. If a method manages to keep all the records and deal with the missing data, it can get a higher accuracy. The other area of improvement is related to the crime classification. Crimes labeled as _Homicide_ are under-represented in the database. An appropriate over-sampling method could result in a better prediction accuracy.

## References

- [1] “Actes Criminels - CKAN.” Portail Données Ouvertes, [donnees.ville.montreal.qc.ca/dataset/actes-criminels](http://donnees.ville.montreal.qc.ca/dataset/actes-criminels).

- [2] Almanie, Tahani, Rsha Mirza, and Elizabeth Lor. “Crime Prediction Based on Crime Types and Using Spatial and Temporal Criminal Hotspots.” International Journal of Data Mining & Knowledge Management Process 5.4 (2015): 01–19. Crossref. Web.

- [3] A. Bogomolov, B. Lepri, J. Staiano, N. Oliver, F. Pianesi and A. Pentland, 'Once Upon a Crime:
Towards Crime Prediction from Demographics and Mobile Data', CoRR, vol. 14092983, 2014.

## Links

- Link to the presentation slides of this report: [Google Slides](https://docs.google.com/presentation/d/1A4TlqJgyWdAggv6G-6znV3cT4ctaH6XQAbrEQ9PcpZ8/edit?usp=sharing)