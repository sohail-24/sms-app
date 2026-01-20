import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Capture key UI screenshots for the user manual using Playwright (headless)."

    def add_arguments(self, parser):
        parser.add_argument("--base-url", default="http://127.0.0.1:8000", help="Site base URL")

    def handle(self, *args, **options):
        try:
            from playwright.sync_api import sync_playwright
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(
                    "Playwright is not installed. Run: pip install playwright && playwright install"
                )
            )
            return

        base_url = options["base_url"].rstrip("/")
        out_dir = os.path.join("accounts", "static", "accounts", "images", "manual")
        os.makedirs(out_dir, exist_ok=True)

        def save(page, name):
            path = os.path.join(out_dir, f"{name}.png")
            page.screenshot(path=path, full_page=True)
            self.stdout.write(self.style.SUCCESS(f"Saved {path}"))

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1366, "height": 768})
            page = context.new_page()

            # Login page
            page.goto(f"{base_url}/login/")
            save(page, "login")

            # Admin login
            page.click("#admin-tab")
            page.fill("#username-admin", "admin_manual")
            page.fill("#password-admin", "AdminPass123!")
            page.click("text=Login as Admin")
            page.wait_for_url(f"{base_url}/dashboard/")
            save(page, "dashboard")

            # Teachers list
            page.click("text=Teachers")
            page.wait_for_url(f"{base_url}/teachers/")
            save(page, "teachers")

            # Students list
            page.click("text=Students")
            page.wait_for_url(f"{base_url}/students/")
            save(page, "students")

            # Courses list
            page.click("text=Courses")
            page.wait_for_url(f"{base_url}/courses/")
            save(page, "courses")

            # Calendar
            page.click("text=Calendar")
            page.wait_for_url(f"{base_url}/calendar/")
            save(page, "calendar")

            # Reports hub
            page.click("text=Reports")
            page.wait_for_url(f"{base_url}/reports/")
            save(page, "reports")

            browser.close()

        self.stdout.write(self.style.SUCCESS("Screenshots captured."))


