````markdown:c:\Users\dario\projects\sentiment-analysis-dashboard\README.md
# Sentiment Analysis Dashboard

A web-based dashboard for analyzing sentiment in text data using Hugging Face transformers and Streamlit.

## Features

- Single text analysis: Analyze sentiment of individual text inputs
- Batch analysis: Upload CSV files with text data for bulk sentiment analysis
- Interactive visualizations of sentiment results
- Download analysis results as CSV

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/dariocostanzo/sentiment-analysis-dashboard.git
   cd sentiment-analysis-dashboard
````

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app locally:

   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

3. Use the dashboard to:
   - Analyze individual text inputs
   - Upload CSV files for batch analysis
   - Visualize sentiment distribution
   - Download analysis results

## Deployment Options

### Streamlit Cloud (Recommended)

1. Push your code to a GitHub repository
2. Go to [https://share.streamlit.io/](https://share.streamlit.io/) and sign in with GitHub
3. Select your repository, branch, and main file (app.py)
4. Your app will be deployed with a shareable URL

### Heroku

1. Create a `Procfile` in the root directory with:
   ```
   web: streamlit run app.py --server.port=$PORT
   ```
2. Push to Heroku:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `streamlit run app.py`

## Sample Data

You can use the sample data in the `data` directory to test the batch analysis feature. To generate sample data:

```bash
python generate_sample_data.py
```

## Technologies Used

- Streamlit: Web application framework
- Hugging Face Transformers: NLP models for sentiment analysis
- Plotly: Interactive data visualizations
- Pandas: Data manipulation and analysis

## License

MIT

## Author

Dario Costanzo
