from django.utils.translation import gettext, gettext_lazy as _
from rest_framework import serializers

from apps.review.models import Review, ReviewComment
from apps.contrib.serializers import MetaInformationSerializerMixin

NOT_ALLOWED_TO_REVIEW = _('You are not allowed to review this entry.')


class ReviewSerializer(MetaInformationSerializerMixin,
                       serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewCommentSerializer(MetaInformationSerializerMixin,
                              serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = ReviewComment
        fields = '__all__'

    def validate_reviews(self, reviews):
        if len(reviews) != len(set([tuple([
            each.get(field) for field in Review.UNIQUE_TOGETHER_FIELDS
        ]) for each in reviews])):
            raise serializers.ValidationError(
                gettext('Unique reviews are expected from a single comment.')
            )
        return reviews

    def validate(self, attrs) -> dict:
        if not attrs['entry'].reviewers.filter(id=self.context['request'].user.id).exists():
            raise serializers.ValidationError(NOT_ALLOWED_TO_REVIEW)
        return super().validate(attrs)

    def create(self, validated_data):
        reviews_data = validated_data.pop('reviews', [])
        review_comment = super().create(validated_data)
        Review.objects.bulk_create([
            Review(
                **review,
                created_by_id=review_comment.created_by.id,
                entry_id=review_comment.entry.id,
                comment_id=review_comment.id
            )
            for review in reviews_data
        ])
        return review_comment
