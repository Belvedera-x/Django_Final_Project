from django.contrib import admin, messages
from .models import User, Housing, Booking, Review
from .enums import Role




@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "role")
    search_fields = ('email', 'username')
    list_filter = ('role',)


@admin.register(Housing)
class HousingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'city',
        'price',
        'number_of_rooms',
        'housing_type',
        'available',
        'ratings_count',
        'owner',
        'created_at',
    )
    list_filter = ('housing_type', 'city', 'available')
    search_fields = ('title', 'description', 'city')
    ordering = ('-created_at',)
    actions = ("toggle_available_action",)

    def _can_toggle(self, user):
        return user.role in {Role.admin.name, Role.tenant.name}

    @admin.action(description="Переключить активное или неактивное")
    def toggle_available_action(self, request, queryset):
        if not self._can_toggle(request.user):
            self.message_user(
                request,
                "У вас нет прав для изменения доступности",
                level=messages.ERROR
            )
            return

        for obj in queryset:
            obj.toggle_available()

    def get_actions(self, request):
        actions = super().get_actions(request)

        if not self._can_toggle(request.user):
            actions.pop("toggle_available_action", None)

        return actions


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'housing',
        'guest',
        'start_date',
        'end_date',
        'status',
    )
    list_filter = ('status',)
    search_fields = ('housing__title', 'guest__email')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'housing',
        'author',
        'rating',
        'created_at',
    )
    list_filter = ('rating',)
    search_fields = ('housing__title', 'author__email', 'text')
