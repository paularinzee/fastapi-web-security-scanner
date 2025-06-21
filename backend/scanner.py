import requests
from bs4 import BeautifulSoup
import urllib.parse
import colorama
import re
from concurrent.futures import ThreadPoolExecutor
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import os
from typing import Set, List, Dict

colorama.init()

class WebSecurityScanner:
    def __init__(self, target_url, max_depth=3, delay=1.0):
        self.target_url = target_url
        self.max_depth = max_depth
        self.delay = delay
        self.vulnerabilities: List[Dict[str, str]] = []
        self.target_links: Set[str] = set()

    def extract_links(self, url: str) -> List[str]:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            links = []
            for link in soup.find_all("a"):
                href = link.get("href")
                if href:
                    href = urllib.parse.urljoin(url, href)
                    if self.target_url in href:
                        links.append(href.split("#")[0])
            return links
        except Exception as e:
            print(f"[ERROR] Failed to extract links from {url}: {e}")
            return []

    def crawl(self, url: str, depth: int = 0):
        if depth > self.max_depth or url in self.target_links:
            return
        self.target_links.add(url)
        print(f"[CRAWLING] {url} (depth={depth})")
        links = self.extract_links(url)
        for link in links:
            self.crawl(link, depth + 1)

    def test_sql_injection(self, url: str):
        payload = "' OR '1'='1"
        test_url = f"{url}{'&' if '?' in url else '?'}input={payload}"
        try:
            response = requests.get(test_url)
            if "sql" in response.text.lower() or "syntax" in response.text.lower():
                self._record_vulnerability(url, "Possible SQL Injection")
        except Exception:
            pass

    def test_xss(self, url: str):
        payload = "<script>alert('XSS')</script>"
        test_url = f"{url}{'&' if '?' in url else '?'}input={payload}"
        try:
            response = requests.get(test_url)
            if payload in response.text:
                self._record_vulnerability(url, "Possible XSS")
        except Exception:
            pass

    def test_directory_traversal(self, url: str):
        payload = "../../../../etc/passwd"
        test_url = f"{url}{'&' if '?' in url else '?'}file={payload}"
        try:
            response = requests.get(test_url)
            if "root:" in response.text:
                self._record_vulnerability(url, "Possible Directory Traversal")
        except Exception:
            pass

    def test_csrf(self, url: str):
        try:
            response = requests.get(url)
            if "<form" in response.text.lower() and "csrf" not in response.text.lower():
                self._record_vulnerability(url, "Possible CSRF (No Token in Form)")
        except Exception:
            pass

    def _record_vulnerability(self, url: str, vuln_type: str):
        self.vulnerabilities.append({
            "type": vuln_type,
            "path": url
        })
        print(colorama.Fore.RED + f"[VULNERABILITY] {url} - {vuln_type}" + colorama.Style.RESET_ALL)

    def scan(self):
        self.crawl(self.target_url)
        print("[*] Starting vulnerability scan...")
        with ThreadPoolExecutor(max_workers=10) as executor:
            for link in self.target_links:
                executor.submit(self.test_sql_injection, link)
                executor.submit(self.test_xss, link)
                executor.submit(self.test_directory_traversal, link)
                executor.submit(self.test_csrf, link)

    def generate_pdf_report(self, file_obj=None):
        if file_obj is None:
            filename = f"scan_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            file_obj = open(filename, "wb")
            close_file = True
        else:
            close_file = False

        c = canvas.Canvas(file_obj, pagesize=letter)
        width, height = letter

        y = height - 50
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, f"Scan Report for {self.target_url}")
        y -= 30

        c.setFont("Helvetica", 12)
        if self.vulnerabilities:
            c.drawString(50, y, "Vulnerabilities Found:")
            y -= 20
            for vuln in self.vulnerabilities:
                text = f"- {vuln['type']} at {vuln['path']}"
                c.drawString(60, y, text)
                y -= 20
                if y < 50:
                    c.showPage()
                    y = height - 50
        else:
            c.drawString(50, y, "No vulnerabilities found.")

        c.save()

        if close_file:
            file_obj.close()
