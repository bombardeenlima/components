import unittest
import os
import tempfile
import re
from list import write_markdown

class TestListMarkdown(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.test_dir)

    def test_write_markdown_creates_file(self):
        """Test that write_markdown creates the list.md file"""
        sample_components = {
            "Test Source": [
                ("Component A", "Description A", "install command A"),
                ("Component B", "Description B", "install command B")
            ]
        }

        write_markdown(sample_components)

        self.assertTrue(os.path.exists("list.md"))

        with open("list.md", "r", encoding="utf-8") as f:
            content = f.read()
            self.assertGreater(len(content), 0)

    def test_write_markdown_content_structure(self):
        """Test that the markdown file has the expected structure"""
        sample_components = {
            "Test Source": [
                ("Test Component", "A test description", "npx test add component")
            ]
        }

        write_markdown(sample_components)

        with open("list.md", "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("# Unified Component List", content)

        self.assertIn("*Generated on:", content)

        self.assertIn("## Test Source", content)

        self.assertIn("Total components: **1**", content)

        self.assertIn("### Test Component", content)
        self.assertIn("A test description", content)
        self.assertIn("**Install:** `npx test add component`", content)

    def test_write_markdown_multiple_sources(self):
        """Test writing markdown with multiple sources"""
        sample_components = {
            "Source 1": [("Comp1", "Desc1", "cmd1")],
            "Source 2": [("Comp2", "Desc2", "cmd2"), ("Comp3", "Desc3", "cmd3")]
        }

        write_markdown(sample_components)

        with open("list.md", "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("## Source 1", content)
        self.assertIn("Total components: **1**", content)
        self.assertIn("## Source 2", content)
        self.assertIn("Total components: **2**", content)

    def test_write_markdown_empty_description(self):
        """Test handling of components with empty descriptions"""
        sample_components = {
            "Test": [("No Desc Comp", "", "cmd")]
        }

        write_markdown(sample_components)

        with open("list.md", "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("*No description available*", content)

    def test_installation_commands_format(self):
        """Test that installation commands follow expected formats"""
        sample_components = {
            "Shadcn Svelte": [
                ("Accordion", "A vertically stacked set", "npx shadcn-svelte@latest add accordion"),
                ("Button", "Displays a button", "npx shadcn-svelte@latest add button"),
                ("Dialog", "A window overlaid", "npx shadcn-svelte@latest add dialog")
            ],
            "Kibo UI": [
                ("Announcement", "A compound badge", "npx shadcn add @kibo-ui/announcement"),
                ("Avatar Stack", "Stack and overlap avatars", "npx shadcn add @kibo-ui/avatar-stack"),
                ("Banner", "A full-width component", "npx shadcn add @kibo-ui/banner")
            ]
        }

        write_markdown(sample_components)

        with open("list.md", "r", encoding="utf-8") as f:
            content = f.read()

        install_commands = re.findall(r'\*\*Install:\*\*\s*`([^`]+)`', content)
        
        self.assertEqual(len(install_commands), 6)
        
        shadcn_commands = [cmd for cmd in install_commands if 'shadcn-svelte' in cmd]
        self.assertEqual(len(shadcn_commands), 3)
        for cmd in shadcn_commands:
            self.assertTrue(cmd.startswith('npx shadcn-svelte@latest add '))
            parts = cmd.split(' ')
            self.assertEqual(len(parts), 4)  
            slug = parts[3]
            self.assertTrue(slug.replace('-', '').isalnum()) 
            
        kibo_commands = [cmd for cmd in install_commands if '@kibo-ui' in cmd]
        self.assertEqual(len(kibo_commands), 3)
        for cmd in kibo_commands:
            self.assertTrue(cmd.startswith('npx shadcn add @kibo-ui/'))
            self.assertIn('@kibo-ui/', cmd)
            slug_part = cmd.split('@kibo-ui/')[1]
            self.assertTrue(slug_part.replace('-', '').isalnum())  

    def test_all_components_have_install_commands(self):
        """Test that every component listed has an install command"""
        sample_components = {
            "Test Source": [
                ("Comp1", "Desc1", "npx test add comp1"),
                ("Comp2", "Desc2", "npx test add comp2"),
                ("Comp3", "", "npx test add comp3")  
            ]
        }

        write_markdown(sample_components)

        with open("list.md", "r", encoding="utf-8") as f:
            content = f.read()

        component_headers = re.findall(r'^### (.+)$', content, re.MULTILINE)
        self.assertEqual(len(component_headers), 3)

        install_commands = re.findall(r'\*\*Install:\*\*\s*`([^`]+)`', content)
        self.assertEqual(len(install_commands), 3)


if __name__ == "__main__":
    unittest.main()