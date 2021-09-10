import streamlit as st
import matplotlib.pyplot as plt 
import tweepy, re
from wordcloud import WordCloud

st.title(" ☁ Head in the Tweets ☁️ ") 
st.subheader("This website creates a wordcloud out of the last 200 tweets of a user.")
st.text_input("Enter a twitter username to begin", key="name")
screen_name = st.session_state.name

if screen_name != "":
    if 'all_stopwords' not in st.session_state:
        text_file = open("all_stopwords.txt", "r")
        stopwords_list = text_file.read().split("\n")
        st.session_state.all_stopwords = set(stopwords_list)
        text_file.close()
    
    auth = tweepy.OAuthHandler(st.secrets["consumer_key"], st.secrets["consumer_secret"])
    auth.set_access_token(st.secrets["access_token_key"], st.secrets["access_token_secret"])

    api = tweepy.API(auth)

    alltweets = []  
    try:
        new_tweets = api.user_timeline(screen_name = screen_name,count=200)
        alltweets.extend(new_tweets)
        outtweets = [tweet.text for tweet in alltweets]
        try: 
            cat = outtweets[9]   
            st.spinner()
            with st.spinner(text='We\'re building the wordcloud. Give it a sec...'):
                text = " ".join(outtweets)
                text = re.sub(pattern=r"http\S+",repl="",string=text.lower())
                text = re.sub(pattern=r"@\S+",repl="",string=text)

                wordcloud = WordCloud(width=1800, height=1200,stopwords=st.session_state.all_stopwords,
                                    max_font_size=250, max_words=100, background_color="white",
                                    colormap='cool', collocations=True).generate(text)  

                fig = plt.figure(figsize=(18,12))
                plt.imshow(wordcloud, interpolation="bilinear")
                plt.axis("off")
                st.pyplot(fig)
                st.balloons()
        except:
            st.markdown("This account has less than 10 tweets. Tweet more and come back later or try again.")  
    except:
        st.markdown("This account doesn't exist. Please try again.")        

