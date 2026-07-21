# Datasets

## Overview

This directory contains datasets for camera calibration, ArUco marker detection, and system testing. Dataset files are managed with Git LFS for large files.

## Structure

```
datasets/
├── calibration/          # Camera calibration data
│   ├── intrinsics/       # Camera intrinsic parameters
│   ├── extrinsics/       # Camera extrinsic parameters
│   ├── images/           # Calibration board images
│   └── ChessboardPattern.pdf
│
└── test_footage/         # Test video and image sequences
    ├── line_following/   # Line detection test videos
    ├── aruco_markers/    # ArUco marker detection test data
    └── warehouse_scenes/ # Warehouse navigation scenarios
```

## Camera Calibration

### Generating Calibration Data

```bash
python vision/src/camera.py --generate-board --size 5x4
# Output: ChessboardPattern.pdf
```

### Performing Calibration

1. Print calibration pattern
2. Capture 20-30 images of board from various angles
3. Run calibration:

```bash
python vision/src/camera.py --calibrate \
    --images datasets/calibration/images/ \
    --board datasets/calibration/ChessboardPattern.pdf \
    --output calibration.yaml
```

### Calibration Results

Output file: `calibration.yaml`

```yaml
camera_matrix:
  - [f_x, 0, c_x]
  - [0, f_y, c_y]
  - [0, 0, 1]

dist_coeffs: [k1, k2, p1, p2, k3]

image_width: 1280
image_height: 720
calibration_error: 0.23  # RMS reprojection error (pixels)
```

## Test Footage

### Line Following Test Videos

- **Simulated line**: Straight line on white background
- **Curved line**: S-curve navigation test
- **Variable width**: 2-10cm line width variations

### ArUco Markers

Standard 5x5 bit marker set (36h11 dictionary):

- Markers 0-35 available
- Markers 0-5 deployed on test field
- 10cm x 10cm physical size

### Warehouse Scenes

Multi-angle warehouse imagery:

- Empty warehouse
- With static obstacles
- With dynamic obstacles (simulated)
- Lighting variations

## Using Test Data

### Load Calibration

```python
import yaml
with open('calibration.yaml', 'r') as f:
    calib_data = yaml.safe_load(f)
    
K = np.array(calib_data['camera_matrix'])
dist = np.array(calib_data['dist_coeffs'])
```

### Run Vision Tests

```bash
pytest vision/tests/test_aruco_detection.py --data-dir datasets/test_footage/aruco_markers/
```

## Adding New Data

1. Capture images/video
2. Organize in appropriate subdirectory
3. Add metadata: `README.md` with:
   - Capture date/environment
   - Camera/lens info
   - Resolution
   - Frame rate
   - Lighting conditions

## Data Privacy

- Test footage contains no personal information
- All hardware is in controlled test environments
- Warehouse scenes are simulated/synthetic

## Large File Management

Dataset files > 50MB are tracked with Git LFS:

```bash
git lfs track "datasets/**/*.mp4"
git lfs track "datasets/**/*.bag"
```

## Future Datasets

- [ ] Real warehouse video (corporate partnership)
- [ ] Multi-robot coordination footage
- [ ] Failure scenario videos
- [ ] Sensor noise calibration data
