# Privileged Scaffold Analysis of Natural Products with Deep Learning-based Indication Prediction Model
In this study, we propose a privileged scaffold identification strategy for natural products. The term ‘privileged scaffold’ or ‘privileged structure’ was first used by Evans in the 1980s to describe scaffolds that could serve as ligands for multiple targets. And the notion was later expanded to that a scaffold is privileged if multiple molecules of the same scaffold have bioactivity. Here we use the term and make some restrictions, that is, multiple molecules of the same scaffold have bioactivity for the same indication. 
To identify privileged scaffolds, a multi-task deep learning model was first trained on the MDDR dataset for indication prediction. By using larger training data than approved drugs, the model could learn how to predict the indication of compounds better. The trained model was applied to the natural product dataset, which was composed of six public datasets to provide more diverse scaffolds. Cross-validation showed that the model had good discrimination ability. The identification strategy made use of entropy-based information metrics to obtain privileged scaffolds for each indication. A Privileged Scaffold Dataset (PSD) for one hundred indications was obtained, which could be used as a novel source for lead discovery and optimization.  

![image](https://github.com/wllllg/Privileged_Scaffold/raw/master/img/privileged_scaffolds_Shannon_Entropy.jpg)
**Figure 1. Privileged Scaffolds Identified using Shannon Entropy.**
![image](https://github.com/wllllg/Privileged_Scaffold/raw/master/img/privileged_scaffolds_p_value_antihypertensive.jpg)
**Figure 2. Privileged Scaffolds for Antihypertensitve Identified using p-value.**

## Methods
The trained indication prediction model was applied to the natural product dataset. In order to get the privileged scaffolds of natural products for each indication, two entropy-based information metrics, p-value and Shannon entropy (SE), were calculated. P-value was used as criteria to get the privileged scaffolds for each indication, and SE was used to determine the promiscuity of a scaffold. The definitions of these two metrics are as follows. Suppose 𝐼 is the set of all indications, 𝑀 is the set of all natural products, and 𝑆 is the set of all scaffolds:  
<p align="center">
  <img src="http://latex.codecogs.com/svg.latex?\\I=\left\{I_{1},I_{2},\ldots,I_{m}\right\}"> <br/>
  <img src="http://latex.codecogs.com/svg.latex?\\M=\left\{m_{1},m_{2},\ldots,m_{l}\right\}"> <br/>
  <img src="http://latex.codecogs.com/svg.latex?\\S=\left\{S_{1},S_{2},\ldots,S_{n}\right\}">
</p>
The indication prediction model 𝑓 is the mapping from the natural product set 𝑀 to the indication set 𝐼:
<p align="center">
  <img src="http://latex.codecogs.com/svg.latex?f_%7BM%7D%5C%20%5Ctextit%3A%5C%20M%5C%20%5Crightarrow%5C%20I%20%5C%5C"> <br/>
</p>
Define the mapping *g* 𝑔 : 𝑆 → 𝑀 such that the set 𝑔(𝑆<sub>𝑖</sub>) is all molecules containing a scaffold 𝑆<sub>𝑖</sub>, 𝑁<sub>𝑆<sub>𝑖</sub></sub>=|𝑔(𝑆<sub>𝑖</sub>)| is the number of molecules in this set, and 𝑁<sub>𝑆<sub>𝑖</sub>, 𝐼<sub>j</sub></sub> is the number of molecules that have a certain indication 𝐼<sub>j</sub> and belong to a certain scaffold 𝑆<sub>𝑖</sub>:
*I = {I<sub>1</sub>, *
Define the mapping 𝑔:𝑆→𝑀 such that the set 𝑔(𝑆<sub>𝑖</sub>) is all molecules containing a scaffold 𝑆𝑆𝑖𝑖, 𝑁𝑁𝑆𝑆𝑖𝑖=|𝑔𝑔(𝑆𝑆𝑖𝑖)| is the number of molecules in this set, and 𝑁𝑁𝑆𝑆𝑖𝑖,𝐼𝐼𝑗𝑗 is the number of molecules that have a certain indication 𝐼𝐼𝑗𝑗 and belong to a certain scaffol d 𝑆𝑆𝑖𝑖: 𝑁𝑁𝑆𝑆𝑖𝑖,𝐼𝐼𝑗𝑗=|�𝑚𝑚|𝑚𝑚∈𝑔𝑔(𝑆𝑆𝑖𝑖) 𝑎𝑎𝑎𝑎𝑎𝑎 𝑓𝑓(𝑚𝑚)=𝐼𝐼𝑗𝑗�| Then the p-value of a scaffold 𝑆𝑆𝑖𝑖 for a certain indication 𝐼𝐼𝑗𝑗 can be defined as: 𝑝𝑝𝐼𝐼𝑗𝑗(𝑆𝑆𝑖𝑖 )=𝑁𝑁𝑆𝑆𝑖𝑖,𝐼𝐼𝑗𝑗 𝑁𝑁𝑆𝑆𝑖𝑖 For a certain scaffold 𝑆𝑆𝑖𝑖, we can calculate the Shannon entropy 𝑆𝑆𝑆𝑆(𝑆𝑆𝑖𝑖) of the scaffold:  𝑆𝑆𝑆𝑆(𝑆𝑆𝑖𝑖)=−�𝑝𝑝𝐼𝐼𝑗𝑗(𝑆𝑆𝑖𝑖 )𝑙𝑙𝑎𝑎𝑝𝑝𝐼𝐼𝑗𝑗(𝑆𝑆𝑖𝑖 ) 𝑚𝑚 𝑗𝑗 The p -value is between 0 and 1. If the p-value is 1, then all natural products with the scaffold 𝑆𝑆𝑖𝑖 have the indication 𝐼𝐼𝑗𝑗, that is, the scaffold 𝑆𝑆𝑖𝑖 is the 

