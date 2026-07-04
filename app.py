import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


st.title("Sentiment analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment analysis of Tweets about US Airlines")

st.markdown("This application is a Streamlit dashboard to analyze the sentiment of Tweets🐦")
st.sidebar.markdown("This application is a Streamlit dashboard to analyze the sentiment of Tweets🐦")

PATH = "Tweets.csv"

@st.cache(persist=True)
def load_data(path):
    data = pd.read_csv(path)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

def get_export_column(source, names, default):
    for name in names:
        if name in source.columns:
            return source[name].fillna(default)
    return pd.Series([default] * len(source), index=source.index)

def load_xquik_export(uploaded_file):
    source = pd.read_csv(uploaded_file)
    data = pd.DataFrame()
    data['airline_sentiment'] = get_export_column(source, ['airline_sentiment', 'sentiment'], 'neutral').astype(str).str.lower()
    data['airline_sentiment_confidence'] = get_export_column(source, ['airline_sentiment_confidence', 'sentiment_confidence'], 1)
    data['negativereason'] = get_export_column(source, ['negativereason', 'negative_reason'], '')
    data['negativereason_confidence'] = get_export_column(source, ['negativereason_confidence', 'negative_reason_confidence'], '')
    data['airline'] = get_export_column(source, ['airline', 'brand', 'query'], 'Xquik export')
    data['name'] = get_export_column(source, ['name', 'username', 'screen_name', 'user'], '')
    data['retweet_count'] = get_export_column(source, ['retweet_count', 'retweets', 'nretweets'], 0)
    data['text'] = get_export_column(source, ['text', 'tweet', 'full_text', 'content'], '')
    data['tweet_created'] = pd.to_datetime(get_export_column(source, ['tweet_created', 'created_at', 'date', 'timestamp'], ''), errors='coerce')
    data['latitude'] = pd.to_numeric(get_export_column(source, ['latitude', 'lat'], np.nan), errors='coerce')
    data['longitude'] = pd.to_numeric(get_export_column(source, ['longitude', 'lon', 'lng'], np.nan), errors='coerce')
    data['tweet_id'] = get_export_column(source, ['tweet_id', 'id', 'id_str'], '')
    data = data.dropna(subset=['tweet_created'])
    return data

uploaded_file = st.sidebar.file_uploader("Upload Xquik CSV export", type=["csv"])
data = load_xquik_export(uploaded_file) if uploaded_file is not None else load_data(PATH)

#st.write(data)
st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio('Sentiment',('positive', 'neutral', 'negative'))
random_tweet_data = data.query('airline_sentiment == @random_tweet')[['text']]
if random_tweet_data.empty:
    st.sidebar.info("No tweets available for this sentiment.")
else:
    st.sidebar.markdown(random_tweet_data.sample(n=1).iat[0,0])

st.sidebar.markdown('### Number of tweets by sentiment')
select = st.sidebar.selectbox('Visualization type', ['Histogram', 'Pie chart'], key='1')
sentiment_count = data['airline_sentiment'].value_counts()
#st.write(sentiment_count)
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})

if st.sidebar.checkbox("Hide", True):
    st.markdown("### Number of tweets by sentiment")
    if select == "Histogram":
        fig = px.bar(sentiment_count,x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

#st.map(data)

st.sidebar.subheader("When and where are users tweeting ?")
hour = st.sidebar.slider("Hour of the day", 0 ,23)#alternatively:hour = st.sidebar.number_input("Hour of the day", min_value=1 ,max_value=24)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Close", True, key='1'):
    st.markdown("##Tweets locations based on the time of day")
    st.markdown("%i tweets %i:00 and %i:00" %(len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data",False):
        st.write(modified_data)

st.sidebar.subheader("Breakdown Airline tweets by sentiment")
choice = st.sidebar.multiselect('Pick airlines', ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America', 'Xquik export'),key='0')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment',histfunc='count', color='airline_sentiment',
    facet_col='airline_sentiment', labels={'airline_sentiment':'tweets'}, height=600, width=800)
    st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Which sentiment type would you like to display a word cloud?', ('positive', 'neutral', 'negative'))

if not st.sidebar.checkbox("Close", True, key='3'):
    st.subheader('Word cloud for %s sentiment' %(word_sentiment))
    df = data[data['airline_sentiment']==word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
