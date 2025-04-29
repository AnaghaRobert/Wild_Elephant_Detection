import torch
from yolov5.models.experimental import attempt_load

# Load your PyTorch model
model = attempt_load('models/elephant_model_windows.pt', map_location='cpu')
model.eval()

# Create dummy input (adjust size to match your model's input)
dummy_input = torch.randn(1, 3, 640, 640)  # (batch, channels, height, width)

# Export to ONNX
torch.onnx.export(
    model,
    dummy_input,
    'models/elephant_model.onnx',
    input_names=['images'],
    output_names=['output'],
    dynamic_axes={
        'images': {0: 'batch', 2: 'height', 3: 'width'},  # variable size
        'output': {0: 'batch'}
    },
    opset_version=12
)
print("Model converted to ONNX format")