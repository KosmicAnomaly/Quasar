import random

from discord import Activity, ActivityType


class Statuses():
    """Statuses for Quasar"""

    def __init__(self):
        playing = {
            "tag with Sagittarius A*"
        }

        listening_to = {
            "a TED Talk",
            "the Music of the Spheres",
            "the Golden Record"
        }

        watching = {
            "Kurzgesagt",
            "the event horizon",
            "for exoplanets",
            "the Moon landing",
            "space documentaries",
            "astronomical events",
            "a solar eclipse"
        }

        self.activities = []

        for p in playing:
            activity = Activity(type=ActivityType.playing, name=p)
            self.activities.append(activity)

        for l in listening_to:
            activity = Activity(type=ActivityType.listening, name=l)
            self.activities.append(activity)

        for w in watching:
            activity = Activity(type=ActivityType.watching, name=w)
            self.activities.append(activity)

        self.shuffled_iter()

    def shuffled_iter(self):
        copy = self.activities
        random.shuffle(copy)
        self.iter = iter(copy)

    def next_status(self):
        try:
            thisStatus = next(self.iter)
        except StopIteration:
            self.shuffled_iter()
            thisStatus = next(self.iter)
        finally:
            return thisStatus
