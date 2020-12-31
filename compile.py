from pathlib import Path
import shutil

import mpy_cross

src_path = Path("src")
dst_path = Path("output")
dst_path.mkdir(exist_ok=True)


paths = [path for path in src_path.glob('**/*.py') if path.is_file()]

for path in paths:
    if path.name == "boot.py":
        shutil.copy(path, dst_path / path.name)
        continue
    output_path = dst_path / Path(path.with_suffix(".mpy").name)
    mpy_cross.run("-o", str(output_path), path)

