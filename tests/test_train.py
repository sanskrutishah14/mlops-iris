from src.train import main


def test_training_accuracy_is_good(tmp_path, monkeypatch):
    monkeypatch.setattr("src.train.MODEL_PATH", str(tmp_path / "m.joblib"))
    monkeypatch.chdir(tmp_path)  # keep mlruns out of the repo
    assert main() > 0.9
