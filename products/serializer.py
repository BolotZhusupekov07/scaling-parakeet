from django.db import models
from rest_framework import serializers

from .models import (
        Product,
        Comment,
        Pictures,
        Reply,
        Variation
)

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['comment','author', 'content', 'rate', 'creation_date']

class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, source='reply_set')

    class Meta:
        model = Comment
        fields = ["id", "product","author", "rate", "content","creation_date", "replies"]

    def create(self, validated_data):
        replies_data = validated_data.pop("reply_set")
        comment = Comment.objects.create(**validated_data)

        for reply in replies_data:
            Reply.objects.create(comment=comment, **reply)
        
        return comment
    def update(self, instance, validated_data):
        replies_data = validated_data.pop("reply_set")
        replies = (instance.reply_set).all()
        replies = list(replies)

        instance.author = validated_data.get("author", instance.author)
        instance.rate = validated_data.get("rate", instance.rate)
        instance.content = validated_data.get("content", instance.content)
        instance.save()

        for reply_data in replies_data:
            reply = replies.pop(0)
            reply.author = reply_data.get("author", reply.author)
            reply.rate = reply_data.get("rate", reply.rate)
            reply.content = reply_data.get("content", reply.content)
            reply.save()
        return instance


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictures
        fields = ["id", "image_url"]


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = ["id", "title", "price", "discount", "creation_date"]
  

class ProductSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True, source="pictures_set")
    comments = CommentSerializer(many=True, source="comment_set")

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "creation_date",
            "pictures",
            "price",
            "discount",
            "supplier",
            "category",
            "comments",
        ]

    def create(self, validated_data):
        comments_data = validated_data.pop("comment_set")
        images_data = validated_data.pop("pictures_set")

        product = Product.objects.create(**validated_data)

        for image in images_data:
            Pictures.objects.create(product=product, **image)

        for comment in comments_data:
            replies_data = comment.pop('reply_set')
            comment = Comment.objects.create(
                product=product,
                author=comment["author"],
                rate=comment["rate"],
                content=comment["content"],
            )
            for reply in replies_data:
                Reply.objects.create(comment=comment, **reply)

        Variation.objects.create(
            product=product, title=product.title, price=product.price, discount=product.discount
        )
        return product

    def update(self, instance, validated_data):
        comments_data = validated_data.pop("comment_set")
        comments = (instance.comment_set).all()
        comments = list(comments)

        pictures_data = validated_data.pop("pictures_set")
        pictures = (instance.pictures_set).all()
        pictures = list(pictures)

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description",
                                                  instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.discount = validated_data.get("discount", instance.discount)
        instance.supplier = validated_data.get("supplier", instance.supplier)
        instance.category = validated_data.get("category", instance.category)
        instance.save()

        Variation.objects.create(
            product=instance, title=instance.title, price=instance.price, 
            discount=instance.discount
        )

        for comment_data in comments_data:
            comment = comments.pop(0)
            comment.author = comment_data.get("author", comment.author)
            comment.rate = comment_data.get("rate", comment.rate)
            comment.content = comment_data.get("content", comment.content)
            comment.save()

        for picture_data in pictures_data:
            picture = pictures.pop(0)
            picture.image_url = picture_data.get("image_url",
                                                 picture.image_url)
            picture.save()

        return instance
