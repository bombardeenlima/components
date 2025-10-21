import requests
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime, timezone, timedelta
from typing import List, Tuple


def scrape_shadcn_svelte() -> List[Tuple[str, str, str]]:
    print("🔹 Scraping Shadcn Svelte components...")
    base_url = "https://www.shadcn-svelte.com"
    components_url = f"{base_url}/docs/components"
    
    try:
        html = requests.get(components_url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        
        component_links = soup.select("a[href*='/docs/components/']")
        component_slugs = sorted(set(
            a["href"].split("/")[-1]
            for a in component_links
            if a["href"].split("/")[-1] and a["href"].split("/")[-1] != "components"
        ))
        
        components = []
        
        for slug in component_slugs:
            component_url = f"{base_url}/docs/components/{slug}"
            print(f"  Fetching {slug}...")
            
            try:
                comp_html = requests.get(component_url, timeout=10).text
                comp_soup = BeautifulSoup(comp_html, "html.parser")
                
                h1 = comp_soup.find("h1")
                name = h1.text.strip() if h1 else slug.replace("-", " ").title()
                
                description = ""
                if h1:
                    next_elem = h1.find_next("p")
                    if next_elem:
                        description = next_elem.text.strip()
                
                if not description:
                    lead = comp_soup.find("p", class_=lambda x: x and "lead" in x.lower())
                    if lead:
                        description = lead.text.strip()
                
                install_command = ""
                code_blocks = comp_soup.find_all("code")
                
                for code in code_blocks:
                    code_text = code.text.strip()
                    if "npx shadcn-svelte" in code_text and "add" in code_text:
                        install_command = code_text
                        break
                    elif "shadcn-svelte add" in code_text:
                        install_command = code_text
                        break
                
                if not install_command:
                    pre_blocks = comp_soup.find_all("pre")
                    for pre in pre_blocks:
                        pre_text = pre.text.strip()
                        if "npx shadcn-svelte" in pre_text or "shadcn-svelte add" in pre_text:
                            lines = pre_text.split("\n")
                            for line in lines:
                                if "shadcn-svelte" in line and "add" in line:
                                    install_command = line.strip()
                                    break
                            if install_command:
                                break
                
                if not install_command:
                    install_command = f"npx shadcn-svelte@latest add {slug}"
                
                components.append((name, description, install_command))
                print(f"    ✓ {name}")
                
                time.sleep(0.5)
                
            except Exception as e:
                print(f"    ✗ Error fetching {slug}: {e}")
                continue
        
        print(f"✅ Found {len(components)} Shadcn Svelte components\n")
        return components
        
    except Exception as e:
        print(f"❌ Error scraping Shadcn Svelte: {e}\n")
        return []


def scrape_kibo_ui() -> List[Tuple[str, str, str]]:
    print("🔹 Scraping Kibo UI components...")
    base_url = "https://www.kibo-ui.com"
    components_url = f"{base_url}/components"
    
    try:
        html = requests.get(components_url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        
        links = soup.select("a[href^='/components/']")
        slugs = sorted(set(
            a["href"].replace("/components/", "").strip("/")
            for a in links
            if "/components/" in a["href"] and a["href"].replace("/components/", "").strip("/")
        ))
        
        components = []
        
        for slug in slugs:
            component_url = f"{base_url}/components/{slug}"
            print(f"  Fetching {slug}...")
            
            try:
                comp_html = requests.get(component_url, timeout=10).text
                comp_soup = BeautifulSoup(comp_html, "html.parser")
                
                h1 = comp_soup.find("h1")
                name = h1.text.strip() if h1 else slug.replace("-", " ").title()
                
                description = ""
                if h1:
                    next_elem = h1.find_next("p")
                    if next_elem:
                        description = next_elem.text.strip()
                
                if not description:
                    desc_elem = comp_soup.find("p", class_=lambda x: x and any(
                        term in str(x).lower() for term in ["description", "lead", "intro"]
                    ))
                    if desc_elem:
                        description = desc_elem.text.strip()
                
                if not description:
                    main_content = comp_soup.find("main") or comp_soup.find("article")
                    if main_content:
                        first_p = main_content.find("p")
                        if first_p:
                            description = first_p.text.strip()
                
                install_command = ""
                
                code_blocks = comp_soup.find_all("code")
                for code in code_blocks:
                    code_text = code.text.strip()
                    if "npx shadcn" in code_text and "@kibo-ui" in code_text:
                        install_command = code_text
                        break
                    elif "npx shadcn add" in code_text:
                        install_command = code_text
                        break
                
                if not install_command:
                    pre_blocks = comp_soup.find_all("pre")
                    for pre in pre_blocks:
                        pre_text = pre.text.strip()
                        lines = pre_text.split("\n")
                        for line in lines:
                            if "npx shadcn" in line and ("add" in line or "@kibo-ui" in line):
                                install_command = line.strip().lstrip("$").strip()
                                break
                        if install_command:
                            break
                
                if not install_command:
                    for heading in comp_soup.find_all(["h2", "h3", "h4"]):
                        heading_text = heading.text.lower()
                        if "cli" in heading_text or "install" in heading_text:
                            next_code = heading.find_next("code")
                            if next_code:
                                cmd_text = next_code.text.strip()
                                if "npx shadcn" in cmd_text:
                                    install_command = cmd_text
                                    break
                            next_pre = heading.find_next("pre")
                            if next_pre:
                                cmd_text = next_pre.text.strip().split("\n")[0].lstrip("$").strip()
                                if "npx shadcn" in cmd_text:
                                    install_command = cmd_text
                                    break
                
                if not install_command:
                    install_command = f"npx shadcn add @kibo-ui/{slug}"
                
                components.append((name, description, install_command))
                print(f"    ✓ {name}")
                
                time.sleep(0.5)
                
            except Exception as e:
                print(f"    ✗ Error fetching {slug}: {e}")
                continue
        
        print(f"✅ Found {len(components)} Kibo UI components\n")
        return components
        
    except Exception as e:
        print(f"❌ Error scraping Kibo UI: {e}\n")
        return []


def write_markdown(all_components):
    filename = "list.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Unified Component List\n\n")
        lima_tz = timezone(timedelta(hours=-5), 'PET')
        current_time = datetime.now(lima_tz).strftime('%Y-%m-%d %H:%M:%S %Z')
        f.write(f"*Generated on: {current_time}*\n\n")
        
        for source, comps in all_components.items():
            f.write(f"## {source}\n\n")
            f.write(f"Total components: **{len(comps)}**\n\n")
            
            for name, description, cmd in comps:
                f.write(f"### {name}\n\n")
                if description:
                    f.write(f"{description}\n\n")
                else:
                    f.write("*No description available*\n\n")
                f.write(f"**Install:** `{cmd}`\n\n")
                f.write("---\n\n")
    
    print(f"📄 Saved combined list to {os.path.abspath(filename)}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Component Scraper - Shadcn Svelte & Kibo UI")
    print("="*60 + "\n")
    
    shadcn = scrape_shadcn_svelte()
    kibo = scrape_kibo_ui()
    
    all_components = {
        "Shadcn Svelte": shadcn,
        "Kibo UI": kibo
    }
    
    print("\n" + "="*60)
    print("Writing results...")
    print("="*60 + "\n")
    
    write_markdown(all_components)
    
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    print(f"Shadcn Svelte: {len(shadcn)} components")
    print(f"Kibo UI: {len(kibo)} components")
    print(f"Total: {len(shadcn) + len(kibo)} components")
    print("="*60 + "\n")