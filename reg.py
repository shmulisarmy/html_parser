import re



print(re.compile(r"""[a-zA-Z]+='[^']*'""").findall(" hello hello HELLO='yo'"))