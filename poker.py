"""Main script for Poker hand simulation"""

import json
from multiprocessing import Pool
from datetime import datetime
from collections import defaultdict
from deuces import Deck
from deuces import Evaluator
from deuces import Card


sample_size = 100000
runs = 1000


def run(number):
    """
    This function generates a population sample with size sample.
    It also computes probabilities for each hand, considering a
    frequentist approach.

    Arguments:
        - number (int): run ID

    Returns:
        - stats (str): returns a JSON formatted string containing
            probabilities for each poker hand
    """
    print('starting run #{0}'.format(number))
    evaluator = Evaluator()
    poker_hands = defaultdict(int)

    for i in range(sample_size):
        deck = Deck()
        p1_hand = deck.draw(5)
        p1_score = evaluator.evaluate(p1_hand, [])
        if p1_score == 1:  # just a little hack
            poker_hands['Royal Flush'] += 1
        else:
            p1_class = evaluator.get_rank_class(p1_score)
            poker_hands[evaluator.class_to_string(p1_class)] += 1

    stats = dict((k, round(float(v)/sample_size, 7))
                 for k, v in poker_hands.items())
    return json.dumps(stats)

if __name__ == '__main__':
    p = Pool(7)
    result = p.map(run, range(runs))

    with open('data.json', 'w') as outfile:
        json.dump(result, outfile, sort_keys=True, indent=4)
