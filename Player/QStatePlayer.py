from utils import *
from Player import BasePlayer
from DBUtils import *


class QStatePlayer(BasePlayer):

    def __init__(self, name):
        self.db= DBUtils()
        super().__init__(name)
        self.decay_gamma = 0.9
        self.lr = 0.1
        self.exp_rate = 0.3
        self.hits = 0
        self.querys = 0

        self.model_dict = self.db.fetchData(table='q_state_player')

        self.prepare_for_next_round()

    def draw(self, card):
        self.hand.append(card)

    def pick_a_card(self, all_player_boards):
        action = None
        max_value = -100
        self.hand.sort()
        #print(self.hand)
        for possible_next_card in self.hand:
            board = copy.copy(self.board)
            hand = copy.copy(self.hand)
            hand.sort()
            hand.remove(possible_next_card)
            add_a_card_to_board(board, possible_next_card)
            state = [board, hand]
            #print(state)
            self.querys += 1
            if str(state) in self.model_dict:
                self.hits += 1
            value = self.model_dict.get(str(state), 0) + random.random() / 1e6
            if value > max_value:
                max_value = value
                action = possible_next_card

        # Take a card based on action
        
        self.hand.remove(action)
        add_a_card_to_board(self.board, action)

        # This state is improved to include both the board and the hand.
        self.hand.sort()
        state = [self.board, self.hand]
        #print("Final State: " + str(state))
        # Add state to memory
        self.states_in_game.append(str(state))

    def get_score(self):
        return get_score(self.board)

    #This function is what calculates the reward - the database connection could go here.
    def feed_reward(self, reward):
        #print(self.name)
        for state in self.states_in_game[::-1]:
            if state not in self.model_dict:
                self.model_dict[state] = 0
            #print("State: "+str(state))
            self.model_dict[state] = (1-self.lr) * self.model_dict[state] + (self.lr * reward)
            q_state = str(state)
            qValue = str(self.model_dict[state])
            self.db.addDataToDb(curr_state=q_state, q_value=qValue, table='q_state_player')
            #print("Model dict"+str(self.model_dict[state]))
            reward *= self.decay_gamma
            #print("Reward: " + str(reward))
        self.db.dbCommit()
        #print(self.model_dict)
        #print()

    def prepare_for_next_round(self):
        super().prepare_for_next_round()
        self.states_in_game = []
        self.states_in_game.append(str(self.board))