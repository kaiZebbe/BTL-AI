from flask import Flask, request, jsonify
from flask_cors import CORS
from game_logic import NumberGame

# MinimaxAI
from ai_agent import MinimaxAI 

app = Flask(__name__)
CORS(app)  

game_instance = None
ai_agent = None

@app.route('/api/start', methods=['POST'])
def start_game():
    global game_instance, ai_agent
    
    data = request.json or {}
    target_n = int(data.get('target_n', 20)) 
    
    game_instance = NumberGame(target_n)
    current_val = game_instance.reset()
    
    # KHỞI TẠO MINIMAX VÀ KHÔNG CẦN TRAIN NỮA (Chạy cực kỳ nhanh)
    ai_agent = MinimaxAI(target_n=target_n)
    print(f"Game mới đã tạo (N={target_n}). Thuật toán Minimax sẵn sàng!")
    
    return jsonify({
        "status": "success",
        "current_value": current_val,
        "target_n": target_n,
        "game_over": False,
        "winner": None
    })

@app.route('/api/move', methods=['POST'])
def player_move():
    global game_instance, ai_agent
    if not game_instance:
        return jsonify({"error": "Trò chơi chưa được khởi tạo"}), 400
    
    data = request.json
    action = data.get('action') 
    
    current_val, game_over, winner = game_instance.step(action, "Người chơi")
    
    if game_over:
        return jsonify({
            "current_value": current_val,
            "game_over": game_over,
            "winner": winner
        })
        
    valid_actions = game_instance.get_valid_actions()
    
    # AI dùng thuật toán duyệt cây Minimax phản công
    ai_action = ai_agent.choose_action(current_val, valid_actions)
    
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