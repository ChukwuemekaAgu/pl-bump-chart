# Premier League Animated Bump Chart

An interactive animated bump chart visualizing the Premier League team
positions across matchweeks using Plotly.

## Features
- Smooth GPU-accelerated animation (ScatterGL)
- Team logos overlayed on lines
- Top-4 and relegation zone highlighting
- Slider-controlled timeline
- FBref-compatible data pipeline
- HTML and GIF export

## Data Source
- FBref (latest available Premier League season)
- Fallback to simulated FBref-shaped data if unavailable

## Tech Stack
- Python
- Plotly
- Pandas
- NumPy
- Kaleido
- ImageIO

## Output
- `premier_league_bump.html` – interactive visualization
- `premier_league_bump.gif` – preview animation

## Usage
```bash
pip install -r requirements.txt
python bump_chart.py
