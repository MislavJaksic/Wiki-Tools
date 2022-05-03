import os
import sys

# Adds "wiki_tools" to sys.path
# Now you can do import with "from wiki_tools.Sub-Package ..."
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "wiki_tools"))
)
