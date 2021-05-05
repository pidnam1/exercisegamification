from django.test import TestCase
from exercisegamification.models import PointAchievement, Profile


# Create your tests here.

class PointAchievementNameTest(TestCase):

    def setUp(self):
        PointAchievement.objects.create(author = None, achievement_title="Go Getter", achievement_text = "Run", achievement_threshold = 200)

    def test_get_title(self):
        go_getter = PointAchievement.objects.get(achievement_title="Go Getter")
        self.assertEqual(go_getter.achievement_title, str(go_getter))

class PointAchievementForeignKey(TestCase):

    def setUp(self):

        PointAchievement.objects.create(author = None, achievement_title="Go Getter", achievement_text = "Run", achievement_threshold = 200)

    def test_get_title(self):
        go_getter = PointAchievement.objects.get(achievement_title="Go Getter")
        self.assertEqual(go_getter.achievement_title, str(go_getter))
