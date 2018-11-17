---
title: "Двойные штрихкода и история одной обработки"
date: 2013-09-08 22:03
Category: "Программирование"
Tags: Практика программирования 1С, Обработка, Запрос
---
###Преамбула
В какой то момент в базе встала проблема двойных штрихкодов. Причем ситация до того как на нее обратили внимание, приобрела катосторофический характер и имела полторы тысячи дублей штрихкодов (когда один штрихкод принадлежит нескольким товарам) и порядка 25ти тысяч дублей товаров (когда у одного товарам есть несколько штрихкодов). Что тому виной? На текущий момент уже сложно сказать. Возможно РИБ, когда одному и тому же товару присваивают штрихкод в разных базах. Возможно свою лепту внесли слияния нескольких баз с одинаковым товаром, но разными штрихкодами. Скорее всего все вместе + какой то еще фактор, который мы пока не можем найти. Слишком много вышло дублей, почти четверть базы. Так или иначе встала задача с этими штрихкодами что то сделать.

###Постановка задачи.
Необходимо найти задублирововашиеся штрихкода и показить пользователю в удобном виде. Дать возможность что то сделать сразу с этими штрихкодами без необходимости лазить по справочникам и регистрам. Если говорить конкретно, то у пользователя должна быть возможность:

1. Удалить все штрихкода у владельца, кроме выделенного.
2. Удалить конкретный лишний штрихкод.
3. Одним махом удалить все лишние дубли, оставив по одному на владельца.
4. Удалить все штрихкода которые засветились как задублированные.

###Приступим к реализации первой части.
Поиск лишних штрихкодов. Сам поиск достататочно банален: нужно воспользоваться функций КОЛИЧЕСТВО(РАЗЛИЧНЫЕ СюдаУказатьПолеДляГруппировки). В самом простом случае, запрос будет выглядеть вот так:

<pre style="text-align: left; font-family: courier new,courier; color: black">
<font color=blue>ВЫБРАТЬ
    </font>Штрихкоды.Штрихкод<font color=blue>,
    </font><font color=brown>КОЛИЧЕСТВО</font><font color=blue>(РАЗЛИЧНЫЕ </font>Штрихкоды.Владелец<font color=blue>) КАК </font>Владелец
<font color=blue>ИЗ
    </font>РегистрСведений.Штрихкоды <font color=blue>КАК </font>Штрихкоды
<font color=blue>СГРУППИРОВАТЬ ПО
    </font>Штрихкоды.Штрихкод</pre>
    
Для того, что бы отфильтровать результаты запроса необходимо его обернуть во вложеный запрос и тогда уже можно накладывать условия на результат его работы. В целом нормально, но как то неудобно, для удобства наверно не помешает сгруппировать результаты по штрихкодам. В результате мы можем получить вот такой запрос. Вот результат его работы в консоли.
![Результат работы запроса](https://api.monosnap.com/image/download?id=5e8qdGdh0ss6sMzCTYOarse6J "Результат работы запроса в консоли")
Этот вариант удобен для первого варианта поиска, сделать запрос для второго варианта по аналогии не должно составить труда. Запросы готовы, но не будет же пользователь смотреть на результат его работы из консоли. Здесь нам и поможет дерево значений. Смысл работы с деревом следующий: дерево содержит колекцию колонок и строк. Коллекция колонок не отличается от коллекции колонок в таблице значений и нас не интересует. Коллекция строк немного инетереснее, каждая строка ее может содержать такую же коллекцию строк, каждая строка которой... вообщем я думаю мысль понятна, таким образом и организуется иерархия. Используем обход результатов запроса по группировкам, для того что сформировать удобное дерево:
<pre style="color: blue;"><code class="_1c8">Выборка <span style="color: red;">=</span> Запрос<span style="color: red;">.</span><span style="color: red;">Выполнить</span><span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">.</span>Выбрать<span style="color: red;">(</span>ОбходРезультатаЗапроса<span style="color: red;">.</span>ПоГруппировкам<span style="color: red;">)</span><span style="color: red;">;</span>
ЭтаФорма<span style="color: red;">.</span>Заголовок <span style="color: red;">=</span> <span style="color: black;">"Найдено "</span> <span style="color: red;">+</span> Выборка<span style="color: red;">.</span>Количество<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
<span style="color: red;">Пока</span> Выборка<span style="color: red;">.</span>Следующий<span style="color: red;">(</span><span style="color: red;">)</span> <span style="color: red;">Цикл</span>	
	НоваяСтрокаТП <span style="color: red;">=</span> ТабличноеПоле<span style="color: red;">.</span>Строки<span style="color: red;">.</span>Добавить<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>	
	НоваяСтрокаТП<span style="color: red;">.</span>Номенклатура <span style="color: red;">=</span> Выборка<span style="color: red;">.</span>Штрихкод<span style="color: red;">;</span>	
	ВыборкаШтрихКода <span style="color: red;">=</span> Выборка<span style="color: red;">.</span>Выбрать<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>	
	<span style="color: red;">Пока</span> ВыборкаШтрихКода<span style="color: red;">.</span>Следующий<span style="color: red;">(</span><span style="color: red;">)</span> <span style="color: red;">Цикл</span>		
		НоваяСтрокаВладелец <span style="color: red;">=</span> НоваяСтрокаТП<span style="color: red;">.</span>Строки<span style="color: red;">.</span>Добавить<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>		
		НоваяСтрокаВладелец<span style="color: red;">.</span>Номенклатура <span style="color: red;">=</span> ВыборкаШтрихКода<span style="color: red;">.</span>Владелец<span style="color: red;">;</span>		
	<span style="color: red;">КонецЦикла</span><span style="color: red;">;</span>	
<span style="color: red;">КонецЦикла</span><span style="color: red;">;</span></code></pre>

Как следствие мы можем получить вот такую форму:
![Форма обработки](https://api.monosnap.com/image/download?id=wDPn9V8vDlujcauOfMSIonqUr "Сгруппированные штрихкода на форме")

###Работа с регистром штрихкодов
Когда есть все нужные данные можно начинать работать с регистром штрихкодов. Так как у нас ищутся не только штрихкода с несколькими владельцами, но и владельцы с несколькими штрихкодами, то состав табличного поля может быть разным, это необходимо учитывать. Приступим к реализации п1 - Удалить все штрихкода кроме выделенного. Для этого подготовим данные для записи в регистр. Выделим значение отобора и штрихкод который нам надо оставить:

<pre style="color: blue;"><code class="_1c8">СтруктураВРегистр <span style="color: red;">=</span> <span style="color: red;">Новый</span> Структура<span style="color: red;">(</span><span style="color: black;">"КлючОтбора, ЗначениеОтбора, ШтрихКод, Владелец"</span><span style="color: red;">)</span><span style="color: red;">;</span>
<span style="color: red;">Если</span> ТипЗнч<span style="color: red;">(</span>СтрокаДерева<span style="color: red;">.</span>Номенклатура<span style="color: red;">)</span> <span style="color: red;">=</span> Тип<span style="color: red;">(</span><span style="color: black;">"СправочникСсылка.Номенклатура"</span><span style="color: red;">)</span>	
	<span style="color: red;">ИЛИ</span> ТипЗнч<span style="color: red;">(</span>СтрокаДерева<span style="color: red;">.</span>Номенклатура<span style="color: red;">)</span> <span style="color: red;">=</span> Тип<span style="color: red;">(</span><span style="color: black;">"СправочникСсылка.ИнформационныеКарты"</span><span style="color: red;">)</span> <span style="color: red;">Тогда</span>	
	СтруктураВРегистр<span style="color: red;">.</span>КлючОтбора <span style="color: red;">=</span> <span style="color: black;">"Штрихкод"</span><span style="color: red;">;</span>	
	СтруктураВРегистр<span style="color: red;">.</span>ЗначениеОтбора <span style="color: red;">=</span> СтрокаДерева<span style="color: red;">.</span>Родитель<span style="color: red;">.</span>Номенклатура<span style="color: red;">;</span>	
	СтруктураВРегистр<span style="color: red;">.</span>Штрихкод <span style="color: red;">=</span> СтрокаДерева<span style="color: red;">.</span>Родитель<span style="color: red;">.</span>Номенклатура<span style="color: red;">;</span>	
	СтруктураВРегистр<span style="color: red;">.</span>Владелец <span style="color: red;">=</span> СтрокаДерева<span style="color: red;">.</span>Номенклатура<span style="color: red;">;</span>	
<span style="color: red;">Иначе</span>	
	СтруктураВРегистр<span style="color: red;">.</span>КлючОтбора <span style="color: red;">=</span> <span style="color: black;">"Владелец"</span><span style="color: red;">;</span>	
	СтруктураВРегистр<span style="color: red;">.</span>ЗначениеОтбора <span style="color: red;">=</span> СтрокаДерева<span style="color: red;">.</span>Родитель<span style="color: red;">.</span>Номенклатура<span style="color: red;">;</span>	
	СтруктураВРегистр<span style="color: red;">.</span>Штрихкод <span style="color: red;">=</span> СтрокаДерева<span style="color: red;">.</span>Номенклатура<span style="color: red;">;</span>	
	СтруктураВРегистр<span style="color: red;">.</span>Владелец <span style="color: red;">=</span> СтрокаДерева<span style="color: red;">.</span>Родитель<span style="color: red;">.</span>Номенклатура<span style="color: red;">;</span>	
<span style="color: red;">КонецЕсли</span><span style="color: red;">;</span></code></pre>

Теперь надо удалить все "лишние" штрихкода кроме конкретного, того на который указал пользователь. Я решил этот вопрос просто: я очищаю набор по указанному отбору и добавляю нужный штрихкод. По моему это самый простой и быстрый способ. Вот код:

<pre style="color: blue;"><code class="_1c8">НаборЗаписей <span style="color: red;">=</span> РегистрыСведений<span style="color: red;">.</span>Штрихкоды<span style="color: red;">.</span>СоздатьНаборЗаписей<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
НаборЗаписей<span style="color: red;">.</span>Отбор<span style="color: red;">[</span>СтруктураСДанными<span style="color: red;">.</span>КлючОтбора<span style="color: red;">]</span><span style="color: red;">.</span>Установить<span style="color: red;">(</span>СтруктураСДанными<span style="color: red;">.</span>ЗначениеОтбора<span style="color: red;">)</span><span style="color: red;">;</span>
НаборЗаписей<span style="color: red;">.</span>Записать<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
НоваяЗаписьНабора <span style="color: red;">=</span> НаборЗаписей<span style="color: red;">.</span>Добавить<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
НоваяЗаписьНабора<span style="color: red;">.</span>Владелец <span style="color: red;">=</span> СтруктураСДанными<span style="color: red;">.</span>Владелец<span style="color: red;">;</span>
НоваяЗаписьНабора<span style="color: red;">.</span>ЕдиницаИзмерения <span style="color: red;">=</span> СтруктураСДанными<span style="color: red;">.</span>Владелец<span style="color: red;">.</span>ЕдиницаХраненияОстатков<span style="color: red;">;</span>
НоваяЗаписьНабора<span style="color: red;">.</span>ТипШтрихкода <span style="color: red;">=</span> ПланыВидовХарактеристик<span style="color: red;">.</span>ТипыШтрихкодов<span style="color: red;">.</span>EAN13<span style="color: red;">;</span>
НоваяЗаписьНабора<span style="color: red;">.</span>Штрихкод <span style="color: red;">=</span> СтруктураСДанными<span style="color: red;">.</span>ШтрихКод<span style="color: red;">;</span>
НоваяЗаписьНабора<span style="color: red;">.</span>Качество <span style="color: red;">=</span> Справочники<span style="color: red;">.</span>Качество<span style="color: red;">.</span><span style="color: red;">Новый</span><span style="color: red;">;</span>
НаборЗаписей<span style="color: red;">.</span>Записать<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span></code></pre>

Перебирая строки дерева значений можно реализовать и п.3. Мы же идем дальше и приступаем к п.2. Для этих целей я использовал менеджер записи, в целом тут все просто до безобразия:
<pre style="color: blue;"><code class="_1c8"><span style="color: red;">Если</span> ТипЗнч<span style="color: red;">(</span>ЭлементыФормы<span style="color: red;">.</span>ТабличноеПоле<span style="color: red;">.</span>ТекущиеДанные<span style="color: red;">.</span>Номенклатура<span style="color: red;">)</span> <span style="color: red;">=</span> Тип<span style="color: red;">(</span><span style="color: black;">"СправочникСсылка.Номенклатура"</span><span style="color: red;">)</span>	
	<span style="color: red;">ИЛИ</span> ТипЗнч<span style="color: red;">(</span>ЭлементыФормы<span style="color: red;">.</span>ТабличноеПоле<span style="color: red;">.</span>ТекущиеДанные<span style="color: red;">.</span>Номенклатура<span style="color: red;">)</span> <span style="color: red;">=</span> Тип<span style="color: red;">(</span><span style="color: black;">"СправочникСсылка.ИнформационныеКарты"</span><span style="color: red;">)</span> <span style="color: red;">Тогда</span>	
	Штрихкод <span style="color: red;">=</span> ЭлементыФормы<span style="color: red;">.</span>ТабличноеПоле<span style="color: red;">.</span>ТекущаяСтрока<span style="color: red;">.</span>Родитель<span style="color: red;">.</span>Номенклатура<span style="color: red;">;</span>	
	Владелец <span style="color: red;">=</span> ЭлементыФормы<span style="color: red;">.</span>ТабличноеПоле<span style="color: red;">.</span>ТекущиеДанные<span style="color: red;">.</span>Номенклатура<span style="color: red;">;</span>	
<span style="color: red;">Иначе</span>	
	Штрихкод <span style="color: red;">=</span> ЭлементыФормы<span style="color: red;">.</span>ТабличноеПоле<span style="color: red;">.</span>ТекущиеДанные<span style="color: red;">.</span>Номенклатура<span style="color: red;">;</span>	
	Владелец <span style="color: red;">=</span> ЭлементыФормы<span style="color: red;">.</span>ТабличноеПоле<span style="color: red;">.</span>ТекущаяСтрока<span style="color: red;">.</span>Родитель<span style="color: red;">.</span>Номенклатура<span style="color: red;">;</span>	
<span style="color: red;">КонецЕсли</span><span style="color: red;">;</span></br>
МенеджерЗаписи <span style="color: red;">=</span> РегистрыСведений<span style="color: red;">.</span>Штрихкоды<span style="color: red;">.</span>СоздатьМенеджерЗаписи<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
МенеджерЗаписи<span style="color: red;">.</span>Штрихкод <span style="color: red;">=</span> Штрихкод<span style="color: red;">;</span>
МенеджерЗаписи<span style="color: red;">.</span>Владелец <span style="color: red;">=</span> Владелец<span style="color: red;">;</span>
МенеджерЗаписи<span style="color: red;">.</span>ТипШтрихкода <span style="color: red;">=</span> ПланыВидовХарактеристик<span style="color: red;">.</span>ТипыШтрихкодов<span style="color: red;">.</span>EAN13<span style="color: red;">;</span>
МенеджерЗаписи<span style="color: red;">.</span>ЕдиницаИзмерения <span style="color: red;">=</span> Владелец<span style="color: red;">.</span>ЕдиницаХраненияОстатков<span style="color: red;">;</span>
МенеджерЗаписи<span style="color: red;">.</span>Качество <span style="color: red;">=</span> Справочники<span style="color: red;">.</span>Качество<span style="color: red;">.</span><span style="color: red;">Новый</span><span style="color: red;">;</span>
МенеджерЗаписи<span style="color: red;">.</span>Прочитать<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
МенеджерЗаписи<span style="color: red;">.</span>Удалить<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span></code></pre>
Остался последний самый простой пункт. Я думаю тут даже код не нужен. Все и так просто. Делаем отбор в наборе и записываем не читая. Вот такая получилась обработка. Почти весь нужный код для работы обработки в этой статье есть. За бортом осталась косметика, украшательства и тд, то, что каждый настраивает по своему вкусу, но если все таки у вас не вышло собрать обработку, то обработку можно [скачать на инфостарте](http://infostart.ru/public/200131/).
