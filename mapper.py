import matplotlib.pyplot as plt

# Dictionary of cities with approximate coordinates (Latitude, Longitude)
# Selected key locations to define the shape of the territory accurately.
locations = {
    "Rush City MN": (45.683, -92.966),
    "Harris MN": (45.583, -92.973),
    "North Branch MN": (45.511, -92.977),
    "Stacy/Linwood MN": (45.398, -93.020),
    "Forest Lake MN": (45.279, -92.986),
    "New Richmond WI": (45.123, -92.536),
    "Osceola WI": (45.320, -92.704),
    "St Croix Falls/Center City": (
        45.400,
        -92.650,
    ),  # Approx center of those northern river towns
    "Marine on St Croix": (45.197, -92.770),
    "Hugo MN": (45.160, -93.000),
    "Lino Lakes MN": (45.164, -93.090),
    "Blaine/Fridley/Mounds View": (45.120, -93.230),  # NW Metro Cluster
    "Roseville/Falcon Heights": (45.006, -93.157),
    "Stillwater/Oak Park Hts": (45.040, -92.830),  # Represents Oak Park/Bayport
    "Hudson WI": (44.974, -92.757),
    "Roberts WI": (44.980, -92.550),
    "River Falls WI": (44.860, -92.620),
    "Woodbury/Lake Elmo": (44.940, -92.930),  # Represents the central grouping
    "Cottage Grove MN": (44.820, -92.940),
    "Hastings MN": (44.744, -92.851),
    "Prescott WI": (44.748, -92.802),
    "Maplewood/N. St Paul": (45.000, -93.030),
    "Mahtomedi/Dellwood": (45.070, -92.950),
    "Lindstrom/Chisago": (45.380, -92.850),
}

lats = [coords[0] for coords in locations.values()]
lons = [coords[1] for coords in locations.values()]
names = list(locations.keys())

plt.figure(figsize=(10, 12))
plt.scatter(lons, lats, c="blue", alpha=0.6, s=100, edgecolors="black")

# Annotate points
for i, txt in enumerate(names):
    plt.annotate(
        txt, (lons[i], lats[i]), xytext=(5, 5), textcoords="offset points", fontsize=8
    )

# Formatting to look like a map
plt.title("Mapped Locations: St. Croix Valley & NE Metro")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True, linestyle="--", alpha=0.5)

# Set approximate bounds to frame the area nicely
plt.xlim(-93.35, -92.40)
plt.ylim(44.70, 45.75)

plt.tight_layout()
plt.show()
