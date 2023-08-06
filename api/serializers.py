from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer): # Converts Project fields into JSON objects
    owner = ProfileSerializer(many=False) # Overrides owner field where instead of the object itself we get all the data
    tags = TagSerializer(many=True) # Same as above but for the tags
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, obj): # To add a new field in the JSON object. Must begin with get_
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data