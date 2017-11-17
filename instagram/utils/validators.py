from rest_framework import serializers


def phone_number(value):
    value = value.replace('-', '')
    if not value.isnumeric():
        raise serializers.ValidationError('숫자로 이루어져있지 않습니다.')
    if len(value) != 10 or len(value) != 11:
        raise serializers.ValidationError('전화번호 길이가 올바르지 않습니다.')
    if not value.starswith('0'):
        raise serializers.ValidationError('전화번호는 0으로 시작해야 합니다.')


def sms_length(value):
    encoded_str = value.encode('cp949')
    if len(encoded_str) > 90:
        raise serializers.ValidationError(
            f'90자 까지만 전송할 수 있습니다. (요청길이 {len(encoded_str)})')
