# Determining-Location-Accuracy
My CapStone Project at LightHouse Labs (presented on March 31, 2022) in partnership with Ocean Wise.

## *Disclaimer*
This repo does not include the real data used. Furthermore:

*Data obtained from the B.C. Cetacean Sightings Network were collected opportunisticailly with limited knowledge of the temporal or spatial distribution of observer effort. A series of calculations used in Geographic Information Systems (GIS) framework were undertaken to reconstruct the distribution of observer effort<sup>1</sup>.*


# Table of Contents
* [About Ocean Wise](#about-ocean-wise)
* [Aim](#aim)
* [Project Description](#project-description)
* [The Approach](#the-approach)
* [How to Run the Model](#how-to-run-the-model)
* [Limitations of the Model](#limitations)
* [Results](#results)
* [Further Improvements](#further-improvements)
* [References](#references)


# About Ocean Wise 🐳

![image](./Images/oceanwise_logo.jpg)

Ocean Wise Conservation Association is a non-profit Organization based in Vancouver, British Columbia. Their mission is to protect our world's oceans and freshwater through empowering communities and individuals to take action. OceanWise also conducts research on marine mammals, ocean polution, and plastics.

To learn more about Ocean Wise, you can click [here](https://ocean.org/).

# Aim
The aim of this project is to streamline the process of determining location accuracy of whale, dolphin and turle sightings off the coast of British Columbia.

# Project Description
This project will determine the location accuracy of animal sightings using data from OceanWise BC Cetacean Sightings Network. Using machine learning, the goal is to create a classification model that can accurately predict the location accuracy. 

Location accuracy takes into account the observer’s specific coordinates that are reported in order to find the animal's proximity. This is because the coordinates submitted are of the observer's position (ie. mobile submission) and not the actual animal, so we want to know how close the observer actually was. 

At the end of the project, the aim is to be able to deploy a model that will intake data and predict the location accuracy for each new animal sighting, thereby automating and streamlining the process for staff at OceanWise. 

# The Approach

In the span of less than 10 days, my approach was rather straightforward. The majority of my time was spent cleaning the data and looking at feature engineering, followed by data analysis (ANOVAs & Chi-Square tests).

After this, I went ahead and ran baseline pipelines to check how different preprocessing of features my impact the model. Once this was done and the final pipeline was built I ran several models: Logistic Regression, SVC, Random Forest and XGBoost (especially since the data was non-linear).

# How to Run the Model
The toy dataset, represents what data is expected as input by the model, but is not actual data from Ocean Wise.


# Limitations of the Model
Finding Location Accuracy of cetaceans can be quite difficult, this is because your target is in constant motion.However, when it came to the limitations of my data for training a model there were two major limitations. 

First, 37% of rows my target variable were missing and as I had no way to fill these out, this resulted in me dropping the data. 

The second limitation also dealt with the target variable. The target variable had 13 categories, which had to be binned. However on top of this, the data was extemely unbalanced as one category had 66% of the data. As such I had to apply a limitation following the organization's protocol. As such, I was left with 31% of the original data.

# Results

As a result of the limitations to my data, the accuracies of the resulting models were not high, but it proves the concept that we can predict Location Accuracy.

![image](./Images/Model_Accuracies.png)

The biggest take away is that there was only one major difference between Model 3 and Model 4. Both used XGBoost, but Model 4 included another column that had 36% of missing data, which this model can handle. This increased the accuracy by 2% as well. Looking more closely we can see that the F1 Score (ie. Sensitivity and Specificity of the model to predict the target values) increased for two categories.

![image](./Images/Model_Comparison.png)

# Further Improvements
There are number of methods that can be done to improve this model.

1. More Data.
2. Identify if coordinates are on land
3. Further Feature Engineering:
    * Use geopy.
4. Try a Deep Learning Model

# References

1. Rechsteiner, E.U, Birdsall, C.F.C., Sandilands, D., Smith, I.U., Phillips, A.V., Barrett-Lennard, L.G. (2013). Quantifying observer effort for opportunistically collected wildlife sightings. B.C. Cetacean Sightings Network: Technical Report. Vancouver, B.C.: Ocean Wise Conservation Association. 43pp.