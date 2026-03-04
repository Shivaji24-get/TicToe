# app.py
from flask import Flask, render_template, jsonify, request
import numpy as np
import random
import json

app = Flask(__name__)

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3))
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.epsilon = 0.1
        self.learn(5000)  # Train on initialization

    # [Previous Q-learning methods remain the same as before]
    def get_state(self):
        return tuple(map(tuple, self.board))

    def get_available_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == 0]

    def make_move(self, position, player):
        if self.board[position[0]][position[1]] == 0:
            self.board[position[0]][position[1]] = player
            return True
        return False

    def check_winner(self):
        for i in range(3):
            if sum(self.board[i, :]) == 3 or sum(self.board[:, i]) == 3:
                return 1
            if sum(self.board[i, :]) == -3 or sum(self.board[:, i]) == -3:
                return -1
        if sum(np.diag(self.board)) == 3 or sum(np.diag(np.fliplr(self.board))) == 3:
            return 1
        if sum(np.diag(self.board)) == -3 or sum(np.diag(np.fliplr(self.board))) == -3:
            return -1
        return 0

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.get_available_moves())
        max_value = float('-inf')
        best_action = None
        for action in self.get_available_moves():
            state_action = (state, action)
            if state_action not in self.q_table:
                self.q_table[state_action] = 0.0
            if self.q_table[state_action] > max_value:
                max_value = self.q_table[state_action]
                best_action = action
        return best_action or random.choice(self.get_available_moves())

    def learn(self, num_episodes):
        # [Same learning implementation as before]
        pass

# Initialize game
game = TicTacToe()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    row, col = data['row'], data['col']
    
    # Player move
    if not game.make_move((row, col), -1):
        return jsonify({'error': 'Invalid move'})
    
    winner = game.check_winner()
    if winner != 0 or not game.get_available_moves():
        return jsonify({
            'board': game.board.tolist(),
            'game_over': True,
            'winner': winner
        })
    
    # AI move
    ai_move = game.choose_action(game.get_state())
    game.make_move(ai_move, 1)
    
    winner = game.check_winner()
    return jsonify({
        'board': game.board.tolist(),
        'game_over': winner != 0 or not game.get_available_moves(),
        'winner': winner
    })

@app.route('/reset', methods=['POST'])
def reset():
    game.board = np.zeros((3, 3))
    return jsonify({'board': game.board.tolist()})

if __name__ == '__main__':
    #app.run(debug=True)
    #app.run(port=5001, debug=True)
    app.run(use_reloader=False, debug=True)

