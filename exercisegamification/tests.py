from django.test import TestCase, RequestFactory
from exercisegamification.models import PointAchievement, Profile, Goal, Workout, Relationship
from datetime import datetime
from exercisegamification import views

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
class ProfileMakerInfo1(TestCase):

    def setUp(self):
        Profile.objects.create(user = None, first_name = "Mandip", last_name = "Bhadra", age = 20 , points_total = 200, weight = 50, bmi = 5, fav_exercise = "Running")

    def test_get_age(self):
        p = Profile.objects.get(first_name = "Mandip")
        self.assertEqual(p.age, 20)
    def test_get_weight(self):
        p = Profile.objects.get(first_name="Mandip")
        self.assertEqual(p.weight, 50)
class ProfileMakerInfo2(TestCase):

    def setUp(self):
        Profile.objects.create(user = None, first_name = "Mandip", last_name = "Bhadra", age = 20 , points_total = 200, weight = 50, bmi = 5, fav_exercise = "Running")

    def test_get_first(self):
        p = Profile.objects.get(first_name = "Mandip")
        self.assertEqual(p.first_name, str(p))
    def test_get_last(self):
        p = Profile.objects.get(last_name = "Bhadra")
        self.assertEqual(p.last_name, "Bhadra")
class ProfileMakerInfo3(TestCase):

    def setUp(self):
        Profile.objects.create(user = None, first_name = "Mandip", last_name = "Bhadra", age = 20 , points_total = 200, weight = 50, bmi = 5, fav_exercise = "Running")

    def test_get_BMI(self):
        p = Profile.objects.get(first_name="Mandip")
        self.assertEqual(p.bmi, 5)
    def test_get_fav_exercise(self):
        p = Profile.objects.get(first_name="Mandip")
        self.assertEqual(p.fav_exercise, "Running")
class ProfileMakerInfo4(TestCase):

    def setUp(self):
        Profile.objects.create(user = None, first_name = "3240", last_name = "@!/*", age = 20 , points_total = 200, weight = 50, bmi = 5, fav_exercise = "Running")

    def test_get_first(self):
        p = Profile.objects.get(first_name = "3240")
        self.assertEqual(p.first_name, str(p))
    def test_get_last(self):
        p = Profile.objects.get(last_name = "@!/*")
        self.assertEqual(p.last_name, "@!/*")
class GoalConnectedtoProfileTestCase(TestCase):
    def setUp(self):
        Profile.objects.create(user = None, first_name="m", last_name="t", age=12, weight=100, bmi=2, fav_exercise="swim", )
        p = Profile.objects.get(first_name="m")
        Goal.objects.create(author=p, title="test", pub_date="2021-05-03", reach_date= datetime.now(), goal_text="testing", accomplished=True)
    def test_get_goal_author(self):
        goal = Goal.objects.get(title="test")
        profile = Profile.objects.get(first_name="m")
        self.assertEqual(goal.author, profile)


class GoalCreationTestCase(TestCase):
    def setUp(self):
        Goal.objects.create(title="test", pub_date="2021-05-03", reach_date=datetime.now(), goal_text="testing", accomplished=True)
    def test_get_goal_name(self):
        goal = Goal.objects.get(title="test")
        self.assertEqual(goal.goal_text, "testing")


class WorkoutPointsTest(TestCase):
    def setUp(self):
        Workout.objects.create(workout_title="Abs", workout_type="Calisthenics", workout_description="50 crunches", points=30)
    def test_get_goal_points(self):
        workout = Workout.objects.get(workout_title="Abs")
        self.assertEqual(workout.points, 30)


class RelationshipAcceptedRequest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        self.user2= User.objects.create_user(username='testuser2', password='12345')
        testprofile1 = Profile.objects.create(user=self.user1, first_name="Joe", last_name="Smith", age=20, points_total=200, weight=50,
                               bmi=5, fav_exercise="Running")
        testprofile2 = Profile.objects.create(user=self.user2, first_name="Bob", last_name="Smith", age = 20 , points_total = 200,
                                       weight = 50, bmi = 5, fav_exercise = "Running")
        Relationship.objects.create(sender=testprofile1, receiver=testprofile2, status='accepted')

    def accepted_request(self):
        self.assertEqual(testprofile1.friends.count(), 1)
        self.assertEqual(testprofile2.friends.count(), 1)


class RelationshipPendingRequest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        self.user2= User.objects.create_user(username='testuser2', password='12345')
        testprofile1 = Profile.objects.create(user=self.user1, first_name="Joe", last_name="Smith", age=20, points_total=200, weight=50,
                               bmi=5, fav_exercise="Running")
        testprofile2 = Profile.objects.create(user=self.user2, first_name="Bob", last_name="Smith", age = 20 , points_total = 200,
                                       weight = 50, bmi = 5, fav_exercise = "Running")
        Relationship.objects.create(sender=testprofile1, receiver=testprofile2, status='pending')

    def pending_request(self):
        user1_friend_requests = Relationship.objects.invatations_received(testprofile1)
        user2_friend_requests = Relationship.objects.invatations_received(testprofile2)

        self.assertEqual(user1_friend_requests.count(), 1)
        self.assertEqual(user2_friend_requests.count(), 1)
 

class WorkoutPointsTest(TestCase):
    def setUp(self):
        Workout.objects.create(workout_title="Abs", workout_type="Calisthenics", workout_description="50 crunches", points=30)
    def test_get_goal_points(self):
        workout = Workout.objects.get(workout_title="Abs")
        self.assertEqual(workout.points, 30)

class WorkoutAuthorTest(TestCase):
    def setUp(self):
        Profile.objects.create(user = None, first_name="John", last_name="T", age=22, weight=175, bmi=18, fav_exercise="Bench",)
        p = Profile.objects.get(first_name = "John")
        Workout.objects.create(author = p, workout_title="Abs", workout_type="Calisthenics", workout_description="50 crunches", points=30, date="2021-05-03")
    def test_workout_get_author(self):
        profile = Profile.objects.get(first_name = "John")
        w = Workout.objects.get(workout_title="Abs")
        self.assertEqual(w.author, profile)

class WorkoutTitleTest(TestCase):
    def setUp(self):
        Workout.objects.create(workout_title="Abs", workout_type="Calisthenics", workout_description="50 crunches", points=30,)
    def setUp(self):
        workout = Workout.objects.get(workout_title="Abs")
        self.assertEqual(workout.workout_title, "Abs")
   

