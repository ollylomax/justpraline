from django.contrib import admin
from .models import Messages, Review, ProductReview


class MessagesAdmin(admin.ModelAdmin):

    readonly_fields = ('date',)

    fields = (
        'user', 'date', 'first_name',
        'last_name', 'email', 'subject',
        'message',
        )

    list_display = (
        'user', 'date', 'first_name',
        'last_name', 'email', 'subject',
        )


class ReviewAdmin(admin.ModelAdmin):

    readonly_fields = ('date',)

    fields = (
        'user', 'date', 'first_name',
        'last_name', 'is_approved', 'appear_anonymous',
        'review',
        )

    list_display = (
        'user', 'date', 'first_name',
        'last_name', 'is_approved', 'appear_anonymous',
        )


class ProductReviewAdmin(admin.ModelAdmin):

    readonly_fields = ('date',)

    fields = (
        'user', 'product', 'date', 'first_name',
        'last_name', 'is_approved', 'appear_anonymous',
        'product_review',
        )

    list_display = (
        'user', 'product', 'date', 'first_name',
        'last_name', 'is_approved', 'appear_anonymous',
        )


admin.site.register(Messages, MessagesAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
