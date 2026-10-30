# -*- coding: utf-8 -*-
from client import OpenClawGenParkSignalAggregator

aggregator = OpenClawGenParkSignalAggregator()

# 1. Kalman Filter Smoothing
noisy_telemetry = [10.2, 10.8, 9.7, 11.4, 10.1, 10.5, 12.0, 10.3, 10.9, 11.1]
kf = aggregator.apply_kalman_filter(noisy_telemetry)
print(f"Kalman Estimate: Final={kf['final_estimated_state']} (Variance: {kf['final_estimation_variance']})")

# 2. Volatility Burst Detection
history_stream = [50, 52, 51, 49, 50, 53, 51, 52, 49, 50, 85] # sudden spike to 85
burst = aggregator.detect_volatility_and_regime_bursts(history_stream, window_size=10, z_threshold=2.5)
print(f"\nRegime Shift Check: {burst['regime_verdict']} (Z-Score: {burst['computed_z_score']})")

# 3. Information Entropy Gain
prior = [0.25, 0.25, 0.25, 0.25] # max uncertainty (2.0 bits)
posterior = [0.85, 0.05, 0.05, 0.05] # concentrated evidence
ig = aggregator.compute_shannon_entropy_gain(prior, posterior)
print(f"\nEntropy Gain: {ig['information_gain_bits']} bits (Uncertainty Reduced by {ig['uncertainty_reduction_pct']}%)")
