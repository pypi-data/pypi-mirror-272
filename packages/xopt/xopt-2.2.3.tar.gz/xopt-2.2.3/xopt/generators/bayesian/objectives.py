from functools import partial

import torch
from botorch.acquisition import GenericMCObjective
from botorch.acquisition.multi_objective import WeightedMCMultiOutputObjective
from botorch.sampling import get_sampler

from xopt.generators.bayesian.custom_botorch.constrained_acquisition import (
    FeasibilityObjective,
)
from xopt.generators.bayesian.utils import set_botorch_weights


def feasibility(X, model, vocs, posterior_transform=None):
    constraints = create_constraint_callables(vocs)
    posterior = model.posterior(X=X, posterior_transform=posterior_transform)

    sampler = get_sampler(
        model.posterior(X),
        sample_shape=torch.Size([512]),
    )
    samples = sampler(posterior)
    objective = FeasibilityObjective(constraints)
    return torch.mean(objective(samples, X), dim=0)


def constraint_function(Z, vocs, name):
    """
    create constraint function
    - constraint functions should return negative values for feasible values and
    positive values for infeasible values
    """
    output_names = vocs.output_names
    constraint = vocs.constraints[name]

    if constraint[0] == "LESS_THAN":
        return Z[..., output_names.index(name)] - constraint[1]
    elif constraint[0] == "GREATER_THAN":
        return -(Z[..., output_names.index(name)] - constraint[1])


def create_constraint_callables(vocs):
    if vocs.constraints is not None:
        constraint_names = vocs.constraint_names
        constraint_callables = []
        for name in constraint_names:
            constraint_callables += [
                partial(
                    constraint_function,
                    vocs=vocs,
                    name=name,
                )
            ]
        return constraint_callables

    else:
        return None


def create_mc_objective(vocs, tkwargs):
    """
    create the objective object

    """
    weights = set_botorch_weights(vocs)

    def obj_callable(Z, X=None):
        return torch.matmul(Z, weights.reshape(-1, 1)).squeeze(-1)

    return GenericMCObjective(obj_callable)


def create_mobo_objective(vocs):
    """
    botorch assumes maximization so we need to negate any objectives that have
    minimize keyword and zero out anything that is a constraint
    """
    output_names = vocs.output_names
    objective_indicies = [output_names.index(name) for name in vocs.objectives]
    weights = set_botorch_weights(vocs)[objective_indicies]

    return WeightedMCMultiOutputObjective(
        weights, outcomes=objective_indicies, num_outcomes=vocs.n_objectives
    )
