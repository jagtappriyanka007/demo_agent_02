# _tools/ — internal implementation directory
#
# Everything under _tools/ is private to this skill.
# Consumers import ONLY from skill.py, never from _tools/ directly.
#
# Typical layout:
#   _tools/
#     __init__.py          ← this file
#     my_module.py         ← plain Python implementation
#     src/                 ← or a full sub-package (e.g. a LangGraph pipeline)
