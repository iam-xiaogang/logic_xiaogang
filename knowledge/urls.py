from django.urls import path
from .views import (
    KnowledgeDetailView, KnowledgeCreateView,
    KnowledgeUpdateView, KnowledgeDeleteView, KnowledgeViewCountIncrease,
    CategoryArticleListView,CommentListCreateView
)

urlpatterns = [
    # path('', KnowledgeListView.as_view(), name='knowledge-list'),
    path('', CategoryArticleListView.as_view()),
    path('create/', KnowledgeCreateView.as_view(), name='knowledge-create'),
    path('<int:id>/', KnowledgeDetailView.as_view(), name='knowledge-detail'),
    path('comment/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('<int:pk>/update/', KnowledgeUpdateView.as_view(), name='knowledge-update'),
    path('<int:pk>/delete/', KnowledgeDeleteView.as_view(), name='knowledge-delete'),
    path('<int:pk>/vc/', KnowledgeViewCountIncrease.as_view(), name='knowledge-vc'),
]
