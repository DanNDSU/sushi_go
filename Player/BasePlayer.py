from utils import *


class BasePlayer:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.board = [0] * len(CARD_ON_BOARD)
        self.prepare_for_next_round()

    def draw(self, card):
        self.hand.append(card)

    def pick_a_card(self, all_player_boards):
        raise NotImplementedError

    def get_score(self):
        return get_score(self.board)

    def feed_reward(self, reward):
        # Defaults to not learning
        return

    # this is used for QRewardPlayer, other players don't learn from it.
    def feed_reward_score(self, reward):
        return 

    def feed_reward_score_plus_minus(self, reward):
        return

    def prepare_for_next_round(self):
        self.hand = []
        #pudding_count = self.board[11]
        self.board = [0] * len(CARD_ON_BOARD)
        #self.board[11] = pudding_count

    def prepare_for_next_game(self):
        self.hand = []
        self.board = [0] * len(CARD_ON_BOARD)
