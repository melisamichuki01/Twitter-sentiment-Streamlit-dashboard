# Twitter-sentiment-Streamlit-dashboard
This is a guided cousera project in which we build a twitter sentiment dashbord using streamlit.

## Run the dashboard

```bash
pip install streamlit pandas numpy plotly wordcloud matplotlib
streamlit run app.py
```

The app loads `Tweets.csv` from the repository by default.

## Analyze an Xquik CSV export

Use the sidebar uploader to load a saved Xquik CSV export. The importer accepts
common export headers such as `created_at`, `date`, `timestamp`, `text`,
`tweet`, `full_text`, `username`, `screen_name`, `retweet_count`, `retweets`,
`latitude`, and `longitude`, then maps them into the dashboard columns.



