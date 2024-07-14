import streamlit as st

def custom_css():
    st.markdown("""
        <style>
            @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

            .main-title {
                font-size: 3em;
                text-align: center;
                color: #ffffff;
                background-color: #333333;
                padding: 0.5em;
                border-radius: 10px;
                margin-top: 20px; /* 타이틀과 다른 요소 간의 공간 확보 */
            }
            .input-container {
                text-align: center;
                margin-top: 2em;
                padding: 2em;
                background-color: #ffffff;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .input-container input {
                font-size: 1.2em;
                width: 80%;
                padding: 0.5em;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-bottom: 1em;
            }
            .input-container button {
                font-size: 1.2em;
                background-color: #333333;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 0.5em 2em;
                cursor: pointer;
            }
            .input-container button:hover {
                background-color: #555555;
            }
            .post-container {
                background-color: #ffffff;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                padding: 1em;
                margin-top: 2em;
            }
            .header-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .sort-refresh-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 10px;
            }
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: #333333;
                color: white;
                text-align: center;
                padding: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: nowrap;
            }
            .footer-content {
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: 100%;
                padding: 0 10px;
            }
            .footer-content p {
                margin: 0;
                white-space: nowrap;
            }
            .language-select {
                display: flex;
                justify-content: flex-end;
                align-items: center;
                margin-left: auto;
            }
            .language-select label {
                margin-right: 10px;
            }
            .language-select select {
                padding: 5px;
                border-radius: 5px;
                border: none;
                font-size: 16px;
                background-color: #ffffff;
                color: #333333;
            }
        </style>
    """, unsafe_allow_html=True)
