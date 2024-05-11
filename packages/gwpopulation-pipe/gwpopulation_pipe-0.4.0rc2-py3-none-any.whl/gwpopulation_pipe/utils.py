import os

from gwpopulation.conversions import convert_to_beta_parameters
from gwpopulation.hyperpe import HyperparameterLikelihood, xp
from gwpopulation.models.spin import (
    iid_spin,
    iid_spin_magnitude_beta,
    independent_spin_magnitude_beta,
)


def prior_conversion(parameters):
    """Wrapper around conversion for prior constraints"""
    for key in ["amax", "amax_1", "amax_2"]:
        if key not in parameters:
            parameters[key] = 1
    parameters, _ = convert_to_beta_parameters(parameters)
    return parameters


def get_path_or_local(path: str) -> str:
    """
    Check if a path exists, if not check if the basename exists, if not raise an error.

    Parameters
    ----------
    path: str
        The path to check.

    Returns
    -------
    path: str
        The path to use.

    Raises
    ------
    ValueError
        If neither the path nor the basename exist.
    """
    if os.path.exists(path):
        return path
    elif os.path.exists(os.path.basename(path)):
        return os.path.basename(path)
    else:
        raise ValueError(f"Cannot find {path} or {os.path.basename(path)}")


KNOWN_ARGUMENTS = {
    iid_spin: ["mu_chi", "sigma_chi", "xi_spin", "sigma_spin"],
    iid_spin_magnitude_beta: ["mu_chi", "sigma_chi"],
    independent_spin_magnitude_beta: [
        "mu_chi_1",
        "mu_chi_2",
        "sigma_chi_1",
        "sigma_chi_2",
    ],
}


class MinimumEffectiveSamplesLikelihood(HyperparameterLikelihood):
    def _compute_per_event_ln_bayes_factors(self, return_uncertainty=True):
        """
        Compute the per event ln Bayes factors and associated variance.

        This method imposes a condition that the number of effective
        samples per Monte Carlo integral must be at least as much
        as the total number of events. Otherwise the lnBF is set to
        - infinity.

        Returns
        -------
        ln_per_event_bfs: array-like
            The ln BF per event subject to having a sufficient number
            of independent samples.
        variance: array-like
            The variances (uncertainties) in the ln BF per event. Only
            returned if `return_uncertainty` is True. This output will
            generally not be used for convergence criteria, as this function
            already enforces a threshold on effective number of samples.
        """
        (
            per_event_bfs,
            n_effectives,
            variance,
        ) = self.per_event_bayes_factors_and_n_effective_and_variances()
        per_event_bfs *= n_effectives > self.n_posteriors
        if return_uncertainty:
            return xp.log(per_event_bfs), variance
        else:
            return xp.log(per_event_bfs)

    def per_event_bayes_factors_and_n_effective_and_variances(self):
        """
        Called by `_compute_per_event_ln_bayes_factors` to compute the
        per event BFs, effective number of samples for each event's computed
        BF, and the associated uncertainty (variance) in the *ln* BF. Computes
        same qunatities as superclass function `_compute_per_event_ln_bayes_factors`
        but additionally provides the effective sample size.

        Returns
        -------
        per_event_bfs: array-like
            The BF per event, computed by reweighting single-event likelihood
            samples into the `hyper_prior` model.
        n_effectives: array-like
            The effective sample size for each Monte Carlo sum computation of the BFs.
            The BF is computed for each event, so this array has length n_events.
        variance: array-like
            The variances (uncertainties) in the ln BF per event.
        """
        weights = self.hyper_prior.prob(self.data) / self.sampling_prior
        per_event_bfs = xp.sum(weights, axis=-1)
        n_effectives = xp.nan_to_num(per_event_bfs**2 / xp.sum(weights**2, axis=-1))
        per_event_bfs /= self.samples_per_posterior
        square_expectation = xp.mean(weights**2, axis=-1)
        variance = (square_expectation - per_event_bfs**2) / (
            self.samples_per_posterior * per_event_bfs**2
        )
        return per_event_bfs, n_effectives, variance

    def per_event_bayes_factors_and_n_effective(self):
        (
            per_event_bfs,
            n_effectives,
            _,
        ) = self.per_event_bayes_factors_and_n_effective_and_variances()
        return per_event_bfs, n_effectives


def maybe_jit(func):
    from gwpopulation.backend import __backend__

    if __backend__ == "jax":
        from jax import jit

        return jit(func)
    else:
        return func
