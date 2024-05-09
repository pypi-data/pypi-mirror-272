# IGC-processor

IGC-processor is a package for processing glider flight log data in IGC file format.

## Intallation
You can install from PyPI.

```bash
pip install igc-processor
```

## How to use

### convert to pandas DataFrame
You can convert text data in IGC file format into a pandas DataFrame.

```python
from pathlib import Path
from igc_processor.parser import igc2df

text = Path("your_igc_file_path").read_text()
df = igc2df(text)
```

### detect circling
From the transition of the glider's coordinates, you can calculate the heading and detect whether it is circling.

```python
from igc_processor.circling import compute_heading_transition, detect_circling

df["heading"] = compute_heading_transition(df["latitude"], df["longitude"])
df["is_circling"] = detect_circling(df["heading"])
```