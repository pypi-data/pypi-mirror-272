import logging
from typing import Dict, List, Optional, Set, Tuple, Union, cast

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from tqdm import tqdm

import avh.constraints as constraints
import avh.data_issues as issues
import avh.metrics as metrics
import avh.utility_functions as utils
from avh.aliases import Seed


class AVH:
    """
    Returns a dictionary with ConjuctivDQProgram for a column
    """

    logger = logging.getLogger(f"{__name__}.AVH")

    def _enable_debug(self, enable: bool):
        self.logger.setLevel(logging.DEBUG if enable else logging.INFO)

    def _reset_verbosity_states(self):
        self._enable_debug(False)

    def __init__(
        self,
        M: Optional[List[metrics.MetricType]] = None,
        E: Optional[List[constraints.ConstraintType]] = None,
        DC: Optional[issues.DQIssueDatasetGenerator] = None,
        columns: Optional[List[str]] = None,
        time_differencing: bool = False,
        random_state: Seed = None,
        verbose: int = 1,
        n_jobs: Optional[int] = None,
    ):

        self.columns = columns
        self.time_differencing = time_differencing
        self.verbose = verbose
        self.random_state = random_state
        self.n_jobs = n_jobs

        self.M = M if M is not None else self.default_metrics
        self.E = E if E is not None else self.default_constraint_estimators

        self.DC = (
            DC
            if DC is not None
            else self._get_default_issue_dataset_generator(
                verbose=self._verbose, random_state=self.random_state
            )
        )

    @property
    def verbose(self) -> int:
        if self._verbose == 0:
            return False
        return True

    @verbose.setter
    def verbose(self, level: Union[int, bool]):
        assert level >= 0, "Verbosity level must be a positive integer"

        self._reset_verbosity_states()
        self._verbose = level

        if level >= 2:
            self._enable_debug(True)

    @property
    def default_data_quality_issues(self) -> List[Tuple[issues.IssueType, dict]]:
        return [
            (issues.SchemaChange, {"p": [0.1, 0.5, 1.0]}),
            (issues.UnitChange, {"p": [0.1, 1.0], "m": [10, 100, 1000]}),
            (issues.IncreasedNulls, {"p": [0.1, 0.5, 1.0]}),
            (issues.VolumeChangeUpsample, {"f": [2, 10]}),
            (issues.VolumeChangeDownsample, {"f": [0.5, 0.1]}),
            (issues.DistributionChange, {"p": [0.1, 0.5], "take_last": [True, False]}),
            (issues.NumericPerturbation, {"p": [0.1, 0.5, 1.0]}),
        ]

    @property
    def default_metrics(self) -> List[metrics.MetricType]:
        return [
            metrics.RowCount,
            metrics.DistinctRatio,
            metrics.DistinctCount,
            metrics.CompleteRatio,
            metrics.Min,
            metrics.Max,
            metrics.Mean,
            metrics.Median,
            metrics.Sum,
            metrics.Range,
            metrics.EMD,
            metrics.JsDivergence,
            metrics.KlDivergence,
            metrics.KsDist,
            metrics.CohenD,
        ]

    @property
    def default_constraint_estimators(self) -> List[constraints.ConstraintType]:
        return [
            constraints.CLTConstraint,
            constraints.ChebyshevConstraint,
            constraints.CantelliConstraint,
        ]

    @property
    def default_beta_ranges(self) -> Dict[constraints.ConstraintType, Tuple[float, float, float]]:
        """
        Returns default beta ranges (in terms fo standard deviations)
            for the default constraint estimators.

        The returned float tuple contains start, end and increment for the beta range.
        All ranges are calculated for estimated FPR in [0.5, 0.0005]
        """
        return {
            constraints.ChebyshevConstraint: (2.0, 50.0, 1.0),
            constraints.CantelliConstraint: (1.0, 49.0, 1.0),
            constraints.CLTConstraint: (1.0, 5.0, 0.5),
        }

    @property
    def default_production_beta_ranges(
        self,
    ) -> Dict[constraints.ConstraintType, Tuple[float, float, float]]:
        """
        Returns default beta ranges (in terms fo standard deviations)
            for the default constraint estimators,
            optimised for production use (when target FPR is small)

        The justification is simple:
            "In production, no one would need 100% expected FPR,
            which comes with beta = 1 * std on Chebyshev,
            or ~0% which comes after beta = 4 * std on CTL"

        The returned float tuple contains start, end and increment for the range.
        All ranges are calculated for estimated FPR in [0.05, 0.005]
        """
        return {
            constraints.ChebyshevConstraint: (5.0, 15.0, 1.0),
            constraints.CantelliConstraint: (5.0, 15.0, 1.0),
            constraints.CLTConstraint: (2.0, 4.0, 0.5),
        }

    def _get_default_issue_dataset_generator(
        self, verbose: int = 0, random_state: Seed = 42
    ) -> issues.DQIssueDatasetGenerator:
        """
        Constructs a DQIssueDatasetTransformer instance
            with DQ issues and parameter space described in the paper
        """

        return issues.DQIssueDatasetGenerator(
            issues=self.default_data_quality_issues,
            verbose=verbose,
            random_state=random_state,
            n_jobs=self.n_jobs,
        )

    @utils.debug_timeit(f"{__name__}.AVH")
    def generate(
        self,
        history: List[pd.DataFrame],
        fpr_target: float,
        optimise_search_space: Union[bool, str] = "auto",
    ) -> Dict[str, constraints.ConjuctivDQProgram]:
        assert optimise_search_space in [
            True,
            False,
            "auto",
        ], "`optimise_search_space` can only be one of [True, False, 'auto']"
        if optimise_search_space == "auto":
            optimise_search_space = True if fpr_target <= 0.05 else False

        if self.n_jobs is None:
            return self._generate_sequential(history, fpr_target, optimise_search_space)
        else:
            return self._generate_parallel(history, fpr_target, optimise_search_space)

    @utils.debug_timeit(f"{__name__}.AVH")
    def _generate_sequential(
        self, history: List[pd.DataFrame], fpr_target: float, optimise_search_space: bool
    ) -> Dict[str, constraints.ConjuctivDQProgram]:

        PS = {}
        DC = self.DC.generate(history[-1])
        columns = self.columns if self.columns else list(history[0].columns)

        for column in tqdm(columns, "Generating P(S for columns...", disable=not self._verbose):
            Q = self._generate_constraint_space(
                [run[column] for run in history[:-1]], optimise_search_space
            )

            PS[column] = self._generate_conjuctive_dq_program(Q, DC[column], fpr_target)

        return PS

    def _generate_parallel_worker(self, column, history, DC, fpr_target, optimise_search_space):
        Q = self._generate_constraint_space(history, optimise_search_space)
        return column, self._generate_conjuctive_dq_program(Q, DC, fpr_target)

    @utils.debug_timeit(f"{__name__}.AVH")
    def _generate_parallel(
        self, history: List[pd.DataFrame], fpr_target: float, optimise_search_space: bool
    ) -> Dict[str, constraints.ConjuctivDQProgram]:
        PS = {}

        DC = self.DC.generate(history[-1])
        columns = self.columns if self.columns else list(history[0].columns)

        results = Parallel(n_jobs=self.n_jobs, return_as="generator_unordered")(
            delayed(self._generate_parallel_worker)(
                column,
                [run[column] for run in history[:-1]],
                DC[column],
                fpr_target,
                optimise_search_space,
            )
            for column in columns
        )

        for column, ps in tqdm(
            results, "creating P(S) (with joblib)...", total=len(columns), disable=not self.verbose
        ):
            PS[column] = ps

        del results
        return PS

    def _get_beta_range(
        self, constraint_estimator: constraints.ConstraintType, optimise_search_space: bool
    ) -> np.ndarray:

        default_beta_ranges = (1.0, 50.0, 1.0)
        if optimise_search_space:
            beta_start, beta_end, beta_increment = self.default_production_beta_ranges.get(
                constraint_estimator, default_beta_ranges
            )
        else:
            beta_start, beta_end, beta_increment = self.default_beta_ranges.get(
                constraint_estimator, default_beta_ranges
            )

        return np.arange(beta_start, beta_end, beta_increment)

    @utils.debug_timeit(f"{__name__}.AVH")
    def _generate_constraint_space(
        self, history: List[pd.Series], optimise_search_space=False
    ) -> List[constraints.Constraint]:
        Q = []
        for metric in self.M:
            if not metric.is_column_compatable(history[0].dtype):
                continue

            precalculated_metric_history = cast(List[float], metric.calculate(history))
            precalculated_std = np.nanstd(precalculated_metric_history)

            for constraint_estimator in self.E:
                if not constraint_estimator.is_metric_compatable(metric):
                    continue

                for beta in self._get_beta_range(constraint_estimator, optimise_search_space):
                    q = constraint_estimator(
                        metric,
                    ).fit(
                        history,
                        hotload_history=precalculated_metric_history,
                        beta=precalculated_std * beta,
                        strategy="raw",
                    )
                    Q.append(q)
        return Q

    @utils.debug_timeit(f"{__name__}.AVH")
    def _precalculate_constraint_recalls(
        self, Q: List[constraints.Constraint], DC: List[Tuple[str, pd.Series]]
    ) -> List[Set[str]]:

        return [{issue for issue, data in DC if not constraint.predict(data)} for constraint in Q]

    @utils.debug_timeit(f"{__name__}.AVH")
    def _precalculate_constraint_recalls_fast(
        self, Q: List[constraints.Constraint], DC: List[Tuple[str, pd.Series]]
    ) -> List[Set[str]]:
        """
        Serves the exact same purpose as _precalculate_constraint_recalls
            but tries to optimise the calculations by precalculating the metric values
            for common constraint predictions.

        This optimisation implementation is highly coupled with current Q space generation,
            since it expects common-metric constraints to be clustered.
        """
        individual_recalls: List[set] = [set() for _ in Q]

        def _cache_metric_from_constraint(constraint: constraints.Constraint, data: pd.Series):
            cached_metric = constraint.metric
            if issubclass(cached_metric, metrics.SingleDistributionMetric):
                precalculated_metric = cached_metric.calculate(data)
            else:
                precalculated_metric = cached_metric.calculate(
                    data, constraint.last_reference_sample_
                )

            return cached_metric, precalculated_metric

        for issue, data in DC:
            cached_metric, precalculated_metric = _cache_metric_from_constraint(Q[0], data)
            for idx, constraint in enumerate(Q):
                if not issubclass(constraint.metric, cached_metric):
                    cached_metric, precalculated_metric = _cache_metric_from_constraint(
                        constraint, data
                    )
                if not constraint._predict(precalculated_metric):
                    individual_recalls[idx].add(issue)

        return individual_recalls

    @utils.debug_timeit(f"{__name__}.AVH")
    def _find_optimal_singleton_conjuctive_dq_program(
        self,
        Q: List[constraints.Constraint],
        constraint_recalls: List[Set[str]],
        fpr_target: float,
    ) -> constraints.ConjuctivDQProgram:
        best_singleton_constraint_idx = np.argmax(
            [
                len(recall) if Q[idx].expected_fpr_ < fpr_target else 0
                for idx, recall in enumerate(constraint_recalls)
            ]
        )

        return constraints.ConjuctivDQProgram(
            constraints=[Q[best_singleton_constraint_idx]],
            recall=constraint_recalls[best_singleton_constraint_idx],
            contributions=[constraint_recalls[best_singleton_constraint_idx]],
        )

    @utils.debug_timeit(f"{__name__}.AVH")
    def _find_optimal_conjunctive_dq_program(
        self,
        Q: List[constraints.Constraint],
        constraint_recalls: List[Set[str]],
        fpr_target: float,
    ) -> constraints.ConjuctivDQProgram:
        current_fpr = 0.0
        q_indexes = list(range(len(Q)))
        ps = constraints.ConjuctivDQProgram()
        while current_fpr < fpr_target and len(q_indexes) != 0:
            recall_increments = [
                constraint_recalls[idx].difference(ps.recall) for idx in q_indexes
            ]

            # stop if there are no more recall improvements possible
            if len(max(recall_increments)) == 0:
                break

            best_idx = np.argmax(
                [
                    len(recall_set) / (Q[idx].expected_fpr_ + 1)  # +1 is to avoid division by 0
                    for idx, recall_set in zip(q_indexes, recall_increments)
                ]
            )

            best_constraint = Q[q_indexes[best_idx]]
            if best_constraint.expected_fpr_ + current_fpr <= fpr_target:
                current_fpr += best_constraint.expected_fpr_
                ps.constraints.append(best_constraint)
                ps.recall.update(recall_increments[best_idx])
                ps.contributions.append(recall_increments[best_idx])

            q_indexes.pop(best_idx)

        return ps

    @utils.debug_timeit(f"{__name__}.AVH")
    def _generate_conjuctive_dq_program(
        self, Q: List[constraints.Constraint], DC: List[Tuple[str, pd.Series]], fpr_target: float
    ):
        individual_recalls = self._precalculate_constraint_recalls_fast(Q, DC)

        ps_singleton = self._find_optimal_singleton_conjuctive_dq_program(
            Q, individual_recalls, fpr_target
        )

        ps = self._find_optimal_conjunctive_dq_program(Q, individual_recalls, fpr_target)

        return ps if len(ps.recall) > len(ps_singleton.recall) else ps_singleton
