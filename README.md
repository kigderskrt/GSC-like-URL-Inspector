# Google Search Console-Inspired URL Inspector

A Python GUI application that simulates Google Search Console's URL inspection functionality, checking indexing status and providing detailed troubleshooting information.

![Application Screenshot](screenshot.png)

## Features

- **GSC-like Interface**: Familiar tabbed interface similar to Google Search Console
- **Indexing Status Check**: Simulates checking if URL is indexed by Google
- **Detailed Reports**: Provides crawl date, rendering status, robots.txt check, and more
- **Troubleshooting Guide**: Explains why URLs might not be indexed with actionable solutions
- **Open in GSC**: Direct link to check the URL in real Google Search Console

## Prerequisites

- Python 3.6 or higher
- pip package manager

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gsc-inspector.git
   cd gsc-inspector
2. pip install -r requirements.txt
3. pip install requests beautifulsoup4 fake-useragent

Usage
Enter the full URL you want to inspect in the search bar

Click "Inspect URL"

View results in the Coverage tab:

Indexing status (green checkmark if indexed)

Last crawl information

Page availability checks

Indexing permission analysis

Read troubleshooting advice if the URL isn't indexed

Click "Open in Google Search Console" to check the real status

Understanding the Results
Indexing Status
✅ URL is on Google: Page is properly indexed

⚠️ URL is not on Google: Page found but not indexed (with reason)

❌ URL is not on Google: Page blocked or unavailable

Common Issues
Blocked by robots.txt: Update your robots.txt file

Noindex tag detected: Remove noindex meta tag

Page not found (404): Fix the URL or implement redirects

Discovered - not indexed: Improve internal linking or request indexing

Limitations
⚠️ Note: This is a simulation tool that demonstrates possible indexing scenarios. For actual indexing status, please use:

Google Search Console

The site: operator in Google search

Official Google Search Console API

Future Enhancements
Integration with real Google Search Console API

Mobile usability checks

Schema markup validation

AMP page validation

Bulk URL checking

Contributing
Contributions are welcome! Please open an issue or submit a pull request.
