---
title: "Программное расположение элементов на форме"
date: 2012-09-07 00:13
Category: "Программирование"
Tags: Практика программирования 1С
description: "Упрощение программного расположения элементов управления на форме."
---
Иногда есть необходимость расположить табличное поле на форме программно, например когда нужно добавить неизвестное заранее количество закладок, хорошо если нужно просто добавить закладки, тогда можно просто отделаться :
<pre style="color: blue;"><code class="_1c8">ЭлементыФормы<span style="color: red;">.</span>ПанельСЗакладками<span style="color: red;">.</span>Страницы<span style="color: red;">.</span>Добавить<span style="color: red;">(</span><span style="color: black;">"ЗакладкаСклад"</span><span style="color: red;">+</span>Склад<span style="color: red;">.</span>НомерСклада<span style="color: red;">,</span> Склад<span style="color: red;">.</span>Наименование<span style="color: red;">)</span><span style="color: red;">;</span></code></pre>

но на закладках должно, что то располагаться и это что то, должно иметь размеры, располагаться в конкретно указанном месте у него,  у него должны быть привязки, определены какие то свойства(которых прошу заметить может быть много) и тд, конечно самый логичный способ это нарисовать образец на форме а потом смотря свойства, просто это все перетащить. Должен получиться какой-то такой код:
<pre style="color: blue;"><code class="_1c8">ЭлементыФормы<span style="color: red;">.</span>ПанельСЗакладками<span style="color: red;">.</span>Страницы<span style="color: red;">.</span>Добавить<span style="color: red;">(</span><span style="color: black;">"ЗакладкаСклад"</span><span style="color: red;">+</span>Склад<span style="color: red;">.</span>НомерСклада<span style="color: red;">,</span> Склад<span style="color: red;">.</span>Наименование<span style="color: red;">)</span><span style="color: red;">;</span>
ЭлементыФормы<span style="color: red;">.</span>ПанельСЗакладками<span style="color: red;">.</span>ТекущаяСтраница <span style="color: red;">=</span> ЭлементыФормы<span style="color: red;">.</span>ПанельСЗакладками<span style="color: red;">.</span>Страницы<span style="color: red;">[</span><span style="color: black;">"ЗакладкаСклад"</span><span style="color: red;">+</span>Склад<span style="color: red;">.</span>НомерСклада<span style="color: red;">]</span><span style="color: red;">;</span>
ТабличноеПоле <span style="color: red;">=</span> ЭлементыФормы<span style="color: red;">.</span>Добавить<span style="color: red;">(</span>Тип<span style="color: red;">(</span><span style="color: black;">"ТабличноеПоле"</span><span style="color: red;">)</span><span style="color: red;">,</span><span style="color: black;">"ТабличноеПоле"</span><span style="color: red;">+</span>Склад<span style="color: red;">.</span>НомерСклада<span style="color: red;">,</span><span style="color: red;">Истина</span><span style="color: red;">,</span>ЭлементыФормы<span style="color: red;">.</span>ПанельСЗакладками<span style="color: red;">)</span><span style="color: red;">;</span>
ТабличноеПоле<span style="color: red;">.</span>Имя <span style="color: red;">=</span> <span style="color: black;">"ТабличноеПоле"</span><span style="color: red;">+</span>Склад<span style="color: red;">.</span>НомерСклада<span style="color: red;">;</span>
ТабличноеПоле<span style="color: red;">.</span>Значение <span style="color: red;">=</span> ДвиженияПоСкладам<span style="color: red;">[</span>ТекущийСклад<span style="color: red;">]</span><span style="color: red;">;</span>
ТабличноеПоле<span style="color: red;">.</span>Верх <span style="color: red;">=</span> <span style="color: black;">6</span><span style="color: red;">;</span>
ТабличноеПоле<span style="color: red;">.</span>Высота <span style="color: red;">=</span> <span style="color: black;">566</span><span style="color: red;">;</span>
ТабличноеПоле<span style="color: red;">.</span>Ширина <span style="color: red;">=</span> <span style="color: black;">747</span><span style="color: red;">;</span>
ТабличноеПоле<span style="color: red;">.</span>Лево <span style="color: red;">=</span> <span style="color: black;">6</span><span style="color: red;">;</span>
ТабличноеПоле<span style="color: red;">.</span>ВертикальнаяПолосаПрокрутки <span style="color: red;">=</span> ИспользованиеПолосыПрокрутки<span style="color: red;">.</span>Использоватьавтоматически<span style="color: red;">;</span>
ТабличноеПоле<span style="color: red;">.</span>Вывод <span style="color: red;">=</span> ИспользованиеВывода<span style="color: red;">.</span>Авто<span style="color: red;">;</span>
ТабличноеПоле<span style="color: red;">.</span>ВысотаПодвала <span style="color: red;">=</span> <span style="color: black;">1</span><span style="color: red;">;</span>
ТабличноеПоле<span style="color: red;">.</span>ВысотаШапки <span style="color: red;">=</span> <span style="color: black;">1</span><span style="color: red;">;</span>
ТабличноеПоле<span style="color: red;">.</span>ГоризонтальнаяПолосаПрокрутки <span style="color: red;">=</span> ИспользованиеПолосыПрокрутки<span style="color: red;">.</span>Использоватьавтоматически<span style="color: red;">;</span>
ТабличноеПоле<span style="color: red;">.</span>ГоризонтальныеЛинии <span style="color: red;">=</span> <span style="color: red;">Истина</span><span style="color: red;">;</span>
ТабличноеПоле<span style="color: red;">.</span>ПорядокОтображения <span style="color: red;">=</span> <span style="color: black;">1</span><span style="color: red;">;</span>
ТабличноеПоле<span style="color: red;">.</span>УстановитьПривязку<span style="color: red;">(</span>ГраницаЭлементаУправления<span style="color: red;">.</span>Низ<span style="color: red;">,</span>ЭтаФорма<span style="color: red;">.</span>Панель<span style="color: red;">,</span>ГраницаЭлементаУправления<span style="color: red;">.</span>Низ<span style="color: red;">)</span><span style="color: red;">;</span>
ТабличноеПоле<span style="color: red;">.</span>УстановитьПривязку<span style="color: red;">(</span>ГраницаЭлементаУправления<span style="color: red;">.</span>Право<span style="color: red;">,</span>ЭтаФорма<span style="color: red;">.</span>Панель<span style="color: red;">,</span>ГраницаЭлементаУправления<span style="color: red;">.</span>Право<span style="color: red;">)</span><span style="color: red;">;</span>
ТабличноеПоле<span style="color: red;">.</span>ТолькоПросмотр <span style="color: red;">=</span> <span style="color: red;">Ложь</span><span style="color: red;">;</span></code></pre>
Разумеется, переписывать параметры руками, это просто жесть, всегда можно, что то забыть, не учесть,
не заметить, да и не всегда удается угадать какой контрол, какой содержит элемент управления, но тут падам!
К нам на выручку спешит чудесная штука ДекомпиляцияИАнализФорм_4.epf делаем формочку, настраиваем поведение, размеры, стили и прочие нужности,
скармливаем обработке, она генерит нам нужный код, очень приятная вешь, про автора известно что это (MRAK) Роман Ершов, больше я про него ничего не знаю,
он пожелал не раскрывать деталей. Собственно на этом все а кому нужно, может скачать
[обработку](https://googledrive.com/host/0BxFnXEinPWUJckpLWkVCVjc0dUU/ДекомпиляцияИАнализФорм_4.epf) которая поможет вам в нелегких буднях 1сника.
