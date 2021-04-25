from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()
result_test = 0
result_original = 0

def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    fromlanding = request.GET.get('from-landing')
    if fromlanding == 'test':
        counter_click['test'] += 1
    elif fromlanding == 'original':
        counter_click['original'] += 1
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    abtestarg = request.GET.get('ab-test-arg')
    if abtestarg == 'original':
        counter_show['original'] += 1
        return render(request, 'landing.html')
    elif abtestarg == 'test':
        counter_show['test'] += 1
        return render(request, 'landing_alternate.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    result_test = counter_click['test']/counter_show['test']
    result_original = counter_click['original']/counter_show['original']
    return render(request, 'stats.html', context={
        'test_conversion': result_test,
        'original_conversion': result_original,
    })
