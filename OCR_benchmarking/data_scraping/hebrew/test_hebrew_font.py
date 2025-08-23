import matplotlib.pyplot as plt
from matplotlib import rcParams

hebrew_fonts = [
    'Ezra SIL', 
    'SILEOT',  # This might be the actual name
    'David CLM', 
    'Frank Ruehl CLM', 
    'Miriam CLM',
    'Noto Sans Hebrew',
    'DejaVu Sans'  # fallback
]

for font in hebrew_fonts:
    try:
        # Use the font variable, not hardcoded 'Ezra SIL'
        rcParams['font.family'] = font
        
        plt.figure(figsize=(6, 4))
        plt.text(0.5, 0.5, "שלום", fontsize=20, ha='center', va='center')
        plt.title(f'Hebrew text with {font}')
        plt.savefig(f'hebrew_{font.replace(" ", "_")}.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"✓ Successfully created image with {font}")
    except Exception as e:
        print(f"✗ Failed with {font}: {e}")