from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "myapp/index.html")


# 显示全部主题
@login_required
def topics(request):
    # 只允许用户访问自己的主题
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {"topics": topics}
    return render(request, "myapp/topics.html", context)


# 每个主题的详情
@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {"topic": topic, "entries": entries}
    return render(request, "myapp/topic.html", context)


# 添加新主题，表单
@login_required
def new_topic(request):
    if request.method != "POST":
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('myapp:topics'))
    context = {'form': form}
    return render(request, "myapp/new_topic.html", context)


# 添加主题下面的内容
@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entey = form.save(commit=False)
            new_entey.topic = topic
            new_entey.save()
            return HttpResponseRedirect(reverse('myapp:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'myapp/new_entry.html', context)


# 修改已经添加了的entry
@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != "POST":
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myapp:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'myapp/edit_entry.html', context)
