import streamlit as st
import pandas as pd
import os

# Paths to the data files
csv_path = 'D:/规范/规范条目合并_最终.csv'
images_path = 'D:/规范/表格图片'
terms_path = 'D:/规范/术语.csv'

# Load data
df = pd.read_csv(csv_path, encoding='utf-8-sig')
terms_df = pd.read_csv(terms_path, encoding='utf-8-sig')

# Load terms into a dictionary
terms_dict = dict(zip(terms_df.iloc[:, 0], terms_df.iloc[:, 1]))

# Streamlit app
st.title("建筑防火通用规范+GB55037-2022")

# Helper function to shorten long text
def shorten_text(text, max_length=30):
    return text if len(text) <= max_length else text[:max_length] + '...'

# Step 1: Select a large item (A column)
# Combine A and B columns for display in the dropdown
level1_options = df['A'].dropna().unique()
level1_display = [f"{opt} - {shorten_text(df[df['A'] == opt]['B'].iloc[0])}" for opt in level1_options]
selected_level1_display = st.sidebar.selectbox('', ['请选择'] + level1_display)

# Proceed only if a valid large item is selected
if selected_level1_display != '请选择':
    # Extract the selected large item (only use the numeric part of A for filtering)
    selected_level1 = selected_level1_display.split(' - ')[0].strip()  # Extract only the numeric part from A
    selected_level1_text = selected_level1_display.split(' - ')[1].strip()  # Extract the text part from A

    # Filter by the selected large item
    df_level1 = df[df['A'].astype(str).str.strip() == selected_level1]

    # Step 2: Select a middle item (C column)
    # Check if the C column exists in the filtered data and if it's not empty
    if 'C' in df.columns and not df_level1['C'].dropna().empty:
        # Combine C and D columns for display in the dropdown
        level2_options = df_level1['C'].dropna().unique()
        level2_display = [f"{opt} - {shorten_text(df_level1[df_level1['C'] == opt]['D'].iloc[0])}" for opt in level2_options]
        selected_level2_display = st.sidebar.selectbox('', ['请选择'] + level2_display)

        # Proceed only if a valid middle item is selected
        if selected_level2_display != '请选择':
            # Extract the selected middle item
            selected_level2 = selected_level2_display.split(' - ')[0].strip()  # Extract only the numeric part from C
            selected_level2_text = selected_level2_display.split(' - ')[1].strip()  # Extract the text part from C

            # Filter by the selected middle item
            df_level2 = df_level1[df_level1['C'].astype(str).str.strip() == selected_level2]

            # Step 3: Select a small item (E column)
            # Check if the E column exists in the filtered data and if it's not empty
            if 'E' in df.columns and not df_level2['E'].dropna().empty:
                # Combine E and F columns for display in the dropdown
                level3_options = df_level2['E'].dropna().unique()
                level3_display = [f"{opt} - {shorten_text(df_level2[df_level2['E'] == opt]['F'].iloc[0])}" for opt in level3_options]
                selected_level3_display = st.sidebar.selectbox('', ['请选择'] + level3_display)

                # Show the details of the selected small item
                if selected_level3_display != '请选择':
                    # Extract the selected small item
                    selected_level3 = selected_level3_display.split(' - ')[0].strip()  # Extract only the numeric part from E

                    # Construct the header using the selected items
                    st.header(f"{selected_level1} - {selected_level1_text}  {selected_level2} - {selected_level2_text}  {selected_level3}")
                    
                    # Find the corresponding row in the dataframe
                    selected_row = df_level2[df_level2['E'].astype(str).str.strip() == selected_level3]
                    
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
                        
                        # Display the image corresponding to the small item (E column) as a link
                        image_path_png = os.path.join(images_path, f"{selected_level3}.png")
                        image_path_jpg = os.path.join(images_path, f"{selected_level3}.jpg")
                        image_path = None
                        if os.path.exists(image_path_png):
                            image_path = image_path_png
                        elif os.path.exists(image_path_jpg):
                            image_path = image_path_jpg

                        if image_path:
                            st.markdown(f"[查看表格图片 - {selected_level3}]({image_path})", unsafe_allow_html=True)
                            st.image(image_path, caption=f"表格图片 - {selected_level3}")
                        
                        # Show the terms with click-to-show functionality
                        for term, explanation in terms_dict.items():
                            if f"<u>{term}</u>" in article_text or f"<u>{term}</u>" in explanation_text:
                                if st.button(f"查看术语: {term}"):
                                    st.write(f"{term}: {explanation}")

# Watermark
st.markdown(
    "<div style='position: fixed; bottom: 10px; right: 10px; font-size: 12px; color: grey;'>MA内测版</div>",
    unsafe_allow_html=True
)



