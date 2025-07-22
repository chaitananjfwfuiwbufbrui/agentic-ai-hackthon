# vertex_init.py

import os
import logging
from typing import Optional

import vertexai
from dotenv import load_dotenv
from google.api_core import exceptions as google_exceptions

# Configure a logger for this module
logger = logging.getLogger(__name__)

# Module-level state to ensure initialization happens only once
_is_initialized = False


def init_vertex_ai(
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> None:
    """
    Initializes the Vertex AI SDK.

    This function is idempotent, meaning it can be called multiple times without
    re-initializing the SDK or causing errors.

    The configuration is resolved in the following order of precedence:
    1. Direct function arguments (project_id, location, credentials_path).
    2. Environment variables loaded from a .env file.
    3. System-wide environment variables.

    Args:
        project_id (Optional[str]): The Google Cloud project ID. If None, it will be
            inferred from the 'PROJECT_ID' environment variable.
        location (Optional[str]): The Google Cloud location (e.g., 'us-central1').
            If None, it will be inferred from the 'LOCATION' environment variable.
        credentials_path (Optional[str]): The path to the service account key file.
            If None, authentication will be inferred from the environment (e.g.,
            'GOOGLE_APPLICATION_CREDENTIALS' env var or gcloud ADC).

    Raises:
        ValueError: If project_id or location cannot be determined.
        google_exceptions.DefaultCredentialsError: If authentication fails.
    """
    global _is_initialized
    if _is_initialized:
        logger.info("Vertex AI SDK already initialized. Skipping.")
        return

    # Load environment variables from a .env file if it exists
    load_dotenv()

    # Resolve configuration
    project = project_id or os.getenv("PROJECT_ID")
    location = location or os.getenv("LOCATION")
    
    # The Google Auth library automatically handles GOOGLE_APPLICATION_CREDENTIALS,
    # but we can set it explicitly if a path is provided.
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    # Validate that we have the necessary configuration
    if not project:
        raise ValueError(
            "GCP Project ID not provided. Please pass it as an argument or set "
            "the 'PROJECT_ID' environment variable."
        )
    if not location:
        raise ValueError(
            "GCP Location not provided. Please pass it as an argument or set "
            "the 'LOCATION' environment variable."
        )

    try:
        logger.info(f"Initializing Vertex AI for project '{project}' in '{location}'...")
        vertexai.init(project=project, location=location)
        _is_initialized = True
        logger.info("Vertex AI SDK initialized successfully.")

    except google_exceptions.DefaultCredentialsError:
        logger.error(
            "Authentication failed. Please configure your credentials. "
            "See https://cloud.google.com/docs/authentication/provide-credentials-adc"
        )
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred during Vertex AI initialization: {e}")
        raise


if __name__ == "__main__":
    # This block runs only when the script is executed directly
    # It serves as a simple test and demonstration of the module's functionality.

    # Configure basic logging to see the output from our function
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    print("--- Running Demo of vertex_init.py ---")
    try:
        # Example 1: Initialize using environment variables from .env file
        print("\nAttempt 1: Initializing from environment variables...")
        init_vertex_ai()

        # Example 2: Calling it again to show it's idempotent
        print("\nAttempt 2: Calling init again (should be skipped)...")
        init_vertex_ai()
        
        print("\nDemo successful!")

    except (ValueError, google_exceptions.DefaultCredentialsError) as e:
        print(f"\nDemo failed: {e}")
        print(
            "\nPlease ensure you have a .env file in the same directory with:"
            '\nPROJECT_ID="your-gcp-project-id"'
            '\nLOCATION="your-gcp-location"'
            '\nAnd that your GOOGLE_APPLICATION_CREDENTIALS are set correctly.'
        )
    except Exception as e:
        print(f"\nAn unexpected error occurred during the demo: {e}")