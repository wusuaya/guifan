import streamlit as st
import pandas as pd
import os

# Paths to the data files (relative paths)
csv_path = '规范条目合并_最终.csv'
images_path = '.'  # 修改此行，指向根目录
terms_path = '术语.csv'

# Load data
try:
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    terms_df = pd.read_csv(terms_path, encoding='utf-8-sig')
except FileNotFoundError as e:
    st.error(f"文件未找到: {e}")
    st.stop()

# Load terms into a dictionary
terms_dict = dict(zip(terms_df.iloc[:, 0], terms_df.iloc[:, 1]))

# Streamlit app
st.title("建筑防火通用规范+GB55037-2022")

# Step 1: Select a large item (A column) with its corresponding B column info
df['A_with_info'] = df['A'].astype(str) + ' - ' + df['B'].astype(str).str.slice(0, 20)
level1_options = df['A_with_info'].dropna().unique()
selected_level1_display = st.sidebar.selectbox('', level1_options, key='level1')
selected_level1 = selected_level1_display.split(' - ')[0] if selected_level1_display else None  # Extract only the item number

# Filter by the selected large item
df_level1 = df[df['A'] == selected_level1] if selected_level1 else pd.DataFrame()

# Step 2: Select a middle item (C column) with its corresponding D column info
if not df_level1.empty:
    df_level1['C_with_info'] = df_level1['C'].astype(str) + ' - ' + df_level1['D'].astype(str).str.slice(0, 20)
    level2_options = df_level1['C_with_info'].dropna().unique()
else:
    level2_options = []

selected_level2_display = st.sidebar.selectbox('', level2_options, key='level2')
selected_level2 = selected_level2_display.split(' - ')[0] if selected_level2_display else None  # Extract only the item number

# Filter by the selected middle item
df_level2 = df_level1[df_level1['C'] == selected_level2] if selected_level2 else pd.DataFrame()

# Step 3: Select a small item (E column) with its corresponding content
if not df_level2.empty:
    df_level2['E_with_info'] = df_level2['E'].astype(str) + ' - ' + df_level2['F'].astype(str).str.slice(0, 20)
    level3_options = df_level2['E_with_info'].dropna().unique()
else:
    level3_options = []

selected_level3_display = st.sidebar.selectbox('', level3_options, key='level3')
selected_level3 = selected_level3_display.split(' - ')[0] if selected_level3_display else None  # Extract only the item number

# Show the details of the selected small item
if selected_level3:
    # Format the header with the selected hierarchy
    level1_info = f"{selected_level1_display.split(' - ')[0]} - {selected_level1_display.split(' - ')[1]}"
    level2_info = f"{selected_level2_display.split(' - ')[0]} - {selected_level2_display.split(' - ')[1]}"
    st.header(f"{level1_info}  {level2_info}  {selected_level3}")
    
    # Find the corresponding row in the dataframe
    selected_row = df_level2[df_level2['E'] == selected_level3]
    
    # Display the 条文 and 条文解释
    if not selected_row.empty:
        article_text = selected_row.iloc[0]['F']  # 条文
        explanation_text = selected_row.iloc[0]['G']  # 条文解释
        
        # Highlight terms in the texts
        for term, explanation in terms_dict.items():
            if term in article_text:
                article_text = article_text.replace(term, f"<u>{term}</u>")
            if term in explanation_text:
                explanation_text = explanation_text.replace(term, f"<u>{term}</u>")
        
        # Display 条文 and 条文解释 with different colors
        st.markdown(f"<div style='color: black;'>{article_text}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color: blue;'>{explanation_text}</div>", unsafe_allow_html=True)
        
        # Display the image corresponding to the small item (E column)
        image_path_jpg = os.path.join(images_path, f"{selected_level3}.jpg")
        if os.path.exists(image_path_jpg):
            st.image(image_path_jpg, caption=f"表格图片 - {selected_level3}")
        else:
            st.write("未找到对应的表格图片。")
        
        # Show the terms with click-to-show functionality
        for term, explanation in terms_dict.items():
            if f"<u>{term}</u>" in article_text or f"<u>{term}</u>" in explanation_text:
                if st.button(f"查看术语: {term}"):
                    st.write(f"{term}: {explanation}")
    
    # Add watermark at the bottom right corner
    st.markdown("""
        <style>
        .watermark {
            position: fixed;
            bottom: 10px;
            right: 10px;
            font-size: 12px;
            color: grey;
            opacity: 0.5;
        }
        </style>
        <div class="watermark">MA内测版</div>
    """, unsafe_allow_html=True)

