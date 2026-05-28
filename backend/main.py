from flask import Flask, request, jsonify
from flask_cors import CORS
from game_logic import NumberGame
from ai_agent import QLearningAI

app = Flask(__name__)
CORS(app)  # Cho phép Frontend gọi API không bị lỗi Block Origin

# Cấu hình số n mục tiêu cố định cho bài tập lớn (ví dụ n = 20, có thể chỉnh tùy ý)
TARGET_N = 6

game_instance = None
ai_agent = QLearningAI(target_n=TARGET_N)

# Tự động train AI khi khởi chạy server nếu chưa có dữ liệu học
print("Đang tối ưu hóa AI qua Training...")
ai_agent.train_ai(episodes=10000)
print("AI đã sẵn sàng với tỷ lệ thắng tối ưu!")

@app.route('/api/start', methods=['POST'])
def start_game():
    global game_instance, ai_agent
    
    # Lấy số n do giao diện frontend truyền lên
    data = request.json or {}
    target_n = int(data.get('target_n', 20)) # Nếu giao diện không truyền, mặc định là 20
    
    # Khởi tạo game và AI với số n mới
    game_instance = NumberGame(target_n)
    current_val = game_instance.reset()
    
    # Khởi tạo và tự động train AI cấp tốc cho số n này
    ai_agent = QLearningAI(target_n=target_n)
    ai_agent.train_ai(episodes=5000) 
    
    return jsonify({
        "status": "success",
        "current_value": current_val,
        "target_n": target_n,
        "game_over": False,
        "winner": None
    })

@app.route('/api/move', methods=['POST'])
def player_move():
    global game_instance
    if not game_instance:
        return jsonify({"error": "Trò chơi chưa được khởi tạo"}), 400
    
    data = request.json
    action = data.get('action') # 'add1' hoặc 'mul2'
    
    # 1. Lượt của con người đi
    current_val, game_over, winner = game_instance.step(action, "Người chơi")
    
    if game_over:
        return jsonify({
            "current_value": current_val,
            "game_over": game_over,
            "winner": winner
        })
        
    # 2. Lượt của AI phản công ngay lập tức
    valid_actions = game_instance.get_valid_actions()
    ai_action = ai_agent.choose_action(current_val, valid_actions, training=False)
    
    if ai_action:
        current_val, game_over, winner = game_instance.step(ai_action, "AI")
        
    return jsonify({
        "current_value": current_val,
        "game_over": game_over,
        "winner": winner,
        "ai_action": "Cộng 1" if ai_action == "add1" else "Nhân 2"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)