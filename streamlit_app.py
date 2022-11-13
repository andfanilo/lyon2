import streamlit as st 

st.title("Links")

st.markdown("Enter password to access links")

user_input = st.text_input("Password :lock:")

if user_input == "":
    st.warning("Enter password :lock:")
    st.stop()

if user_input != st.secrets["password"]:
    st.warning("Wrong password :x:")
    st.stop()

st.markdown("Introduction mural: https://app.mural.co/t/lyon220229782/m/lyon220229782/1668070393435/8f87e4f02bd9933a1ce831b259c6ed579aee2a62?sender=u01edca1123f9bcac4c852828")
st.markdown("Commands mural: https://app.mural.co/t/lyon220229782/m/lyon220229782/1668357609298/9b8f62ec1e24fbfa7ee1715fe636939cb825c10d?sender=u01edca1123f9bcac4c852828")
