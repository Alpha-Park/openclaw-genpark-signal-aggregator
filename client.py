# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Signal Aggregator - Discrete Kalman Filter & Entropy Gain Telemetry Aggregator
Standard Library only: math, typing.
Implements 1D Discrete Kalman Filter to track true latent market/agent demand signals
from noisy telemetry, detects volatility regime bursts via rolling Z-score, and calculates
Shannon information entropy gain.
"""

import math
from typing import Dict, List, Any

class OpenClawGenParkSignalAggregator:
    def __init__(self, default_process_var: float = 1e-4, default_meas_var: float = 0.04):
        self.default_q = default_process_var
        self.default_r = default_meas_var

    def apply_kalman_filter(self, measurements: List[float],
                            process_variance: float = None,
                            measurement_variance: float = None) -> Dict[str, Any]:
        """
        Executes discrete Kalman filter recursions across measurement sequence:
        Predict: x_k^- = x_{k-1}, P_k^- = P_{k-1} + Q
        Update:  K_k = P_k^- / (P_k^- + R)
                 x_k = x_k^- + K_k * (z_k - x_k^-)
                 P_k = (1 - K_k) * P_k^-
        """
        Q = process_variance if process_variance is not None else self.default_q
        R = measurement_variance if measurement_variance is not None else self.default_r

        if not measurements:
            return {"filtered_estimates": [], "kalman_gains": []}

        # Initialize state with first measurement
        x_est = measurements[0]
        p_est = 1.0

        filtered = []
        gains = []

        for z in measurements:
            # 1. Predict
            x_pred = x_est
            p_pred = p_est + Q

            # 2. Update
            k_gain = p_pred / (p_pred + R)
            x_est = x_pred + k_gain * (z - x_pred)
            p_est = (1.0 - k_gain) * p_pred

            filtered.append(round(x_est, 5))
            gains.append(round(k_gain, 4))

        return {
            "measurements_count": len(measurements),
            "process_noise_q": Q,
            "measurement_noise_r": R,
            "final_estimated_state": filtered[-1],
            "final_estimation_variance": round(p_est, 6),
            "filtered_estimates": filtered,
            "kalman_gains": gains
        }

    def detect_volatility_and_regime_bursts(self, time_series: List[float],
                                           window_size: int = 10,
                                           z_threshold: float = 2.5) -> Dict[str, Any]:
        """
        Detects anomalous information bursts or market regime shifts via rolling Z-score.
        """
        if len(time_series) < window_size:
            return {"error": "Time series length smaller than window size"}

        history = time_series[:-1]
        latest_val = time_series[-1]
        recent_window = history[-window_size:]

        mean_val = sum(recent_window) / len(recent_window)
        variance = sum((x - mean_val) ** 2 for x in recent_window) / max(1, len(recent_window) - 1)
        std_dev = math.sqrt(variance)

        z_score = (latest_val - mean_val) / max(1e-6, std_dev)
        is_burst = abs(z_score) >= z_threshold

        if is_burst:
            verdict = "CRITICAL_VOLATILITY_BURST_TRIGGERED" if z_score > 0 else "CRITICAL_DEMAND_PLUNGE"
        else:
            verdict = "NOMINAL_STABLE_REGIME"

        return {
            "window_size": window_size,
            "window_mean": round(mean_val, 4),
            "window_std_dev": round(std_dev, 4),
            "latest_value": round(latest_val, 4),
            "computed_z_score": round(z_score, 3),
            "z_threshold": z_threshold,
            "is_anomaly_burst": is_burst,
            "regime_verdict": verdict
        }

    def compute_shannon_entropy_gain(self, prior_probs: List[float],
                                     posterior_probs: List[float]) -> Dict[str, Any]:
        """
        Calculates Shannon information entropy H(P) = -sum(p_i * log2(p_i))
        and Information Gain (KL-reduction): Delta H = H(Prior) - H(Posterior).
        """
        def entropy(probs):
            total = sum(probs)
            if total <= 0: return 0.0
            norm = [p / total for p in probs]
            return -sum(p * math.log2(p) for p in norm if p > 0)

        h_prior = entropy(prior_probs)
        h_post = entropy(posterior_probs)
        info_gain = h_prior - h_post

        return {
            "prior_entropy_bits": round(h_prior, 4),
            "posterior_entropy_bits": round(h_post, 4),
            "information_gain_bits": round(info_gain, 4),
            "uncertainty_reduction_pct": round(max(0.0, (info_gain / max(1e-6, h_prior)) * 100.0), 2)
        }
