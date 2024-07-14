import os
import pickle
import requests
import streamlit as st

def load_posts(pickle_file):
    """Pickle 파일에서 게시물을 불러오는 함수"""
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as f:
            return pickle.load(f)
    return []

def save_posts(posts, pickle_file):
    """게시물을 Pickle 파일에 저장하는 함수"""
    with open(pickle_file, 'wb') as f:
        pickle.dump(posts, f)

def display_posts(posts, sort_by, lang, translations):
    """게시물을 화면에 표시하는 함수"""
    if sort_by == translations[lang]['sort_by_likes']:
        posts = sorted(posts, key=lambda x: x['likes'], reverse=True)
    elif sort_by == translations[lang]['sort_by_recent']:
        posts = sorted(posts, key=lambda x: x['timestamp'], reverse=True)

    for i, post in enumerate(posts):
        st.markdown(f"""
        <div style="border: 1px solid #d3d3d3; padding: 10px; border-radius: 10px; margin-bottom: 10px; background-color: #f9f9f9;">
            <p><strong>Input:</strong> {post['input']}</p>
            <p><strong>Output:</strong> {post['output']}</p>
            <p style="color: #888888; font-size: 12px;">{post['timestamp']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"👍 {translations[lang]['likes']}: {post['likes']}", key=f'like-{i}'):
            post['likes'] += 1
            save_posts(posts, 'posts.pkl')
            st.experimental_rerun()

def get_user_country():
    """사용자의 IP를 기반으로 국가 정보를 반환하는 함수"""
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        return data.get('country', 'US')
    except Exception as e:
        print(e)
        return 'US'  # 기본값으로 미국을 반환
