from streamlit.testing.v1 import AppTest


def test_streamlit_app_predicts():
    at = AppTest.from_file("streamlit_app.py", default_timeout=60).run()
    assert not at.exception
    at.button[0].click().run()
    assert not at.exception
    assert "setosa" in at.success[0].value
