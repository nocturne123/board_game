import toml

a = toml.load("new_toml_file.toml")
print(a)
b = toml.load("new_toml_file.toml")
print(b)
