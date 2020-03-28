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
  <br/>
  <img src="http://latex.codecogs.com/svg.latex?f_%7BM%7D%5C%20%5Ctextit%3A%5C%20M%5C%20%5Crightarrow%5C%20I%20%5C%5C">
</p>
Define the mapping *g* 𝑔 : 𝑆 → 𝑀 such that the set 𝑔(𝑆<sub>𝑖</sub>) is all molecules containing a scaffold 𝑆<sub>𝑖</sub>, 𝑁<sub>𝑆<sub>𝑖</sub></sub>=|𝑔(𝑆<sub>𝑖</sub>)| is the number of molecules in this set, and 𝑁<sub>𝑆<sub>𝑖</sub>, 𝐼<sub>j</sub></sub> is the number of molecules that have a certain indication 𝐼<sub>j</sub> and belong to a certain scaffold 𝑆<sub>𝑖</sub>:
<p align="center">
  <br/>
  <img src="http://latex.codecogs.com/svg.latex?N_%7BS_%7Bi%7D%2C%20I_%7Bj%7D%7D%3D%5Cleft%7C%5Cleft%5C%7Bm%20%7C%20m%20%5Cin%20g%5Cleft%28S_%7Bi%7D%5Cright%29%20%5Ctext%20%7B%20and%20%7D%20f%28m%29%3DI_%7Bj%7D%5Cright%5C%7D%5Cright%7C"> 
</p>

