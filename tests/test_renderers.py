import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ascii_architect.renderers import get_renderer

shapes = ["BOX", "SOFTBOX", "CYLINDER", "DIAMOND"]
tests = [
    "Short",
    "Medium Length Text",
    "This is a longer text that should wrap eventually if max_width is exceeded"
]

for shape in shapes:
    print(f"\n--- Testing {shape} ---")
    renderer = get_renderer(shape)
    for test in tests:
        print(f"\nText: {test}")
        print(renderer.render(test))
