#!/usr/bin/env python3
"""
Basic debug script with comprehensive error handling
"""

import sys
import traceback

def main():
    try:
        print("🚀 Starting Medical Analyzer Debug...")
        print(f"Python version: {sys.version}")
        print("=" * 50)
        
        # Test 1: Basic imports
        print("\n📦 Testing imports...")
        try:
            import requests
            print("✅ requests imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import requests: {e}")
            print("💡 Install with: pip install requests")
            return
        
        try:
            import json
            print("✅ json imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import json: {e}")
            return
        
        # Test 2: Basic Ollama connection
        print("\n🔍 Testing Ollama connection...")
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            print(f"✅ Connected to Ollama (Status: {response.status_code})")
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                print(f"📋 Found {len(models)} models:")
                
                for model in models:
                    model_name = model.get('name', 'Unknown')
                    model_size = model.get('size', 'Unknown size')
                    print(f"   - {model_name} ({model_size})")
                
                # Check for gpt-oss models
                gpt_models = [m for m in models if 'gpt-oss' in m.get('name', '').lower()]
                if gpt_models:
                    print(f"🤖 Found {len(gpt_models)} gpt-oss models")
                    
                    # Test a simple query
                    test_model = gpt_models[0]['name']
                    print(f"\n🧪 Testing query with {test_model}...")
                    
                    payload = {
                        "model": test_model,
                        "prompt": "Say hello briefly.",
                        "stream": False,
                        "options": {"temperature": 0.1, "max_tokens": 20}
                    }
                    
                    response = requests.post(
                        "http://localhost:11434/api/generate",
                        json=payload,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        ai_response = result.get('response', 'No response')
                        print(f"✅ Model responded: {ai_response}")
                        print(f"\n🎉 SUCCESS: Everything appears to be working!")
                        
                        # Now test medical query
                        print(f"\n🏥 Testing medical query...")
                        medical_payload = {
                            "model": test_model,
                            "prompt": "Patient has headache and fever. Most likely condition?",
                            "stream": False,
                            "options": {"temperature": 0.3, "max_tokens": 100}
                        }
                        
                        medical_response = requests.post(
                            "http://localhost:11434/api/generate",
                            json=medical_payload,
                            timeout=300
                        )
                        
                        if medical_response.status_code == 200:
                            medical_result = medical_response.json()
                            medical_text = medical_result.get('response', 'No response')
                            print(f"✅ Medical analysis: {medical_text[:200]}...")
                        else:
                            print(f"❌ Medical query failed: {medical_response.status_code}")
                    else:
                        print(f"❌ Test query failed: {response.status_code}")
                        print(f"Response: {response.text}")
                else:
                    print("❌ No gpt-oss models found!")
                    print("💡 Install with: ollama pull gpt-oss-20b")
            else:
                print(f"❌ Ollama responded with status {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to Ollama at http://localhost:11434")
            print("💡 Make sure Ollama is running:")
            print("   - Open another terminal/command prompt")
            print("   - Run: ollama serve")
            print("   - Then run this script again")
        except requests.exceptions.Timeout:
            print("❌ Connection to Ollama timed out")
            print("💡 Ollama might be starting up - wait a moment and try again")
        except Exception as e:
            print(f"❌ Error connecting to Ollama: {str(e)}")
            print(f"Error type: {type(e).__name__}")
    
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        print("\n🔍 Full traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ SCRIPT FAILED TO START: {str(e)}")
        traceback.print_exc()
    finally:
        print("\n" + "=" * 50)
        print("Debug script completed.")
        input("Press Enter to close...")  