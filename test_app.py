import unittest
from unittest.mock import patch
from app import ImageSpider


class TestImageSpider(unittest.TestCase):

    def setUp(self):
        self.spider = ImageSpider()

    # Test 1: Extract an image filename
    def test_extract_image_name(self):
        url = "https://example.com/images/photo.jpg"

        result = self.spider.extract_image_name(url)

        self.assertEqual(result, "photo.jpg")

    # Test 2: Extract a website domain
    def test_extract_site_name(self):
        url = "https://example.com/images/photo.jpg"

        result = self.spider.extract_site_name(url)

        self.assertEqual(result, "example.com")

    # Test 3: Extract image links from HTML
    @patch("app.requests.get")
    def test_grab_all_image_links(self, mock_get):
        mock_get.return_value.text = """
            <img src="https://example.com/photo.jpg">
            <img src="//example.com/banner.png">
        """

        result = self.spider.grab_all_image_links(
            "https://example.com"
        )

        expected = [
            "https://example.com/photo.jpg",
            "https://example.com/banner.png"
        ]

        self.assertEqual(result, expected)

    # Test 4: Handle a website containing no images
    @patch("app.requests.get")
    def test_no_image_links(self, mock_get):
        mock_get.return_value.text = """
            <html><p>No images here.</p></html>
        """

        result = self.spider.grab_all_image_links(
            "https://example.com"
        )

        self.assertEqual(result, [])

    # Test 5: Extract absolute website links
    @patch("app.requests.get")
    def test_grab_all_links(self, mock_get):
        mock_get.return_value.text = """
            <a href="https://example.com/about">About</a>
            <a href="https://example.com/contact">Contact</a>
            <a href="/relative">Relative Link</a>
        """

        result = self.spider.grab_all_links(
            "https://example.com"
        )

        expected = [
            "https://example.com",
            "https://example.com/about",
            "https://example.com/contact"
        ]

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()