# pkeorley/emojis
#### Parse and download all emojis from [discadia.com](https://discadia.com) with `pkeorley/emojis`
## You can use console to fast parsing
```bash
python emojis.py query --json filename --download --print
```
## Also you can use code to get all emojis by topic
```python
from emojis import Emojis

emoji_parser = Emojis()

# loading, cat, dog...
parsed_emojis = emoji_parser.search("topic")

# You will get list of emojis | List[dict[str, Any]]
print(parsed_emojis)
```