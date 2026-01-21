# ZIP Password Brute Force Tool

## Overview

A Python-based brute-force password cracking tool designed to recover passwords for password-protected ZIP files. This tool systematically attempts all possible numeric combinations within a specified length range to unlock encrypted ZIP archives.

## Features

- **Brute-force attack**: Systematically tries all numeric password combinations
- **Configurable password length**: Adjustable from 1 to N characters
- **Real-time progress tracking**: Shows current attempt length
- **Automatic extraction**: Automatically extracts contents upon successful password recovery
- **Error handling**: Robust error handling for file operations and password attempts
- **Memory efficient**: Uses generators to handle large password spaces without memory overhead

## Requirements

### Prerequisites
- Python 3.6 or higher
- A password-protected ZIP file (numeric password only)

### Python Libraries
All required libraries are included in Python's standard library:
- `zipfile` (for ZIP file operations)
- `itertools` (for password combination generation)
- `string` (for character set definition)

## Project Structure

```
zip-password-cracker/
│
├── zip_cracker.py          # Main script file
├── your_file.zip           # Target ZIP file (replace with your file)
├── uncompressed_content/   # Auto-created directory for extracted files
└── README.md               # This documentation
```

## Installation

1. **Clone or download the script:**
   ```bash
   git clone <repository-url>
   cd zip-password-cracker
   ```

2. **Ensure Python is installed:**
   ```bash
   python --version
   ```
   Should show Python 3.6 or higher.

3. **Place your ZIP file in the same directory as the script and rename it to `your_file.zip`, or modify the script to use your filename.**

## Usage

### Basic Usage
```bash
python zip_cracker.py
```

### How It Works
1. The script attempts passwords of increasing length:
   - 1-digit passwords (0-9): 10 attempts
   - 2-digit passwords (00-99): 100 attempts
   - 3-digit passwords (000-999): 1,000 attempts
   - 4-digit passwords (0000-9999): 10,000 attempts

2. For each password attempt:
   - Tries to extract the ZIP file
   - If successful, displays the password and extracts contents
   - If failed, continues to next combination

3. Upon finding the correct password:
   - Prints the password to console
   - Extracts all files to `./uncompressed_content/`
   - Terminates the search

### Customization Options

#### 1. Change Target ZIP File
Modify line 19 in `zip_cracker.py`:
```python
zip_filename = 'your_actual_file.zip'  # Change to your ZIP filename
```

#### 2. Adjust Password Length Range
Modify line 23 in `zip_cracker.py`:
```python
for length in range(1, 6):  # Now tries lengths 1-5
```

#### 3. Change Character Set
Modify line 18 in `zip_cracker.py`:

**Digits only (default):**
```python
chars = string.digits  # 0-9
```

**Lowercase letters:**
```python
chars = string.ascii_lowercase  # a-z
```

**Uppercase letters:**
```python
chars = string.ascii_uppercase  # A-Z
```

**Letters and digits:**
```python
chars = string.ascii_letters + string.digits  # a-zA-Z0-9
```

**All printable characters:**
```python
chars = string.printable  # Includes letters, digits, punctuation, whitespace
```

#### 4. Change Output Directory
Modify line 33 in `zip_cracker.py`:
```python
zip_ref.extractall(path="custom_output_folder", pwd=found_password.encode('utf-8'))
```

## Algorithm Details

### Brute-Force Strategy
The tool implements a **systematic exhaustive search**:
1. **Iterative deepening**: Tries shorter passwords before longer ones
2. **Cartesian product**: Generates all possible combinations using `itertools.product()`
3. **Early termination**: Stops immediately when correct password is found

### Password Space Calculation
- **1 character**: 10 possibilities (0-9)
- **2 characters**: 100 possibilities (00-99)
- **3 characters**: 1,000 possibilities (000-999)
- **4 characters**: 10,000 possibilities (0000-9999)
- **Total attempts (1-4 chars)**: 11,110 maximum attempts

### Time Complexity
- **Worst-case**: O(N^L) where N=character set size, L=max password length
- For 4-digit passwords: 10^4 = 10,000 attempts
- **Approximate time**: ~0.5-2 seconds for 4-digit numeric passwords on modern hardware

## Testing

### Test with Sample ZIP File
1. Create a test ZIP file with password:
   ```bash
   # On Linux/Mac:
   zip -P 1234 test.zip file1.txt file2.txt
   
   # Or use Python:
   python -c "import zipfile; z = zipfile.ZipFile('test.zip', 'w'); z.write('file.txt'); z.setpassword(b'1234'); z.close()"
   ```

2. Run the script:
   ```bash
   python zip_cracker.py
   ```

### Expected Output
```
Trying passwords of length 1...
Trying passwords of length 2...
Trying passwords of length 3...
Trying passwords of length 4...

Password found: 1234
Files extracted to 'uncompressed_content' directory.
```

## Limitations & Considerations

### Current Limitations
1. **Numeric passwords only** by default (modifiable)
2. **Maximum password length** of 4 in default configuration
3. **No dictionary attack** - only brute force
4. **No multi-threading** - single-threaded execution
5. **No progress percentage** - only shows current length

### Performance Considerations
- **4-digit numeric**: Fast (<2 seconds)
- **6-digit numeric**: 1,111,110 attempts (~1-5 minutes)
- **4-character alphanumeric**: 14,776,336 attempts (~30-60 minutes)
- **6-character alphanumeric**: ~56.8 billion attempts (impractical)

### Security Notes
 **Important Legal Disclaimer:**
- This tool is for **educational purposes only**
- Only use on ZIP files **you own or have explicit permission** to test
- Unauthorized access to computer systems is illegal
- The developers assume no responsibility for misuse

## Extending the Tool

### Add Dictionary Attack
```python
def dictionary_attack(zip_ref, wordlist_file):
    with open(wordlist_file, 'r') as f:
        for word in f:
            password = word.strip()
            if extract_zip(zip_ref, password):
                return password
    return None
```

### Add Multi-threading
```python
from concurrent.futures import ThreadPoolExecutor
import queue

def worker(password_queue, zip_ref):
    while not password_queue.empty():
        password = password_queue.get()
        if extract_zip(zip_ref, password):
            return password
    return None
```

### Add Progress Bar
```python
from tqdm import tqdm

total_attempts = sum(len(chars)**l for l in range(1, max_length+1))
with tqdm(total=total_attempts, desc="Brute-forcing") as pbar:
    for length in range(1, max_length+1):
        for guess in itertools.product(chars, repeat=length):
            password = ''.join(guess)
            # ... attempt password ...
            pbar.update(1)
```

## Troubleshooting

### Common Issues

1. **File not found error:**
   ```
   Error: The file 'your_file.zip' was not found
   ```
   **Solution:** Ensure the ZIP file exists in the same directory or update the filename in the script.

2. **Unicode encode error:**
   ```
   UnicodeEncodeError: 'utf-8' codec can't encode character...
   ```
   **Solution:** Use only ASCII characters in the password or modify the encoding.

3. **No password found:**
   ```
   Password not found within the specified character set and length range.
   ```
   **Solution:**
   - Increase the maximum password length
   - Expand the character set
   - Verify the ZIP file uses a numeric password

4. **Extraction fails after password found:**
   **Solution:** Ensure write permissions in the output directory.

### Debug Mode
Add debug prints to see attempted passwords:
```python
print(f"Trying: {password}")  # Add this before extract_zip call
```

## Resources

- [Python zipfile Documentation](https://docs.python.org/3/library/zipfile.html)
- [Python itertools Documentation](https://docs.python.org/3/library/itertools.html)
- [Brute-force Attack Wikipedia](https://en.wikipedia.org/wiki/Brute-force_attack)
- [Computer Fraud and Abuse Act (CFAA)](https://en.wikipedia.org/wiki/Computer_Fraud_and_Abuse_Act)

---

**Remember:** Always use ethical hacking principles. Only test on systems you own or have written permission to test.
