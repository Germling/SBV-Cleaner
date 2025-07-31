import openai
import pandas as pd
import re
from IPython.display import display

# Set up OpenAI API key
openai.api_key = ###Your API key###
def read_sbv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def parse_sbv(lines):
    """Extract timestamps and text separately from SBV."""
    entries = []
    current_timestamp = ""
    current_text = []
    
    timestamp_pattern = re.compile(r'\d{1,2}:\d{2}:\d{2}\.\d{1,3},\d{1,2}:\d{2}:\d{2}\.\d{1,3}')
    
    for line in lines:
        line = line.strip()t
        if timestamp_pattern.match(line):
            if current_timestamp and current_text:
                entries.append((current_timestamp, "\n".join(current_text)))
            current_timestamp = line
            current_text = []
        elif line:
            current_text.append(line)
    
    if current_timestamp and current_text:
        entries.append((current_timestamp, "\n".join(current_text)))
    
    if not entries:
        print("Warning: No valid subtitles detected. Check the SBV format.")
    else:
        print(f"Detected {len(entries)} subtitle entries.")
    return entries

def gpt_post_edit_text(text):
    """Send only subtitle text to GPT for post-editing while keeping format."""
    if not text.strip():
        return text
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a language editor for YouTube subtitle files. Refine the English text to sound more natural while keeping all line breaks and formatting exactly as they are."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip() or text  # Ensure text is not empty

def add_final_caption(entries):
    """Append a final 4-second caption at the end of the SBV file."""
    if entries:
        last_timestamp = entries[-1][0]
        start_time, end_time = last_timestamp.split(',')
        
        try:
            h, m, s = map(float, end_time.split(':'))
            total_seconds = h * 3600 + m * 60 + s + 4
            new_h, remainder = divmod(total_seconds, 3600)
            new_m, new_s = divmod(remainder, 60)
            new_end_time = f"{int(new_h):02}:{int(new_m):02}:{new_s:06.3f}"
            new_timestamp = f"{end_time},{new_end_time}"
            entries.append((new_timestamp, "Discover degree programs."))
        except ValueError:
            print("Error: Timestamp parsing failed in add_final_caption(). Skipping final caption.")
    return entries

def process_sbv(file_path, output_path):
    lines = read_sbv(file_path)
    entries = parse_sbv(lines)
    
    if not entries:
        print("Error: No subtitles found. Exiting process.")
        return
    
    print(f"Processing {len(entries)} subtitle entries...")
    edited_entries = [(ts, gpt_post_edit_text(txt)) for ts, txt in entries]
    edited_entries = add_final_caption(edited_entries)
    
    with open(output_path, 'w', encoding='utf-8') as file:
        for timestamp, text in edited_entries:
            file.write(f"{timestamp}\n{text}\n\n")
    
    print(f"Processed SBV file saved to {output_path}")

def compare_sbv_files(input_file, output_file):
    input_content = read_sbv(input_file)
    output_content = read_sbv(output_file)
    
    df = pd.DataFrame({'Original SBV': input_content, 'Edited SBV': output_content})
    display(df)

process_sbv(###Input file####, ###output file###)
