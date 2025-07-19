"""
LLM Configuration System
A professional class-based system for managing different LLM models and providers.
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load environment variables
load_dotenv('hack.env')


class LLMConfig:
    """
    Professional LLM Configuration Manager
    
    This class provides a centralized way to manage different LLM models,
    handle API keys, and make model invocations across the application.
    """
    
    def __init__(self):
        """Initialize the LLM configuration manager"""
        self._current_model = None
        self._current_provider = None
        self._current_model_name = None
        
        # Available models configuration
        self._available_models = {
            "google": {
                "gemini-2.0-flash": {
                    "description": "Google's latest Gemini model",
                    "provider": "google_genai"
                },
                "gemini-1.5-pro": {
                    "description": "Google's Gemini Pro model", 
                    "provider": "google_genai"
                },
                "gemini-2.5-pro": {
                    "description": "Google's Gemini 2.5 Pro model",
                    "provider": "google_genai"
                }
            }
        }
    
    @property
    def current_model(self) -> Optional[Any]:
        """Get the currently initialized model"""
        return self._current_model
    
    @property
    def current_provider(self) -> Optional[str]:
        """Get the current provider name"""
        return self._current_provider
    
    @property
    def current_model_name(self) -> Optional[str]:
        """Get the current model name"""
        return self._current_model_name
    
    @property
    def is_initialized(self) -> bool:
        """Check if a model is currently initialized"""
        return self._current_model is not None
    
    def setup_api_keys(self) -> bool:
        """
        Setup API keys for different providers
        
        Returns:
            bool: True if setup successful, False otherwise
        """
        try:
            # Load Google API key from environment
            if not os.environ.get("GOOGLE_API_KEY"):
                # Try to load from .env file
                load_dotenv('hack.env')
                if not os.environ.get("GOOGLE_API_KEY"):
                    print("❌ GOOGLE_API_KEY not found in environment or .env file")
                    return False
            
            print("✅ API keys setup completed")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up API keys: {str(e)}")
            return False
    
    def list_available_models(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """
        Get list of all available models grouped by provider
        
        Returns:
            Dict containing available models by provider
        """
        return self._available_models
    
    def get_model_info(self, model_name: str, provider: str = "google") -> Optional[Dict[str, str]]:
        """
        Get information about a specific model
        
        Args:
            model_name: Name of the model
            provider: Provider name (default: "google")
            
        Returns:
            Dict with model information or None if not found
        """
        if provider in self._available_models:
            if model_name in self._available_models[provider]:
                return self._available_models[provider][model_name]
        return None
    
    def init_model(self, model_name: str, provider: str = "google") -> bool:
        """
        Initialize a specific model
        
        Args:
            model_name: Name of the model to initialize
            provider: Provider name (default: "google")
            
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Validate provider
            if provider not in self._available_models:
                print(f"❌ Provider '{provider}' not supported")
                return False
            
            # Validate model
            if model_name not in self._available_models[provider]:
                print(f"❌ Model '{model_name}' not available for provider '{provider}'")
                return False
            
            # Get model configuration
            model_config = self._available_models[provider][model_name]
            
            # Initialize the model
            self._current_model = init_chat_model(
                model_name, 
                model_provider=model_config["provider"]
            )
            
            # Update state
            self._current_provider = provider
            self._current_model_name = model_name
            
            print(f"✅ Successfully initialized {model_name} from {provider}")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing model '{model_name}': {str(e)}")
            return False
    
    def get_current_model_info(self) -> Dict[str, Any]:
        """
        Get information about the currently loaded model
        
        Returns:
            Dict with current model information
        """
        if self.is_initialized:
            return {
                "provider": self._current_provider,
                "model_name": self._current_model_name,
                "initialized": True,
                "description": self.get_model_info(self._current_model_name, self._current_provider)["description"]
            }
        return {
            "provider": None,
            "model_name": None,
            "initialized": False,
            "description": None
        }
    
    def invoke(self, prompt: str) -> Optional[str]:
        """
        Send a prompt to the current model and get response
        
        Args:
            prompt: The prompt to send to the model
            
        Returns:
            str: Model response or None if error
        """
        if not self.is_initialized:
            print("❌ No model initialized. Please use init_model() first.")
            return None
        
        try:
            response = self._current_model.invoke(prompt)
            return response.content
            
        except Exception as e:
            print(f"❌ Error during model invocation: {str(e)}")
            return None
    
    def quick_query(self, query: str) -> Optional[str]:
        """
        Quick query without starting a conversation session
        
        Args:
            query: The query to send to the model
            
        Returns:
            str: Model response or None if error
        """
        return self.invoke(query)
    
    def reset(self):
        """Reset the current model and provider"""
        self._current_model = None
        self._current_provider = None
        self._current_model_name = None
        print("🔄 Model configuration reset")


# Global instance for application-wide use
llm_config = LLMConfig()


def main():
    """Main function to demonstrate the LLM configuration system"""
    print("🚀 LLM Configuration System")
    print("=" * 40)
    
    # Setup API keys
    if not llm_config.setup_api_keys():
        print("❌ Failed to setup API keys")
        return
    
    while True:
        print("\n📋 Available Options:")
        print("1. List available models")
        print("2. Initialize a model")
        print("3. Quick query")
        print("4. Show current model info")
        print("5. Reset model")
        print("6. Exit")
        
        choice = input("\n🎯 Select an option (1-6): ").strip()
        
        if choice == "1":
            models = llm_config.list_available_models()
            print("\n📚 Available Models:")
            for provider, model_list in models.items():
                print(f"\n{provider.upper()}:")
                for model_name, config in model_list.items():
                    print(f"  - {model_name}: {config['description']}")
        
        elif choice == "2":
            print("\n🎯 Initialize Model:")
            print("Available providers: google")
            provider = input("Enter provider: ").strip().lower()
            
            if provider == "google":
                print("Available Google models:")
                for model_name in llm_config._available_models["google"].keys():
                    print(f"  - {model_name}")
                model_name = input("Enter model name: ").strip()
            else:
                print("❌ Invalid provider")
                continue
            
            llm_config.init_model(model_name, provider)
        
        elif choice == "3":
            if not llm_config.is_initialized:
                print("❌ No model initialized. Please initialize a model first.")
                continue
            
            query = input("Enter your query: ").strip()
            response = llm_config.quick_query(query)
            if response:
                print(f"\n🤖 Response: {response}")
        
        elif choice == "4":
            info = llm_config.get_current_model_info()
            if info["initialized"]:
                print(f"\n📊 Current Model Info:")
                print(f"Provider: {info['provider']}")
                print(f"Model: {info['model_name']}")
                print(f"Description: {info['description']}")
                print(f"Status: Initialized")
            else:
                print("❌ No model currently initialized")
        
        elif choice == "5":
            llm_config.reset()
        
        elif choice == "6":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
