import json
import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# Cấu hình trang
st.set_page_config(page_title="Trợ lý Soạn Bài Hoạt động Trải nghiệm", page_icon="📚")

## --- GIAO DIỆN NHẬP LIỆU ---
st.title("🚀 Công cụ Hỗ trợ Soạn bài HĐTN & HN")
st.info("Nhập thông tin bên dưới để tạo Prompt tối ưu cho AI.")

col1, col2 = st.columns(2)

with col1:
    bo_sach = st.selectbox("Lựa chọn bộ sách 📚", 
                           ["Kết nối tri thức với cuộc sống", "Cánh diều", "Chân trời sáng tạo (Bản 1)", "Chân trời sáng tạo (Bản 2)"])
    lop = st.selectbox("Lựa chọn lớp 🎓", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"])

with col2:
    chu_de = st.text_input("Chủ đề 📂", placeholder="VD: Tự tạo động lực và ứng phó với áp lực...")
    noi_dung = st.text_area("Nội dung bài dạy 📝", placeholder="VD: Nhiệm vụ 1: Tìm hiểu những thay đổi...")

chu_de_required = bool(chu_de.strip())
noi_dung_required = bool(noi_dung.strip())
if not chu_de_required:
    st.warning("Vui long nhap ten chu de de tiep tuc.")
if not noi_dung_required:
    st.warning("Vui long nhap noi dung bai day de tiep tuc.")

yeu_cau_list = ["Thiết kế bài dạy", "Thiết kế trò chơi khởi động", "Gợi ý các tình huống thảo luận nhóm", "Yêu cầu khác"]
yeu_cau_chinh = st.selectbox("Yêu cầu thực hiện 🎯", yeu_cau_list)

# Nếu chọn "Yêu cầu khác", hiện khung nhập văn bản
yeu_cau_cu_the = ""
if yeu_cau_chinh == "Yêu cầu khác":
    yeu_cau_cu_the = st.text_input("Nhập yêu cầu cụ thể của bạn:")
else:
    yeu_cau_cu_the = yeu_cau_chinh

thoi_gian = st.radio("Thời gian thực hiện ⏱️", ["1 tiết (45 phút)", "2 tiết (90 phút)", "3 tiết (135 phút)"], horizontal=True)
bo_sung = st.text_area("Yêu cầu bổ sung 💡", placeholder="VD: Sử dụng phương pháp đóng vai, lồng ghép trò chơi dân gian...")

st.markdown("---")

## --- XỬ LÝ LOGIC GHÉP PROMPT ---

# Vai trò mặc định
role = "Bạn là một chuyên gia thiết kế hoạt động trải nghiệm và hướng nghiệp có nhiều kinh nghiệm. "

# Bối cảnh bài dạy
context = f"Tôi đang soạn bài dạy cho học sinh {lop}, chủ đề '{chu_de}', nội dung bài dạy '{noi_dung}'. "
context += f"Giúp tôi {yeu_cau_cu_the} môn hoạt động trải nghiệm và hướng nghiệp nhằm đạt được mục tiêu của chương trình giáo dục phổ thông 2018 và phù hợp với tiến trình dạy học của bộ sách {bo_sach}. "
context += f"Thời gian thực hiện dự kiến là {thoi_gian}. "

# Logic riêng cho "Thiết kế bài dạy"
if yeu_cau_chinh == "Thiết kế bài dạy":
    structure = """
Trình bày theo cấu trúc gồm Mục tiêu, Chuẩn bị, Tiến trình hoạt động như sau:
1/ Mục tiêu:
- Kiến thức:
- KN:
- Thái độ:
- Phát triển NL:
2/ Nội dung:
- Nội dung 1: Tên HĐ 1.
- Nội dung 2: Tên HĐ 2.
- Nội dung 3: Tên HĐ 3...
3/ Chuẩn bị: Dự kiến phương pháp, phương tiện, hình thức trải nghiệm, sản phẩm.
4/ Tổ chức HĐ: (Trình bày chi tiết từng HĐ gồm Mục tiêu và Cách tiến hành).
"""
    context += structure

# Tiêu chí và yêu cầu bổ sung
criteria = f"\nTiêu chí: Yêu cầu sáng tạo, ít tốn chi phí đạo cụ, phù hợp với sĩ số 40 học sinh và thực hiện tại không gian lớp học. "
if bo_sung:
    criteria += f"\nLưu ý bổ sung: {bo_sung}"

full_prompt = role + context + criteria

## --- HIỂN THỊ VÀ GỬI DỮ LIỆU ---

if "show_prompt" not in st.session_state:
    st.session_state.show_prompt = False

inputs_ready = chu_de_required and noi_dung_required

if st.button("🧩 Tạo prompt", use_container_width=True, disabled=not inputs_ready):
    st.session_state.show_prompt = True

if st.session_state.show_prompt:
    st.subheader("📄 Prompt đã tạo")
    st.code(full_prompt, language="text")

# Tạo Link chuyển tiếp
# Lưu ý: Với ChatGPT, chúng ta truyền qua URL query 'q'. 
# Với Gemini, hiện tại link trực tiếp nội dung phức tạp qua URL có thể bị giới hạn, 
# nhưng ta sẽ dùng phương pháp encode URL cơ bản.

encoded_prompt = urllib.parse.quote(full_prompt)
prompt_json = json.dumps(full_prompt)

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    chatgpt_url = f"https://chatgpt.com/?q={encoded_prompt}"
    st.link_button("🚀 Gửi sang ChatGPT", chatgpt_url, type="primary", use_container_width=True, disabled=not inputs_ready)

with col_btn2:
    # Copy prompt button for easy pasting into any AI app
    components.html(
        f"""
        <div style="width: 100%;">
            <button id="copy-btn" {'disabled="disabled"' if not inputs_ready else ''} style="width: 100%; padding: 0.5rem 0.75rem; border-radius: 0.5rem; border: 1px solid #d0d0d0; background: #ffffff; cursor: pointer;">
                📋 Copy Prompt
            </button>
            <div id="copy-status" style="margin-top: 0.4rem; font-size: 0.85rem; color: #2e7d32; display: none;">
                Da sao chep Prompt.
            </div>
            <div id="copy-hint" style="margin-top: 0.4rem; font-size: 0.85rem; color: #a65c00; {'display: none;' if inputs_ready else ''}">
                Vui long nhap chu de va noi dung bai day de mo khoa nut sao chep.
            </div>
        </div>
        <script>
            const btn = document.getElementById("copy-btn");
            const status = document.getElementById("copy-status");
            const text = {prompt_json};
            btn.addEventListener("click", async () => {{
                if (btn.hasAttribute("disabled")) return;
                try {{
                    await navigator.clipboard.writeText(text);
                    status.style.display = "block";
                    setTimeout(() => {{ status.style.display = "none"; }}, 2000);
                }} catch (e) {{
                    alert("Khong the copy tu dong. Hay chon va copy o khung Prompt.");
                }}
            }});
        </script>
        """,
        height=90,
    )

st.success(" Bam nut Copy Prompt de dan sang ung dung AI khac.")