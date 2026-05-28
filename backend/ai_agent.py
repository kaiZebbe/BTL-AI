import os
import json
import random
from game_logic import NumberGame

class QLearningAI:
    def __init__(self, target_n, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.target_n = target_n
        self.alpha = alpha       # Tốc độ học
        self.gamma = gamma       # Hệ số giảm tương lai
        self.epsilon = epsilon   # Tỷ lệ khám phá
        self.q_table = {}        # Cấu trúc: { str(state): {"add1": q_val, "mul2": q_val} }
        self.file_path = os.path.join(os.path.dirname(__file__), '../data/q_table.json')
        self.load_q_table()

    def get_q_values(self, state):
        state_str = str(state)
        if state_str not in self.q_table:
            self.q_table[state_str] = {"add1": 0.0, "mul2": 0.0}
        return self.q_table[state_str]

    def choose_action(self, state, valid_actions, training=False):
        if not valid_actions:
            return None
        
        # Chiến lược Epsilon-Greedy khi huấn luyện
        if training and random.random() < self.epsilon:
            return random.choice(valid_actions)
        
        q_vals = self.get_q_values(state)
        # Chỉ lấy Q-value của những hành động hợp lệ
        valid_q = {act: q_vals[act] for act in valid_actions}
        max_q = max(valid_q.values())
        
        # Chọn ngẫu nhiên trong số các hành động có Q-value lớn nhất bằng nhau
        best_actions = [act for act, q in valid_q.items() if q == max_q]
        return random.choice(best_actions)

    def learn(self, state, action, reward, next_state, next_valid_actions):
        q_vals = self.get_q_values(state)
        next_q_vals = self.get_q_values(next_state)
        
        max_next_q = 0.0
        if next_valid_actions:
            max_next_q = max([next_q_vals[act] for act in next_valid_actions])
            
        # Công thức cập nhật Q-Value chuẩn Bellman Equation
        q_vals[action] += self.alpha * (reward + self.gamma * max_next_q - q_vals[action])

    def train_ai(self, episodes=5000):
        """Cho AI tự thực hành với chính nó để đạt tỷ lệ thắng tối đa"""
        for _ in range(episodes):
            game = NumberGame(self.target_n)
            state = game.reset()
            game_over = False
            
            history = [] # Lưu lại lịch sử các bước đi (state, action) để phạt/thưởng sau trận
            current_turn = "AI_1"
            
            while not game_over:
                valid_acts = game.get_valid_actions(state)
                if not valid_acts:
                    break
                
                action = self.choose_action(state, valid_acts, training=True)
                next_state, game_over, winner = game.step(action, current_turn)
                
                history.append((state, action, current_turn))
                state = next_state
                current_turn = "AI_2" if current_turn == "AI_1" else "AI_1"

            # Phân phối phần thưởng sau khi kết thúc trận đấu
            for s, a, p in history:
                next_valid = game.get_valid_actions(s) # Đơn giản hóa trạng thái tiếp theo
                if winner is not None:
                    reward = 100 if winner == p else -100
                else:
                    reward = 0
                self.learn(s, a, reward, s, next_valid)
                
        self.save_q_table()

    def save_q_table(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.q_table, f, indent=4)

    def load_q_table(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.q_table = json.load(f)
            except:
                self.q_table = {}