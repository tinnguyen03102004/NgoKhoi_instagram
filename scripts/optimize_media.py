"""
Media Optimization Script
Converts images to WebP and compresses videos for web deployment
Uses FFmpeg and ImageMagick from media-processing skill
"""

import os
import subprocess
import shutil
from pathlib import Path
import json

# Tool paths (Windows)
MAGICK_PATH = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
FFMPEG_PATH = r"C:\Users\tinnh\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"

# Configuration
SOURCE_DIR = Path("assets/media/instagram")
OUTPUT_DIR = Path("assets/media/optimized")
THUMB_DIR = Path("assets/media/thumbnails")

# Image settings - WebP compression
IMAGE_QUALITY = 80
MAX_IMAGE_WIDTH = 1200

# Video settings - H.264 compression
VIDEO_CRF = 28  # Higher = smaller file, lower quality (18-28 recommended)
VIDEO_PRESET = "medium"  # ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
VIDEO_MAX_HEIGHT = 720

def ensure_dirs():
    """Create output directories"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created output directories")

def optimize_image(src_path: Path, dest_path: Path):
    """Convert image to WebP format with compression"""
    webp_path = dest_path.with_suffix('.webp')
    
    cmd = [
        MAGICK_PATH,
        str(src_path),
        "-resize", f"{MAX_IMAGE_WIDTH}x>",  # Resize only if larger
        "-quality", str(IMAGE_QUALITY),
        "-strip",  # Remove metadata
        str(webp_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        original_size = src_path.stat().st_size
        new_size = webp_path.stat().st_size
        reduction = (1 - new_size / original_size) * 100
        print(f"  ✓ {src_path.name} → {webp_path.name} ({reduction:.1f}% smaller)")
        return webp_path
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Failed: {src_path.name} - {e}")
        return None

def optimize_video(src_path: Path, dest_path: Path):
    """Compress video with H.264 and create poster"""
    mp4_path = dest_path.with_suffix('.mp4')
    poster_path = THUMB_DIR / f"{src_path.stem}_poster.jpg"
    
    # Compress video
    cmd = [
        FFMPEG_PATH, "-y",
        "-i", str(src_path),
        "-c:v", "libx264",
        "-preset", VIDEO_PRESET,
        "-crf", str(VIDEO_CRF),
        "-vf", f"scale=-2:{VIDEO_MAX_HEIGHT}",  # 720p
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",  # Fast web playback
        str(mp4_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Generate poster/thumbnail
        poster_cmd = [
            FFMPEG_PATH, "-y",
            "-i", str(src_path),
            "-ss", "00:00:01",  # 1 second in
            "-vframes", "1",
            "-vf", f"scale={MAX_IMAGE_WIDTH}:-1",
            "-q:v", "2",
            str(poster_path)
        ]
        subprocess.run(poster_cmd, check=True, capture_output=True)
        
        original_size = src_path.stat().st_size
        new_size = mp4_path.stat().st_size
        reduction = (1 - new_size / original_size) * 100
        print(f"  ✓ {src_path.name} → {mp4_path.name} ({reduction:.1f}% smaller)")
        return mp4_path, poster_path
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Failed: {src_path.name} - {e}")
        return None, None

def generate_media_data():
    """Generate updated media-data.js with optimized paths"""
    images = []
    videos = []
    
    # Scan optimized directory
    for file in OUTPUT_DIR.iterdir():
        if file.suffix == '.webp':
            images.append({
                "src": f"assets/media/optimized/{file.name}",
                "type": "image"
            })
        elif file.suffix == '.mp4':
            poster = THUMB_DIR / f"{file.stem}_poster.jpg"
            videos.append({
                "src": f"assets/media/optimized/{file.name}",
                "poster": f"assets/media/thumbnails/{poster.name}" if poster.exists() else None,
                "type": "video"
            })
    
    return images, videos

def main():
    print("=" * 60)
    print("MEDIA OPTIMIZATION SCRIPT")
    print("=" * 60)
    
    ensure_dirs()
    
    # Get all media files
    images = list(SOURCE_DIR.glob("*.jpg")) + list(SOURCE_DIR.glob("*.jpeg")) + list(SOURCE_DIR.glob("*.png"))
    videos = list(SOURCE_DIR.glob("*.mp4"))
    
    print(f"\nFound: {len(images)} images, {len(videos)} videos")
    
    # Calculate original size
    original_size = sum(f.stat().st_size for f in images + videos)
    print(f"Original total size: {original_size / 1024 / 1024:.2f} MB\n")
    
    # Process images
    print("OPTIMIZING IMAGES (JPG → WebP)...")
    for img in images:
        dest = OUTPUT_DIR / img.name
        optimize_image(img, dest)
    
    # Process videos
    print("\nOPTIMIZING VIDEOS (MP4 compression)...")
    for vid in videos:
        dest = OUTPUT_DIR / vid.name
        optimize_video(vid, dest)
    
    # Calculate new size
    optimized_files = list(OUTPUT_DIR.iterdir())
    new_size = sum(f.stat().st_size for f in optimized_files)
    
    print("\n" + "=" * 60)
    print("OPTIMIZATION COMPLETE")
    print("=" * 60)
    print(f"Original: {original_size / 1024 / 1024:.2f} MB")
    print(f"Optimized: {new_size / 1024 / 1024:.2f} MB")
    print(f"Reduction: {(1 - new_size / original_size) * 100:.1f}%")
    print(f"\nFiles saved to: {OUTPUT_DIR}")
    print(f"Thumbnails saved to: {THUMB_DIR}")

if __name__ == "__main__":
    main()
