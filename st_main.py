import streamlit as st
import streamlit.components.v1 as components

st.set_page_config("Sahayak", page_icon="⚡", layout="wide")

st.title("Sahayak AI")
google_translate_code = """
<div id="google_translate_element"></div>
<script type="text/javascript">
function googleTranslateElementInit() {
  new google.translate.TranslateElement(
    {pageLanguage: 'en'}, 'google_translate_element'
  );
}
</script>
<script type="text/javascript"
  src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit">
</script>
"""

# components.html(google_translate_code, height=100)

pg = st.navigation(
        pages=[
        st.Page(page="pages/dashboard.py", title="Dashboard"),
        st.Page(page="pages/classes.py", title="Classes"),
        st.Page(page="pages/ai_agents.py", title="Ai Agents"),

    ]
)

pg.run()