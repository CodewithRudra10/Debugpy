from debugmate.core.parser import parse_traceback


if __name__ == '__main__':
    sample_traceback = '''Traceback (most recent call last):
  File "app.py", line 4, in <module>
    print(missing_var)
NameError: name 'missing_var' is not defined'''

    parsed = parse_traceback(sample_traceback)
    print(parsed)
