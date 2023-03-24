import os

tool_path = os.path.dirname(os.path.realpath(__file__))
source_path = os.path.realpath(os.path.join(tool_path, '..', 'source_data'))
destination_path = os.path.realpath(os.path.join(tool_path, '..', 'public', 'data'))