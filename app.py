import streamlit as st
from helper import make_stopwords, authenticate, get_user_tweeets, make_wordcloud

st.title(" ☁ Head in the Tweets ☁️ ") 
st.subheader("Create a wordcloud out of your last 200 tweets!")
st.text_input("Enter a twitter username to begin", key="name")

if "last_name" not in st.session_state:
    st.session_state.last_name = ""

if st.session_state.last_name != st.session_state.name:    

    if "all_stopwords" not in st.session_state:
        st.session_state.all_stopwords = make_stopwords()
    if "api" not in st.session_state:    
        st.session_state.api = authenticate()
    try:
        outtweets = get_user_tweeets(st.session_state.name,st.session_state.api)
        try:
            cat = outtweets[9]   
            st.spinner()
            with st.spinner(text='We\'re building the wordcloud. Give it a sec...'):
                figure = make_wordcloud(st.session_state.all_stopwords, outtweets)
                st.pyplot(figure)
                st.balloons()
        except:
            st.markdown("This account has less than 10 tweets. Tweet more and come back later or try again.")  
    except:
        st.markdown("This account doesn't exist. Please try again.")        

