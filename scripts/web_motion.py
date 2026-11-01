from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
for name,count in [('right',8),('left',8),('wave',4),('jump',5),('idle',6)]:
    atlas=Image.open(root/'app'/'motion'/f'{name}.png')
    frames=[]
    for i in range(count):
        for k in range(6):
            tile=atlas.crop((k*192,i*208,(k+1)*192,(i+1)*208))
            tile=Image.alpha_composite(Image.new('RGBA',tile.size,'#fff9e9'),tile).convert('RGB')
            frames.append(tile)
    frames[0].save(root/'site'/'assets'/f'{name}.webp',save_all=True,append_images=frames[1:],duration=16,loop=0,quality=90)
    frames[0].save(root/'site'/'assets'/f'{name}-still.webp',quality=90)
print('Web motion previews rendered')
