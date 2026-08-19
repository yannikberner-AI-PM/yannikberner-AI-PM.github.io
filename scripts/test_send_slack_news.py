import importlib.util
import unittest
from pathlib import Path


def load_news():
    path = Path(__file__).with_name("send_slack_news.py")
    spec = importlib.util.spec_from_file_location("send_slack_news", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


CASES = [
    ("Bundesnetzagentur startet Konsultation zur Reform der Netzentgeltsystematik Strom", "energy"),
    ("Überzeichnung der Ausschreibung für PV-Freiflächenanlagen", "energy"),
    ("Streit um Deutschlands Stromreserve", "energy"),
    ("Peter Thiel steigt bei Argentiniens größtem Öl-Exporteur ein", None),
    ("Lufthansa und Air France geben Angebote für TAP ab", None),
    ("Rente: Traumland im Ruhestand", None),
    ("Bundesnetzagentur legt Bedingungen für Leerrohre der Telekom fest", None),
    ("How we redesigned our B2B platform API for enterprise customers", "pm"),
    ("Build an AI code review bot in 30 minutes", None),
]


class ClassifyTitleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.news = load_news()

    def test_spec_fixtures(self):
        for title, expected in CASES:
            with self.subTest(title=title):
                self.assertEqual(self.news.classify_title(title), expected)


class SelectItemsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.news = load_news()

    def test_energy_before_pm_and_caps(self):
        candidates = [
            (f"B2B platform API item {i}", f"https://pm/{i}", "PM")
            for i in range(4)
        ] + [
            (f"Stromnetz Reform {i}", f"https://en/{i}", "Energy")
            for i in range(10)
        ]
        selected = self.news.select_items(candidates, already_sent=set())
        self.assertLessEqual(len(selected), 8)
        pm_count = sum(
            1 for title, _, _ in selected if self.news.classify_title(title) == "pm"
        )
        self.assertLessEqual(pm_count, 2)
        kinds = [self.news.classify_title(t) for t, _, _ in selected]
        if "pm" in kinds and "energy" in kinds:
            self.assertLess(kinds.index("energy"), kinds.index("pm"))

    def test_skips_already_sent_and_offtopic(self):
        candidates = [
            ("Lufthansa Streik", "https://x/1", "HB"),
            ("Stromreserve Streit", "https://x/2", "HB"),
            ("Stromreserve Streit copy", "https://x/2", "HB"),
        ]
        selected = self.news.select_items(candidates, already_sent={"https://x/2"})
        self.assertEqual(selected, [])


class SourceAndHeaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.news = load_news()

    def test_handelsblatt_energie_not_schlagzeilen(self):
        urls = [url for _, url, _ in self.news.FEEDS]
        self.assertIn("https://www.handelsblatt.com/contentexport/feed/energie", urls)
        self.assertTrue(all("schlagzeilen" not in u for u in urls))
        self.assertTrue(all("tagesschau.de" not in u for u in urls))
        self.assertTrue(all("lennysnewsletter.com" not in u for u in urls))
        self.assertTrue(all("saastr.com" not in u for u in urls))
        self.assertTrue(all("mindtheproduct.com" not in u for u in urls))

    def test_required_new_feeds(self):
        urls = [url for _, url, _ in self.news.FEEDS]
        self.assertIn("https://www.cleanenergywire.org/rss.xml", urls)
        self.assertTrue(any("RSSNewsfeed_Pressemitteilungen.xml" in u for u in urls))
        self.assertTrue(any("RSSNewsfeed_EEG.xml" in u for u in urls))

    def test_header_constant(self):
        self.assertEqual(self.news.SLACK_HEADER, "*Energie-News*")


if __name__ == "__main__":
    unittest.main()
