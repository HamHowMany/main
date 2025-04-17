# 파일 위치: code/macbti_test.py

import streamlit as st
import pages.test_code.macbti as macbti  # 같은 폴더에 있다면 import 가능

def main():
    st.set_page_config(page_title="맥비티아이 테스트", layout="centered")
    macbti.run()

if __name__ == "__main__":
    main()