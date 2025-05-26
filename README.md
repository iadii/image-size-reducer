# Image Reducer

A Python script that automatically compresses and resizes images while maintaining quality. This tool processes images from a specified folder, creates backups of originals, and saves compressed versions in an organized folder structure.

## Features

- **Automatic image compression** with adjustable JPEG quality
- **Smart resizing** with maximum dimension limits
- **Format conversion** from RGBA/P to RGB for better compression
- **EXIF orientation handling** to maintain proper image rotation
- **Backup creation** to preserve original images
- **Batch processing** for multiple images
- **Detailed progress reporting** with file size statistics
- **Organized output** with separate backup and reduced folders


## Prerequisites

### Python Requirements
- Python 3.6 or higher
- Pillow (PIL) library

### Installation

1. **Install Python** (if not already installed):
   - Download from [python.org](https://www.python.org/downloads/)
   - Or use Homebrew on macOS: `brew install python3`

2. **Install Pillow library**:
   ```bash
   pip3 install Pillow


## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)
- WebP (.webp)

Starting image compression...
Input folder: ./photos
Backup folder: ./backup
Reduced folder: ./reduced
Quality: 85, Max dimensions: 1200x1200
Found 18 image(s) to process
--------------------------------------------------
Created backup: vacation_photo.jpg
Resized vacation_photo.jpg from 4032x3024 to 1200x900
Compressed vacation_photo.jpg: 2847.3KB → 456.7KB (84.0% reduction)
Created backup: screenshot.png
Compressed screenshot.png: 1234.5KB → 234.1KB (81.0% reduction)
--------------------------------------------------
Processing complete!
Images processed: 18
Total size reduction: 45.2MB → 8.7MB (80.7% reduction)

Original images backed up in: ./backup
Reduced images saved in: ./reduced