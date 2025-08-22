#!/usr/bin/env python3
"""
AI PDF Splitter - Step 2: AI Preprocessing & Training Context
This module uses Gemini API to directly analyze PDFs using media input.
"""

import os
import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import google.generativeai as genai
from dotenv import load_dotenv
import fitz  # PyMuPDF for file size checking

# Load environment variables
load_dotenv()

class GeminiPDFProcessor:
    """PDF processor using Gemini AI for direct PDF analysis"""
    
    def __init__(self):
        """Initialize Gemini API client"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        
        # System prompts for training the AI
        self.system_prompts = self._get_system_prompts()
        
    def _get_system_prompts(self) -> str:
        """Get comprehensive system prompts for training the AI"""
        return """
You are an expert PDF analyzer specialized in extracting section information and page ranges.

SYSTEM INSTRUCTIONS:
1. Read and analyze the provided PDF content directly
2. Identify all section headers (chapters, parts, appendices, etc.)
3. Record each section's start and end page numbers
4. **CRITICAL: Extract FULL chapter names and titles, not just "Chapter 1"**
5. Return output STRICTLY in JSON format
6. Be precise with page numbers and ranges, and include the full chapter name and title without new line or "\n"

EXPECTED OUTPUT FORMAT:
{
    "sections": [
        {
            "title": "Section Title",
            "start_page": 0,
            "end_page": 0,
            "page_range": "0",
            "type": "front_matter"
        },
        {
            "title": "FULL_CHAPTER_NAME_WITH_TITLE",
            "start_page": 1,
            "end_page": 15,
            "page_range": "1-15",
            "type": "chapter"
        }
    ],
    "metadata": {
        "total_pages": 0,
        "total_sections": 0,
        "file_name": "filename.pdf"
    }
}

FEW-SHOT EXAMPLES:

EXAMPLE 1 - "WF_4262_The Paris Library_Whole Book.pdf":
{
    "sections": [
        {
            "title": "Front_page",
            "start_page": 0,
            "end_page": 0,
            "page_range": "0",
            "type": "front_matter"
        },
        {
            "title": "WF_4262_The Paris Library_About The Author",
            "start_page": 1,
            "end_page": 3,
            "page_range": "1-3",
            "type": "front_matter"
        },
        {
            "title": "WF_4262_The Paris Library_Acknowledgements",
            "start_page": 4,
            "end_page": 6,
            "page_range": "4-6",
            "type": "front_matter"
        },
        {
            "title": "WF_4262_The Paris Library_Author's Note",
            "start_page": 7,
            "end_page": 10,
            "page_range": "7-10",
            "type": "front_matter"
        },
        {
            "title": "WF_4262_The Paris Library_Chapter 1_Odile",
            "start_page": 11,
            "end_page": 25,
            "page_range": "11-25",
            "type": "chapter"
        },
        {
            "title": "WF_4262_The Paris Library_Chapter 2_Lily",
            "start_page": 26,
            "end_page": 40,
            "page_range": "26-40",
            "type": "chapter"
        }
    ],
    "metadata": {
        "total_pages": 400,
        "total_sections": 50,
        "file_name": "WF_426 Library_Whole Book.pdf"
    }
}

CRITICAL RULES:
- ALWAYS return valid JSON
- **EXTRACT FULL CHAPTER NAMES**: Look for chapter titles, subtitles, or descriptive text**
- Use exact section titles as they appear in the PDF
- Page numbers start from 0 (zero-based indexing)
- For single pages, use same start and end page
- For page ranges, use format "start-end" (e.g., "4-10")
- Include all sections: front matter, chapters, back matter
- Be thorough and accurate with page ranges
- **For chapters, if you see "Chapter 1" but there's also a title/subtitle, include BOTH**
- **Example: "Chapter 1: The Beginning" or "Chapter 1 - Introduction"**
"""

    def check_file_size(self, pdf_path: str) -> bool:
        """Check if PDF file is within Gemini's 50MB limit"""
        try:
            file_size_bytes = os.path.getsize(pdf_path)
            file_size_mb = file_size_bytes / (1024 * 1024)
            
            print(f"📁 File size: {file_size_mb:.2f} MB")
            
            if file_size_mb > 50:
                print(f"❌ File size ({file_size_mb:.2f} MB) exceeds Gemini's 50 MB limit")
                return False
            
            print(f"✅ File size within Gemini's 50 MB limit")
            return True
            
        except OSError as e:
            print(f"❌ Error checking file size: {e}")
            return False

    def analyze_pdf_with_gemini(self, pdf_path: str) -> Dict:
        """Analyze PDF directly using Gemini's media input capabilities"""
        try:
            print(f"🔍 Analyzing PDF: {Path(pdf_path).name}")
            
            # Check file size first
            if not self.check_file_size(pdf_path):
                raise Exception("PDF file exceeds Gemini's 50 MB limit")
            
            print(f"🤖 Sending PDF directly to Gemini AI for analysis...")
            
            # Prepare prompt for Gemini
            prompt = f"""
{self.system_prompts}

TASK: Analyze this PDF document and extract all sections with their page ranges.

**CRITICAL REQUIREMENTS:**
1. Read the PDF content directly
2. Identify all section headers and their page numbers
3. **EXTRACT FULL CHAPTER NAMES**: Look for chapter titles, subtitles, or descriptive text**
4. Be thorough in finding all sections
5. Return valid JSON only

**IMPORTANT FOR CHAPTERS:**
- Don't just write "Chapter 1" - look for the actual chapter title
- Check for subtitles, descriptions, or additional text after "Chapter X"
- Include both chapter number and title in the section name
- Example: "Chapter 1: The Beginning" instead of just "Chapter 1"

Return the result in the exact JSON format specified above.
"""
            
            # Read the PDF file
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
            
            # Create the content parts for Gemini
            content_parts = [
                prompt,
                {
                    "mime_type": "application/pdf",
                    "data": pdf_data
                }
            ]
            
            # Generate response from Gemini with PDF input
            response = self.model.generate_content(content_parts)
            
            if not response.text:
                raise Exception("No response received from Gemini API")
            
            print(f"✅ Received response from Gemini AI")
            
            # Parse JSON response
            try:
                result = json.loads(response.text)
                print(f"✅ Successfully parsed JSON response")
                return result
                
            except json.JSONDecodeError as e:
                print(f"⚠️  JSON parsing failed, attempting to fix...")
                # Try to extract JSON from response
                cleaned_response = self._extract_json_from_response(response.text)
                if cleaned_response:
                    return cleaned_response
                else:
                    raise Exception(f"Failed to parse JSON response: {e}")
                    
        except Exception as e:
            raise Exception(f"Error in Gemini analysis: {e}")
    
    def _extract_json_from_response(self, response_text: str) -> Optional[Dict]:
        """Extract JSON from Gemini response text"""
        try:
            # Look for JSON content between curly braces
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}')
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx + 1]
                return json.loads(json_str)
            
            return None
            
        except Exception:
            return None
    
    def save_analysis_result(self, result: Dict, output_path: str):
        """Save analysis result to JSON file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"💾 Analysis result saved to: {output_path}")
            
        except Exception as e:
            raise Exception(f"Error saving result: {e}")
    
    def print_analysis_summary(self, result: Dict):
        """Print a summary of the analysis results"""
        try:
            sections = result.get('sections', [])
            metadata = result.get('metadata', {})
            
            print(f"\n📊 ANALYSIS SUMMARY")
            print(f"=" * 50)
            print(f"📁 File: {metadata.get('file_name', 'Unknown')}")
            print(f"📄 Total Pages: {metadata.get('total_pages', 'Unknown')}")
            print(f"📚 Total Sections: {metadata.get('total_sections', len(sections))}")
            print(f"\n📖 SECTIONS FOUND:")
            print(f"-" * 30)
            
            for i, section in enumerate(sections[:10], 1):  # Show first 10 sections
                title = section.get('title', 'Unknown')
                page_range = section.get('page_range', 'Unknown')
                section_type = section.get('type', 'Unknown')
                print(f"{i:2d}. {title}")
                print(f"    📍 Pages: {page_range} | Type: {section_type}")
            
            if len(sections) > 10:
                print(f"    ... and {len(sections) - 10} more sections")
            
            print(f"\n✅ Analysis completed successfully!")
            
        except Exception as e:
            print(f"⚠️  Error printing summary: {e}")

def main():
    """Main CLI function for AI PDF processing"""
    parser = argparse.ArgumentParser(
        description="AI PDF Splitter - Step 2: AI Preprocessing & Training Context",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ai_processor.py input.pdf
  python ai_processor.py input.pdf --output analysis.json
  python ai_processor.py input.pdf --verbose
        """
    )
    
    parser.add_argument(
        "input_file",
        help="Input PDF file path (must be under 50 MB for Gemini)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output JSON file path (default: input_analysis.json)"
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
        print(f"❌ Error: Input file '{input_path}' does not exist.")
        sys.exit(1)
    
    if not input_path.suffix.lower() == '.pdf':
        print(f"❌ Error: Input file '{input_path}' is not a PDF file.")
        sys.exit(1)
    
    # Set output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.parent / f"{input_path.stem}_analysis.json"
    
    if args.verbose:
        print(f"Input file: {input_path}")
        print(f"Output file: {output_path}")
        print("-" * 50)
    
    try:
        # Initialize Gemini processor
        print("🚀 Initializing Gemini AI processor...")
        processor = GeminiPDFProcessor()
        print("✅ Gemini AI processor initialized successfully")
        
        # Analyze PDF
        print(f"\n🔍 Starting PDF analysis...")
        result = processor.analyze_pdf_with_gemini(str(input_path))
        
        # Save results
        processor.save_analysis_result(result, str(output_path))
        
        # Print summary
        processor.print_analysis_summary(result)
        
        print(f"\n🎯 Step 2 completed successfully!")
        print(f"📁 Analysis saved to: {output_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
