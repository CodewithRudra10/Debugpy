# def parse_traceback(traceback: str) -> ParsedError:
#     lines = traceback.splitlines()

#     error_line = lines[-1]

#     error_type, message = error_line.split(":", 1)
#     error_type = error_type.strip()
#     message = message.strip()

#     for line in lines:
#         if "File " in line:
#             parts = line.split('"')

#             file = parts[1]

#             location_parts = parts[2].split("line")
#             number_part = location_parts[1].split(",")
#             line_number = int(number_part[0].strip())


from dataclasses import dataclass


@dataclass
class ParsedError:
    error_type: str
    message: str
    file: str
    line: int


from debugmate.core.parser import parse_traceback


traceback = """Traceback (most recent call last):
  File "app.py", line 4, in <module>
    print(numbers[5])
IndexError: list index out of range
"""

result = parse_traceback(traceback)
print("FILE:", repr(result.file))

print(result)
