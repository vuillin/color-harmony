import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def render_palette(colors, title, output_folder="exports", file_format="png"):
    """
    Renders a color palette as an image with HEX codes and titles.
    Saves the file to the specified output folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    num_colors = len(colors)
    fig, ax = plt.subplots(figsize=(num_colors * 2, 3))
    
    ax.set_xlim(0, num_colors)
    ax.set_ylim(0, 1)
    ax.axis('off')

    for i, color in enumerate(colors):
        rect = patches.Rectangle((i, 0), 1, 1, linewidth=0, edgecolor=None, facecolor=color)
        ax.add_patch(rect)
        
        text_color = 'white'
        
        # Simple brightness check for text contrast
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        if brightness > 180:
            text_color = '#333333'

        ax.text(i + 0.5, 0.5, color.upper(), 
                ha='center', va='center', fontsize=12, 
                fontweight='bold', color=text_color, fontfamily='sans-serif')

    plt.title(title, fontsize=16, pad=20, fontweight='bold', color='#333333')
    
    filename = f"{title.lower().replace(' ', '_')}.{file_format}"
    filepath = os.path.join(output_folder, filename)
    
    plt.savefig(filepath, bbox_inches='tight', dpi=300, format=file_format)
    plt.close()
    
    print(f"Saved: {filepath}")