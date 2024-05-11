# GmailBox Package

This Python package provides a simple interface to fetch emails via the Gmail API based on specific criteria.

## Features

- Retrieve unread emails
- Fetch emails sent to a specific recipient
- Search for emails with specific raw Gmail query terms (e.g., has:attachment)

## Installation

Install this package using pip:

```bash
pip install gmailimbox
```

## Usage
Here is a basic example of how to use the GmailBox to fetch unread emails with attachments:

```python
from gmailimbox import GmailBox

gmail = GmailBox()
emails = gmail.messages(unread=True, raw='has:attachment')
for email in emails:
    print(email)
```

Ensure you have configured your OAuth credentials correctly as described in the project documentation.

## Contributing
Contributions are welcome! Please feel free to submit pull requests or issues to improve the functionality of this package.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Author
Santosh Kumar

GitHub: santoshray02
For more information, visit the GitHub repository.


### 2. LICENSE
```plaintext
MIT License

Copyright (c) 2023 Santosh Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.