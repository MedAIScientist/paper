import yaml

# Load the environment.yml file
with open("environment.yml", "r") as f:
    env_data = yaml.safe_load(f)

# Extract dependencies
dependencies = env_data.get("dependencies", [])

# Filter only string entries (ignore nested dicts/lists like 'pip:' blocks or complex conda entries)
pip_packages = [dep for dep in dependencies if isinstance(dep, str)]

# Write to requirements.txt
with open("requirements.txt", "w") as f:
    for package in pip_packages:
        f.write(f"{package}\n")

print("requirements.txt has been created.")
