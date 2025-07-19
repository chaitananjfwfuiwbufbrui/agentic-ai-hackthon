#!/usr/bin/env python3
"""
Main Entry Point
Professional entry point for the LLM Configuration System
"""

from llm_config import llm_config


def main():
    """
    Main function that demonstrates the LLM configuration system
    
    This function showcases the professional LLM configuration system
    with proper error handling and user feedback.
    """
    print("🚀 LLM Configuration System - Main Entry")
    print("=" * 50)
    
    # Setup API keys and initialize model
    print("🔧 Setting up LLM configuration...")
    
    if not llm_config.setup_api_keys():
        print("❌ Failed to setup API keys")
        print("💡 Please check your hack.env file contains GOOGLE_API_KEY")
        return
    
    # Initialize default model
    print("🤖 Initializing model...")
    success = llm_config.init_model("gemini-2.0-flash", "google")
    
    if success:
        print("✅ Model initialized successfully!")
        
        # Display current model info
        model_info = llm_config.get_current_model_info()
        print(f"📊 Current Model: {model_info['model_name']}")
        print(f"📊 Provider: {model_info['provider']}")
        
        # Example usage
        print("\n📝 Example: Writing a program for self-driving car")
        response = llm_config.quick_query("write a program for self driving car")
        
        if response:
            print(f"\n🤖 Response Preview:")
            print(f"{response[:200]}...")
            print(f"\n📄 Full response length: {len(response)} characters")
        else:
            print("❌ Failed to get response from model")
            
        # Interactive option
        print("\n" + "="*50)
        interactive = input("Would you like to start interactive mode? (y/n): ").strip().lower()
        
        if interactive in ['y', 'yes']:
            print("\n🎯 Starting interactive mode...")
            print("Type 'help' for available commands, 'quit' to exit")
            
            while True:
                try:
                    command = input("\n🎯 Command: ").strip().lower()
                    
                    if command == 'quit' or command == 'exit':
                        print("👋 Goodbye!")
                        break
                    elif command == 'help':
                        print("Available commands:")
                        print("- 'query <text>': Send a query to the model")
                        print("- 'info': Show current model info")
                        print("- 'models': List available models")
                        print("- 'change <model>': Change to a different model")
                        print("- 'quit': Exit interactive mode")
                    elif command.startswith('query '):
                        query = command[6:].strip()
                        response = llm_config.quick_query(query)
                        if response:
                            print(f"\n🤖 Response: {response}")
                        else:
                            print("❌ Failed to get response")
                    elif command == 'info':
                        info = llm_config.get_current_model_info()
                        print(f"📊 Model Info: {info}")
                    elif command == 'models':
                        models = llm_config.list_available_models()
                        print("📚 Available Models:")
                        for provider, model_list in models.items():
                            print(f"\n{provider.upper()}:")
                            for model_name, config in model_list.items():
                                print(f"  - {model_name}: {config['description']}")
                    elif command.startswith('change '):
                        model_name = command[7:].strip()
                        if llm_config.init_model(model_name, "google"):
                            print(f"✅ Changed to {model_name}")
                        else:
                            print(f"❌ Failed to change to {model_name}")
                    else:
                        print("❌ Unknown command. Type 'help' for available commands.")
                        
                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
                    break
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
        else:
            print("👋 Goodbye!")
    else:
        print("❌ Failed to initialize model. Please check your API key.")
        print("💡 Make sure your hack.env file contains a valid GOOGLE_API_KEY")


if __name__ == "__main__":
    main()