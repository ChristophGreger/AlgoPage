from typing import Set

# List for the colors to be used to color finished branches in tableau tree
mycolors = ["#008000", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#FFA500",
            "#808080", "#A9A9A9", "#ADFF2F", "#8B0000", "#00008B", "#808000", "#ADD8E6", "#FF6347", "#FFFFE0",
            "#006400", "#D3D3D3"]


# Function to get color from the list of colors, that hasn't been used yet
def getColor(alreadyused: Set):
    for x in mycolors:
        if x not in alreadyused:
            return x
