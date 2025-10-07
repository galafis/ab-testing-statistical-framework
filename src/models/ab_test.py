"""
A/B Testing Statistical Framework

Statistical testing framework for A/B experiments with power analysis and sequential testing.

Author: Gabriel Demetrios Lafis
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Tuple, Optional
from loguru import logger


class ABTest:
    """
    A/B testing framework with statistical analysis.
    """
    
    def __init__(
        self,
        alpha: float = 0.05,
        power: float = 0.80,
        alternative: str = 'two-sided'
    ):
        """
        Initialize A/B test.
        
        Args:
            alpha: Significance level
            power: Statistical power
            alternative: Alternative hypothesis ('two-sided', 'greater', 'less')
        """
        self.alpha = alpha
        self.power = power
        self.alternative = alternative
        
        logger.info(f"Initialized A/B test with alpha={alpha}, power={power}")
    
    def calculate_sample_size(
        self,
        baseline_rate: float,
        mde: float,
        metric_type: str = 'proportion'
    ) -> int:
        """
        Calculate required sample size per group.
        
        Args:
            baseline_rate: Baseline conversion rate or mean
            mde: Minimum detectable effect (absolute)
            metric_type: Type of metric ('proportion' or 'continuous')
            
        Returns:
            Required sample size per group
        """
        from statsmodels.stats.power import zt_ind_solve_power, tt_ind_solve_power
        
        if metric_type == 'proportion':
            # Calculate effect size (Cohen's h)
            p1 = baseline_rate
            p2 = baseline_rate + mde
            effect_size = 2 * (np.arcsin(np.sqrt(p2)) - np.arcsin(np.sqrt(p1)))
            
            # Calculate sample size
            n = zt_ind_solve_power(
                effect_size=effect_size,
                alpha=self.alpha,
                power=self.power,
                alternative=self.alternative
            )
        else:
            # For continuous metrics, assume effect size
            effect_size = mde / baseline_rate if baseline_rate != 0 else mde
            
            n = tt_ind_solve_power(
                effect_size=effect_size,
                alpha=self.alpha,
                power=self.power,
                alternative=self.alternative
            )
        
        sample_size = int(np.ceil(n))
        logger.info(f"Required sample size per group: {sample_size}")
        
        return sample_size
    
    def proportion_test(
        self,
        control_conversions: int,
        control_total: int,
        treatment_conversions: int,
        treatment_total: int
    ) -> Dict:
        """
        Two-proportion z-test.
        
        Args:
            control_conversions: Number of conversions in control
            control_total: Total in control group
            treatment_conversions: Number of conversions in treatment
            treatment_total: Total in treatment group
            
        Returns:
            Dictionary with test results
        """
        logger.info("Running two-proportion z-test...")
        
        # Calculate proportions
        p_control = control_conversions / control_total
        p_treatment = treatment_conversions / treatment_total
        
        # Pooled proportion
        p_pooled = (control_conversions + treatment_conversions) / (control_total + treatment_total)
        
        # Standard error
        se = np.sqrt(p_pooled * (1 - p_pooled) * (1/control_total + 1/treatment_total))
        
        # Z-statistic
        z_stat = (p_treatment - p_control) / se
        
        # P-value
        if self.alternative == 'two-sided':
            p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        elif self.alternative == 'greater':
            p_value = 1 - stats.norm.cdf(z_stat)
        else:  # less
            p_value = stats.norm.cdf(z_stat)
        
        # Confidence interval
        ci_se = np.sqrt(p_control * (1 - p_control) / control_total + 
                       p_treatment * (1 - p_treatment) / treatment_total)
        ci_margin = stats.norm.ppf(1 - self.alpha/2) * ci_se
        
        lift = (p_treatment - p_control) / p_control if p_control > 0 else 0
        
        results = {
            'control_rate': p_control,
            'treatment_rate': p_treatment,
            'absolute_lift': p_treatment - p_control,
            'relative_lift': lift,
            'z_statistic': z_stat,
            'p_value': p_value,
            'significant': p_value < self.alpha,
            'confidence_interval': (
                p_treatment - p_control - ci_margin,
                p_treatment - p_control + ci_margin
            )
        }
        
        logger.info(f"Test results: p-value={p_value:.4f}, significant={results['significant']}")
        
        return results
    
    def t_test(
        self,
        control_data: np.ndarray,
        treatment_data: np.ndarray,
        equal_var: bool = False
    ) -> Dict:
        """
        Independent t-test for continuous metrics.
        
        Args:
            control_data: Control group data
            treatment_data: Treatment group data
            equal_var: Whether to assume equal variance
            
        Returns:
            Dictionary with test results
        """
        logger.info("Running independent t-test...")
        
        # Calculate statistics
        control_mean = np.mean(control_data)
        treatment_mean = np.mean(treatment_data)
        control_std = np.std(control_data, ddof=1)
        treatment_std = np.std(treatment_data, ddof=1)
        
        # Perform t-test
        t_stat, p_value = stats.ttest_ind(
            treatment_data,
            control_data,
            equal_var=equal_var,
            alternative=self.alternative
        )
        
        # Confidence interval
        n1, n2 = len(control_data), len(treatment_data)
        if equal_var:
            pooled_std = np.sqrt(((n1-1)*control_std**2 + (n2-1)*treatment_std**2) / (n1+n2-2))
            se = pooled_std * np.sqrt(1/n1 + 1/n2)
            df = n1 + n2 - 2
        else:
            se = np.sqrt(control_std**2/n1 + treatment_std**2/n2)
            df = ((control_std**2/n1 + treatment_std**2/n2)**2 / 
                  ((control_std**2/n1)**2/(n1-1) + (treatment_std**2/n2)**2/(n2-1)))
        
        ci_margin = stats.t.ppf(1 - self.alpha/2, df) * se
        
        lift = (treatment_mean - control_mean) / control_mean if control_mean != 0 else 0
        
        results = {
            'control_mean': control_mean,
            'treatment_mean': treatment_mean,
            'control_std': control_std,
            'treatment_std': treatment_std,
            'absolute_lift': treatment_mean - control_mean,
            'relative_lift': lift,
            't_statistic': t_stat,
            'p_value': p_value,
            'degrees_of_freedom': df,
            'significant': p_value < self.alpha,
            'confidence_interval': (
                treatment_mean - control_mean - ci_margin,
                treatment_mean - control_mean + ci_margin
            )
        }
        
        logger.info(f"Test results: p-value={p_value:.4f}, significant={results['significant']}")
        
        return results
    
    def mann_whitney_test(
        self,
        control_data: np.ndarray,
        treatment_data: np.ndarray
    ) -> Dict:
        """
        Mann-Whitney U test (non-parametric).
        
        Args:
            control_data: Control group data
            treatment_data: Treatment group data
            
        Returns:
            Dictionary with test results
        """
        logger.info("Running Mann-Whitney U test...")
        
        u_stat, p_value = stats.mannwhitneyu(
            treatment_data,
            control_data,
            alternative=self.alternative
        )
        
        results = {
            'control_median': np.median(control_data),
            'treatment_median': np.median(treatment_data),
            'u_statistic': u_stat,
            'p_value': p_value,
            'significant': p_value < self.alpha
        }
        
        logger.info(f"Test results: p-value={p_value:.4f}, significant={results['significant']}")
        
        return results
    
    def sequential_test(
        self,
        control_conversions: int,
        control_total: int,
        treatment_conversions: int,
        treatment_total: int,
        spending_function: str = 'obrien_fleming'
    ) -> Dict:
        """
        Sequential testing with alpha spending.
        
        Args:
            control_conversions: Number of conversions in control
            control_total: Total in control group
            treatment_conversions: Number of conversions in treatment
            treatment_total: Total in treatment group
            spending_function: Alpha spending function
            
        Returns:
            Dictionary with test results
        """
        logger.info("Running sequential test...")
        
        # Calculate current sample fraction
        max_sample = control_total + treatment_total
        current_fraction = (control_total + treatment_total) / max_sample
        
        # Calculate spent alpha (simplified O'Brien-Fleming)
        if spending_function == 'obrien_fleming':
            spent_alpha = 2 * (1 - stats.norm.cdf(stats.norm.ppf(1 - self.alpha/2) / np.sqrt(current_fraction)))
        else:
            spent_alpha = self.alpha * current_fraction
        
        # Run proportion test with adjusted alpha
        original_alpha = self.alpha
        self.alpha = spent_alpha
        
        results = self.proportion_test(
            control_conversions, control_total,
            treatment_conversions, treatment_total
        )
        
        results['spent_alpha'] = spent_alpha
        results['sample_fraction'] = current_fraction
        
        self.alpha = original_alpha
        
        logger.info(f"Sequential test: spent_alpha={spent_alpha:.4f}")
        
        return results


if __name__ == "__main__":
    # Example usage
    
    # Initialize test
    ab_test = ABTest(alpha=0.05, power=0.80)
    
    # Calculate sample size
    sample_size = ab_test.calculate_sample_size(
        baseline_rate=0.10,
        mde=0.02,
        metric_type='proportion'
    )
    print(f"\nRequired sample size per group: {sample_size}")
    
    # Run proportion test
    results = ab_test.proportion_test(
        control_conversions=102,
        control_total=1000,
        treatment_conversions=125,
        treatment_total=1000
    )
    
    print("\nA/B Test Results:")
    print(f"  Control rate: {results['control_rate']:.2%}")
    print(f"  Treatment rate: {results['treatment_rate']:.2%}")
    print(f"  Relative lift: {results['relative_lift']:.2%}")
    print(f"  P-value: {results['p_value']:.4f}")
    print(f"  Significant: {results['significant']}")
    print(f"  95% CI: [{results['confidence_interval'][0]:.4f}, {results['confidence_interval'][1]:.4f}]")
