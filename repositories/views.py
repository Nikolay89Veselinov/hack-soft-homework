from ast import Num
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.http import HttpResponse
from datetime import timedelta, date

from .models import Repository, ViewRepository
from users.models import User


def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
      yield date1 + timedelta(n)


def get_view_lass_two_week(dict):
  count_per_day = []
  uniques_per_day = []
  index = 0
  
  for index in range(len(dict['views'])):
    for k, v in dict['views'][index].items():
      if k == 'timestamp':
        count_per_day.append(int(dict['views'][index]['count']))
        uniques_per_day.append(int(dict['views'][index]['uniques']))
  return count_per_day, uniques_per_day


def filter_start_date(dict, start_date):
  for index in range(len(dict['views'])):
    for k, v in dict['views'][index].items():
      if k == 'timestamp':
        if start_date in dict['views'][index][k]:
          return index
  return 0


def filter_end_date(dict, index, end_date):
  count = 0
  uniques = 0
  count_per_day = []
  uniques_per_day = []

  for x in range(index, len(dict['views'])):
    for k, v in dict['views'][x].items():
      if k == 'timestamp':
        count += int(dict['views'][x]['count'])
        uniques += int(dict['views'][x]['uniques'])
        count_per_day.append(int(dict['views'][x]['count']))
        uniques_per_day.append(int(dict['views'][x]['uniques']))
        if end_date in dict['views'][x][k]:
          return count, uniques, count_per_day, uniques_per_day
  return count, uniques, count_per_day, uniques_per_day


def repos_list(request, user_token):
  context = {}
  try:
    user = User.objects.get(token=user_token)
    repos = user.repository_set.all()
    context.update({
        'repos': repos
    })
  except User.DoesNotExist:
    return HttpResponse("<p>The user doesn't exist</p>")
  return render(request, 'partials/repos_list.html', context)
from datetime import datetime


def repo_detail(request, user_token, repository_id):
    context = {}
    today = date.today()
    last_two_weeks = []
    start_dt = today - timedelta(13)
    end_dt = today
    view_json = ViewRepository.objects.last()
    view = json.loads(view_json.the_json)

    try:
      user = User.objects.get(token=user_token)
      repo = Repository.objects.get(pk=repository_id)
    except User.DoesNotExist:
      return HttpResponse("<p>The user doesn't exist</p>")
    except Repository.DoesNotExist:
      return HttpResponse("<p>The repository doesn't exist</p>")

    if repo.user == user:
      context.update({
      'repo': repo,
      })
    else:
      context.update({
      'no_exist': True,
      })

    for dt in daterange(start_dt, end_dt):
      last_two_weeks.append(dt.strftime("%Y-%d-%-m"))
    count_per_day, uniques_per_day = get_view_lass_two_week(view)
    context.update({
      'last_two_weeks': mark_safe(DjangoJSONEncoder().encode(last_two_weeks)),
      'views': view['count'],
      'uniques': view['uniques'],
      'count_per_day': count_per_day,
      'uniques_per_day': uniques_per_day,
      })

    try:
      start_date = request.GET['start']
      end_date = request.GET['end']
      start_index = filter_start_date(view, start_date)

      count_view, uniques, count_per_day, uniques_per_day = filter_end_date(view, start_index, end_date)
      date_start_view = datetime.strptime(start_date, '%Y-%d-%m')
      date_start_period = datetime.strptime(last_two_weeks[0], '%Y-%d-%m')
      start_date_view = date_start_view - date_start_period
      date_end_view = datetime.strptime(end_date, '%Y-%d-%m')
      date_end_period = datetime.strptime(last_two_weeks[-1], '%Y-%d-%m')
      end_date_view = date_end_period - date_end_view

      for count in range(0, start_date_view.days):
        count_per_day.insert(0, '')
        uniques_per_day.insert(0, '')

      for count in range(0, end_date_view.days):
        count_per_day.append('')
        uniques_per_day.append('')

      context.update({
          'last_two_weeks': mark_safe(DjangoJSONEncoder().encode(last_two_weeks)),
          'views': count_view,
          'uniques': uniques,
          'count_per_day': mark_safe(count_per_day),
          'uniques_per_day': mark_safe(uniques_per_day),
      })
    except MultiValueDictKeyError:
      pass
    return render(request, 'partials/repo_detail.html', context)
