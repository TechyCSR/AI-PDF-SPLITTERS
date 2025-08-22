# AI PDF Splitter - Step 1: File Handling & Compression

This is the first step of a full-proof automated system in Python with AI to process PDF documents. This step handles file input validation, size checking, and compression.

## Features

- **File Size Validation**: Accepts PDF files up to 400 MB
- **Smart Compression**: Compresses PDFs to ~50 MB while maintaining text readability
- **CLI Interface**: Easy-to-use command-line tool
- **Lossless Text**: Preserves text quality during compression
- **Flexible Output**: Customizable output paths and target sizes

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd AI-PDF-SPLITTERS
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
python pdf_compressor.py input.pdf
```

### Advanced Options

```bash
# Specify output file
python pdf_compressor.py input.pdf --output compressed.pdf

# Set custom target size (in MB)
python pdf_compressor.py input.pdf --target-size 40

# Enable verbose output
python pdf_compressor.py input.pdf --verbose

# Combine options
python pdf_compressor.py input.pdf --output small.pdf --target-size 30 --verbose
```

### Command Line Arguments

- `input_file`: Path to the input PDF file (required)
- `-o, --output`: Output file path (default: `input_compressed.pdf`)
- `-t, --target-size`: Target file size in MB (default: 50)
- `-v, --verbose`: Enable verbose output
- `-h, --help`: Show help message

## Examples

### Example 1: Basic Compression
```bash
python pdf_compressor.py document.pdf
```
Output:
```
Step 1: Checking file size...
✅ File size check passed: 150.25 MB
📦 Compressing file from 150.25 MB to target 50 MB...
✅ Compression completed successfully!
📊 Original size: 150.25 MB
📊 Compressed size: 48.75 MB
📊 Compression ratio: 67.6%
📁 Compressed file saved to: document_compressed.pdf
```

### Example 2: File Already Small Enough
```bash
python pdf_compressor.py small_document.pdf
```
Output:
```
Step 1: Checking file size...
✅ File size check passed: 25.50 MB
📄 File is already within target size (25.50 MB ≤ 50 MB)
📋 Copying file to: small_document_compressed.pdf
✅ File copied successfully
```

### Example 3: File Too Large
```bash
python pdf_compressor.py large_document.pdf
```
Output:
```
Step 1: Checking file size...
❌ File size check failed: File size (450.75 MB) exceeds maximum allowed size (400 MB)
```

## How It Works

1. **File Validation**: Checks if the input file exists and is a PDF
2. **Size Check**: Validates file size against the 400 MB limit
3. **Compression Decision**: 
   - If file ≤ 50 MB: Copies file without compression
   - If file > 50 MB: Applies compression to reach target size
4. **Compression Process**: Uses PyMuPDF and PIL to compress images while maintaining text quality
5. **Output**: Saves compressed file with detailed compression statistics

## Requirements

- Python 3.7+
- PyPDF2
- Pillow (PIL)
- PyMuPDF
- pathlib2

## Error Handling

The script handles various error scenarios:
- File not found
- Invalid file format (non-PDF)
- File size exceeds limits
- Compression failures
- Permission issues

## Output Files

- **Compressed PDF**: Main output file with reduced size
- **Naming Convention**: `{original_name}_compressed.pdf` (unless specified otherwise)

## Next Steps

This is Step 1 of the AI PDF Splitter system. Future steps will include:
- AI-powered PDF analysis
- Section extraction
- JSON metadata generation
- Further processing capabilities

## License

See LICENSE file for details.
