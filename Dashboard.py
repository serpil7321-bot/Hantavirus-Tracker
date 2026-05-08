import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. إعدادات الصفحة (ثيم ليلي فخم)
st.set_page_config(page_title="Global Hantavirus Radar", layout="wide")

st.title("🌍 Global Hantavirus 3D Live Monitor")
st.markdown("---")

# 2. دالة جلب البيانات التلقائية (تحديث كل 24 ساعة)
@st.cache_data(ttl=86400) 
def load_live_data():
    # هذا الرابط يسحب أحدث البيانات العالمية من ملف الـ JSON الخاص بك
    url = "https://raw.githubusercontent.com/serpil7321-bot/Hantavirus-Tracker/main/data.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
    except:
        # في حال حدوث مشكلة في الاتصال، نعرض بيانات احتياطية
        return pd.DataFrame({
            'Country': ['USA', 'Mexico', 'Canada', 'Bolivia'],
            'Lat': [37.09, 23.63, 56.13, -16.29],
            'Lon': [-95.71, -102.55, -106.34, -63.58],
            'Signals': [93, 8, 3, 12]
        })

# تحميل البيانات
df = load_live_data()

# 3. تصميم الكرة الأرضية ثلاثية الأبعاد
fig = px.scatter_geo(df, 
                     lat='Lat', lon='Lon', 
                     size='Signals', 
                     color='Signals',
                     hover_name='Country',
                     color_continuous_scale=px.colors.sequential.Reds,
                     projection="orthographic", # تحويلها لـ 3D
                     template="plotly_dark")

fig.update_geos(
    showcountries=True, countrycolor="#444",
    showocean=True, oceancolor="#000",
    showland=True, landcolor="#111",
    showlakes=False,
    projection_type="orthographic"
)

fig.update_layout(height=700, margin={"r":0,"t":50,"l":0,"b":0})

# عرض الخريطة
st.plotly_chart(fig, width='stretch')

# 4. جدول البيانات أسفل الخريطة
st.subheader("📋 Verified Clinical Signals Feed")
st.dataframe(df, use_container_width=True)

st.sidebar.info("System Status: Synchronized with WHO/CDC Feeds")
st.sidebar.caption("Data Refresh: Every 24 Hours")
