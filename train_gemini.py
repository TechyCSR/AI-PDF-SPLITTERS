#!/usr/bin/env python3
"""
Training Script for Gemini AI PDF Processor
This script demonstrates the AI processing capabilities and expected outputs.
"""

import json
import os
from pathlib import Path
from ai_processor import GeminiPDFProcessor

def create_training_example():
    """Create a training example based on the Paris Library PDF structure"""
    
    training_example = {
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
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 3_Odile",
                "start_page": 41,
                "end_page": 55,
                "page_range": "41-55",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 4_Lily",
                "start_page": 56,
                "end_page": 70,
                "page_range": "56-70",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 5_Odile",
                "start_page": 71,
                "end_page": 85,
                "page_range": "71-85",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 6_Odile",
                "start_page": 86,
                "end_page": 100,
                "page_range": "86-100",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 7_Margaret",
                "start_page": 101,
                "end_page": 115,
                "page_range": "101-115",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 8_Odile",
                "start_page": 116,
                "end_page": 130,
                "page_range": "116-130",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 9_Odile",
                "start_page": 131,
                "end_page": 145,
                "page_range": "131-145",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 10_Odile",
                "start_page": 146,
                "end_page": 160,
                "page_range": "146-160",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 11_Odile",
                "start_page": 161,
                "end_page": 175,
                "page_range": "161-175",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 12_Lily",
                "start_page": 176,
                "end_page": 190,
                "page_range": "176-190",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 13_Odile",
                "start_page": 191,
                "end_page": 205,
                "page_range": "191-205",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 14_Odile",
                "start_page": 206,
                "end_page": 220,
                "page_range": "206-220",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 15_Odile",
                "start_page": 221,
                "end_page": 235,
                "page_range": "221-235",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 16_Odile",
                "start_page": 236,
                "end_page": 250,
                "page_range": "236-250",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 17_Odile",
                "start_page": 251,
                "end_page": 265,
                "page_range": "251-265",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 18_Odile",
                "start_page": 266,
                "end_page": 280,
                "page_range": "266-280",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 19_Miss Reeder",
                "start_page": 281,
                "end_page": 295,
                "page_range": "281-295",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 20_Odile",
                "start_page": 296,
                "end_page": 310,
                "page_range": "296-310",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 21_Lily",
                "start_page": 311,
                "end_page": 325,
                "page_range": "311-325",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 22_Odile",
                "start_page": 326,
                "end_page": 340,
                "page_range": "326-340",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 23_Odile",
                "start_page": 341,
                "end_page": 355,
                "page_range": "341-355",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 24_Odile",
                "start_page": 356,
                "end_page": 370,
                "page_range": "356-370",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 25_Odile",
                "start_page": 371,
                "end_page": 385,
                "page_range": "371-385",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 26_Lily",
                "start_page": 386,
                "end_page": 400,
                "page_range": "386-400",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 27_Odile",
                "start_page": 401,
                "end_page": 415,
                "page_range": "401-415",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 28_Margaret",
                "start_page": 416,
                "end_page": 430,
                "page_range": "416-430",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 29_Odile",
                "start_page": 431,
                "end_page": 445,
                "page_range": "431-445",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 30_Odile",
                "start_page": 446,
                "end_page": 460,
                "page_range": "446-460",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 31_Odile",
                "start_page": 461,
                "end_page": 475,
                "page_range": "461-475",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 32_Boris",
                "start_page": 476,
                "end_page": 490,
                "page_range": "476-490",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 33_Lily",
                "start_page": 491,
                "end_page": 505,
                "page_range": "491-505",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 34_Odile",
                "start_page": 506,
                "end_page": 520,
                "page_range": "506-520",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 35_Paul",
                "start_page": 521,
                "end_page": 535,
                "page_range": "521-535",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 36_Odile",
                "start_page": 536,
                "end_page": 550,
                "page_range": "536-550",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 37_Odile",
                "start_page": 551,
                "end_page": 565,
                "page_range": "551-565",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 38_Odile",
                "start_page": 566,
                "end_page": 580,
                "page_range": "566-580",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 39_Lily",
                "start_page": 581,
                "end_page": 595,
                "page_range": "581-595",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 40_Odile",
                "start_page": 596,
                "end_page": 610,
                "page_range": "596-610",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 41_Odile",
                "start_page": 611,
                "end_page": 625,
                "page_range": "611-625",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 42_The Barbershop Quartet",
                "start_page": 626,
                "end_page": 640,
                "page_range": "626-640",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 43_Odile",
                "start_page": 641,
                "end_page": 655,
                "page_range": "641-655",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 44_Lily",
                "start_page": 656,
                "end_page": 670,
                "page_range": "656-670",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 45_Odile",
                "start_page": 671,
                "end_page": 685,
                "page_range": "671-685",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 46_Lily",
                "start_page": 686,
                "end_page": 700,
                "page_range": "686-700",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 47_Odile",
                "start_page": 701,
                "end_page": 715,
                "page_range": "701-715",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Chapter 48_Lily",
                "start_page": 716,
                "end_page": 730,
                "page_range": "716-730",
                "type": "chapter"
            },
            {
                "title": "WF_4262_The Paris Library_Cover",
                "start_page": 731,
                "end_page": 731,
                "page_range": "731",
                "type": "front_matter"
            },
            {
                "title": "WF_4262_The Paris Library_Front Index",
                "start_page": 732,
                "end_page": 740,
                "page_range": "732-740",
                "type": "back_matter"
            },
            {
                "title": "WF_4262_The Paris Library_The American Library In Paris  A History",
                "start_page": 741,
                "end_page": 750,
                "page_range": "741-750",
                "type": "back_matter"
            },
            {
                "title": "WF_4262_The Paris Library_Back Index",
                "start_page": 751,
                "end_page": 760,
                "page_range": "751-760",
                "type": "back_matter"
            }
        ],
        "metadata": {
            "total_pages": 760,
            "total_sections": 52,
            "file_name": "WF_4262_The Paris Library_Whole Book.pdf"
        }
    }
    
    return training_example

def save_training_example():
    """Save the training example to a JSON file"""
    training_data = create_training_example()
    
    output_file = "training_example_paris_library.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Training example saved to: {output_file}")
    print(f"📊 Contains {len(training_data['sections'])} sections")
    print(f"📄 Total pages: {training_data['metadata']['total_pages']}")
    
    return output_file

def demonstrate_ai_processing():
    """Demonstrate the AI processing capabilities"""
    print("🚀 AI PDF Processor Training Demonstration")
    print("=" * 60)
    
    # Check if we have the compressed PDF
    compressed_pdf = "WF_4262_The Paris Library_Whole Book_compressed.pdf"
    
    if not Path(compressed_pdf).exists():
        print(f"❌ Compressed PDF not found: {compressed_pdf}")
        print("Please run the PDF compressor first:")
        print("python pdf_compressor.py 'WF_4262_The Paris Library_Whole Book.pdf'")
        return
    
    print(f"✅ Found compressed PDF: {compressed_pdf}")
    
    # Check if .env file exists and has API key
    if not Path(".env").exists():
        print("❌ .env file not found. Please create it with your Gemini API key:")
        print("GEMINI_API_KEY=your_actual_api_key_here")
        return
    
    # Check API key
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == "your_gemini_api_key_here":
        print("❌ Please set your actual Gemini API key in the .env file")
        return
    
    print("✅ Gemini API key configured")
    
    # Show what the AI processor will do
    print(f"\n🔍 The AI processor will:")
    print(f"   1. Extract text from {compressed_pdf}")
    print(f"   2. Send content to Gemini AI for analysis")
    print(f"   3. Extract section information with page ranges")
    print(f"   4. Return structured JSON output")
    
    print(f"\n📖 Expected output format:")
    print(f"   - Section titles (exact as they appear)")
    print(f"   - Start and end page numbers")
    print(f"   - Page ranges (e.g., '4-10')")
    print(f"   - Section types (front_matter, chapter, back_matter)")
    
    print(f"\n🎯 To run the AI processor:")
    print(f"   python ai_processor.py '{compressed_pdf}' --verbose")

def main():
    """Main function"""
    print("🧠 Gemini AI PDF Processor Training")
    print("=" * 50)
    
    # Save training example
    print("\n📚 Creating training example...")
    training_file = save_training_example()
    
    # Demonstrate AI processing
    print(f"\n🤖 AI Processing Demonstration...")
    demonstrate_ai_processing()
    
    print(f"\n✅ Training setup completed!")
    print(f"📁 Files created:")
    print(f"   - {training_file} (training example)")
    print(f"   - ai_processor.py (AI processing module)")
    print(f"   - .env (API configuration)")
    
    print(f"\n🚀 Next steps:")
    print(f"   1. Set your Gemini API key in .env")
    print(f"   2. Install dependencies: pip install -r requirements.txt")
    print(f"   3. Run: python ai_processor.py 'WF_4262_The Paris Library_Whole Book_compressed.pdf'")

if __name__ == "__main__":
    main()
