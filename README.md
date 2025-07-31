# SBV Subtitle Cleaner & Translator

This tool processes `.sbv` (YouTube subtitle) files by cleaning or refining already translated subtitles while preserving all timestamps. It can also be adapted for translation tasks by modifying the system prompt used with OpenAI's GPT model.

## Features

- 🧹 **Clean and post-edit subtitles** for natural language flow
- ⏱️ **Retain original timestamps** and subtitle formatting
- 🌐 **Translate subtitles** by changing the system prompt
- 🆚 **Compare original vs. edited subtitles** in a side-by-side view

## Installation

1. Install dependencies (Python 3.7+):
    ```bash
    pip install openai pandas
    ```

2. Get your OpenAI API key from https://platform.openai.com and add it to the script:
    ```python
    openai.api_key = "your-api-key-here"
    ```

## Usage

### 1. Clean or Post-Edit an SBV File

Replace the placeholders in the script:
```python
process_sbv("input_file.sbv", "output_file.sbv")
```

The script will:
- Parse the SBV file
- Send subtitle text to GPT for refinement (without modifying timestamps)
- Save the cleaned version to a new SBV file
- Append a final 4-second caption with custom text

### 2. Compare Input and Output Files

```python
compare_sbv_files("input_file.sbv", "output_file.sbv")
```

This displays a side-by-side comparison using a pandas DataFrame (useful in Jupyter notebooks).

## Customization

### Change GPT Behavior
To translate instead of clean, modify the system prompt:
```python
{"role": "system", "content": "You are a professional translator. Translate the following subtitles to French, keeping all line breaks and formatting intact."}
```

You can localize into any language by adjusting this message.

### Final Caption
Customize the final call-to-action text in the `add_final_caption()` function:
```python
entries.append((new_timestamp, "Discover degree programs."))
```

## Format Requirements

Ensure the SBV file has:
- One timestamp line followed by 1+ text lines
- No extra spacing or malformed timestamps

Example format:
```
0:00:01.000,0:00:03.000
Hello and welcome.

0:00:03.100,0:00:05.000
Today we're learning Python.
```

## Known Issues

- Improper SBV formatting may cause parsing errors.
- GPT responses may occasionally exceed rate limits—handle API throttling as needed.

## License

MIT License. Use freely, modify, and adapt for your workflow.
