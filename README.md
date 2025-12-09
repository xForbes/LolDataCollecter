# League of Legends Data Collector

This repository collects and analyzes match data from **League of Legends** to track real-time champion performance metrics such as win rates, pick rates, and ban rates.

The project uses the official Riot Games API to gather data starting from top-ranked players and expanding outward through their match history. This approach focuses on competitive, high-skill gameplay to generate more accurate statistics.

---

## How It Works

The data collection process follows these steps:

1. Starts with one or more highly ranked seed players  
2. Retrieves recent match histories using the Riot Games API  
3. Extracts:
   - Champions played
   - Champions banned
   - Win/loss results
   - Teammates and opponents
   - Match IDs to prevent duplicates
4. Repeats the process until:
   - A game limit is reached, or  
   - There are no new matches left to analyze  

---

## Requirements

- Python 3.9+
- Riot Games API Key
- Dependencies listed in `requirements.txt`

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/xForbes/LolDataCollecter.git
cd LolDataCollecter
