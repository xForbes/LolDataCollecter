League of Legends Data Collector

This repository collects and analyzes match data from League of Legends to track real-time champion performance metrics such as win rates, pick rates, and ban rates.

The project uses the official Riot Games API to gather high-quality match data starting from top-ranked players and expanding outward through their match histories. This approach focuses on collecting competitive, high-skill gameplay data to produce more accurate statistics.

How It Works

The data collection process follows these steps:

Seed Player Selection
The script starts by identifying one or more highly ranked players.

Match Retrieval
It pulls recent match histories for these players using the Riot API.

Data Extraction
For each match, the program records:

Champions played

Champions banned

Player win/loss results

Teammates and opponents

Match IDs to avoid duplicate processing

Recursive Expansion
The collector continues gathering data from newly discovered players until:

A configured match limit is reached, or

There are no more new matches to process

This creates a continuously growing dataset of competitive match data.

Requirements

Python 3.9+

Riot Games API Key

Required Python packages (see requirements.txt)

Setup Instructions

Clone the repository

git clone https://github.com/xForbes/LolDataCollecter.git
cd LolDataCollecter


Create a Riot API configuration

Create a file named config.py in the project root with the following content:

RIOT_API_KEY = "your_api_key_here"


You can obtain an API key from the Riot Developer Portal:
https://developer.riotgames.com

Install dependencies

pip install -r requirements.txt


Run the collector

python main.py

Configuration

You can adjust data collection behavior by modifying variables in the project:

Maximum number of matches to collect

Regions/servers to query

Queue types (Ranked Solo, Flex, etc.)

These settings are located in the project’s configuration files.

Output

The script generates structured data files containing:

Champion win rates

Pick rates

Ban rates

Raw match data for further analysis

Output files are saved in the /data directory.

Notes

Riot API keys are rate-limited, so large data collection runs may behave slowly.

This project is for educational and analytical purposes and is not affiliated with Riot Games.