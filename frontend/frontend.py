import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000/api"

st.set_page_config(page_title="BTL AI - Trò chơi Viết Số", page_icon="🎮", layout="centered")

st.title("🎮 Trò Chơi Viết Số Thách Thức AI")
st.markdown("Luật chơi: Từ số 1, luân phiên **+1** hoặc **x2**. Ai chạm số Đích trước sẽ **Thắng**!")

# --- THÊM Ô NHẬP N NGAY TRÊN GIAO DIỆN ---
input_n = st.number_input("Chọn số Đích (N) để thách đấu:", min_value=5, max_value=100, value=20, step=1)

if "current_value" not in st.session_state:
    st.session_state.current_value = 1
if "target_n" not in st.session_state:
    st.session_state.target_n = "--"
if "game_over" not in st.session_state:
    st.session_state.game_over = True
if "log" not in st.session_state:
    st.session_state.log = "Hệ thống: Chọn số N bên trên rồi bấm nút Bắt đầu."

# Gửi số target_n lên backend khi bắt đầu game
def start_game(chosen_n):
    try:
        res = requests.post(f"{BACKEND_URL}/start", json={"target_n": chosen_n})
        if res.status_code == 200:
            data = res.json()
            st.session_state.current_value = data["current_value"]
            st.session_state.target_n = data["target_n"]
            st.session_state.game_over = False
            st.session_state.log = f"Trận đấu với N = {chosen_n} bắt đầu! Đến lượt bạn."
    except requests.exceptions.ConnectionError:
        st.error("Lỗi: Không thể kết nối tới Backend Flask.")

def make_move(action):
    try:
        res = requests.post(f"{BACKEND_URL}/move", json={"action": action})
        if res.status_code == 200:
            data = res.json()
            st.session_state.current_value = data["current_value"]
            if data["game_over"]:
                st.session_state.game_over = True
                if data["winner"] == "Người chơi":
                    st.session_state.log = "🎉 Chúc mừng! Bạn đã chiến thắng AI!"
                else:
                    st.session_state.log = "🤖 AI thắng cuộc! Bạn cần tính toán kỹ hơn rồi."
            else:
                st.session_state.log = f"🤖 AI vừa chọn [ {data['ai_action']} ]. Đến lượt bạn!"
    except requests.exceptions.ConnectionError:
        st.error("Mất kết nối với Backend!")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="SỐ HIỆN TẠI", value=st.session_state.current_value)
with col2:
    st.metric(label="SỐ ĐÍCH (N)", value=st.session_state.target_n)

st.info(st.session_state.log)

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    btn_add = st.button("Cộng 1 (+1)", use_container_width=True, disabled=st.session_state.game_over)
    if btn_add:
        make_move("add1")
        st.rerun()

with col_btn2:
    btn_mul = st.button("Nhân 2 (x2)", use_container_width=True, disabled=st.session_state.game_over)
    if btn_mul:
        make_move("mul2")
        st.rerun()

st.markdown("---")
# Truyền giá trị từ ô nhập input_n vào hàm start_game
if st.button("Bắt Đầu Trò Chơi Mới", type="primary", use_container_width=True):
    start_game(input_n)
    st.rerun()