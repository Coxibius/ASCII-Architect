import sys
import os

# Adjust path to find src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from router import AutoRouter
from engine import ArchitectEngine

class MockEngine:
    def generate(self, expert_type, tags, metadata):
        # Return unique signature for verification
        # Avoiding N, S, E, W because inject_text replaces them!
        if expert_type == "BOX":
            return "[__BOX__]\n|       |\n[__BOX__]"
        elif expert_type == "CYLINDER":
            return "(__CYL__)\n|      |\n(__CYL__)"
        elif expert_type == "DIAMOND":
            return "<__DIA__>\n|       |\n<__DIA__>"
        elif expert_type == "SOFTBOX":
            return "(__RND__)\n|       |\n(__RND__)"
        elif expert_type == "ARROW":
             return "===>"
        return "???"

def run_tests():
    router = AutoRouter()
    router.brain = MockEngine()

    print("\n>>> TEST 1: Grid Parsing (A -> B ; C -> D)")
    flow = "A -> B ; C -> D"
    output = router.draw_flow(flow)
    lines = output.split('\n')
    
    line_a = -1
    line_c = -1
    for i, l in enumerate(lines):
        if "A" in l and "+" not in l: line_a = i
        if "C" in l and "+" not in l: line_c = i
        
    print(f"DEBUG: 'A' at {line_a}, 'C' at {line_c}")
    
    if line_a == -1 or line_c == -1:
        print("FAIL: Could not find nodes")
        sys.exit(1)
        
    if line_c <= line_a:
        print(f"FAIL: C should be below A. ({line_c} <= {line_a})")
        sys.exit(1)

    print("PASS: Vertical Check")

    print("\n>>> TEST 2: Uneven Grid Alignment")
    flow = "LONG_NODE -> B ; A -> C"
    output = router.draw_flow(flow)
    lines = output.split('\n')
    
    def find_x(text):
        for l in lines:
            if text in l and "+" not in l:
                return l.find(text)
        return -1
        
    x_b = find_x("B")
    x_c = find_x("C")
    
    print(f"DEBUG: B at x={x_b}, C at x={x_c}")
    
    if x_b == -1 or x_c == -1:
        print("FAIL: Could not find B or C")
        print(output)
        sys.exit(1)
        
    if abs(x_b - x_c) > 2:
        print(f"FAIL: Columns not aligned. Diff {abs(x_b - x_c)}")
        print(output)
        sys.exit(1)
    
    print("PASS: Alignment Check")
    
    print("\n>>> TEST 3: V2 Shape Dispatch")
    # Keywords: USER (Softbox), API (Box), DB (Cylinder), ? (Diamond)
    flow = "USER -> API ; MY_DB -> ?"
    output = router.draw_flow(flow)
    lines = output.split('\n')
    
    # helper
    def has_shape(text):
        for l in lines:
            if text in l: return True
        return False
        
    # Check Softbox
    if not has_shape("(__RND__)"):
        print("FAIL: USER should trigger SOFTBOX")
        print(output)
        sys.exit(1)
        
    # Check Box
    if not has_shape("[__BOX__]"):
        print("FAIL: API should trigger BOX")
        print(output)
        sys.exit(1)
        
    # Check Cylinder
    if not has_shape("(__CYL__)"):
        print("FAIL: MY_DB should trigger CYLINDER")
        print(output)
        sys.exit(1)
        
    # Check Diamond
    if not has_shape("<__DIA__>"):
        print("FAIL: '?' should trigger DIAMOND")
        print(output)
        sys.exit(1)

    print("PASS: Shape Logic Verified")
    print("\nALL TESTS PASSED")

if __name__ == "__main__":
    run_tests()
