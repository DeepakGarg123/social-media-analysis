# Instagram AI Growth Report

An AI-powered Instagram analytics application that analyzes a public Instagram profile, tracks follower growth, analyzes post performance, generates visual analytics, and provides AI-powered growth recommendations.

The application uses **Apify** for Instagram data collection, **Python** for analytics, **Matplotlib** for visualization, **Ollama with Llama 3.2** for AI recommendations, and **Streamlit** for the frontend.

---

## Features

- Analyze a public Instagram profile using its profile URL
- Collect Instagram profile information
- Collect Instagram post data
- Track follower growth over time
- Calculate follower growth and growth percentage
- Analyze content types
- Analyze posting-time performance
- Identify top-performing posts
- Generate analytics charts
- Generate human-readable post names using a local LLM
- Generate AI-powered Instagram growth recommendations
- Display profile details, growth analytics, charts, and recommendations in a Streamlit dashboard
- Maintain historical follower snapshots
- Maintain application logs
- Store analytics and collected data locally

---

## Project Architecture

```text
Instagram Profile URL
        |
        v
Apify Instagram Scraper
        |
        v
Profile + Post Data
        |
        +----------------------+
        |                      |
        v                      v
Profile History         Post Analytics
        |                      |
        +----------+-----------+
                   |
                   v
            Analytics Engine
                   |
                   v
          analytics_report.json
                   |
          +--------+--------+
          |        |        |
          v        v        v
       Charts   Insights  Post Names
          |        |        |
          +--------+--------+
                   |
                   v
          Ollama / Llama 3.2
                   |
                   v
        AI Growth Recommendations
                   |
                   v
          Streamlit Dashboard
```

---

## Project Structure

```text
Social-media-ai-report/
│
├── backend/
│   ├── analytics/
│   │   └── analytics.py
│   │
│   ├── data/
│   │   ├── instagram_data.json
│   │   ├── instagram_profile.json
│   │   ├── profile_history.json
│   │   ├── analytics_report.json
│   │   └── llm_recommendations.json
│   │
│   ├── llm/
│   │   ├── llm.py
│   │   ├── post_namer.py
│   │   └── recommendation_builder.py
│   │
│   ├── logs/
│   │   ├── logs.py
│   │   └── app.log
│   │
│   ├── mcp_server/
│   │   └── server.py
│   │
│   ├── scrapers/
│   │   └── instagram_scraper.py
│   │
│   ├── test/
│   │   ├── test_apify.py
│   │   └── check_post_data.py
│   │
│   └── visualization/
│       └── charts.py
│
├── frontend/
│   └── app.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Technologies Used

- **Python** - Core programming language
- **Streamlit** - Frontend and interactive dashboard
- **Apify** - Instagram data collection
- **Ollama** - Local LLM runtime
- **Llama 3.2** - Local AI model
- **Matplotlib** - Data visualization
- **Requests** - HTTP communication with Ollama
- **python-dotenv** - Environment variable management
- **JSON** - Local data storage

---

## Installation

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd Social-media-ai-report
```

### 2. Create a Virtual Environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
APIFY_API_TOKEN=your_apify_api_token
```

Replace `your_apify_api_token` with your actual Apify API token.
Do not commit the `.env` file to GitHub.

---

## Ollama Setup

This project uses Ollama to run the LLM locally.
Install Ollama and download the Llama 3.2 model:

```bash
ollama pull llama3.2
```

The project currently uses:

```text
llama3.2:latest
```

Ollama runs locally, so AI recommendation generation does not require a paid external LLM API.

---

## Running the Application

Run the Streamlit application from the project root:

```bash
python -m streamlit run frontend/app.py
```

Streamlit will start a local server.
Open the displayed local URL in your browser, usually:

```text
http://localhost:8501
```

---

## How the Application Works

### Step 1: Enter Instagram URL
The user enters a public Instagram profile URL.
Example:

```text
https://www.instagram.com/username/
```

### Step 2: Collect Instagram Data
The application uses Apify to collect:
- Instagram profile information
- Follower count
- Following count when available
- Post count
- Verification status
- Instagram posts
- Post engagement information

The collected information is saved locally for further processing.

### Step 3: Profile Details
The Streamlit dashboard displays profile information such as:
- Username
- Followers
- Following
- Number of posts
- Verification status

### Step 4: Follower Growth
The application stores follower snapshots in:

```text
backend/data/profile_history.json
```

The snapshots are used to calculate follower growth.
Example:

```text
Start Followers:    15,000
Current Followers:  15,500
Growth:             +500
Growth Percentage:  +3.33%
Direction:          Increase
```

The application does not invent historical follower counts.
Historical data is only available from the point at which tracking begins.
For example, if tracking starts in October, the application cannot calculate September-to-October growth unless September data already exists.

### Instagram Analytics
The analytics engine analyzes the collected Instagram data.
Current analytics include:

- **Content Distribution**: Analyzes the distribution of posts according to their content type.
- **Average Likes by Content Type**: Calculates and compares average likes for the analyzed content types.
- **Posting Time Performance**: Analyzes the performance of posts across observed posting hours.
- **Top Performing Posts**: Identifies the top-performing posts according to available engagement data.

### Dashboard Charts
The Streamlit dashboard displays four main charts:
- Content Distribution
- Average Likes by Content Type
- Posting Time Performance
- Top 3 Performing Posts

The charts are generated using Matplotlib and displayed directly inside the Streamlit application.

### Human-Readable Post Names
Instagram posts can contain technical identifiers such as:

```text
DZh470dtCr5
```

These identifiers are not useful for normal users.
The project uses the local LLM to generate short human-readable names from available information such as the post caption and hashtags.

Example:
- **Technical Identifier**: `DZh470dtCr5`
- **Human-Readable Name**: `Karans Big Day`

These human-readable names can then be used in analytics and charts.
The LLM is instructed to use only information available in the post data and avoid inventing unsupported details.

### AI Growth Recommendations
The application uses Ollama and Llama 3.2 to generate Instagram growth recommendations.
The recommendation pipeline is:

```text
Instagram Data
      |
      v
Python Analytics
      |
      v
Reliable Insights
      |
      v
Recommendation Builder
      |
      v
Ollama / Llama 3.2
      |
      v
AI Growth Recommendations
```

Python first identifies analytical insights supported by the available data.
The supported recommendations are then passed to the LLM.
The LLM converts those recommendations into clear and understandable actions for the Instagram account owner.
This approach helps reduce unsupported or invented recommendations.

---

## Data Storage

Collected and generated data is stored inside:

```text
backend/data/
```

- `instagram_data.json`: Stores collected Instagram post data.
- `instagram_profile.json`: Stores collected Instagram profile information.
- `profile_history.json`: Stores historical follower snapshots.
- `analytics_report.json`: Stores generated analytics and analytical insights.
- `llm_recommendations.json`: Stores AI-generated growth recommendations.

---

## Logging

The application maintains logs inside:

```text
backend/logs/app.log
```

The logging system records important events such as:
- Instagram profile scraping
- Instagram post collection
- Follower snapshot creation
- Analytics processing
- Application errors

Logging helps with debugging and monitoring the application.

---

## API Usage

The project uses Apify to collect Instagram data.
Apify usage may consume account credits depending on the Actor used and the amount of data collected.
During development, unnecessary repeated scraping should be avoided.
Previously collected data can be reused for local:
- Analytics
- Chart generation
- LLM development
- Streamlit UI development

This helps reduce unnecessary API usage.

---

## Security

API credentials should never be hard-coded into the source code.
Use environment variables instead:

```env
APIFY_API_TOKEN=your_apify_api_token
```

The `.env` file should never be committed to GitHub.
Make sure `.env` is included in `.gitignore`.

---

## Current Limitations

- The project currently focuses on Instagram.
- Instagram historical follower data is only available from the point at which tracking begins.
- Apify usage may consume account credits.
- Instagram data availability depends on publicly accessible data and the selected Apify Actor.
- Some Instagram profile fields may not always be available.
- Analytics depend on the quantity and quality of collected post data.
- AI recommendations are limited to insights supported by the analytics pipeline.
- The application is currently an MVP and is not intended to be a production-scale social-media analytics platform.

---

## Future Improvements

- Month-to-month follower growth filtering
- Interactive follower growth charts
- More detailed Instagram analytics
- Improved dashboard design
- Additional engagement metrics
- Improved AI recommendation quality
- More interactive visualizations
- MCP-based tool integration
- Additional social-media platform support
- Advanced analytics and reporting

---

## Project Goal

The goal of this project is to build an AI-powered Instagram analytics assistant where a user can enter an Instagram profile URL and receive useful information about the profile's growth and content performance.

The application combines:

```text
Data Collection
      +
Analytics
      +
Visualization
      +
Local LLM
      +
AI Recommendations
      +
Streamlit Dashboard
```

into a single application.

---

## Example Workflow

```text
User enters Instagram URL
          |
          v
Apify collects profile and post data
          |
          v
Follower history is updated
          |
          v
Analytics engine processes the data
          |
          v
Follower growth is calculated
          |
          v
Performance charts are generated
          |
          v
Supported insights are identified
          |
          v
Ollama / Llama 3.2 generates recommendations
          |
          v
Results are displayed in Streamlit
```

---

## Author

**Deepak Garg**  
AI/ML & Generative AI Developer

---

## Project Status

🚧 **Under Development**  
The project is currently being developed as an AI-powered Instagram analytics and growth recommendation system with a Streamlit frontend.