import numpy as np
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

################################################ Ranges #############################################################
RF_hops = [1, 0.05, 1, 5]

# Boolean Random Forest:
isr_ranges = [range(56, 77), np.arange(0.1, 0.20, 0.05), range(19, 30), range(5, 10, 5)]
swe_ranges = [range(80, 101), np.arange(0.5, 1.05, 0.05), range(3, 9), range(15, 20, 5)]
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

AB_hops = [1, 1, 0.05, 1, 5]
# Boolean AdaBoost:
isr_ranges = [range(109, 115), range(31, 40), np.arange(0.3, 0.35, 0.05), range(2, 3), range(10, 20, 5)]
swe_ranges = [range(70, 75), range(10, 15), np.arange(0.65, 0.8, 0.05), range(2, 3), range(20, 40, 5)]
mixed_ranges = [range(2, 9), range(79, 89), np.arange(0.8, 1.05, 0.05), range(10, 20), range(5, 15, 5)]
isr_m_ranges = [range(92, 104), range(3, 4), np.arange(0.45, 0.55, 0.05), range(1,2), range(20, 45, 5)]
swe_m_ranges = [range(85, 91), range(5, 10), np.arange(0.3, 0.55, 0.05), range(21, 26), range(5, 10, 5)]
mixed_m_ranges = [range(78, 81), range(75, 85), np.arange(0.15, 0.20, 0.05), range(1, 2), range(20, 35, 5)]
isr_f_ranges = [range(99, 100), range(2, 9), np.arange(0.65, 0.7, 0.05), range(2, 3), range(15, 25, 5)]
swe_f_ranges = [range(41, 56), range(38, 42), np.arange(1, 1.05, 0.05), range(38, 48), range(5, 30, 5)]
mixed_f_ranges = [range(87, 94), range(111, 120), np.arange(0.7, 0.8, 0.05), range(2, 5), range(25, 30, 5)]
BAB_PARM = isr_ranges, swe_ranges, mixed_ranges, isr_m_ranges, swe_m_ranges, mixed_m_ranges, isr_f_ranges, \
           swe_f_ranges, mixed_f_ranges, AB_hops

# Regression AdaBoost:
isr_ranges = [range(140, 151), range(2, 23), np.arange(0.65, 1, 0.05), range(8, 13), range(10, 15, 5)]
sw_ranges = [range(7, 18), range(4, 5), np.arange(0.7, 0.85, 0.05), range(12, 13), range(5, 20, 5)]
mix_ranges = [range(75, 86), range(2, 23), np.arange(0.85, 1, 0.05), range(12, 13), range(5, 10, 5)]
isr_m_ranges = [range(78, 85), range(90, 91), np.arange(0.55, 0.6, 0.05), range(4, 5), range(5, 10, 5)]
swe_m_ranges = [range(29, 40), range(6, 12), np.arange(0.1, 0.65, 0.05), range(25, 36), range(5, 10, 5)]
mixed_m_ranges = [range(18, 29), range(2, 13), np.arange(0.1, 0.55, 0.05), range(31, 42), range(5, 10, 5)]
isr_f_ranges = [range(30, 31), range(188, 190), np.arange(0.5, 0.65, 0.05), range(18, 29), range(5, 10, 5)]
swe_f_ranges = [range(27, 38), range(2, 13), np.arange(0.3, 0.8, 0.05), range(16, 27), range(5, 15, 5)]
mixed_f_ranges = [range(12, 23), range(0), np.arange(0.2, 0.55, 0.05), range(7, 18), range(5, 15, 5)]
RAB_PARM = isr_ranges, swe_ranges, mixed_ranges, isr_m_ranges, swe_m_ranges, mixed_m_ranges, isr_f_ranges, \
           swe_f_ranges, mixed_f_ranges, AB_hops


################################################ Final classifiers #####################################################
# Classification forest:
isr_class_forest = RandomForestClassifier(max_depth=20, max_features=0.1, random_state=1,
                                          min_samples_leaf=5, n_estimators=57)
swe_class_forest = RandomForestClassifier(max_depth=42, max_features=0.55, random_state=1,
                                          min_samples_leaf=15, n_estimators=84)

# Regression forests:
isr_forest = RandomForestRegressor(max_depth=20, max_features=0.8, random_state=1, min_samples_split=2,
                                   min_samples_leaf=10, n_estimators=143)
swe_forest = RandomForestRegressor(max_depth=16, max_features=0.85, random_state=1, min_samples_split=2,
                                   min_samples_leaf=30, n_estimators=45)
R_forests = isr_forest, swe_forest

# AdaBoost classifiers:
adaboost_isr_forest = RandomForestClassifier(max_depth=2, max_features=0.3, random_state=1,
                                             min_samples_leaf=10, n_estimators=35)
adaboost_isr_classifier = AdaBoostClassifier(base_estimator=adaboost_isr_forest, n_estimators=113, random_state=1)

adaboost_swe_forest = RandomForestClassifier(max_depth=2, max_features=0.7, random_state=1,
                                             min_samples_leaf=20, n_estimators=12)
adaboost_swe_classifier = AdaBoostClassifier(base_estimator=adaboost_swe_forest, n_estimators=72, random_state=1)
C_ada = adaboost_isr_classifier, adaboost_swe_classifier

# AdaBoost Regressors:
# First format:
r_forest1 = RandomForestRegressor(max_depth=10, max_features=0.75, random_state=1, min_samples_split=2,
                                  min_samples_leaf=10, n_estimators=12)
isr_ada1 = AdaBoostRegressor(base_estimator=r_forest1, n_estimators=141, random_state=1)

r_forest2 = RandomForestRegressor(max_depth=12, max_features=0.8, random_state=1, min_samples_split=2,
                                  min_samples_leaf=15, n_estimators=4)
swe_ada1 = AdaBoostRegressor(base_estimator=r_forest2, n_estimators=11, random_state=1)

r_forest3 = RandomForestRegressor(max_depth=12, max_features=1, random_state=1, min_samples_split=2,
                                  min_samples_leaf=5, n_estimators=11)
mix_ada1 = AdaBoostRegressor(base_estimator=r_forest3, n_estimators=77, random_state=1)


# Second format:
isr_ada2 = AdaBoostRegressor(base_estimator=None, n_estimators=150, random_state=1)
swe_ada2 = AdaBoostRegressor(base_estimator=None, n_estimators=22, random_state=1)

R_ada = isr_ada1, swe_ada1, mix_ada1, isr_ada2, swe_ada2

################################################# Final k ##############################################################
# Regression RF k's :
is_RF_k = 17
sw_RF_k = 13

# Regression AB k's
is_AB_k = 24
sw_AB_k = 13

RF_k = is_RF_k, sw_RF_k
AB_k = is_AB_k, sw_AB_k

# Classification RF k's :
is_cl_RF_k = 14
sw_cl_RF_k = 12

# Classification AB k's
is_cl_AB_k = 22
sw_cl_AB_k = 12

RF_cl_k = is_cl_AB_k, sw_cl_AB_k
AB_cl_k = is_cl_AB_k, sw_cl_AB_k