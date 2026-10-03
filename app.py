
import streamlit as st

# =========================
# CẤU HÌNH GIAO DIỆN
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 ỨNG DỤNG TÍNH LÃI GỬI TIẾT KIỆM")
st.write(
    "Nhập thông tin khoản tiền gửi để tính tiền lãi "
    "theo kỳ hạn và hình thức nhận lãi."
)

st.divider()

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ".replace(",", ".")


# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin khoản tiền gửi")

with st.form("form_tinh_lai"):

    so_tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=1_000_000,
        value=100_000_000,
        step=1_000_000,
        format="%d"
    )

    col1, col2 = st.columns(2)

    with col1:
        ky_han = st.number_input(
            "Kỳ hạn gửi (tháng)",
            min_value=1,
            max_value=120,
            value=12,
            step=1
        )

    with col2:
        lai_suat = st.number_input(
            "Lãi suất (%/năm)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=0.1,
            format="%.2f"
        )

    hinh_thuc = st.selectbox(
        "Hình thức nhận lãi",
        [
            "Cuối kỳ",
            "Hàng tháng",
            "Hàng quý"
        ]
    )

    bam_tinh = st.form_submit_button(
        "🧮 TÍNH TIỀN LÃI",
        use_container_width=True
    )


# =========================
# TÍNH TOÁN VÀ HIỂN THỊ
# =========================
if bam_tinh:

    # Lãi suất năm đổi thành số thập phân
    lai_suat_nam = lai_suat / 100

    # Tiền lãi trong toàn bộ kỳ hạn
    # Giả định lãi đơn, không nhập lãi vào gốc
    tong_lai = (
        so_tien_gui
        * lai_suat_nam
        * ky_han / 12
    )

    # Xác định số kỳ nhận lãi
    if hinh_thuc == "Cuối kỳ":
        so_ky = 1
        ten_ky = "cuối kỳ"

    elif hinh_thuc == "Hàng tháng":
        so_ky = ky_han
        ten_ky = "mỗi tháng"

    else:
        so_ky = ky_han // 3
        phan_thang_le = ky_han % 3

        if phan_thang_le == 0:
            ten_ky = "mỗi quý"
        else:
            ten_ky = "mỗi quý, kỳ cuối điều chỉnh"

    # Tính lãi mỗi kỳ nhận
    if hinh_thuc == "Cuối kỳ":
        lai_dinh_ky = tong_lai

    elif hinh_thuc == "Hàng tháng":
        lai_dinh_ky = (
            so_tien_gui * lai_suat_nam / 12
        )

    else:
        lai_dinh_ky = (
            so_tien_gui * lai_suat_nam / 4
        )

    # Với kỳ hạn không chia hết cho 3 tháng,
    # kỳ cuối nhận phần lãi còn lại.
    if hinh_thuc == "Hàng quý" and ky_han % 3 != 0:
        lai_ky_cuoi = tong_lai - (
            lai_dinh_ky * (ky_han // 3)
        )
    else:
        lai_ky_cuoi = lai_dinh_ky

    # Tổng gốc và lãi khi đáo hạn
    tong_goc_va_lai = so_tien_gui + tong_lai

    # =========================
    # KẾT QUẢ
    # =========================
    st.divider()
    st.subheader("📊 Kết quả tính toán")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="💰 Tiền lãi định kỳ",
            value=dinh_dang_tien(lai_dinh_ky)
        )

    with col2:
        st.metric(
            label="📈 Tổng tiền lãi",
            value=dinh_dang_tien(tong_lai)
        )

    st.metric(
        label="🏦 Tổng gốc và lãi khi đáo hạn",
        value=dinh_dang_tien(tong_goc_va_lai)
    )

    # Thông tin chi tiết
    st.subheader("📝 Chi tiết khoản tiền gửi")

    st.write(f"**Số tiền gốc:** {dinh_dang_tien(so_tien_gui)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc}")
    st.write(f"**Tổng tiền lãi:** {dinh_dang_tien(tong_lai)}")
    st.write(
        f"**Tổng gốc và lãi:** "
        f"{dinh_dang_tien(tong_goc_va_lai)}"
    )

    if hinh_thuc == "Cuối kỳ":
        st.info(
            f"Bạn nhận {dinh_dang_tien(tong_lai)} tiền lãi "
            "khi khoản tiền gửi đáo hạn."
        )

    elif hinh_thuc == "Hàng tháng":
        st.info(
            f"Bạn nhận khoảng {dinh_dang_tien(lai_dinh_ky)} "
            "tiền lãi mỗi tháng. Tiền gốc được hoàn trả "
            "khi đáo hạn."
        )

    else:
        st.info(
            f"Bạn nhận khoảng {dinh_dang_tien(lai_dinh_ky)} "
            "tiền lãi mỗi quý đủ 3 tháng. "
            "Kỳ cuối có thể được điều chỉnh theo kỳ hạn thực tế. "
            "Tiền gốc được hoàn trả khi đáo hạn."
        )

    st.caption(
        "Lưu ý: Kết quả là số tiền ước tính theo phương pháp lãi đơn, "
        "giả định lãi suất cố định trong suốt kỳ hạn, "
        "không tái đầu tư tiền lãi và chưa tính thuế hoặc "
        "các điều kiện riêng của ngân hàng."
    )
