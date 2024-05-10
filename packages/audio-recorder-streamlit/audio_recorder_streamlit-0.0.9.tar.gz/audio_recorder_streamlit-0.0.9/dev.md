# Development mode
## Test local dev version
```sh
pdm dev-backend
pdm dev
```

## Test local built version
```sh
pdm start
```

## Test deployed version
```sh
python3 -m venv test-env
source test-env/bin/activate
pip install "streamlit >= 0.63" "altair<5"  # for pypi-test only
pip install -i https://test.pypi.org/simple/ audio-recorder-streamlit==X.X.X
# OR
pip install audio-recorder-streamlit==X.X.X
streamlit run audio_recorder_streamlit/example.py
```