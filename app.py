import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline
import numpy as np

# Set page config
st.set_page_config(
    page_title="Sentiment Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Initialize sentiment analysis pipeline
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis")

sentiment_analyzer = load_model()

# App title and description
st.title("Sentiment Analysis Dashboard")
st.markdown("""
This dashboard allows you to analyze sentiment from text data.
Upload a CSV file with text data or enter text directly to analyze.
""")

# Sidebar
st.sidebar.header("Options")
analysis_type = st.sidebar.radio(
    "Choose analysis type:",
    ("Single Text Analysis", "Batch Analysis from CSV")
)

# Single text analysis
if analysis_type == "Single Text Analysis":
    st.header("Analyze Text Sentiment")
    
    text_input = st.text_area("Enter text to analyze:", height=150)
    
    if st.button("Analyze Sentiment"):
        if text_input:
            with st.spinner("Analyzing sentiment..."):
                result = sentiment_analyzer(text_input)
                
                # Display result
                sentiment = result[0]["label"]
                score = result[0]["score"]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Sentiment", sentiment)
                
                with col2:
                    st.metric("Confidence", f"{score:.2%}")
                
                # Visualization
                fig = px.bar(
                    x=["POSITIVE", "NEGATIVE"],
                    y=[score if sentiment == "POSITIVE" else 1-score, 
                       score if sentiment == "NEGATIVE" else 1-score],
                    labels={"x": "Sentiment", "y": "Score"},
                    color=["POSITIVE", "NEGATIVE"],
                    title="Sentiment Analysis Result"
                )
                st.plotly_chart(fig)
        else:
            st.warning("Please enter some text to analyze.")

# Batch analysis
else:
    st.header("Batch Analysis from CSV")
    
    st.info("Upload a CSV file with a column containing text to analyze.")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Load data
        df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded data:")
        st.dataframe(df.head())
        
        # Select column to analyze
        text_column = st.selectbox("Select text column for analysis:", df.columns)
        
        if st.button("Run Batch Analysis"):
            with st.spinner("Analyzing sentiments... This may take a while depending on the data size."):
                # Process in batches to avoid memory issues
                batch_size = 50
                results = []
                
                progress_bar = st.progress(0)
                
                for i in range(0, len(df), batch_size):
                    batch = df[text_column].iloc[i:i+batch_size].tolist()
                    batch_results = sentiment_analyzer(batch)
                    results.extend(batch_results)
                    progress_bar.progress(min(1.0, (i + batch_size) / len(df)))
                
                # Add results to dataframe
                df["sentiment"] = [r["label"] for r in results]
                df["confidence"] = [r["score"] for r in results]
                
                # Display results
                st.success("Analysis complete!")
                st.write("Results:")
                st.dataframe(df)
                
                # Visualizations
                st.header("Visualization")
                
                # Sentiment distribution
                sentiment_counts = df["sentiment"].value_counts().reset_index()
                sentiment_counts.columns = ["Sentiment", "Count"]
                
                fig1 = px.pie(
                    sentiment_counts, 
                    values="Count", 
                    names="Sentiment", 
                    title="Sentiment Distribution"
                )
                st.plotly_chart(fig1)
                
                # Confidence distribution
                fig2 = px.histogram(
                    df, 
                    x="confidence", 
                    color="sentiment",
                    title="Confidence Score Distribution",
                    labels={"confidence": "Confidence Score", "count": "Frequency"}
                )
                st.plotly_chart(fig2)
                
                # Download results
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name="sentiment_analysis_results.csv",
                    mime="text/csv",
                )

# Footer
st.markdown("---")
st.markdown("Created by Dario Costanzo | [GitHub](https://github.com/dariocostanzo)")