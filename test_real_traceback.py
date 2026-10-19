
from debugmate.core.parser import parse_traceback

traceback_text = r'''Traceback (most recent call last):
  File "C:\Users\yadav\OneDrive\Documents\Open source tools\Debugpy\app.py", line 4, in <module>
    print(numbers[5])
          ~~~~~~~^^^
IndexError: list index out of range'''

parsed = parse_traceback(traceback_text)

print("Error type:", parsed.error_type)
print("Message:", parsed.message)
print("File:", parsed.file)
print("Line:", parsed.line)
