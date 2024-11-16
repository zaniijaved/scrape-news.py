# Import required libraries
import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to scrape news data from the BBC website
def scrap_news_data():
    url = "https://www.bbc.com/news/world"  # BBC World News URL
    response = requests.get(url)  # Get the page content

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all relevant HTML elements for articles
    titles = soup.find_all("h2", attrs={"data-testid": "card-headline"})
    publish_dates = soup.find_all("span", {"data-testid": "card-metadata-lastupdated"})
    publish_country = soup.find_all("span", {"data-testid": "card-metadata-tag"})
    summaries = soup.find_all("p", attrs={"data-testid": "card-description"})

    # Initialize a list to store each article's details
    articles = []

    # Loop through the extracted data and build a list of articles
    for title, publish_date, publish_country, summary in zip(titles, publish_dates, publish_country, summaries):
        articles.append({
            "title": title.text,
            "date": publish_date.text,
            "country": publish_country.text,
            "summary": summary.text
        })

    return articles  # Return the list of articles

# Function to display the news dashboard in Streamlit
def display_news_dashboard():
    articles = scrap_news_data()  # Retrieve articles by calling the scrap_news_data function

    # Sidebar with search category filter
    st.sidebar.header("Filters")
    search_category = st.sidebar.selectbox(
        "Search Categories",
        ["All", "Technology", "Innovation", "Health", "Business", "World", "Entertainment"]
    )

    # Main page title and description
    st.title("Latest News Dashboard - BBC")
    st.subheader("Browse the latest news articles")

    # Filter articles based on selected category
    filtered_articles = [
        article for article in articles
        if (search_category == "All" or search_category.lower() in article["title"].lower() or
            search_category.lower() in article["summary"].lower())
    ]

    # Display filtered articles
    if filtered_articles:
        for article in filtered_articles:
            st.markdown(f"#### {article['title']}")  # Article title
            st.write(f"**Date:** {article['date']}")  # Publication date
            st.write(f"{article['country']}")  # Country tag
            st.write(f"**Summary:** {article['summary']}")  # Article summary
            st.write("---")  # Divider between articles
    else:
        st.write("No articles found for the specified filters.")  # Message if no articles match the filter

# Run the Streamlit app
if __name__ == '__main__':
    display_news_dashboard()