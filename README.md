# Analyzing Criminal Acts In The City of Montreal

## Abstract
In this report, we focus on finding spatial and temporal criminal hotspots. We analyze the dataset from the city of Montreal and our goal is to find criminal patterns and predict potential criminal types. We are going to use Random Forest classifier and Support Vector Machines in order to predict potential crime types. This report would help the people living in Montreal to be more aware of criminal activities in different neighbourhoods and would help the police to predict future crimes in a specific location within a particular time therefore  helping them to put more/less patrol in certain areas of the city at a particular time.

## Introduction
Crimes can affect the economic growth of a city by different means, including the prvention of people moving to that city or affecting the travelers. However these factors can be controlled by knowing the fact that crimes usually happen in some neighborhoods more than others since criminals normally commit the same crimes at a same location Mining the Montreal crime dataset will provide information about which blocks and streets crimes happen more frequently. When presented demographically, the result can help civilians to know which neighborhoods to buy houses in or help _SPVM_ relocate forces to fight crimes more efficiently.

### Problem Statement
Our project tries to spot different criminal zones in the Montreal city and predicts different crime types given specific requirements. Some of the problems we are faced include incomplete datasets and finding good measurements to classify neighborhoods' safety. To overcome some of these obstacles, we define new features that are independant from the missing values.

### Related Work
There have been several works done in order to identify crime spots using the locations. Also, there are several applications that show the exact location and crime type for a given city. Furthurmore, there are some previous work regarding the relationship between the time and location of the crime. Other works mainly focus on the relationships between the criminal activity and socio-economics variables such as ethnicity, education and income level. In this project we try to focus on the prediction of a crime type and the safety of a neighbourhood.
## Materials and Methods

### Dataset
Our dataset is the criminal acts recorded by the Montreal Police Service. The dataset is consisted of 8 columns:

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


### Methods and Algorithms

>**Random Forest:** Random Forest is a classifier technic that integrate out the arbitrariness of decision trees in order to get some expectations over all of the decision trees that could have fit the data. It builds a lot of different decision trees that fit the data and then averages their predictions.

>**Support Vector Machines:** SVMs are supervised learning models that tries to fit a hyperplane to the data in order to classify it. It can be used for binary classification as well as multi-class classification. A good classification is achieved by the hyperplane that has the largest distance to the nearest training-data point of any class. 

In this project we are going to use these methods with existing features such as type of the crime and the location of the crime, as well as defining new features such as frequency of the crime in order to predict whether that location is safe or not, and if not, what kind of crime is probable to happen at that place. For this purpose we are going to use some tools for data preprocessing such as _Spark_ to define and extract the new features. Afterwards, we are going to use the _scikit-learn_ python library in order to build our model, make predictions and compute the accuracy.
