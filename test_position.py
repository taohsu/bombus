import streamlit as st

# 定义CSS
st.markdown("""
<style>
.back-button-wrapper {
    position: fixed !important;
    top: 200px !important;
    left: 100px !important;
    z-index: 10000 !important;
    background-color: white !important;
    padding: 10px !important;
    border: 1px solid #ddd !important;
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)

# 使用back-button-wrapper包裹按钮
st.markdown('<div class="back-button-wrapper">', unsafe_allow_html=True)
if st.button("返回", key="back_button"):
    pass
st.markdown("</div>", unsafe_allow_html=True)

st.write("下面是其它内容...")
