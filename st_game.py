import streamlit as st
from game_generator import generate_game_code
import subprocess
import sys

st.set_page_config(layout="wide")

st.title("Context-Based 2D Game Generator")

st.write("Enter a context (e.g., 'waste management') to generate a 2D interactive game.")

# Input for the game context
context = st.text_input("Game Context", "waste management")

if st.button("Generate Game"):
    if context:
        st.session_state.game_code = generate_game_code(context)
        st.success("Game code generated successfully!")

if 'game_code' in st.session_state:
    st.subheader("Generated Game Code")
    st.code(st.session_state.game_code, language='python')

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Launch Game"):
            # Save the generated code to a temporary file
            with open("temp_game.py", "w") as f:
                f.write(st.session_state.game_code)

            # Run the game as a separate process
            st.info("Launching the game in a new window. Close the game window to continue.")
            try:
                # Use the same python interpreter that's running streamlit
                subprocess.run([sys.executable, "temp_game.py"], check=True)
            except subprocess.CalledProcessError as e:
                st.error(f"Error launching game: {e}")
            except FileNotFoundError:
                st.error("Error: Could not find the generated game file to run.")


    with col2:
        # Save the generated code to a text file
        st.download_button(
            label="Save Game Code",
            data=st.session_state.game_code,
            file_name=f"{context.replace(' ', '_')}_game.py",
            mime="text/plain"
        )