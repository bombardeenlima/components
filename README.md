# Components Scraper

A Python script that scrapes UI component documentation from Shadcn Svelte and Kibo UI websites, collecting component names, descriptions, and installation commands into a unified markdown list.

## Features

- Scrapes Shadcn Svelte components from https://www.shadcn-svelte.com
- Scrapes Kibo UI components from https://www.kibo-ui.com
- Generates a comprehensive markdown file (`list.md`) with all components
- Includes install commands for each component
- Handles rate limiting with delays between requests

## Dependencies

This project requires the following Python packages:

- `requests` - For making HTTP requests
- `beautifulsoup4` - For HTML parsing

Install them using pip:

```bash
pip install requests beautifulsoup4
```

## Usage

Run the scraper script:

```bash
python list.py
```

The script will:

1. Scrape components from both sources
2. Generate `list.md` with all components organized by source
3. Display a summary of found components

## Output

The generated `list.md` file contains:

- Component names and descriptions
- Installation commands for each component
- Organized by source (Shadcn Svelte and Kibo UI)
- Timestamp of generation

## Testing

Run the unit tests:

```bash
python test_list.py
```

Tests cover:

- Markdown file generation
- Content structure validation
- Install command formatting
- Handling of empty descriptions

## License
The code is under GPLv3