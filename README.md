# Determining-Location-Accuracy
Final Project for LightHouse Labs Data Science Bootcamp, in partnership with OceanWise.

## *Disclaimer*
This repo does not illstrate all my work, just the final product after 10 days for my CapStone Project at LHL (presented on March 31, 2022). In this repo you will see some plots, old models trained, in addition to a toy dataset, requirements.txt and python file for running the model.

# Table of Contents
* [Aim](#aim)
* [About Ocean Wise](#about-ocean-wise)
* [Project Description](#project-description)
* [Trends in the Data](#trends-in-the-data)
* [The Approach](#the-approach)
* [Limitation](#limitations)
* [Results](#results)
* [Further Improvements](#further-improvements)
* [How to Work the Model](#how-to-work-the-model)

# Aim
The aim of this project is to streamline the process of determining location accuracy of whale, dolphin and turle sightings off the coast of British Columbia.

# About Ocean Wise

![image](./Images/oceanwise_logo.jpg)

OceanWise Conservation Association is a nonprofit Organization based in Vancouver, British Columbia. Their mission is to protect our world's oceans and freshwater through empowering communities and individuals to take action. OceanWise also conducts research on marine mammals, ocean polution, and plastics.

To learn more about Ocean Wise, you can go [here](https://ocean.org/).

# Project Description
This project will determine the location accuracy of animal sightings using data from OceanWise BC Cetacean Sightings Network. Using machine learning, the goal is to create a classification model that can accurately predict the location accuracy. 

Location accuracy takes into account the observer’s specific coordinates that are reported in order to find the animal's proximity. This is because the coordinates submitted are of the observer's position (ie. mobile submission) and not the actual animal, so we want to know how close the observer actually was. 

At the end of the project, the aim is to be able to deploy a model that will intake data and predict the location accuracy for each new animal sighting, thereby automating and streamlining the process for staff at OceanWise. 

# Trends in the Data
![plot](./Images/Plots/Data_Source.png)

![plot](./Images/Plots/Experience.png)

![plot](./Images/Plots/Time_Of_Day.png)

![plot](./Images/Plots/Seasons_Species.png)

![plot](./Images/Plots/SeaConditions_LocationAccuracy.png)

# The Approach


# Limitations
Finding Location Accuracy of cetaceans can be quite difficult, this is because your target is in constant motion.

# Results


# Further Improvements
There are number of methods that can be done to improve this model.

1. More Data - I was quite Limited.
2. Further Feature Engineering:
* Use geopy on ranges of sighting distance given by observer and find average.
* Further group other features such as Sighting Platform

# How to Work the Model