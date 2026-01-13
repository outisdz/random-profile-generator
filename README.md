## Random Profile Generator 🔐

A privacy-focused command-line tool for generating realistic but fictional user profiles using curated character name lists.  
Designed for anonymity, operational security (OPSEC), and cybersecurity-minded workflows.

This tool helps you create **non-attributable identities** suitable for account separation, threat modeling, sandboxing, research environments, and privacy-preserving online activities.

---

## Key Features ✨

* **Fictional identity generation** 🧙‍♂️

  * Names sourced from curated fictional character lists (anime, TV series, etc.) 📚
  * Fully supports custom YAML name lists 🗂️

* **Strong username & password generation** 🔑

  * Cryptographically secure randomness (`secrets`) 🔒
  * Configurable password length and character sets ⚙️
  * Passwords generated using password-manager-grade entropy 🧾

* **Geographic realism** 🌍

  * Random country and city selection via offline GeoNames data 🗺️
  * Optional country pinning 📍

* **Privacy-first design** 🕶️

  * No network calls 🚫🌐
  * No telemetry 📵
  * No data collection 🧾❌
  * Runs fully offline 🖥️

* **Flexible output** 📤

  * Human-readable text 📝
  * Structured JSON for automation and tooling 🧩
  * Explicit control over file saving and formats 💾

---

## Threat Model & Privacy Considerations 🛡️

This tool is designed with the assumption that:

* You **do not want generated identities to be linkable to you** 🔒
* You **do not trust third-party profile generators** 🚫
* You **want reproducibility without surveillance** 🔍

### What this tool does *not* do: 🚫

* No fingerprinting 🖐️
* No remote APIs 🌐❌
* No analytics 📊❌
* No logging of generated data beyond local output 🗃️

All randomness is generated locally using Python’s `secrets` module, suitable for security-sensitive contexts.

---

## Installation ⚙️

### Requirements

* Python 3.10+
* Dependencies:

  * `pyyaml`
  * `geonamescache`

Install dependencies:

```bash
pip install pyyaml geonamescache
```

---

## Usage ▶️

Basic usage:

```bash
python profile_generator.py
```

Generate a profile with a password:

```bash
python profile_generator.py --with-password
```

Save profile as text:

```bash
python profile_generator.py --save profile.txt
```

Save profile as JSON:

```bash
python profile_generator.py --save profile.json
```

Specify output format explicitly:

```bash
python profile_generator.py --save profile.txt --format text
```

Generate a longer password without symbols:

```bash
python profile_generator.py \
  --with-password \
  --password-length 96 \
  --no-password-symbols
```

Hide password from terminal output but keep it in the saved file:

```bash
python profile_generator.py --with-password --save profile.json
```

---

## Custom Name Lists 🧾

You can provide your own character list:

```yaml
Series Name:
  - Character One
  - Character Two
```

Then use it:

```bash
python profile_generator.py --names my_characters.yaml
```

This allows you to fully control naming conventions and cultural context.

---

## Output Formats 📦

### Text (`.txt`) 📝

* Human-readable
* Easy to inspect manually
* Suitable for notes or quick usage

### JSON (`.json`) 🧩

* Structured
* Automation-friendly
* Ideal for pipelines, scripts, and tooling

---

## Intended Audience 🎯

* Privacy advocates 🛡️
* Cybersecurity professionals 🧑‍💻
* OPSEC practitioners 🕵️
* Threat researchers 🔬
* Users managing multiple isolated identities 👥
* Anyone who prefers **control over convenience** ⚖️

---

## Disclaimer ⚠️

This tool generates **fictional data only**.  
You are responsible for how and where generated identities are used.

---

## Philosophy 💭

> Privacy is not about hiding wrongdoing; it is about reducing attack surface.  
> Transparency belongs to institutions; privacy belongs to people.

This project exists to give users **local, auditable, and deterministic control** over identity generation without relying on opaque third-party services.