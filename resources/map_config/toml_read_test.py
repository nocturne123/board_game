import toml

with open("base_map.toml") as f:
    raw_data = toml.load(f)

print(raw_data)
