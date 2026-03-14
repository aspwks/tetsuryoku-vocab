import streamlit as st
import json
import os
from datetime import datetime

FILE_NAME = "vocab_history.json"

def load_data():
    """保存されたJSONデータを読み込む"""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r",encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    """データをJSONファイルに書き込んで保存する"""
    with open(FILE_NAME, "w",encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="オリジナルアキュミュレーション",page_icon=":books:")
st.title("MY表現/単語集")
st.write("知らなかった表現や単語をまとめる")

vocab_list = load_data()

st.subheader("新しい表現を収録する")
with st.form("vocab_form",clear_on_submit=True):
    co11,co12 = st.columns(2)
    with co11:
        word = st.text_input("単語・表現",placeholder="例: take ~ into account")
    with co12:
        meaning = st.text_input("意味",placeholder="例: ~を考慮に入れる")

    usage = st.text_area("使い方・例文・メモ",placeholder="例: we must take his age into account.\n(*第二回校内模試で出題された！)")

    submitted = st.form_submit_button("データベースに登録")

    if submitted:
        if word and meaning:
            new_entry = {
                "data":datetime.now().strftime("%Y-%m-%d %H:%M:"),
                "word":word,
                "meaning":meaning,
                "usage":usage
            }
            vocab_list.append(new_entry)
            save_data(vocab_list)
            st.success(f"「{word}」を登録しました！")
            st.rerun()
        else:
            st.error("「単語・表現」と「意味」は必須項目です。")

st.subheader("これまでに収録した表現")
if vocab_list:
    for item in reversed(vocab_list):
        with st.expander(f"**{item['word']}**: ({item['meaning']})"):
            st.caption(f"登録日時: {item['data']}")
            st.markdown("**使い方・例文・メモ**")
            st.write(item["usage"] if item["usage"] else "(メモなし)")
else:
    st.info("まだ表現が登録されていません。上のフォームから追加してください！")
