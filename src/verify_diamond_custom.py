import sys
import os

# Ensure src is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path: sys.path.append(current_dir)

from router import AutoRouter

def verify():
    router = AutoRouter()
    
    # TEST 1: Diamond Anchors & Sizing
    # "IS_LOGGED?" length is 10 -> Should be Medium (13x13)
    t1 = "Start -> IS_LOGGED? -> Process"
    
    output = router.draw_flow(t1).replace("░", " ")
    
    with open("diamond_verification.txt", "w", encoding="utf-8") as f:
        f.write("TEST 1: IS_LOGGED? (10 chars)\n")
        f.write(output)
        f.write("\n\n")
        
        # TEST 2: Long Text
        # "IS_THE_USER_LOGGED_IN?" (22 chars) -> Should be Large (17x17)
        t2 = "Start -> IS_THE_USER_LOGGED_IN? -> End"
        f.write("TEST 2: IS_THE_USER_LOGGED_IN? (22 chars)\n")
        f.write(router.draw_flow(t2).replace("░", " "))

if __name__ == "__main__":
    verify()
