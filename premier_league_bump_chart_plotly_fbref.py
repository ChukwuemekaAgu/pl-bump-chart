import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
from io import StringIO
import imageio.v2 as imageio
import os

TEAM_META = {
    "Arsenal": {"color": "#EF0107", "logo": "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg"},
    "Aston Villa": {"color": "#95BFE5", "logo": "https://upload.wikimedia.org/wikipedia/en/f/f9/Aston_Villa_FC_crest_%282016%29.svg"},
    "Bournemouth": {"color": "#DA291C", "logo": "https://upload.wikimedia.org/wikipedia/en/e/e5/AFC_Bournemouth_%282013%29.svg"},
    "Brentford": {"color": "#E30613", "logo": "https://upload.wikimedia.org/wikipedia/en/2/2a/Brentford_FC_crest.svg"},
    "Brighton": {"color": "#0057B8", "logo": "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg"},
    "Chelsea": {"color": "#034694", "logo": "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg"},
    "Crystal Palace": {"color": "#1B458F", "logo": "https://upload.wikimedia.org/wikipedia/en/a/a2/Crystal_Palace_FC_logo_%282022%29.svg"},
    "Everton": {"color": "#003399", "logo": "https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg"},
    "Fulham": {"color": "#FFFFFF", "logo": "https://upload.wikimedia.org/wikipedia/en/3/3f/Fulham_FC_%282001%29.svg"},
    "Ipswich Town": {"color": "#3A5DAE", "logo": "https://upload.wikimedia.org/wikipedia/en/4/43/Ipswich_Town.svg"},
    "Leicester City": {"color": "#003090", "logo": "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg"},
    "Liverpool": {"color": "#C8102E", "logo": "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg"},
    "Manchester City": {"color": "#6CABDD", "logo": "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg"},
    "Manchester Utd": {"color": "#DA291C", "logo": "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg"},
    "Newcastle Utd": {"color": "#241F20", "logo": "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg"},
    "Nott'ham Forest": {"color": "#DD0000", "logo": "https://upload.wikimedia.org/wikipedia/en/e/e5/Nottingham_Forest_F.C._logo.svg"},
    "Southampton": {"color": "#D71920", "logo": "https://upload.wikimedia.org/wikipedia/en/c/c9/Southampton_FC.svg"},
    "Tottenham": {"color": "#132257", "logo": "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg"},
    "West Ham": {"color": "#7A263A", "logo": "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg"},
    "Wolves": {"color": "#FDB913", "logo": "https://upload.wikimedia.org/wikipedia/en/f/fc/Wolverhampton_Wanderers.svg"}
}

def generate_sample_data(matchweeks=20):
    teams = list(TEAM_META.keys())
    data = []
    current_ranks = np.arange(1, 21)
    for mw in range(1, matchweeks + 1):
        if mw > 1:
            for _ in range(2):
                idx1, idx2 = np.random.randint(0, 20, 2)
                current_ranks[idx1], current_ranks[idx2] = current_ranks[idx2], current_ranks[idx1]
        
        for i, team in enumerate(teams):
            data.append({"Matchweek": mw, "Team": team, "Position": int(current_ranks[i])})
    return pd.DataFrame(data)

def build_plot(df, matchweeks):
    teams = df["Team"].unique()
    frames = []

    for mw in range(1, matchweeks + 1):
        traces = []
        images = []
        current_subset = df[df["Matchweek"] <= mw]

        for team in teams:
            team_df = current_subset[current_subset["Team"] == team]
            if team_df.empty: continue
            
            latest = team_df.iloc[-1]
            color = TEAM_META.get(team, {"color": "gray"})["color"]

            traces.append(go.Scatter(
                x=team_df["Matchweek"],
                y=team_df["Position"],
                mode="lines",
                line=dict(color=color, width=1.5),
                name=team,
                hovertemplate=f"<b>{team}</b><br>Position: %{{y}}<br>MW: %{{x}}<extra></extra>"
            ))

            images.append(dict(
                source=TEAM_META.get(team, {"logo": ""})["logo"],
                x=latest["Matchweek"],
                y=latest["Position"],
                xref="x", yref="y",
                sizex=0.7, sizey=0.7,
                xanchor="center", yanchor="middle",
                layer="above",
                sizing="contain"
            ))

        frames.append(go.Frame(data=traces, layout=dict(images=images), name=str(mw)))

    fig = go.Figure(data=frames[0].data, frames=frames)

    fig.update_layout(
        title={
            'text': "PREMIER LEAGUE POSITION TRACKER",
            'y':0.95, 'x':0.5, 'xanchor': 'center', 'font': {'size': 22, 'family': 'Arial'}
        },
        xaxis=dict(title="MATCHWEEK", range=[0.8, matchweeks + 0.5], gridcolor="#F0F0F0", dtick=1),
        yaxis=dict(title="POSITION", range=[20.5, 0.5], tickvals=list(range(1, 21)), gridcolor="#F0F0F0", autorange=False),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        hovermode="closest",
        margin=dict(t=80, b=80, l=50, r=50),
        
        shapes=[
            dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=0.5, y1=4.5,
                 fillcolor="rgba(0, 200, 0, 0.04)", line_width=0, layer="below"),
            dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=17.5, y1=20.5,
                 fillcolor="rgba(200, 0, 0, 0.04)", line_width=0, layer="below"),
        ]
    )

    fig.update_layout(
        updatemenus=[{
            "type": "buttons", "x": 0.05, "y": -0.15,
            "buttons": [{"label": "▶ Play", "method": "animate", 
                         "args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}]}]
        }],
        sliders=[{
            "steps": [{"method": "animate", "label": f"{mw}", "args": [[str(mw)], {"frame": {"duration": 100, "redraw": True}}]} 
                      for mw in range(1, matchweeks + 1)],
            "x": 0.15, "y": -0.15, "len": 0.8
        }]
    )

    return fig

def export_outputs(fig):
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    html_path = os.path.join(desktop, "pl_tracker.html")
    gif_path = os.path.join(desktop, "pl_tracker.gif")

    fig.write_html(html_path, include_plotlyjs="cdn")
    print(f"✅ HTML: {html_path}")

    print("⏳ Creating GIF (Lowering scale for speed)...")
    os.makedirs("temp_frames", exist_ok=True)
    images = []
    
    for i, frame in enumerate(fig.frames):
        fig.update(data=frame.data, layout=frame.layout)
        frame_path = f"temp_frames/f_{i}.png"
        fig.write_image(frame_path, scale=1.0) 
        images.append(imageio.imread(frame_path))
        os.remove(frame_path)

    imageio.mimsave(gif_path, images, fps=5)
    os.rmdir("temp_frames")
    print(f"✅ GIF: {gif_path}")

def main():
    df = generate_sample_data(20)
    fig = build_plot(df, 20)
    export_outputs(fig)

if __name__ == "__main__":
    main()
