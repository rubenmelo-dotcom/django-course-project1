from pathlib import Path
import sys
# Pega o caminho três níveis acima
root_dir = Path(__file__).resolve().parent.parent.parent.parent

# Adiciona ao sys.path se ainda não estiver lá
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))
from utils.browser import make_edge_browser
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class RecipeBasePageFunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = make_edge_browser('--headless')
        return super().setUp()
    
    def tearDown(self):
        self.browser.quit()
        return super().tearDown()
    
    def sleep(self, seconds=2):
        time.sleep(seconds)
        