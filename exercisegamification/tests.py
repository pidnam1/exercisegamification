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
        Profile.objects.create(user = None, first_name = "Mandip", last_name = "Bhadra", age = 20 )
        p = Profile.objects.get(first_name="Mandip")
        PointAchievement.objects.create(author = p, achievement_title="Go Getter", achievement_text = "Run", achievement_threshold = 200)

    def test_get_key(self):
        p = Profile.objects.get(first_name = "Mandip")
        go_getter = PointAchievement.objects.get(achievement_title="Go Getter")
        self.assertEqual(p, go_getter.author)

class PointsTracker(TestCase):
    def setUp(self):
        Profile.objects.create(user = None, first_name = "Mandip", last_name = "Bhadra", age = 20 , points_total = 200)
        p = Profile.objects.get(first_name="Mandip")
        PointAchievement.objects.create(author = p, achievement_title="Go Getter", achievement_text = "Run", achievement_threshold = 200)

    def test_get_achieve(self):
        p = Profile.objects.get(first_name = "Mandip")
        go_getter = PointAchievement.objects.get(achievement_title="Go Getter")
        self.assertEqual(p.points_total, go_getter.achievement_threshold)
class ProfileMaker(TestCase):

    def setUp(self):
        Profile.objects.create(user = None, first_name = "Mandip", last_name = "Bhadra", age = 20 , points_total = 200, weight = 50, bmi = 5, fav_exercise = "Running")

    def test_get_first(self):
        p = Profile.objects.get(first_name = "Mandip")
        self.assertEqual(p.first_name, str(p))
    def test_get_age(self):
        p = Profile.objects.get(first_name = "Mandip")
        self.assertEqual(p.age, 20)
    def test_get_weight(self):
        p = Profile.objects.get(first_name="Mandip")
        self.assertEqual(p.weight, 50)
    def test_get_BMI(self):
        p = Profile.objects.get(first_name="Mandip")
        self.assertEqual(p.bmi, 5)
    def test_get_fav_exercise(self):
        p = Profile.objects.get(first_name="Mandip")
        self.assertEqual(p.fav_exercise, "Running")
