import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor

RF_hops = [1, 0.05, 1, 5]

# Boolean Random Forest:
isr_ranges = [range(56, 77), np.arange(0.1, 0.20, 0.05), range(19, 30), range(5, 10, 5)]
swe_ranges = [range(80, 101), np.arange(0.5, 1.05, 0.05), range(39, 60), range(15, 20, 5)]
mixed_ranges = [range(40, 61), np.arange(0.6, 0.65, 0.05), range(4, 10), range(5, 10, 5)]
isr_m_ranges = [range(47, 76), np.arange(0.15, 0.45, 0.05), range(1, 4), range(10, 45, 5)]
swe_m_ranges = [range(9, 30), np.arange(0.15, 1.05, 0.05), range(8, 29), range(5, 30, 5)]
mixed_m_ranges = [range(130, 151), np.arange(0.1, 0.25, 0.05), range(3, 9), range(35, 40, 5)]
isr_f_ranges = [range(163, 201), np.arange(0.35, 0.45, 0.05), range(2, 6), range(5, 10, 5)]
swe_f_ranges = [range(171, 201), np.arange(0.7, 1.05, 0.05), range(2, 6), range(5, 15, 5)]
mixed_f_ranges = [range(190, 201), np.arange(0.15, 0.2, 0.05), range(5, 8), range(10, 15, 5)]
BRF_PARM = isr_ranges, swe_ranges, mixed_ranges, isr_m_ranges, swe_m_ranges, mixed_m_ranges, isr_f_ranges, \
           swe_f_ranges, mixed_f_ranges, RF_hops

# Regression Random Forest:
isr_ranges = [range(128, 149), np.arange(0.1, 1.05, 0.05), range(20, 41), range(10, 30, 5)]
sw_ranges = [range(39, 60), np.arange(0.25, 0.95, 0.05), range(3, 17), range(15, 35, 5)]
mix_ranges = [range(56, 75), np.arange(0.25, 0.9, 0.05), range(3, 9), range(15, 45, 5)]
isr_m_ranges = [range(94, 114), range(0), range(12, 32), range(5, 20, 5)]
swe_m_ranges = [range(48, 68), range(0), range(5, 25), range(5, 30, 5)]
mixed_m_ranges = [range(83, 103), range(0), range(5, 25), range(5, 35, 5)]
isr_f_ranges = [range(80, 95), np.arange(0.1, 0.5, 0.05), range(0), range(5, 25, 5)]
swe_f_ranges = [range(31, 51), np.arange(0.2, 1, 0.05), range(6, 26), range(5, 20, 5)]
mixed_f_ranges = [range(79, 99), np.arange(0.25, 1, 0.05), range(5, 25), range(5, 25, 5)]
RRF_PARM = isr_ranges, swe_ranges, mixed_ranges, isr_m_ranges, swe_m_ranges, mixed_m_ranges, isr_f_ranges, \
           swe_f_ranges, mixed_f_ranges, RF_hops

# TODO - fill the rest of the parameters for AdaBoost
AB_hops = [1, 1, 0.05, 1, 5]
# Boolean AdaBoost:
isr_ranges = []
sw_ranges = []
mix_ranges = []
isr_m_ranges = []
swe_m_ranges = []
mixed_m_ranges = []
isr_f_ranges = []
swe_f_ranges = []
mixed_f_ranges = []
BAB_PARM = isr_ranges, swe_ranges, mixed_ranges, isr_m_ranges, swe_m_ranges, mixed_m_ranges, isr_f_ranges, \
           swe_f_ranges, mixed_f_ranges, AB_hops

# Regression AdaBoost:
isr_ranges = [range(140, 151), range(2, 23), np.arange(0.65, 1, 0.05), range(8, 13), range(10, 15, 5)]
sw_ranges = []
mix_ranges = []
isr_m_ranges = []
swe_m_ranges = []
mixed_m_ranges = []
isr_f_ranges = [range(30, 31), range(188, 190), np.arange(0.5, 0.65, 0.05), range(18, 29), range(5, 10, 5)]
swe_f_ranges = []
mixed_f_ranges = []
RAB_PARM = isr_ranges, swe_ranges, mixed_ranges, isr_m_ranges, swe_m_ranges, mixed_m_ranges, isr_f_ranges, \
           swe_f_ranges, mixed_f_ranges, AB_hops

# Regression forests:
isr_forest = RandomForestRegressor(max_depth=20, max_features=0.8, random_state=1, min_samples_split=2,
                                   min_samples_leaf=10, n_estimators=143)
swe_forest = RandomForestRegressor(max_depth=16, max_features=0.85, random_state=1, min_samples_split=2,
                                   min_samples_leaf=30, n_estimators=45)
R_forests = isr_forest, swe_forest

# Regression AdaBoost classifiers:
# TODO - to complete
r_forest = RandomForestRegressor(max_depth=10, max_features=0.75, random_state=1, min_samples_split=2,
                                 min_samples_leaf=10, n_estimators=12)
isr_ada = AdaBoostRegressor(base_estimator=r_forest, n_estimators=141, random_state=1)
swe_ada = 1
R_ada = isr_ada, swe_ada

# Regression RF k's :
is_RF_k = 17
sw_RF_k = 13

# Regression AB k's
# TODO - to complete
is_AB_k = 17
sw_AB_k = 13

RF_k = is_RF_k, sw_RF_k
AB_k = is_AB_k, sw_AB_k
