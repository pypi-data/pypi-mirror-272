# clocksays

This small projects converts a given time (datetime.datetime) in a string of natural language. Languages supported so far:
* German
* English

Feel free to add other languages and issue pull request.

## Usage
```python
import clocksays.saytime as st
import datetime as dt
t_str = st.clocksays(t = dt.datetime.now(), language='de', prefix='Es ist ', suffix='.')
print(t_str)
```
