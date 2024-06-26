import torch
import torchvision

print("Torch version:", torch.__version__)
print("Torchvision version:", torchvision.__version__)

print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("Number of CUDA devices:", torch.cuda.device_count())
    print("Current device index:", torch.cuda.current_device())
    print("Current device name:", torch.cuda.get_device_name(torch.cuda.current_device()))

tensor = torch.randn(2, 2)
if torch.cuda.is_available():
    tensor = tensor.to('cuda')  # move tensor to GPU
print("Tensor created and moved to GPU if available:", tensor)

print("----------------------------")
print("Additional tensor operations:")
x = torch.tensor([1.0, 2.0, 3.0])
y = torch.tensor([4.0, 5.0, 6.0])
z = x + y
print("Result of tensor addition:", z)

print("----------------------------")
print("Test completed successfully!")
