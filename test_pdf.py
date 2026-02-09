import sys
import voltsafe_python.pdf_gen as pdf_gen
from voltsafe_python.content import CONTENT_BLOCKS

# Mock data
answers = {
    "q1": "lv_install",
    "q2": "no_dead_only",
    "q3": False,
    "q4": False,
    "q5": False,
    "q6": False,
    "q7": False,
    "q8": "general"
}

risk_profile = {
    "level": "Low",
    "score": 0,
    "flags": []
}

content_map = {
    "sms_core": True
}

try:
    print("Attempting to generate PDF...")
    pdf_bytes = pdf_gen.generate_sms_pdf(answers, risk_profile, content_map, CONTENT_BLOCKS)
    print(f"Success! Generated {len(pdf_bytes)} bytes.")
    
    if isinstance(pdf_bytes, (bytes, bytearray)):
         print("Output is correctly bytes/bytearray.")
    else:
         print(f"Output type is {type(pdf_bytes)}, which might be wrong.")

except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)
