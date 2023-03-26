import os

tool_path = os.path.dirname(os.path.realpath(__file__))
source_path = os.path.realpath(os.path.join(tool_path, '..', 'data', 'source'))
generated_path = os.path.realpath(os.path.join(tool_path, '..', 'data', 'generated'))
public_path = os.path.realpath(os.path.join(tool_path, '..', 'public', 'data'))