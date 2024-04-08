import numpy as np
import torch
import matplotlib.pyplot as plt
import functions as func

import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
plt.rcParams['font.sans-serif'] = 'Times New Roman'
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['axes.labelsize'] = 8
figsize_single = (3.5, 3.5 * 0.618)

data = func.SeversonBattery('../SeversonBattery.mat', seq_len=1)
results_SoH_CaseA_Baseline = torch.load('../Results/4 Presentation/SoH Estimation/SoH_CaseA_Baseline.pth')
inputs_dict, targets_dict = func.create_chosen_cells(
    data,
    idx_cells_train=[91, 100],
    idx_cells_test=[124],
    perc_val=0.2
)
inputs_test = inputs_dict['test']
Min = torch.min(inputs_test, dim=0, keepdim=True).values
Max = torch.max(inputs_test, dim=0, keepdim=True).values
inputs_test_norm = (inputs_test - Min) / (Max - Min)
inputs_dim = inputs_test.shape[-1]
linestyles = ['-', '--', '-', '--', ':', '-', '--', ':']
labels = ['Omega', 'b', 'Tavg', 'IR', 'Charge Time', 'dQdV_max', 'dQdV_min', 'dQdV_var']
colors = [
    (238/255, 28/255, 37/255),
    (238/255, 28/255, 37/255),
    (1/255, 168/255, 158/255),
    (1/255, 168/255, 158/255),
    (1/255, 168/255, 158/255),
    (0/255, 84/255, 165/255),
    (0/255, 84/255, 165/255),
    (0/255, 84/255, 165/255),
]
fig = plt.figure(figsize=figsize_single)
grid = plt.GridSpec(1, 3)
main_ax = fig.add_subplot(grid[0:2])
for i in range(inputs_dim - 1):
    main_ax.plot(
        results_SoH_CaseA_Baseline['Cycles'],
        inputs_test_norm[:, :, i],
        linestyle=linestyles[i],
        linewidth=1.5,
        color=colors[i],
        label=labels[i]
    )
main_ax.legend(prop={'size': 8})
main_ax.grid(True, linestyle="--", alpha=0.5)
main_ax.set_xlim(min(results_SoH_CaseA_Baseline['Cycles']), max(results_SoH_CaseA_Baseline['Cycles']))
main_ax.set_xlabel('Monitoring Time (Unit: Cycles)')
main_ax.set_ylabel('Extracted Features')
plt.show()

settings_SoH_CaseB = torch.load('Settings/settings_SoH_CaseB.pth')
num_rounds_SoH_CaseB = settings_SoH_CaseB['num_rounds']
num_epoch_SoH_CaseB = settings_SoH_CaseB['num_epoch']
weights_SoH_CaseB_DeepHPM_AdpBal = torch.load('../Results/3 Adaptive Balancing/weights_rounds_SoH_CaseB_DeepHPM_AdpBal.pth')

num_row = 2
num_col = 3
fig, axes = plt.subplots(num_row, num_col, figsize=(7, 2.884), sharex=True, sharey=True)
for i in range(num_row):
    for j in range(num_col):
        round = 3 * i + j
        if round > num_rounds_SoH_CaseB - 1:
            break
        lambda_U_SoH_CaseB_DeepHPM_AdpBal = weights_SoH_CaseB_DeepHPM_AdpBal[round]['lambda_U'] / (
                weights_SoH_CaseB_DeepHPM_AdpBal[round]['lambda_U'] + weights_SoH_CaseB_DeepHPM_AdpBal[round]['lambda_F'] +
                weights_SoH_CaseB_DeepHPM_AdpBal[round]['lambda_F_t'])
        lambda_F_SoH_CaseB_DeepHPM_AdpBal = weights_SoH_CaseB_DeepHPM_AdpBal[round]['lambda_F'] / (
                weights_SoH_CaseB_DeepHPM_AdpBal[round]['lambda_U'] + weights_SoH_CaseB_DeepHPM_AdpBal[round]['lambda_F'] +
                weights_SoH_CaseB_DeepHPM_AdpBal[round]['lambda_F_t'])
        lambda_F_t_SoH_CaseB_DeepHPM_AdpBal = weights_SoH_CaseB_DeepHPM_AdpBal[round]['lambda_F_t'] / (
                weights_SoH_CaseB_DeepHPM_AdpBal[round]['lambda_U'] + weights_SoH_CaseB_DeepHPM_AdpBal[round]['lambda_F'] +
                weights_SoH_CaseB_DeepHPM_AdpBal[round]['lambda_F_t'])

        weights_SoH_CaseB_DeepHPM_AdpBal[round]['lambda_U'] = lambda_U_SoH_CaseB_DeepHPM_AdpBal.numpy().tolist()
        weights_SoH_CaseB_DeepHPM_AdpBal[round]['lambda_F'] = lambda_F_SoH_CaseB_DeepHPM_AdpBal.numpy().tolist()
        weights_SoH_CaseB_DeepHPM_AdpBal[round]['lambda_F_t'] = lambda_F_t_SoH_CaseB_DeepHPM_AdpBal.numpy().tolist()
        # ax = fig.add_subplot(2, 3, round+1)
        axes[i, j].stackplot(torch.arange(0, num_epoch_SoH_CaseB).numpy().tolist(), weights_SoH_CaseB_DeepHPM_AdpBal[round].values(),
                      labels=['Lambda_u', 'Lambda_f', 'Lambda_ft'],
                      colors=[(244 / 255, 207 / 255, 213 / 255), (252 / 255, 245 / 255, 232 / 255),
                              (169 / 255, 207 / 255, 226 / 255)], alpha=1)
        axes[i, j].set_xlim(0, num_epoch_SoH_CaseB)
        axes[i, j].set_ylim(0, 1)
        axes[i, j].grid(True, linestyle="--", alpha=0.5)
        # axes[i, j].legend()
axes[0, 0].legend(prop={'size': 8})
fig.text(0.5, 0, 'Training epochs', ha='center', va='baseline', fontsize=8)
fig.text(0, 0.25, 'Relative weight coefficients (Unit: 1)', ha='left', va='baseline', fontsize=8, rotation=90)
fig.tight_layout()
plt.show()

results_SoH_CaseA_Baseline = torch.load('../Results/4 Presentation/SoH Estimation/SoH_CaseA_Baseline.pth')
results_SoH_CaseA_Verhulst_Sum = torch.load('../Results/4 Presentation/SoH Estimation/SoH_CaseA_Verhulst_Sum.pth')
results_SoH_CaseA_Verhulst_AdpBal = torch.load('../Results/4 Presentation/SoH Estimation/SoH_CaseA_Verhulst_AdpBal.pth')
results_SoH_CaseA_DeepHPM_Sum = torch.load('../Results/4 Presentation/SoH Estimation/SoH_CaseA_DeepHPM_Sum.pth')
results_SoH_CaseA_DeepHPM_AdpBal = torch.load('../Results/4 Presentation/SoH Estimation/SoH_CaseA_DeepHPM_AdpBal.pth')

plt.figure(figsize=figsize_single)
plt.plot(
    results_SoH_CaseA_Baseline['Cycles'],
    results_SoH_CaseA_Baseline['U_true'],
    linewidth=2,
    color=(238/255, 28/255, 37/255),
    label='Ground Truth'
)
plt.plot(
    results_SoH_CaseA_Baseline['Cycles'],
    results_SoH_CaseA_Baseline['U_pred'],
    linestyle='--',
    linewidth=2,
    color=(238/255, 28/255, 37/255),
    alpha=1.,
    label='Baseline'
)
plt.plot(
    results_SoH_CaseA_Verhulst_Sum['Cycles'],
    results_SoH_CaseA_Verhulst_Sum['U_pred'],
    linestyle='--',
    linewidth=2,
    color=(1/255, 168/255, 158/255),
    alpha=1.,
    label='PINN-Verhulst (Sum)'
)
plt.plot(
    results_SoH_CaseA_Verhulst_AdpBal['Cycles'],
    results_SoH_CaseA_Verhulst_AdpBal['U_pred'],
    linewidth=2,
    color=(1/255, 168/255, 158/255),
    alpha=1.,
    label='PINN-Verhulst (AdpBal)'
)
plt.plot(
    results_SoH_CaseA_DeepHPM_Sum['Cycles'],
    results_SoH_CaseA_DeepHPM_Sum['U_pred'],
    linestyle='--',
    linewidth=2,
    color=(0/255, 84/255, 165/255),
    alpha=1.,
    label='PINN-DeepHPM (Sum)'
)
plt.plot(
    results_SoH_CaseA_DeepHPM_AdpBal['Cycles'],
    results_SoH_CaseA_DeepHPM_AdpBal['U_pred'],
    linewidth=2,
    color=(0/255, 84/255, 165/255),
    alpha=1.,
    label='PINN-DeepHPM (AdpBal)'
)
plt.legend(prop={'size': 8})
plt.grid(True, linestyle="--", alpha=0.5)
plt.xlim(min(results_SoH_CaseA_Baseline['Cycles']), max(results_SoH_CaseA_Baseline['Cycles']))
plt.xlabel('Monitoring Time (Unit: Cycles)')
plt.ylabel('State of Health (Unit: 1)')
plt.show()

results_SoH_CaseB_Baseline = torch.load('../Results/4 Presentation/SoH Estimation/SoH_CaseB_Baseline.pth')
results_SoH_CaseB_Verhulst_Sum = torch.load('../Results/4 Presentation/SoH Estimation/SoH_CaseB_Verhulst_Sum.pth')
results_SoH_CaseB_Verhulst_AdpBal = torch.load('../Results/4 Presentation/SoH Estimation/SoH_CaseB_Verhulst_AdpBal.pth')
results_SoH_CaseB_DeepHPM_Sum = torch.load('../Results/4 Presentation/SoH Estimation/SoH_CaseB_DeepHPM_Sum.pth')
results_SoH_CaseB_DeepHPM_AdpBal = torch.load('../Results/4 Presentation/SoH Estimation/SoH_CaseB_DeepHPM_AdpBal.pth')

plt.figure(figsize=figsize_single)
plt.plot(
    results_SoH_CaseB_Baseline['Cycles'],
    results_SoH_CaseB_Baseline['U_true'],
    linewidth=2,
    color=(238/255, 28/255, 37/255),
    label='Ground Truth'
)
plt.plot(
    results_SoH_CaseB_Baseline['Cycles'],
    results_SoH_CaseB_Baseline['U_pred'],
    linestyle='--',
    linewidth=2,
    color=(238/255, 28/255, 37/255),
    alpha=1.,
    label='Baseline'
)
plt.plot(
    results_SoH_CaseB_Verhulst_Sum['Cycles'],
    results_SoH_CaseB_Verhulst_Sum['U_pred'],
    linestyle='--',
    linewidth=2,
    color=(1/255, 168/255, 158/255),
    alpha=1.,
    label='PINN-Verhulst (Sum)'
)
plt.plot(
    results_SoH_CaseB_Verhulst_AdpBal['Cycles'],
    results_SoH_CaseB_Verhulst_AdpBal['U_pred'],
    linewidth=2,
    color=(1/255, 168/255, 158/255),
    alpha=1.,
    label='PINN-Verhulst (AdpBal)'
)
plt.plot(
    results_SoH_CaseB_DeepHPM_Sum['Cycles'],
    results_SoH_CaseB_DeepHPM_Sum['U_pred'],
    linestyle='--',
    linewidth=2,
    color=(0/255, 84/255, 165/255),
    alpha=1.,
    label='PINN-DeepHPM (Sum)'
)
plt.plot(
    results_SoH_CaseB_DeepHPM_AdpBal['Cycles'],
    results_SoH_CaseB_DeepHPM_AdpBal['U_pred'],
    linewidth=2,
    color=(0/255, 84/255, 165/255),
    alpha=1.,
    label='PINN-DeepHPM (AdpBal)'
)
plt.legend(prop={'size': 8})
plt.grid(True, linestyle="--", alpha=0.5)
plt.xlim(min(results_SoH_CaseB_Baseline['Cycles']), max(results_SoH_CaseB_Baseline['Cycles']))
plt.xlabel('Monitoring Time (Unit: Cycles)')
plt.ylabel('State of Health (Unit: 1)')
plt.show()

results_RUL_CaseA_Baseline = torch.load('../Results/4 Presentation/RUL Prognostics/RUL_CaseA_Baseline.pth')
results_RUL_CaseA_DeepHPM_Sum = torch.load('../Results/4 Presentation/RUL Prognostics/RUL_CaseA_DeepHPM_Sum.pth')
results_RUL_CaseA_DeepHPM_AdpBal = torch.load('../Results/4 Presentation/RUL Prognostics/RUL_CaseA_DeepHPM_AdpBal.pth')

plt.figure(figsize=figsize_single)
plt.plot(
    results_RUL_CaseA_Baseline['Cycles'],
    results_RUL_CaseA_Baseline['U_true'],
    linewidth=2,
    color=(238/255, 28/255, 37/255),
    label='Ground Truth'
)
plt.plot(
    results_RUL_CaseA_Baseline['Cycles'],
    results_RUL_CaseA_Baseline['U_pred'],
    linestyle='--',
    linewidth=2,
    color=(238/255, 28/255, 37/255),
    alpha=1.,
    label='Baseline'
)
plt.plot(
    results_RUL_CaseA_DeepHPM_Sum['Cycles'],
    results_RUL_CaseA_DeepHPM_Sum['U_pred'],
    linestyle='--',
    linewidth=2,
    color=(0/255, 84/255, 165/255),
    alpha=1.,
    label='PINN-DeepHPM (Sum)'
)
plt.plot(
    results_RUL_CaseA_DeepHPM_AdpBal['Cycles'],
    results_RUL_CaseA_DeepHPM_AdpBal['U_pred'],
    linewidth=2,
    color=(0/255, 84/255, 165/255),
    alpha=1.,
    label='PINN-DeepHPM (AdpBal)'
)
plt.legend(prop={'size': 8})
plt.grid(True, linestyle="--", alpha=0.5)
plt.xlim(min(results_RUL_CaseA_Baseline['Cycles']), max(results_RUL_CaseA_Baseline['Cycles']))
plt.xlabel('Monitoring Time (Unit: Cycles)')
plt.ylabel('Remaining Useful Life (Unit: Cycles)')
plt.show()

results_RUL_CaseB_Baseline = torch.load('../Results/4 Presentation/RUL Prognostics/RUL_CaseB_Baseline.pth')
results_RUL_CaseB_DeepHPM_Sum = torch.load('../Results/4 Presentation/RUL Prognostics/RUL_CaseB_DeepHPM_Sum.pth')
results_RUL_CaseB_DeepHPM_AdpBal = torch.load('../Results/4 Presentation/RUL Prognostics/RUL_CaseB_DeepHPM_AdpBal.pth')

plt.figure(figsize=figsize_single)
plt.plot(
    results_RUL_CaseB_Baseline['Cycles'],
    results_RUL_CaseB_Baseline['U_true'],
    linewidth=2,
    color=(238/255, 28/255, 37/255),
    label='Ground Truth'
)
plt.plot(
    results_RUL_CaseB_Baseline['Cycles'],
    results_RUL_CaseB_Baseline['U_pred'],
    linestyle='--',
    linewidth=2,
    color=(238/255, 28/255, 37/255),
    alpha=1.,
    label='Baseline'
)
plt.plot(
    results_RUL_CaseB_DeepHPM_Sum['Cycles'],
    results_RUL_CaseB_DeepHPM_Sum['U_pred'],
    linestyle='--',
    linewidth=2,
    color=(0/255, 84/255, 165/255),
    alpha=1.,
    label='PINN-DeepHPM (Sum)'
)
plt.plot(
    results_RUL_CaseB_DeepHPM_AdpBal['Cycles'],
    results_RUL_CaseB_DeepHPM_AdpBal['U_pred'],
    linewidth=2,
    color=(0/255, 84/255, 165/255),
    alpha=1.,
    label='PINN-DeepHPM (AdpBal)'
)
plt.legend(prop={'size': 8})
plt.grid(True, linestyle="--", alpha=0.5)
plt.xlim(min(results_RUL_CaseB_Baseline['Cycles']), max(results_RUL_CaseB_Baseline['Cycles']))
plt.xlabel('Monitoring Time (Unit: Cycles)')
plt.ylabel('Remaining Useful Life (Unit: Cycles)')
plt.show()

results_RUL_CaseC_Baseline = torch.load('../Results/4 Presentation/RUL Prognostics/RUL_CaseC_Baseline.pth')
results_RUL_CaseC_DeepHPM_Sum = torch.load('../Results/4 Presentation/RUL Prognostics/RUL_CaseC_DeepHPM_Sum.pth')
results_RUL_CaseC_DeepHPM_AdpBal = torch.load('../Results/4 Presentation/RUL Prognostics/RUL_CaseC_DeepHPM_AdpBal.pth')

plt.figure(figsize=figsize_single)
results_RUL_CaseC_idx = np.argsort(results_RUL_CaseC_Baseline['U_true'])
errors_RUL_CaseC_Baseline = np.abs(results_RUL_CaseC_Baseline['U_pred'] - results_RUL_CaseC_Baseline['U_true'])
errors_RUL_CaseC_DeepHPM_Sum = np.abs(results_RUL_CaseC_DeepHPM_Sum['U_pred'] - results_RUL_CaseC_Baseline['U_true'])
errors_RUL_CaseC_DeepHPM_AdpBal = np.abs(results_RUL_CaseC_DeepHPM_AdpBal['U_pred'] - results_RUL_CaseC_Baseline['U_true'])
errors_RUL_CaseC_total = errors_RUL_CaseC_Baseline + errors_RUL_CaseC_DeepHPM_Sum + errors_RUL_CaseC_DeepHPM_AdpBal
plt.stackplot(
    results_RUL_CaseC_Baseline['U_true'][results_RUL_CaseC_idx],
    errors_RUL_CaseC_Baseline[results_RUL_CaseC_idx],
    errors_RUL_CaseC_DeepHPM_Sum[results_RUL_CaseC_idx],
    errors_RUL_CaseC_DeepHPM_AdpBal[results_RUL_CaseC_idx],
    labels=['Baseline', 'PINN-DeepHPM (Sum)', 'PINN-DeepHPM(AdpBal)'],
    colors=[(238/255, 28/255, 37/255), (1/255, 168/255, 158/255),
          (0/255, 84/255, 165/255)],
    alpha=1
)
plt.legend(prop={'size': 8})
plt.grid(True, linestyle="--", alpha=0.5)
plt.xlim(min(results_RUL_CaseC_Baseline['Cycles']), max(results_RUL_CaseC_Baseline['Cycles']))
plt.ylim(0, max(errors_RUL_CaseC_total))
plt.xlabel('Actual RUL (Unit: Cycles)')
plt.ylabel('Prognostic Errors (Unit: Cycles)')
plt.show()

plt.figure(figsize=figsize_single)
plt.plot(
    results_SoH_CaseB_Baseline['Cycles'],
    (results_SoH_CaseB_Baseline['U_t_pred'] - np.mean(results_SoH_CaseB_Baseline['U_t_pred'])) /
    np.std(results_SoH_CaseB_Baseline['U_t_pred']),
    linestyle='--',
    linewidth=2,
    color=(238/255, 28/255, 37/255),
    alpha=1.,
    label='Baseline'
)
plt.plot(
    results_SoH_CaseB_Verhulst_Sum['Cycles'],
    (results_SoH_CaseB_Verhulst_Sum['U_t_pred'] - np.mean(results_SoH_CaseB_Verhulst_Sum['U_t_pred'])) /
    np.std(results_SoH_CaseB_Verhulst_Sum['U_t_pred']),
    linestyle='--',
    linewidth=2,
    color=(1/255, 168/255, 158/255),
    alpha=1.,
    label='PINN-Verhulst (Sum)'
)
plt.plot(
    results_SoH_CaseB_Verhulst_AdpBal['Cycles'],
    (results_SoH_CaseB_Verhulst_AdpBal['U_t_pred'] - np.mean(results_SoH_CaseB_Verhulst_AdpBal['U_t_pred'])) /
    np.std(results_SoH_CaseB_Verhulst_AdpBal['U_t_pred']),
    linewidth=2,
    color=(1/255, 168/255, 158/255),
    alpha=1.,
    label='PINN-Verhulst (AdpBal)'
)
plt.plot(
    results_SoH_CaseB_DeepHPM_Sum['Cycles'],
    (results_SoH_CaseB_DeepHPM_Sum['U_t_pred'] - np.mean(results_SoH_CaseB_DeepHPM_Sum['U_t_pred'])) /
    np.std(results_SoH_CaseB_DeepHPM_Sum['U_t_pred']),
    linestyle='--',
    linewidth=2,
    color=(0/255, 84/255, 165/255),
    alpha=1.,
    label='PINN-DeepHPM (Sum)'
)
plt.plot(
    results_SoH_CaseB_DeepHPM_AdpBal['Cycles'],
    (results_SoH_CaseB_DeepHPM_AdpBal['U_t_pred'] - np.mean(results_SoH_CaseB_DeepHPM_AdpBal['U_t_pred'])) /
    np.std(results_SoH_CaseB_DeepHPM_AdpBal['U_t_pred']),
    linewidth=2,
    color=(0/255, 84/255, 165/255),
    alpha=1.,
    label='PINN-DeepHPM (AdpBal)'
)
plt.legend(prop={'size': 8})
plt.grid(True, linestyle="--", alpha=0.5)
plt.xlim(min(results_SoH_CaseB_Baseline['Cycles']), max(results_SoH_CaseB_Baseline['Cycles']))
plt.xlabel('Monitoring Time (Unit: Cycles)')
plt.ylabel('Partial Derivatives')
plt.show()