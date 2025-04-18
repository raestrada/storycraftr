#!/usr/bin/env python3
"""
Test script to verify LlamaIndex installation
"""
import os
import sys
import importlib

def test_llamaindex_imports():
    """Test if LlamaIndex modules can be imported correctly"""
    try:
        from llama_index.core import Settings, VectorStoreIndex, Document
        from llama_index.llms.openai import OpenAI
        from llama_index.embeddings.openai import OpenAIEmbedding
        print("✅ All LlamaIndex modules imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Error importing LlamaIndex modules: {e}")
        return False

def test_dependencies():
    """Check if all required dependencies are installed"""
    dependencies = [
        "numpy", "pydantic", "openai", "tiktoken", 
        "aiohttp", "dataclasses_json"  # Note: underscore instead of hyphen
    ]
    
    all_passed = True
    for dep in dependencies:
        try:
            importlib.import_module(dep)
            print(f"✅ Dependency {dep} is installed")
        except ImportError as e:
            print(f"❌ Dependency {dep} is missing: {e}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("Testing LlamaIndex installation...\n")
    
    # Test imports first
    imports_ok = test_llamaindex_imports()
    
    # Test dependencies 
    print("\nChecking dependencies...")
    deps_ok = test_dependencies()
    
    # Summary
    print("\n---- Test Summary ----")
    if imports_ok and deps_ok:
        print("✅ LlamaIndex is correctly installed and ready to use!")
        print("NOTE: You will need to set OPENAI_API_KEY environment variable before using LlamaIndex with real data.")
        sys.exit(0)
    else:
        print("❌ There are issues with the LlamaIndex installation.")
        sys.exit(1) 