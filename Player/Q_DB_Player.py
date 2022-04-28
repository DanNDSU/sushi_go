from utils import *
from Player import BasePlayer
from DBUtils import *


class Q_DB_Player(BasePlayer):

    def __init__(self, name):
        self.db= DBUtils()
        super().__init__(name)
        self.decay_gamma = 0.9
        self.lr = 0.01
        self.exp_rate = 0.3
        self.hits = 0
        self.querys = 0
        self.cursor= self.db.db_cursor

        self.model_dict = self.db.fetchData(self.cursor)

        self.prepare_for_next_round()

    def draw(self, card):
        self.hand.append(card)

    def pick_a_card(self, all_player_boards):
        action = None
        max_value = -100
        for possible_next_card in set(self.hand):
            board = copy.copy(self.board)
            add_a_card_to_board(board, possible_next_card)
            self.querys += 1
            if str(board) in self.model_dict:
                self.hits += 1
            value = self.model_dict.get(str(board), 0) + random.random() / 1e6
            if value > max_value:
                max_value = value
                action = possible_next_card

        # Take a card based on action
        self.hand.remove(action)
        add_a_card_to_board(self.board, action)

        # Add state to memory
        self.states_in_game.append(str(self.board))

    def get_score(self):
        return get_score(self.board)

    #This function is what calculates the reward - the database connection could go here.
    def feed_reward(self, reward):
        #db = DBUtils()
        #print(self.name)
        for state in self.states_in_game[::-1]:
            if state not in self.model_dict:
                self.model_dict[state] = 0
                print("State"+str(state))
            self.model_dict[state] += (reward - self.model_dict[state]) * self.lr
            q_state = str(state)
            qValue = str(self.model_dict[state])
            self.db.addDataToDb(curr_state=q_state, q_value=qValue)
            #print("Model dict"+str(self.model_dict[state]))
            reward *= self.decay_gamma
            print("reward" + str(reward))

          #  print(self.model_dict)
            print()
        self.db.dbCommit()

    def prepare_for_next_round(self):
        super().prepare_for_next_round()
        self.states_in_game = []
        self.states_in_game.append(str(self.board))