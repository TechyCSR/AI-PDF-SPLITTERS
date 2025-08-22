#!/usr/bin/env python3
"""
AI PDF Splitter - Step 1: File Handling & Compression
This script accepts a PDF input, checks file size, and compresses it to ~50 MB.
"""

import argparse
import os
import sys
from pathlib import Path
import PyPDF2
from PIL import Image
import io
import fitz  # PyMuPDF for better PDF handling

def check_file_size(file_path, max_size_mb=400):
    """
    Check if file size is within acceptable limits.
    
    Args:
        file_path (str): Path to the PDF file
        max_size_mb (int): Maximum file size in MB (default: 400)
    
    Returns:
        tuple: (is_valid, file_size_mb, error_message)
    """
    try:
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = file_size_bytes / (1024 * 1024)
        
        if file_size_mb > max_size_mb:
            return False, file_size_mb, f"File size ({file_size_mb:.2f} MB) exceeds maximum allowed size ({max_size_mb} MB)"
        
        return True, file_size_mb, None
    
    except OSError as e:
        return False, 0, f"Error accessing file: {e}"

def compress_pdf(input_path, output_path, target_size_mb=50):
    """
    Compress PDF to target size while maintaining text readability.
    
    Args:
        input_path (str): Path to input PDF
        output_path (str): Path for compressed PDF output
        target_size_mb (int): Target file size in MB (default: 50)
    
    Returns:
        tuple: (success, compressed_size_mb, error_message)
    """
    try:
        # Open the PDF with PyMuPDF for better control
        pdf_document = fitz.open(input_path)
        
        # Create a new PDF document for compression
        compressed_doc = fitz.open()
        
        # Calculate target size in bytes
        target_size_bytes = target_size_mb * 1024 * 1024
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            
            # Get page content with higher compression
            # Use a lower resolution matrix for better compression
            matrix = fitz.Matrix(0.8, 0.8)  # Reduce resolution to 80%
            pix = page.get_pixmap(matrix=matrix)
            
            # Convert to PIL Image for compression
            img_data = pix.tobytes("jpeg")  # Use JPEG instead of PNG for better compression
            img = Image.open(io.BytesIO(img_data))
            
            # Convert to RGB if needed (JPEG requires RGB)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Compress image with aggressive settings
            img_compressed = img.copy()
            
            # Add compressed page to new document
            img_bytes = io.BytesIO()
            
            # Use JPEG with high compression
            img_compressed.save(img_bytes, format='JPEG', quality=60, optimize=True)
            
            # Create new page with compressed content
            new_page = compressed_doc.new_page(width=page.rect.width, height=page.rect.height)
            new_page.insert_image(page.rect, stream=img_bytes.getvalue())
            
            # Check if we're approaching target size
            current_size = len(compressed_doc.write())
            if current_size > target_size_bytes * 1.1:  # Allow 10% buffer
                print(f"⚠️  Warning: Target size may not be achievable with current compression")
                break
        
        # Save compressed document with maximum compression
        compressed_doc.save(
            output_path, 
            garbage=4, 
            deflate=True, 
            clean=True,
            linear=True,  # Linearize for web viewing
            pretty=False  # Minimize whitespace
        )
        compressed_doc.close()
        pdf_document.close()
        
        # Check final size
        final_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        
        return True, final_size_mb, None
        
    except Exception as e:
        return False, 0, f"Error during compression: {e}"

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="AI PDF Splitter - Step 1: File Handling & Compression",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pdf_compressor.py input.pdf
  python pdf_compressor.py input.pdf --output compressed.pdf
  python pdf_compressor.py input.pdf --target-size 40
        """
    )
    
    parser.add_argument(
        "input_file",
        help="Input PDF file path"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output compressed PDF file path (default: input_compressed.pdf)"
    )
    
    parser.add_argument(
        "-t", "--target-size",
        type=int,
        default=50,
        help="Target file size in MB (default: 50)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist.")
        sys.exit(1)
    
    if not input_path.suffix.lower() == '.pdf':
        print(f"Error: Input file '{input_path}' is not a PDF file.")
        sys.exit(1)
    
    # Set output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.parent / f"{input_path.stem}_compressed{input_path.suffix}"
    
    if args.verbose:
        print(f"Input file: {input_path}")
        print(f"Output file: {output_path}")
        print(f"Target size: {args.target_size} MB")
        print("-" * 50)
    
    # Step 1: Check file size
    print("Step 1: Checking file size...")
    is_valid, file_size_mb, error_msg = check_file_size(input_path)
    
    if not is_valid:
        print(f"❌ File size check failed: {error_msg}")
        sys.exit(1)
    
    print(f"✅ File size check passed: {file_size_mb:.2f} MB")
    
    # If file is already small enough, just copy it
    if file_size_mb <= args.target_size:
        print(f"📄 File is already within target size ({file_size_mb:.2f} MB ≤ {args.target_size} MB)")
        print(f"📋 Copying file to: {output_path}")
        
        import shutil
        shutil.copy2(input_path, output_path)
        print("✅ File copied successfully")
        sys.exit(0)
    
    # Step 2: Compress the file
    print(f"📦 Compressing file from {file_size_mb:.2f} MB to target {args.target_size} MB...")
    
    success, compressed_size_mb, error_msg = compress_pdf(
        str(input_path), 
        str(output_path), 
        args.target_size
    )
    
    if not success:
        print(f"❌ Compression failed: {error_msg}")
        sys.exit(1)
    
    # Calculate compression ratio
    compression_ratio = ((file_size_mb - compressed_size_mb) / file_size_mb) * 100
    
    print(f"✅ Compression completed successfully!")
    print(f"📊 Original size: {file_size_mb:.2f} MB")
    print(f"📊 Compressed size: {compressed_size_mb:.2f} MB")
    print(f"📊 Compression ratio: {compression_ratio:.1f}%")
    print(f"📁 Compressed file saved to: {output_path}")
    
    if args.verbose:
        print(f"🎯 Target achieved: {'Yes' if compressed_size_mb <= args.target_size else 'No'}")

if __name__ == "__main__":
    main()
