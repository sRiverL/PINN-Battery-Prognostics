# PINN_Battery_Prognostics

This repository includes the code and data for the paper "***Physics-Informed Neural Networks for Prognostics and Health Management of Lithium-Ion Batteries***"

## Abstract

For Prognostics and Health Management (PHM) of Lithium-ion (Li-ion) batteries, many models have been established to characterize their degradation process. The existing empirical or physical models can reveal important information regarding the degradation dynamics. However, there are no general and flexible methods to fuse the information represented by those models. Physics-Informed Neural Network (PINN) is an efficient tool to fuse empirical or physical dynamic models with data-driven models. To take full advantage of various information sources, we propose a model fusion scheme based on PINN. It is implemented by developing a semi-empirical semi-physical Partial Differential Equation (PDE) to model the degradation dynamics of Li-ion batteries. When there is little prior knowledge about the dynamics, we leverage the data-driven Deep Hidden Physics Model (DeepHPM) to discover the underlying governing dynamic models. The uncovered dynamics information is then fused with that mined by the surrogate neural network in the PINN framework. Moreover, an uncertainty-based adaptive weighting method is employed to balance the multiple learning tasks when training the PINN. The proposed methods are verified on a public dataset of Li-ion Phosphate (LFP)/graphite batteries.

![PINN-Verhulst](https://github.com/WenPengfei0823/PINN-Battery-Prognostics/blob/main/Documents/PINN_Verhulst.jpg "Model fusion with *a priori* known dynamic model.")

![PINN-DeepHPM](https://github.com/WenPengfei0823/PINN-Battery-Prognostics/blob/main/Documents/PINN_DeepHPM.jpg "Model fusion without *a priori* known dynamic model.")

## Citation

> ```
> @article{Wen2023_PINN,
> author = {Wen, Pengfei and Ye, Zhi-Sheng and Li, Yong and Chen, Shaowei and Xie, Pu and Zhao, Shuai},
> title = {Physics-informed neural networks for prognostics and health management of lithium-ion batteries},
> journal = {IEEE Transactions on Intelligent Vehicles},
> year = {2023},
> type = {Journal Article},
> pages = {to be published},
> doi = {10.1109/TIV.2023.3315548}
> }
> ```


## Instruction

1. Run "LoadData.m" to load data.
2. Run "ProcessData.m" to process data.
3. Run "ExtractFeature.m" to extract the involved features.
4. Then the users can run the codes in the folders "Experiments" to replicate our experiments.

## 数据集
https://data.matr.io/1/projects/5c48dd2bc625d700019f3204

## 数据集介绍
This dataset, used in our publication “Data-driven prediction of battery cycle life before capacity degradation”, consists of 124 commercial lithium-ion batteries cycled to failure under fast-charging conditions. These lithium-ion phosphate (LFP)/graphite cells, manufactured by A123 Systems (APR18650M1A), were cycled in horizontal cylindrical fixtures on a 48-channel Arbin LBT potentiostat in a forced convection temperature chamber set to 30°C. The cells have a nominal capacity of 1.1 Ah and a nominal voltage of 3.3 V.

The objective of this work is to optimize fast charging for lithium-ion batteries. As such, all cells in this dataset are charged with a one-step or two-step fast-charging policy. This policy has the format “C1(Q1)-C2”, in which C1 and C2 are the first and second constant-current steps, respectively, and Q1 is the state-of-charge (SOC, %) at which the currents switch. The second current step ends at 80% SOC, after which the cells charge at 1C CC-CV. The upper and lower cutoff potentials are 3.6 V and 2.0 V, respectively, which are consistent with the manufacturer’s specifications. These cutoff potentials are fixed for all current steps, including fast charging; after some cycling, the cells may hit the upper cutoff potential during fast charging, leading to significant constant-voltage charging. All cells discharge at 4C.

The dataset is divided into three “batches”, representing approximately 48 cells each. Each batch is defined by a “batch date”, or the date the tests were started. Each batch has a few irregularities, as detailed on the page for each batch.

The data is provided in two formats. For each batch, a MATLAB struct is available. The struct provides a convenient data container in which the data for each cycle is easily accessible. This struct can be loaded in either MATLAB or python (via the h5py package). Pandas dataframes can be generated via the provided code. Additionally, the raw data for each cell is available as a CSV file. Note that the CSV files occasionally exhibit errors in both test time and step time in which the test time resets to zero mid-cycle; these errors are corrected for in the structs.

The temperature measurements are performed by attaching a Type T thermocouple with thermal epoxy (OMEGATHERM 201) and Kapton tape to the exposed cell can after stripping a small section of the plastic insulation. Note that the temperature measurements are not perfectly reliable; the thermal contact between the thermocouple and the cell can may vary substantially, and the thermocouple sometimes loses contact during cycling.

Internal resistance measurements were obtained during charging at 80% SOC by averaging 10 pulses of ±3.6C with a pulse width of 30 ms (2017-05-12 and 2017-06-30) or 33 ms (2018-04-12).

The following repository contains some starter code to load the datasets in either MATLAB or python:

https://github.com/rdbraatz/data-driven-prediction-of-battery-cycle-life-before-capacity-degradation

Low rate data used to generate figure 4:

initialdata_all.mat
2018-02-20_batchdata_updated_struct_errorcorrect.mat
2018-04-03_varcharge_batchdata_updated_struct_errorcorrect.mat
finaldata_4.mat
finaldata_6and8.mat
Full structured dataset as a zipped file:

BEEP structured data

If using this dataset in a publication, please cite: Severson et al. Data-driven prediction of battery cycle life before capacity degradation. Nature Energy volume 4, pages 383–391 (2019).
