from rest_framework import serializers

class VideoSerializer(serializers.Serializer):
	pk = serializers.IntegerField(read_only=True)
	video = serializers.FileField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    time = serializers.DateTimeField(format=None, input_formats=None)
    compressed_video = serializers.FileField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)

    def create(self, validated_data):
        """
        Create and return a new `Video` instance, given the validated data.
        """
        return Video.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Video` instance, given the validated data.
        """
        instance.video = validated_data.get('video', instance.video)
        instance.title = validated_data.get('title', instance.title)
        instance.time = validated_data.get('time', instance.time)
        instance.compressed_video = validated_data.get('compressed_video', instance.compressed_video)
        instance.save()
        return instance