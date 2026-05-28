class NumberGame:
    def __init__(self, target_n):
        self.target_n = target_n
        self.current_value = 1
        self.game_over = False
        self.winner = None

    def reset(self):
        self.current_value = 1
        self.game_over = False
        self.winner = None
        return self.current_value

    def get_valid_actions(self, value=None):
        if value is None:
            value = self.current_value
        actions = []
        if value + 1 <= self.target_n:
            actions.append('add1')
        if value * 2 <= self.target_n:
            actions.append('mul2')
        return actions

    def step(self, action, player_name):
        if self.game_over:
            return self.current_value, self.game_over, self.winner

        if action == 'add1' and (self.current_value + 1 <= self.target_n):
            self.current_value += 1
        elif action == 'mul2' and (self.current_value * 2 <= self.target_n):
            self.current_value *= 2
        else:
            # Hành động không hợp lệ (vượt quá n) -> Xử thua người đi lỗi
            self.game_over = True
            self.winner = "Opponent"
            return self.current_value, self.game_over, self.winner

        if self.current_value == self.target_n:
            self.game_over = True
            self.winner = player_name

        return self.current_value, self.game_over, self.winner