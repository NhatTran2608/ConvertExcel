import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Pivot Sheet1 → Sheet2", layout="wide")
st.title("🔄 Chuyển Sheet1 (long) sang Sheet2 (wide)")


uploaded_file = st.file_uploader(
    "📂 Tải lên file Excel có Sheet1 (refYear, partnerDesc, cmdCode, fobvalue)", 
    type=["xlsx", "xls"]
)

if uploaded_file:
    try:
       
        df_long = pd.read_excel(uploaded_file, sheet_name=0)
        st.subheader("📄 Dữ liệu gốc (Sheet1)")
        st.dataframe(df_long)

        
        required = {"refYear", "partnerDesc", "cmdCode", "fobvalue"}
        if not required.issubset(df_long.columns):
            st.error(f"❌ Sheet1 phải chứa cột: {required}")
        else:
        
            df_wide = (
                df_long
                .pivot_table(
                    index=["partnerDesc", "refYear"],
                    columns="cmdCode",
                    values="fobvalue",
                    aggfunc="sum"          
                )
                .reset_index()
            )

    
            df_wide = df_wide.rename(columns={
                "partnerDesc": "Country",
                "refYear":    "Year"
            })

            df_wide = df_wide.sort_values(by=["Country", "Year"])

            st.subheader("✅ Kết quả (Sheet2)")
            st.dataframe(df_wide)

            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df_long.to_excel(writer, sheet_name="Sheet1", index=False)
                df_wide.to_excel(writer, sheet_name="Sheet2", index=False)
            output.seek(0)

            st.download_button(
                label="📥 Tải về file kết quả (Sheet1 + Sheet2)",
                data=output,
                file_name="converted_pivot.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"❌ Lỗi khi xử lý: {e}")
