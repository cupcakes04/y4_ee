"""
Master Data & Plotting Script for EEEE3054 CW2 (Dongola / Argo Island: 19.1646°N, 30.4788°E)

What this script does:
1. Fetches official monthly climate data (Solar, Wind, Temp, Rainfall) from NASA POWER API -> saves `nasa_power_dongola.csv`
2. Generates monthly PNG plots from the NASA CSV (`nasa_solar_psh.png`, `nasa_wind_speed.png`, `nasa_temp_rain.png`)
3. Crops the official figures from `GSA_Report_Dongola.pdf` (`gsa_site_info_map.png`, `gsa_monthly_hourly_solar.png`)
4. Plots the Global Wind Atlas CSVs from `gwa-plot-data_.../` (`gwa_wind_chart.png`)
5. Plots the 4-hour Load vs. Solar & Net Power profile (`net_power_profile.png`)

Run from terminal:
    python fetch_climate_data.py
"""

import os
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymupdf

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Remove old duplicate CSV if present
old_csv = os.path.join(DATA_DIR, "nasa_power_argo_island_19.5N_30.4E.csv")
if os.path.exists(old_csv):
    os.remove(old_csv)

# ==============================================================================
# 1. FETCH MONTHLY CLIMATE DATA FROM NASA POWER API (Dongola: 19.1646°N, 30.4788°E)
# ==============================================================================
LAT = 19.1646
LON = 30.4788

nasa_url = (
    "https://power.larc.nasa.gov/api/temporal/climatology/point"
    "?parameters=ALLSKY_SFC_SW_DWN,WS10M,WS50M,T2M,T2M_MAX,PRECTOTCORR"
    f"&community=RE&longitude={LON}&latitude={LAT}&format=JSON"
)

print(f"Fetching NASA POWER data for ({LAT}, {LON})...")
resp = requests.get(nasa_url, timeout=15).json()
df_nasa = pd.DataFrame(resp["properties"]["parameter"])
csv_out = os.path.join(DATA_DIR, "nasa_power_dongola.csv")
df_nasa.to_csv(csv_out)
print(f"Saved NASA POWER CSV to: {csv_out}")

# Extract monthly rows (JAN..DEC) and annual average (ANN)
month_keys = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
months_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
df_m = df_nasa.loc[month_keys]
ann = df_nasa.loc["ANN"]

# ==============================================================================
# 2. GENERATE NASA POWER PLOTS (Solar PSH, Wind Speed, Temp & Rainfall)
# ==============================================================================
# 2a. Solar PSH Bar Chart
plt.figure(figsize=(7, 3.8), dpi=150)
plt.bar(months_labels, df_m["ALLSKY_SFC_SW_DWN"], color="#f59e0b", edgecolor="black")
plt.axhline(ann["ALLSKY_SFC_SW_DWN"], color="red", linestyle="--", label=f"Annual Avg = {ann['ALLSKY_SFC_SW_DWN']:.2f} kWh/m²/day (PSH)")
plt.title("Monthly Solar Irradiance (PSH) at Dongola, Sudan (NASA POWER)")
plt.ylabel("Irradiance / PSH (kWh/m²/day)")
plt.ylim(0, 9)
plt.grid(axis="y", linestyle=":", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(DATA_DIR, "nasa_solar_psh.png"))
plt.close()

# 2b. Wind Speed Chart (10m and 50m)
plt.figure(figsize=(7, 3.8), dpi=150)
plt.plot(months_labels, df_m["WS10M"], marker="o", linewidth=2, color="#0284c7", label=f"10m Wind Speed (Avg = {ann['WS10M']:.2f} m/s)")
plt.plot(months_labels, df_m["WS50M"], marker="s", linewidth=2, color="#0d9488", label=f"50m Wind Speed (Avg = {ann['WS50M']:.2f} m/s)")
plt.title("Monthly Mean Wind Speed (10m & 50m) at Dongola, Sudan (NASA POWER)")
plt.ylabel("Wind Speed (m/s)")
plt.ylim(0, 9.5)
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(DATA_DIR, "nasa_wind_speed.png"))
plt.close()

# 2c. Temperature & Rainfall Chart (PRECTOTCORR is mm/day -> multiply by 30.4 for mm/month)
rain_mm_month = df_m["PRECTOTCORR"] * 30.4
rain_ann_mm = ann["PRECTOTCORR"] * 365.0
fig, ax1 = plt.subplots(figsize=(7, 3.8), dpi=150)
ax1.plot(months_labels, df_m["T2M"], color="#dc2626", marker="s", linewidth=2, label=f"Avg Temp (°C) [Mean = {ann['T2M']:.1f}°C]")
ax1.set_ylabel("Average Temperature (°C)", color="#dc2626")
ax1.set_ylim(0, 42)
ax1.grid(True, linestyle=":", alpha=0.6)
ax2 = ax1.twinx()
ax2.bar(months_labels, rain_mm_month, color="#3b82f6", alpha=0.5, width=0.4, label=f"Rainfall (mm/month) [Total ≈ {rain_ann_mm:.1f} mm/yr]")
ax2.set_ylabel("Rainfall (mm/month)", color="#3b82f6")
ax2.set_ylim(0, 10)
plt.title("Monthly Temperature & Rainfall at Dongola, Sudan (NASA POWER)")
fig.tight_layout()
plt.savefig(os.path.join(DATA_DIR, "nasa_temp_rain.png"))
plt.close()

# ==============================================================================
# 3. CROP FIGURES DIRECTLY FROM GLOBAL SOLAR ATLAS PDF (GSA_Report_Dongola.pdf)
# ==============================================================================
gsa_pdf_path = os.path.join(DATA_DIR, "GSA_Report_Dongola.pdf")
if os.path.exists(gsa_pdf_path):
    doc = pymupdf.open(gsa_pdf_path)
    p1 = doc[0]
    r1 = p1.rect
    clip1 = pymupdf.Rect(r1.x0 + 0.05*r1.width, r1.y0 + 0.23*r1.height, r1.x0 + 0.95*r1.width, r1.y0 + 0.85*r1.height)
    p1.get_pixmap(clip=clip1, dpi=200).save(os.path.join(DATA_DIR, "gsa_site_info_map.png"))

    p2 = doc[1]
    r2 = p2.rect
    clip2 = pymupdf.Rect(r2.x0 + 0.05*r2.width, r2.y0 + 0.14*r2.height, r2.x0 + 0.95*r2.width, r2.y0 + 0.51*r2.height)
    p2.get_pixmap(clip=clip2, dpi=200).save(os.path.join(DATA_DIR, "gsa_monthly_hourly_solar.png"))
    doc.close()

# ==============================================================================
# 4. PLOT GLOBAL WIND ATLAS (GWA) CSV DATA FROM gwa-plot-data FOLDER
# ==============================================================================
gwa_folders = [f for f in os.listdir(DATA_DIR) if f.startswith("gwa-plot-data")]
if gwa_folders:
    gwa_dir = os.path.join(DATA_DIR, gwa_folders[0])
    ws_df = pd.read_csv(os.path.join(gwa_dir, "windSpeed.csv"))
    pd_df = pd.read_csv(os.path.join(gwa_dir, "powerDensity.csv"))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.8), dpi=150)

    ax1.plot(ws_df["perc"], ws_df["val"], color="#0284c7", linewidth=2.5, marker="o", markersize=3)
    ax1.axhline(ws_df["val"].median(), color="navy", linestyle="--", label=f"Median (50%): {ws_df['val'].median():.2f} m/s")
    ax1.set_title("GWA Mean Wind Speed vs. Area (%)")
    ax1.set_xlabel("Percentage of Area (%)")
    ax1.set_ylabel("Wind Speed (m/s)")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend()

    ax2.plot(pd_df["perc"], pd_df["val"], color="#0d9488", linewidth=2.5, marker="s", markersize=3)
    ax2.axhline(pd_df["val"].median(), color="darkgreen", linestyle="--", label=f"Median (50%): {pd_df['val'].median():.1f} W/m²")
    ax2.set_title("GWA Wind Power Density vs. Area (%)")
    ax2.set_xlabel("Percentage of Area (%)")
    ax2.set_ylabel("Power Density (W/m²)")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(DATA_DIR, "gwa_wind_chart.png"))
    plt.close()

# ==============================================================================
# 5. PLOT 4-HOUR LOAD VS. SOLAR & NET POWER PROFILE
# ==============================================================================
intervals = ["0 to 4", "4 to 8", "8 to 12", "12 to 16", "16 to 20", "20 to 24"]
p_load = [0.2, 1.0, 2.0, 1.5, 0.5, 0.2]
p_solar = [0.0, 0.0, 2.7, 2.7, 0.0, 0.0]
p_net = [s - l for s, l in zip(p_solar, p_load)]

x = np.arange(len(intervals))
width = 0.35
plt.figure(figsize=(7.5, 4.0), dpi=150)
plt.bar(x - width/2, p_load, width, label="Health Centre Load (kW)", color="#ef4444", edgecolor="black")
plt.bar(x + width/2, p_solar, width, label="Solar PV Generation (kW)", color="#22c55e", edgecolor="black")
plt.plot(x, p_net, color="#1d4ed8", marker="o", linewidth=2.5, label="Net Power (P_solar - P_load) [kW]")
plt.axhline(0, color="black", linewidth=1)
plt.xticks(x, intervals)
plt.ylabel("Power (kW)")
plt.title("4-Hour Load, Solar Generation & Net Battery Power Profile")
plt.grid(axis="y", linestyle=":", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(DATA_DIR, "net_power_profile.png"))
plt.close()

print("All CSVs and PNG plots in data/ are up to date!")

