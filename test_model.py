import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="my-project-0011-490714", location="us-central1")

models_to_try = [
    "gemini-2.0-flash-001",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash-lite-001",
    "gemini-1.5-flash-002",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash",
    "gemini-1.5-pro-002",
    "gemini-1.5-pro-001",
    "gemini-1.0-pro-002",
]

for model_name in models_to_try:
    try:
        m = GenerativeModel(model_name)
        r = m.generate_content("Say hi in one word")
        print("[OK]   %s: %s" % (model_name, r.text[:30]))
    except Exception as e:
        err = str(e)[:100]
        label = "[404]" if "404" in err else "[FAIL]"
        print("%s  %s: %s" % (label, model_name, err))
