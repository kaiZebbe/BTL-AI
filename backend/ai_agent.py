import random

class MinimaxAI:
    def __init__(self, target_n):
        self.target_n = target_n
        self.memo = {}  # Bộ nhớ đệm (Quy hoạch động) giúp AI tính không bị lag

    def is_winning_state(self, current_val):
        """
        Hàm đệ quy duyệt cây Minimax: Kiểm tra xem con số hiện tại có phải là THẾ THẮNG hay không.
        Nguyên lý: Nếu tôi có thể đẩy đối thủ vào một con số mà từ đó đối thủ CHẮC CHẮN THUA, 
                   thì con số hiện tại của tôi là THẾ THẮNG.
        """
        # Nếu đã tính toán con số này rồi thì lấy luôn kết quả cho nhanh
        if current_val in self.memo:
            return self.memo[current_val]
        
        # Nếu đã lố hoặc chạm đích (tức là đối thủ vừa đi bước quyết định), mình thua
        if current_val >= self.target_n:
            return False 

        valid_moves = []
        if current_val + 1 <= self.target_n:
            valid_moves.append(current_val + 1)
        if current_val * 2 <= self.target_n:
            valid_moves.append(current_val * 2)

        # Duyệt qua các nước đi khả thi
        for next_val in valid_moves:
            # Nếu nước đi tiếp theo là THẾ THUA của đối thủ -> Mình đã tìm ra đường thắng!
            if not self.is_winning_state(next_val):
                self.memo[current_val] = True
                return True
                
        # Nếu thử mọi cách mà đối thủ vẫn có đường thắng -> Mình đành chịu thua
        self.memo[current_val] = False
        return False

    def choose_action(self, state, valid_actions, training=False):
        """AI chọn nước đi tối ưu nhất"""
        if not valid_actions: 
            return None
            
        # 1. Tìm nước đi Sát thủ: Đẩy đối thủ vào thế thua
        for action in valid_actions:
            next_val = state + 1 if action == 'add1' else state * 2
            
            # Nếu nước đi này khiến đối thủ rơi vào is_winning_state = False -> Chọn ngay!
            if not self.is_winning_state(next_val):
                return action 
                
        # 2. Nếu đang ở thế bí (đi nước nào đối thủ cũng thắng), 
        #    AI đành chọn ngẫu nhiên để kéo dài thời gian chờ đối thủ sai lầm.
        return random.choice(valid_actions)