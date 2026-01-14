"""
Generate media-data.js from optimized files
"""
from pathlib import Path
import re

OPTIMIZED_DIR = Path("assets/media/optimized")
THUMB_DIR = Path("assets/media/thumbnails")
OUTPUT_FILE = Path("js/media-data.js")

def extract_date(filename):
    """Extract date from filename like 2024-03-04_05-16-17_UTC_1.webp"""
    match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
    return match.group(1) if match else "2023-01-01"

def main():
    images = []
    videos = []
    profile_pic = None
    
    for file in sorted(OPTIMIZED_DIR.iterdir()):
        if 'profile_pic' in file.name:
            profile_pic = f"assets/media/optimized/{file.name}"
            continue
            
        date = extract_date(file.name)
        
        if file.suffix == '.webp':
            images.append({
                "src": f"assets/media/optimized/{file.name}",
                "date": date
            })
        elif file.suffix == '.mp4':
            poster_name = f"{file.stem}_poster.jpg"
            poster_path = THUMB_DIR / poster_name
            poster = f"assets/media/thumbnails/{poster_name}" if poster_path.exists() else None
            videos.append({
                "src": f"assets/media/optimized/{file.name}",
                "date": date,
                "poster": poster
            })
    
    # Sort by date descending
    images.sort(key=lambda x: x['date'], reverse=True)
    videos.sort(key=lambda x: x['date'], reverse=True)
    
    # Generate JS
    js_content = f'''// Media Data - Generated from Instagram @anhkhoiii_090
// Optimized: {len(images)} images (WebP) + {len(videos)} videos (Compressed MP4)

const MEDIA_DATA = {{
  profile: {{
    username: 'anhkhoiii_090',
    profilePic: '{profile_pic or "assets/media/optimized/profile_pic.webp"}'
  }},
  
  images: [
'''
    
    for img in images:
        js_content += f"    {{ src: '{img['src']}', date: '{img['date']}' }},\n"
    
    js_content = js_content.rstrip(',\n') + '\n  ],\n\n  videos: [\n'
    
    for vid in videos:
        poster_str = f"'{vid['poster']}'" if vid['poster'] else 'null'
        js_content += f"    {{ src: '{vid['src']}', date: '{vid['date']}', poster: {poster_str} }},\n"
    
    js_content = js_content.rstrip(',\n') + '''
  ]
};

// Combine all media sorted by date (newest first)
const ALL_MEDIA = [
  ...MEDIA_DATA.images.map(img => ({ ...img, type: 'image' })),
  ...MEDIA_DATA.videos.map(vid => ({ ...vid, type: 'video' }))
].sort((a, b) => new Date(b.date) - new Date(a.date));

export { MEDIA_DATA, ALL_MEDIA };
'''
    
    OUTPUT_FILE.write_text(js_content, encoding='utf-8')
    print(f"✓ Generated {OUTPUT_FILE}")
    print(f"  - {len(images)} images")
    print(f"  - {len(videos)} videos")

if __name__ == "__main__":
    main()
