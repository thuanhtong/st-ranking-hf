import streamlit as st

def default_window():
    st.set_page_config(
        page_title="Ranking Đoạn Text",
        layout="wide",  # Sử dụng layout rộng
    )
    st.title("Ranking Đoạn Text")

def save_data(question, sentences, order, scores):
    with open("ranking_data.txt", "a", encoding="utf-8") as file:
        file.write("\n--- New Submission ---\n")
        file.write(question + "\n")
        for i, sentence_index in enumerate(order):
            file.write(f"Câu {i+1}: {sentences[sentence_index-1]} - Điểm: {scores[sentences[sentence_index-1]]}\n")

def ranking_review(question, sentences, max_occurrences = 2):
    global placeholder
    with placeholder.container():
        st.write(f"Câu hỏi: {question}")

        # Biến để lưu trữ thứ tự và điểm số
        order = list(range(1, len(sentences) + 1))
        scores = {sentence: 3 for sentence in sentences} 

        score_counts = {i: 0 for i in range(1, len(sentences) + 1)}
        duplicate_score = set()

        # Tạo hai cột để chia cửa sổ
        col1, col2, col3 = st.columns([2.5, 0.5, 2.5])

        print(question, sentences, order, scores)

        # Biến cờ để theo dõi trạng thái cảnh báo
        has_warning = False

        # Cột bên trái để đánh giá điểm
        with col1:
            st.subheader("Đánh giá Điểm")

            for i, sentence in enumerate(sentences):
                score = st.slider(f"Điểm cho **{sentence}**", 0, len(sentences), 3)
                
                if score != 0:
                # Kiểm tra nếu có điểm giống nhau
                    if score_counts[score] >= max_occurrences:
                        duplicate_score.add(score)
                        has_warning = True

                    score_counts[score] += 1
                scores[sentence] = score

            # Hiển thị cảnh báo nếu có điểm giống nhau
            if has_warning:
                st.warning(f"Các câu có cùng điểm {duplicate_score} đã vượt quá {max_occurrences} lần xuất hiện. Số lần xuất hiện của từng điểm là {score_counts}.")

                # Nếu có cảnh báo, đặt lại thứ tự và scores để hiển thị đúng kết quả
                order = sorted(order, key=lambda x: scores[sentences[x-1]], reverse=True)

        # Cột bên phải để hiển thị thứ tự theo điểm của người dùng
        with col3:
            st.subheader("Thứ Tự theo Điểm")
            ranked_sentences = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

            st.write("Xếp hạng câu:")
            for i, sentence in enumerate(ranked_sentences):
                st.write(f"{i+1}. {sentence} - Điểm: {scores[sentence]}")
        
            # Nút Submit (Chỉ hiện ra khi không có cảnh báo)
            if not has_warning:
                if st.button("Submit"):
                    # Lưu dữ liệu vào file txt
                    save_data(question, sentences, order, scores)
                    placeholder.empty()
                    ranking_review("Câu nào hay hơn?", choose_data(choose_id()))

def choose_id():
    # ... (Thực hiện chọn data id chưa được ranking) 
    st.session_state.id += 1
    return st.session_state.id

# @st.cache_data
def load_data():
    input1 = ["Câu 1", "Câu 2", "Câu 3", "Câu 4", "Câu 5"]
    input2 = ["Câu 6", "Câu 7", "Câu 9", "Câu 10", "Câu 8", "Câu 11"]
    return input1, input2

# Chọn input data dựa trên id
def choose_data(id):
    input1, input2 = load_data()

    print("choose_input i: ", id)
    
    if id % 2 == 0:
        return input1
    else:
        return input2


if "id" not in st.session_state:
    st.session_state.id = 0
    choose_id()

default_window()
placeholder = st.empty()
ranking_review("Câu nào hay hơn?", choose_data(st.session_state.id))
