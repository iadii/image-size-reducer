import json
import os
import sys
import shutil
from PIL import Image, ImageOps

def reduce_image_size(image_path, output_path, quality=85, max_width=1200, max_height=1200):
    """
    Reduce image size by compressing and optionally resizing.

    Args:
        image_path: Path to the original image.
        output_path: Path to save the compressed image.
        quality: JPEG quality (1-100, lower = smaller file).
        max_width: Maximum width in pixels.
        max_height: Maximum height in pixels.
    """
    try:
        with Image.open(image_path) as img:
            img = ImageOps.exif_transpose(img)

            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            original_width, original_height = img.size

            if original_width > max_width or original_height > max_height:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                print(f"Resized {os.path.basename(image_path)} from {original_width}x{original_height} to {img.size[0]}x{img.size[1]}")

            original_size = os.path.getsize(image_path)

            img.save(output_path, 'JPEG', quality=quality, optimize=True)

            new_size = os.path.getsize(output_path)
            reduction_percent = ((original_size - new_size) / original_size) * 100

            print(f"Compressed {os.path.basename(image_path)}: {original_size/1024:.1f}KB → {new_size/1024:.1f}KB ({reduction_percent:.1f}% reduction)")
            
            return original_size, new_size

    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return 0, 0

def get_image_files(folder_path):
    """
    Get all image files from a folder.
    
    Args:
        folder_path: Path to the folder containing images.
        
    Returns:
        List of image file paths.
    """
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
    image_files = []
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(supported_formats):
            image_files.append(os.path.join(folder_path, filename))
    
    return sorted(image_files)

def create_folders(base_path):
    """
    Create backup and reduced folders.
    
    Args:
        base_path: Base path where folders will be created.
        
    Returns:
        Tuple of (backup_folder_path, reduced_folder_path)
    """
    backup_folder = os.path.join(base_path, "backup")
    reduced_folder = os.path.join(base_path, "reduced")
    
    os.makedirs(backup_folder, exist_ok=True)
    os.makedirs(reduced_folder, exist_ok=True)
    
    return backup_folder, reduced_folder

def main():
    QUALITY = 85
    MAX_WIDTH = 1200
    MAX_HEIGHT = 1200
    

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(script_dir, "photos")
    

    if not os.path.exists(input_folder):
        print(f"Error: Photos folder not found at {input_folder}")
        return
    
    if not os.path.isdir(input_folder):
        print(f"Error: {input_folder} is not a directory")
        return
    

    image_files = get_image_files(input_folder)
    
    if not image_files:
        print(f"No image files found in {input_folder}")
        print("Supported formats: .jpg, .jpeg, .png, .bmp, .tiff, .webp")
        return
    

    backup_folder, reduced_folder = create_folders(script_dir)
    
    print(f"Starting image compression...")
    print(f"Input folder: {input_folder}")
    print(f"Backup folder: {backup_folder}")
    print(f"Reduced folder: {reduced_folder}")
    print(f"Quality: {QUALITY}, Max dimensions: {MAX_WIDTH}x{MAX_HEIGHT}")
    print(f"Found {len(image_files)} image(s) to process")
    print("-" * 50)
    
    processed_count = 0
    total_original_size = 0
    total_new_size = 0
    

    for image_path in image_files:
        filename = os.path.basename(image_path)
        backup_path = os.path.join(backup_folder, filename)
        reduced_path = os.path.join(reduced_folder, filename)
        
        try:
            shutil.copy2(image_path, backup_path)
            print(f"Created backup: {filename}")
            
            original_size, new_size = reduce_image_size(
                image_path, 
                reduced_path, 
                quality=QUALITY, 
                max_width=MAX_WIDTH, 
                max_height=MAX_HEIGHT
            )
            
            if original_size > 0 and new_size > 0:
                total_original_size += original_size
                total_new_size += new_size
                processed_count += 1
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
    print("-" * 50)
    print(f"Processing complete!")
    print(f"Images processed: {processed_count}")
    
    if processed_count > 0:
        total_reduction = ((total_original_size - total_new_size) / total_original_size) * 100
        print(f"Total size reduction: {total_original_size/1024/1024:.1f}MB → {total_new_size/1024/1024:.1f}MB ({total_reduction:.1f}% reduction)")
        print(f"\nOriginal images backed up in: {backup_folder}")
        print(f"Reduced images saved in: {reduced_folder}")

if __name__ == "__main__":
    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow library not found.")
        print("Please install it using: pip install Pillow")
        sys.exit(1)
    
    main()
