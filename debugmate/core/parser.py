from dataclasses import dataclass 

@dataclass
class ParsedError:
    error_type: str
    message: str
    file: str
    line: int


def parse_traceback(traceback : str ) -> ParsedError:
    lines = traceback.splitlines()
    error_line = lines[-1]

    error_type, message = error_line.split(":", 1)

    error_type = error_type.strip()
    message = message.strip()


    for line in lines:
        if "File " in line:
            print(line)

            parts = line.split('"')
        
            file = parts[1]



            location_parts = parts[2].split("line")
            number_part = location_parts[1].split(",")
            line_number = int(number_part[0].strip())


    
    return ParsedError(
        error_type=error_type,
        message=message,
        file=file,
        line=line_number
    )