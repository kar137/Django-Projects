from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

# Model for Topics related to rooms
class Topic(models.Model):
    name = models.CharField(max_length=200)  # Name of the topic, limited to 200 characters

    def __str__(self):
        return self.name  # Return the topic name as its string representation

# Model for Rooms where users can interact
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Host of the room (can be null if the host is deleted)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)  # Associated topic for the room (can be null if the topic is deleted)
    name = models.CharField(max_length=200)  # Name of the room, limited to 200 characters
    description = models.TextField(null=True, blank=True)  # Optional description for the room
    # participants = # Placeholder for participants functionality
    updated = models.DateTimeField(auto_now=True)  # Timestamp for the last update (auto-updates on save)
    created = models.DateTimeField(auto_now_add=True)  # Timestamp for when the room was created (auto-set on creation)

    class Meta:
        ordering = ['-updated', '-created']  # Order rooms by most recently updated or created

    def __str__(self):
        return self.name  # Return the room name as its string representation

# Model for Messages within rooms
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who sent the message (deletes message if user is deleted)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Room where the message was sent (deletes message if room is deleted)
    body = models.TextField()  # The text content of the message
    updated = models.DateTimeField(auto_now=True)  # Timestamp for the last update (auto-updates on save)
    created = models.DateTimeField(auto_now_add=True)  # Timestamp for when the message was created (auto-set on creation)

    def __str__(self):
        return self.body[0:50]  # Return the first 50 characters of the message body as its string representation

