from pprint import pprint

from ai.probabilistic_reasoning import print_tools
from ai.probabilistic_reasoning.bayesian_network import BayesianNetworkBuilder, BayesianNetwork, probability, \
    single_variable_probability, get_markov_blanket, multivariable_with_hidden_probability, rejection_sampling, \
    likelihood_weighting

try:
    assert False
    # noinspection PyUnreachableCode
    raise ValueError('Please enable assertions')
except AssertionError:
    pass


def _create_alarm_bayesian_network() -> BayesianNetwork:
    builder = BayesianNetworkBuilder()
    burglary = builder.create_variable('Burglary', lambda *_: 0.001)
    earthquake = builder.create_variable('Earthquake', lambda *_: 0.002)

    def _f(nodes, truth) -> float:
        b_truth = e_truth = None
        for n, n_truth in zip(nodes, truth):
            if n.id == burglary:
                b_truth = n_truth
            elif n.id == earthquake:
                e_truth = n_truth
            else:
                raise ValueError
            if b_truth is not None and e_truth is not None:
                break
        if b_truth and e_truth:
            return 0.95
        if b_truth:
            return 0.94
        if e_truth:
            return 0.29
        return 0.001

    alarm = builder.create_variable('Alarm', _f)
    builder.add_arrow(burglary, alarm)
    builder.add_arrow(earthquake, alarm)

    def _f2(_, truth) -> float:
        return 0.9 if truth[0] else 0.05
    john_calls = builder.create_variable('John Calls', _f2)
    builder.add_arrow(alarm, john_calls)

    def _f3(_, truth) -> float:
        return 0.7 if truth[0] else 0.01
    mary_calls = builder.create_variable('Mary Calls', _f3)
    builder.add_arrow(alarm, mary_calls)
    return \
        builder.build(), \
        tuple(
           map(
               lambda d: builder.get_variable_by_id(d),
               (burglary, earthquake, alarm, john_calls, mary_calls)
           )
        )


def entry_point():
    network, all_nodes = _create_alarm_bayesian_network()
    print_tools.print_bayesian_network(network)
    burglary, earthquake, alarm, john_calls, mary_calls = all_nodes
    p = probability(
        {
            burglary: False,
            earthquake: False,
            alarm: True,
            john_calls: True,
            mary_calls: True
        }
    )

    print(
        'Probability to be called by John and Mary when alarm activates but neither earthquake nor burglary: ',
        p, ', expected 0.000628')
    assert abs(p - 0.000628) < 0.000001

    print(
        'Probability of alarm',
        single_variable_probability((burglary, earthquake, john_calls, mary_calls), alarm)
    )

    # p(B|j, m) = p(B, j, m) / p(j, m)
    p = single_variable_probability((earthquake, alarm), burglary, john_calls, mary_calls) / \
        single_variable_probability((earthquake, alarm, burglary), john_calls, mary_calls)
    print('Probability of burglar given both John and Mary called', p)
    assert abs(p - 0.284) < 0.001
    # p(!B|j, m) = p(!B, j, m)/p(j, m)
    not_p = multivariable_with_hidden_probability(
        (earthquake, alarm), {burglary: False, john_calls: True, mary_calls: True}) / \
        single_variable_probability((earthquake, alarm, burglary), john_calls, mary_calls)
    assert p + not_p == 1
    print('Markov blanket for Burglary')
    pprint(list(get_markov_blanket(burglary)))
    pb_jm = rejection_sampling(
        burglary, {john_calls: True, mary_calls: True},
        network)
    print('P(B|j, m), Probability by rejection sampling: {}'.format(
        pb_jm
    ))
    try:
        assert abs(pb_jm - p) < 0.001
    except AssertionError:
        print('Unfortunately rejection sampling rejects too many events')

    # Likehood weighting should work a bit better than rejection sampling.
    pb_jm = likelihood_weighting(
        burglary, {john_calls: True, mary_calls: True},
        network)
    print('P(B|j, m), Probability by likehood weighting: {}'.format(
        pb_jm
    ))
    assert abs(pb_jm - p) < 0.05



if __name__ == '__main__':
    entry_point()
