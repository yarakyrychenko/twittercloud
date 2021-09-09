import streamlit as st
import matplotlib.pyplot as plt 
import tweepy, re
from wordcloud import WordCloud, STOPWORDS

st.header(" ☁ Head in the Tweets ☁️ ") 
st.text("This website creates a wordcloud out of the last 200 tweets of a user.")
st.text_input("Enter a twitter username to begin", key="name")
screen_name = st.session_state.name

st.echo()
with st.echo():
    st.write('Code will be executed and printed')
    
auth = tweepy.OAuthHandler(st.secrets["consumer_key"], st.secrets["consumer_secret"])
auth.set_access_token(st.secrets["access_token_key"], st.secrets["access_token_secret"])

api = tweepy.API(auth)

alltweets = []  
try:
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    outtweets = [tweet.text for tweet in alltweets]
    try: 
        cat = outtweets[1]   
        st.spinner()
        with st.spinner(text='We\'re building the wordcloud. Give it a sec...'):
            text = " ".join(outtweets)
            text = re.sub(pattern=r"http\S+",repl="",string=text.lower())
            text = re.sub(pattern=r"@\S+",repl="",string=text)
            stopwords = set(STOPWORDS)
            stopwords.update(["rt"])
            wordcloud = WordCloud(width=1800, height=1200,stopwords=st.session_state.stopwords, max_font_size=250, max_words=200, background_color="white").generate(text)  
            fig = plt.figure(figsize=(18,12),facecolor='k')
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.tight_layout(pad=0)
            st.pyplot(fig)
            st.balloons()
    except:
        st.text("This account has no tweets. Please try again.")  
except:
    st.text("This account doesn't exist. Please try again.")        

