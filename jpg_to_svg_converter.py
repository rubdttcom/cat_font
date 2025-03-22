#!/usr/bin/env python3
"""
Script to convert all .jpg files to .svg format and save them in a 'cat_svg' folder.
"""
import os
import cv2
import numpy as np
from pathlib import Path
import potrace
from PIL import Image

def create_output_directory(output_dir):
    """Create the output directory if it doesn't exist."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

def convert_jpg_to_svg(input_file, output_file):
    """Convert a JPG file to SVG format."""
    try:
        # Read the image using PIL
        pil_img = Image.open(input_file)
        img_width, img_height = pil_img.size
        
        # Convert to grayscale and get data
        pil_img = pil_img.convert('L')
        img_data = np.array(pil_img)
        
        # Apply threshold to create a binary image
        # potrace expects True for black, False for white
        bitmap = np.where(img_data > 127, False, True)
        
        # Create a bitmap from the binary image
        bmp = potrace.Bitmap(bitmap)
        
        # Trace the bitmap to create a path
        path = bmp.trace()
        
        # Create SVG string
        svg_content = f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        svg_content += f'<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
        svg_content += f'<svg width="{img_width}" height="{img_height}" version="1.1" xmlns="http://www.w3.org/2000/svg">\n'
        
        # Add path data to SVG
        for curve in path:
            svg_content += '  <path d="'
            
            # Start point
            start_x, start_y = curve.start_point
            svg_content += f'M{start_x},{start_y} '
            
            # Segments
            for segment in curve.segments:
                if segment.is_corner:
                    c_x, c_y = segment.c
                    end_x, end_y = segment.end_point
                    svg_content += f'L{c_x},{c_y} L{end_x},{end_y} '
                else:
                    c1_x, c1_y = segment.c1
                    c2_x, c2_y = segment.c2
                    end_x, end_y = segment.end_point
                    svg_content += f'C{c1_x},{c1_y} {c2_x},{c2_y} {end_x},{end_y} '
            
            svg_content += 'z" fill="black" />\n'
        
        svg_content += '</svg>'
        
        # Write SVG content to file
        with open(output_file, 'w') as f:
            f.write(svg_content)
        
        print(f"Converted {input_file} to {output_file}")
        return True
    
    except Exception as e:
        print(f"Error converting {input_file}: {str(e)}")
        return False

def main():
    # Define input and output directories
    current_dir = Path(__file__).parent
    input_dir = current_dir / "cat_jpg"
    output_dir = current_dir / "cat_svg"
    
    # Create output directory if it doesn't exist
    create_output_directory(output_dir)
    
    # Find all .jpg files in the current directory
    jpg_files = list(input_dir.glob("*.jpg"))
    
    if not jpg_files:
        print("No .jpg files found in the current directory.")
        return
    
    print(f"Found {len(jpg_files)} .jpg files. Starting conversion...")
    
    # Convert each .jpg file to .svg
    success_count = 0
    for jpg_file in jpg_files:
        # Create output file path with the same name but .svg extension
        output_file = output_dir / f"{jpg_file.stem}.svg"
        
        # Convert the file
        if convert_jpg_to_svg(str(jpg_file), str(output_file)):
            success_count += 1
    
    print(f"Conversion completed. Successfully converted {success_count} out of {len(jpg_files)} files.")
    print(f"SVG files are saved in the '{output_dir}' directory.")

if __name__ == "__main__":
    main()
