---
title: "Анализ списка инвентаризаций одним махом."
date: 2014-10-28 23:07
Category: "Программирование"
Tags: Практика программирования 1С, Обработка, Запрос
---

###Постановка задачи
После того как мы сделали ряд инвентаризаций и по результатам ввели документы, оказалось, что найти документ какую то конкретную инвентаризацию, что бы потом быстро что то поправить, в оприходованиях или списаниях целая задача. Было решено набросать набросать обработку которая будет:
* показывать все инвентаризации
* документы которые введены на ее основании
* номенклатуру остаток которой был исправлен этими документами.
При двойном щелчке по документу получаем сам документ, двойном щелчке по номенклатуре получаем историю движению по регистру хранения остатков. Цели ясны, задачи определены, приступаем.

###Получение нужных данных.
Вот сам запрос:
<pre style="text-align: left; font-family: courier new,courier; color: black">
<font color=blue>ВЫБРАТЬ
    </font>ОприходованиеТоваров.<font color=brown>Ссылка </font><font color=blue>КАК </font><font color=brown>Ссылка</font><font color=blue>,
    </font>ОприходованиеТоваров.ИнвентаризацияТоваровНаСкладе <font color=blue>КАК </font>ИнвентаризацияТоваровНаСкладе<font color=blue>,
    </font>ОприходованиеТоваров.ИнвентаризацияТоваровНаСкладе.Дата <font color=blue>КАК </font>ИнвентаризацияТоваровНаСкладеДата
<font color=blue>ИЗ
    </font>Документ.ОприходованиеТоваров <font color=blue>КАК </font>ОприходованиеТоваров
<font color=blue>ОБЪЕДИНИТЬ ВСЕ
ВЫБРАТЬ
    </font>СписаниеТоваров.Ссылка<font color=blue>,
    </font>СписаниеТоваров.ИнвентаризацияТоваровНаСкладе<font color=blue>,
    </font>СписаниеТоваров.ИнвентаризацияТоваровНаСкладе.Дата
<font color=blue>ИЗ
    </font>Документ.СписаниеТоваров <font color=blue>КАК </font>СписаниеТоваров
<font color=blue>УПОРЯДОЧИТЬ ПО
    </font>ИнвентаризацияТоваровНаСкладеДата <font color=blue>УБЫВ
ИТОГИ ПО
    </font>ИнвентаризацияТоваровНаСкладе</pre>

Далее мы выполняем запрос и обходим его по группировкам.
<pre style="color: blue;"><code class="_1c8">Выборка <span style="color: red;">=</span> Запрос<span style="color: red;">.</span><span style="color: red;">Выполнить</span><span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">.</span>Выбрать<span style="color: red;">(</span>ОбходРезультатаЗапроса<span style="color: red;">.</span>ПоГруппировкам<span style="color: red;">)</span><span style="color: red;">;</span>
<span style="color: red;">Пока</span> Выборка<span style="color: red;">.</span>Следующий<span style="color: red;">(</span><span style="color: red;">)</span> <span style="color: red;">Цикл</span>
    СтрокаИнвентаризация <span style="color: red;">=</span> СписокДокументов<span style="color: red;">.</span>Строки<span style="color: red;">.</span>Добавить<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
    СтрокаИнвентаризация<span style="color: red;">.</span>Док <span style="color: red;">=</span> Выборка<span style="color: red;">.</span>ИнвентаризацияТоваровНаСкладе<span style="color: red;">;</span>
    СтрокаИнвентаризация<span style="color: red;">.</span>Картинко <span style="color: red;">=</span> <span style="color: red;">?</span><span style="color: red;">(</span>СтрокаИнвентаризация<span style="color: red;">.</span>Док<span style="color: red;">.</span>Проведен<span style="color: red;">,</span> <span style="color: black;">1</span><span style="color: red;">,</span> <span style="color: red;">?</span><span style="color: red;">(</span>СтрокаИнвентаризация<span style="color: red;">.</span>Док<span style="color: red;">.</span>ПометкаУдаления<span style="color: red;">,</span> <span style="color: black;">2</span><span style="color: red;">,</span> <span style="color: black;">0</span><span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
    СкладскиеДокументы <span style="color: red;">=</span> Выборка<span style="color: red;">.</span>Выбрать<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
    <span style="color: red;">Пока</span> СкладскиеДокументы<span style="color: red;">.</span>Следующий<span style="color: red;">(</span><span style="color: red;">)</span> <span style="color: red;">Цикл</span>
        СтрокаСклад <span style="color: red;">=</span> СтрокаИнвентаризация<span style="color: red;">.</span>Строки<span style="color: red;">.</span>Добавить<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
        СтрокаСклад<span style="color: red;">.</span>Док <span style="color: red;">=</span> СкладскиеДокументы<span style="color: red;">.</span>Ссылка<span style="color: red;">;</span>
        СтрокаСклад<span style="color: red;">.</span>Картинко <span style="color: red;">=</span> <span style="color: red;">?</span><span style="color: red;">(</span>СтрокаСклад<span style="color: red;">.</span>Док<span style="color: red;">.</span>Проведен<span style="color: red;">,</span> <span style="color: black;">1</span><span style="color: red;">,</span> <span style="color: red;">?</span><span style="color: red;">(</span>СтрокаСклад<span style="color: red;">.</span>Док<span style="color: red;">.</span>ПометкаУдаления<span style="color: red;">,</span> <span style="color: black;">2</span><span style="color: red;">,</span> <span style="color: black;">0</span><span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
        ВсегоПройдетПоДокументу <span style="color: red;">=</span> <span style="color: black;">0</span><span style="color: red;">;</span>
        <span style="color: red;">Для</span> <span style="color: red;">Каждого</span> СтрокаДокумента <span style="color: red;">Из</span> СтрокаСклад<span style="color: red;">.</span>Док<span style="color: red;">.</span>Товары <span style="color: red;">Цикл</span>
            СтрокаСТоваром <span style="color: red;">=</span> СтрокаСклад<span style="color: red;">.</span>Строки<span style="color: red;">.</span>Добавить<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
            СтрокаСТоваром<span style="color: red;">.</span>Док <span style="color: red;">=</span> СтрокаДокумента<span style="color: red;">.</span>Номенклатура<span style="color: red;">;</span>
            СтрокаСТоваром<span style="color: red;">.</span>Количество <span style="color: red;">=</span> СтрокаДокумента<span style="color: red;">.</span>Количество<span style="color: red;">;</span>
            ВсегоПройдетПоДокументу <span style="color: red;">=</span> ВсегоПройдетПоДокументу <span style="color: red;">+</span> СтрокаДокумента<span style="color: red;">.</span>Количество<span style="color: red;">;</span>
        <span style="color: red;">КонецЦикла</span><span style="color: red;">;</span>
        СтрокаСклад<span style="color: red;">.</span>Количество <span style="color: red;">=</span> ВсегоПройдетПоДокументу<span style="color: red;">;</span>
    <span style="color: red;">КонецЦикла</span><span style="color: red;">;</span>
<span style="color: red;">КонецЦикла</span><span style="color: red;">;</span></code></pre>
 Готово! Теперь у нас есть вот такого вида форма
![Дерево на форме](http://i.imgur.com/LoUtLYg.png)

###Вывод картинки отображающей статус для каждого документа.
Следует заметить, что для наглядности в дереве отмечается статус документов(проведен, не проведен, помечен на удаление), как вы поняли в выше приведенном коде за этот момент отвечает вот эта строка:
<pre><p>СтрокаСклад<font color=red>.</font>Картинко <font color=red>= ?(</font>СтрокаСклад<font color=red>.</font>Док<font color=red>.</font>Проведен<font color=red>, </font><font color=black>1</font><font color=red>, ?(</font>СтрокаСклад<font color=red>.</font>Док<font color=red>.</font>ПометкаУдаления<font color=red>, </font><font color=black>2</font><font color=red>, </font><font color=black>0</font><font color=red>));<br>
</font></p></pre>
Для начала определимся с самой картинкой, вот она: ![Статус проведенности документа](http://i.imgur.com/PD7usod.png)
Для того, что бы увидеть эту картинку в одной из колонок нужно:
1. Добавить эту картинку в свойство `КартинкиСтрок` у колонки для которой мы хотим отображать эту картинку.
1. Указать у нужной колонки свойство `ДанныеКартинки`. Указав данное свойство, мы фактически добавили еще одну колонку в которой будет храниться индекс отображаемой картинки
1. Заполнить свойство `ДанныеКартинки` при добавлении строки.

###Формирование отчета СКД из существующего макета.
Так как у нас просто есть схема которая лежит в макете, внешней обработки, то нам надо програмно:
* Загрузить схему в компоновщик макета.
* Инициализировать настройки на основании, нашей схемы.
* Установить параметры отчета.

Вроде бы все достаточно просто, но на понимание того как это должно происходить, может уйти достаточно много времени. После детального изучения вопроса, была найдена [статья](http://infostart.ru/public/80164/) откуда была выдернута вот эта процедура
<pre style="color: blue;"><code class="_1c8"><span style="color: red;">Процедура</span> ПолучитьДанныеНаОснованииСКД<span style="color: red;">(</span>СКД<span style="color: red;">,</span> ОбъектДляЗагрузки<span style="color: red;">,</span> ИсполняемыеНастройки <span style="color: red;">=</span> <span style="color: red;">Неопределено</span><span style="color: red;">,</span> СтруктураПараметров <span style="color: red;">=</span> <span style="color: red;">Неопределено</span><span style="color: red;">,</span> 
РасшифровкаСКД <span style="color: red;">=</span> <span style="color: red;">Неопределено</span><span style="color: red;">,</span> МакетКомпоновки <span style="color: red;">=</span> <span style="color: red;">Неопределено</span><span style="color: red;">,</span> ВнешниеНаборыДанных <span style="color: red;">=</span> <span style="color: red;">Неопределено</span><span style="color: red;">)</span> <span style="color: red;">Экспорт</span>
    КомпоновщикМакета <span style="color: red;">=</span> <span style="color: red;">Новый</span> КомпоновщикМакетаКомпоновкиДанных<span style="color: red;">;</span>
    <span style="color: red;">Если</span> ТипЗнч<span style="color: red;">(</span>ОбъектДляЗагрузки<span style="color: red;">)</span> <span style="color: red;">=</span> Тип<span style="color: red;">(</span><span style="color: black;">"ПолеТабличногоДокумента"</span><span style="color: red;">)</span> <span style="color: red;">ИЛИ</span> ТипЗнч<span style="color: red;">(</span>ОбъектДляЗагрузки<span style="color: red;">)</span> <span style="color: red;">=</span> Тип<span style="color: red;">(</span><span style="color: black;">"ТабличныйДокумент"</span><span style="color: red;">)</span> <span style="color: red;">Тогда</span>
        ТипГенератора <span style="color: red;">=</span> Тип<span style="color: red;">(</span><span style="color: black;">"ГенераторМакетаКомпоновкиДанных"</span><span style="color: red;">)</span><span style="color: red;">;</span>
    <span style="color: red;">Иначе</span>
        ТипГенератора <span style="color: red;">=</span> Тип<span style="color: red;">(</span><span style="color: black;">"ГенераторМакетаКомпоновкиДанныхДляКоллекцииЗначений"</span><span style="color: red;">)</span><span style="color: red;">;</span>
    <span style="color: red;">КонецЕсли</span><span style="color: red;">;</span></br>
    <span style="color: red;">Если</span> ИсполняемыеНастройки <span style="color: red;">=</span> <span style="color: red;">Неопределено</span> <span style="color: red;">Тогда</span>
        ИсполняемыеНастройки <span style="color: red;">=</span> СКД<span style="color: red;">.</span>НастройкиПоУмолчанию<span style="color: red;">;</span>
    <span style="color: red;">КонецЕсли</span><span style="color: red;">;</span></br>
    <span style="color: red;">Если</span> СтруктураПараметров <span style="color: red;">&lt;</span><span style="color: red;">&gt;</span> <span style="color: red;">Неопределено</span> <span style="color: red;">Тогда</span>
        КоллекцияЗначенийПараметров <span style="color: red;">=</span> ИсполняемыеНастройки<span style="color: red;">.</span>ПараметрыДанных<span style="color: red;">.</span>Элементы<span style="color: red;">;</span>
        <span style="color: red;">Для</span> <span style="color: red;">каждого</span> Параметр <span style="color: red;">Из</span> СтруктураПараметров <span style="color: red;">Цикл</span>
            НайденноеЗначениеПараметра <span style="color: red;">=</span> КоллекцияЗначенийПараметров<span style="color: red;">.</span>Найти<span style="color: red;">(</span>Параметр<span style="color: red;">.</span>Ключ<span style="color: red;">)</span><span style="color: red;">;</span>
            <span style="color: red;">Если</span> НайденноеЗначениеПараметра <span style="color: red;">&lt;</span><span style="color: red;">&gt;</span> <span style="color: red;">Неопределено</span> <span style="color: red;">Тогда</span>
                НайденноеЗначениеПараметра<span style="color: red;">.</span>Использование <span style="color: red;">=</span> <span style="color: red;">Истина</span><span style="color: red;">;</span>
                НайденноеЗначениеПараметра<span style="color: red;">.</span>Значение <span style="color: red;">=</span> Параметр<span style="color: red;">.</span>Значение<span style="color: red;">;</span>
            <span style="color: red;">КонецЕсли</span><span style="color: red;">;</span>
        <span style="color: red;">КонецЦикла</span><span style="color: red;">;</span>
    <span style="color: red;">КонецЕсли</span><span style="color: red;">;</span></br>
    МакетКомпоновкиСКД <span style="color: red;">=</span> КомпоновщикМакета<span style="color: red;">.</span><span style="color: red;">Выполнить</span><span style="color: red;">(</span>СКД<span style="color: red;">,</span> ИсполняемыеНастройки<span style="color: red;">,</span> РасшифровкаСКД<span style="color: red;">,</span> МакетКомпоновки<span style="color: red;">,</span> ТипГенератора<span style="color: red;">)</span><span style="color: red;">;</span>
    ПроцессорКомпоновки <span style="color: red;">=</span> <span style="color: red;">Новый</span> ПроцессорКомпоновкиДанных<span style="color: red;">;</span>
    ПроцессорКомпоновки<span style="color: red;">.</span>Инициализировать<span style="color: red;">(</span>МакетКомпоновкиСКД<span style="color: red;">,</span> ВнешниеНаборыДанных<span style="color: red;">,</span> РасшифровкаСКД<span style="color: red;">)</span><span style="color: red;">;</span></br>
    <span style="color: red;">Если</span> ТипЗнч<span style="color: red;">(</span>ОбъектДляЗагрузки<span style="color: red;">)</span> <span style="color: red;">=</span> Тип<span style="color: red;">(</span><span style="color: black;">"ПолеТабличногоДокумента"</span><span style="color: red;">)</span> <span style="color: red;">ИЛИ</span> ТипЗнч<span style="color: red;">(</span>ОбъектДляЗагрузки<span style="color: red;">)</span> <span style="color: red;">=</span> Тип<span style="color: red;">(</span><span style="color: black;">"ТабличныйДокумент"</span><span style="color: red;">)</span> <span style="color: red;">Тогда</span>
        ПроцессорВывода <span style="color: red;">=</span> <span style="color: red;">Новый</span> ПроцессорВыводаРезультатаКомпоновкиДанныхВТабличныйДокумент<span style="color: red;">;</span>
        ПроцессорВывода<span style="color: red;">.</span>УстановитьДокумент<span style="color: red;">(</span>ОбъектДляЗагрузки<span style="color: red;">)</span><span style="color: red;">;</span>
    <span style="color: red;">Иначе</span>
        ПроцессорВывода <span style="color: red;">=</span> <span style="color: red;">Новый</span> ПроцессорВыводаРезультатаКомпоновкиДанныхВКоллекциюЗначений<span style="color: red;">;</span>
        ПроцессорВывода<span style="color: red;">.</span>УстановитьОбъект<span style="color: red;">(</span>ОбъектДляЗагрузки<span style="color: red;">)</span><span style="color: red;">;</span>
    <span style="color: red;">КонецЕсли</span><span style="color: red;">;</span></br>
    ПроцессорВывода<span style="color: red;">.</span>ОтображатьПроцентВывода <span style="color: red;">=</span> <span style="color: red;">Истина</span><span style="color: red;">;</span>
    ПроцессорВывода<span style="color: red;">.</span>Вывести<span style="color: red;">(</span>ПроцессорКомпоновки<span style="color: red;">,</span> <span style="color: red;">Истина</span><span style="color: red;">)</span><span style="color: red;">;</span>
<span style="color: red;">КонецПроцедуры</span></code></pre>
ее суть проста: на входе макет, на выходе табличный документ. Теперь когда мы умеем формировать табличный документ на основе макета, мы можем одним легким движением, добавить расшифровку движений по складу для номенклатуры которая есть в нашем отчете. Приступаем.

###Формирование истории движений конкретной номенклатуру по событию ни форме.
Когда возникают вопросы: "А в чем дело, почему у меня тосола -15 банок, я ведь все правильно делал", самое время пожать плечами и молча ткнуть пользователя в историю движений. Тут нам и поможет наш отчет на СКД. Мысль следующая: когда мы щелкаем на поле два раза по какой то номенклатуре, инициализируется простейший отчет на СКД который выводит все движения по таблице остатки и обороты регистра `ТоварыВРознице`. Отчет достаточно простой постороенный вот на таком запросе.
<pre style="text-align: left; font-family: courier new,courier; color: black">
<font color=blue>ВЫБРАТЬ
    </font>ТоварыВРозницеОстаткиИОбороты.Период<font color=blue>,
    </font>ТоварыВРозницеОстаткиИОбороты.Регистратор<font color=blue>,
    </font>ТоварыВРозницеОстаткиИОбороты.КоличествоНачальныйОстаток<font color=blue>,
    </font>ТоварыВРозницеОстаткиИОбороты.КоличествоПриход<font color=blue>,
    </font>ТоварыВРозницеОстаткиИОбороты.КоличествоРасход<font color=blue>,
    </font>ТоварыВРозницеОстаткиИОбороты.КоличествоКонечныйОстаток
<font color=blue>ИЗ
    </font>РегистрНакопления.ТоварыВРознице.ОстаткиИОбороты<font color=blue>(
            ,
            ,
            </font>Регистратор<font color=blue>,
            ,
            </font>Номенклатура <font color=blue>= </font><font color=#008b8b>&Номенклатура
                </font><font color=brown>И </font>Склад <font color=blue>= </font><font color=#008b8b>&Склад</font><font color=blue>) КАК </font>ТоварыВРозницеОстаткиИОбороты</pre> я думаю вы натыкаете его мышкой за 2 минуты.
*Перед тем как продолжить, я хотел бы попросить читателя если он еще не разобрался, понять что табличное поле и табличный документ это абсолютно разные сущности. Табличное поле, может быть списком значений, таблицей значений или деревом значений. Табличный документ это объект для формирования печатных форм, он имеет структуру схожую с excel но схожесть чисто внешняя.*
####Подготовительные действия.
Добавляем макет в обработку, указываем тип макета "Схема компоновки данных". Теперь можно им пользоваться в самой обработке. Можно сразу вывести отчет в табличный документ и на этом расслабиться, но тогда в нем не будет работать расшифровка, что бы в отчете работала расшифровка, табличный документ должен находиться на какой нибудь форме. Поэтому нам нужна форма и мы ее добавим как произвольную форму для обработки и поместим на нее табличный документ куда и будем выводить наш отчет. На этом все подготовительные действия закончены.

####Вывод отчета из подготовленного макета в подготоваленную форму.
Далее нам нужен план действий, приблизительно следующего вида, когда пользователь щелкает по строке табличного поля на форме, то:
1. Если он щелкает по строке указывающей на документ, от открывается форма документа.
1. Если он щелкает по номенклатуре, то нам нужно
  1. Загрузить макет формирующий историю движений.
  1. Получить форму отчета, с табличным документом куда мы будем грузить отчет и реквизитом `ОбработчикРасшифровки` произвольного типа куда мы будем передавать расшифровку.
  1. Вывести на основании макета отчет в полученную форму и настроить обработку расшифровки.

Вешаем на событие 'Выбор' табличного поля, следующую процедуру:
<pre style="color: blue;"><code class="_1c8"><span style="color: red;">Процедура</span> СписокДокументовВыбор<span style="color: red;">(</span>Элемент<span style="color: red;">,</span> ВыбраннаяСтрока<span style="color: red;">,</span> Колонка<span style="color: red;">,</span> СтандартнаяОбработка<span style="color: red;">)</span>
    СтандартнаяОбработка <span style="color: red;">=</span> <span style="color: red;">Ложь</span><span style="color: red;">;</span>
    <span style="color: red;">Если</span> Документы<span style="color: red;">.</span>ТипВсеСсылки<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">.</span>СодержитТип<span style="color: red;">(</span>ТипЗнч<span style="color: red;">(</span>ВыбраннаяСтрока<span style="color: red;">.</span>Док<span style="color: red;">)</span><span style="color: red;">)</span> <span style="color: red;">Тогда</span>
        ВыбраннаяСтрока<span style="color: red;">.</span>Док<span style="color: red;">.</span>ПолучитьФорму<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">.</span>Открыть<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
    <span style="color: red;">Иначе</span></br>
        СхемаКомпоновкиДанных <span style="color: red;">=</span> ПолучитьМакет<span style="color: red;">(</span><span style="color: black;">"ОтчетПоДвижениямНоменклатуры"</span><span style="color: red;">)</span><span style="color: red;">;</span>
        СтруктураПараметров <span style="color: red;">=</span> <span style="color: red;">Новый</span> Структура<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
        СтруктураПараметров<span style="color: red;">.</span>Вставить<span style="color: red;">(</span><span style="color: black;">"НачалоПериода"</span><span style="color: red;">,</span> ТекущаяДата<span style="color: red;">(</span><span style="color: red;">)</span> <span style="color: red;">-</span> <span style="color: black;">31556926</span><span style="color: red;">)</span><span style="color: red;">;</span>
        СтруктураПараметров<span style="color: red;">.</span>Вставить<span style="color: red;">(</span><span style="color: black;">"КонецПериода"</span><span style="color: red;">,</span> ТекущаяДата<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
        СтруктураПараметров<span style="color: red;">.</span>Вставить<span style="color: red;">(</span><span style="color: black;">"Номенклатура"</span><span style="color: red;">,</span> ЭлементыФормы<span style="color: red;">.</span>СписокДокументов<span style="color: red;">.</span>ТекущаяСтрока<span style="color: red;">.</span>Док<span style="color: red;">)</span><span style="color: red;">;</span>
        СтруктураПараметров<span style="color: red;">.</span>Вставить<span style="color: red;">(</span><span style="color: black;">"Склад"</span><span style="color: red;">,</span> ЭлементыФормы<span style="color: red;">.</span>СписокДокументов<span style="color: red;">.</span>ТекущаяСтрока<span style="color: red;">.</span>Родитель<span style="color: red;">.</span>Док<span style="color: red;">.</span>Склад<span style="color: red;">)</span><span style="color: red;">;</span></br>
        Расшифровка <span style="color: red;">=</span> <span style="color: red;">Новый</span> ДанныеРасшифровкиКомпоновкиДанных<span style="color: red;">;</span>
        ФормаОтчета <span style="color: red;">=</span> ПолучитьФорму<span style="color: red;">(</span><span style="color: black;">"ИсторияДвижений"</span><span style="color: red;">)</span><span style="color: red;">;</span>
        ПолучитьДанныеНаОснованииСКД<span style="color: red;">(</span>СхемаКомпоновкиДанных<span style="color: red;">,</span> ФормаОтчета<span style="color: red;">.</span>ЭлементыФормы<span style="color: red;">.</span>ПолеТабличногоДокумента1<span style="color: red;">,</span> СхемаКомпоновкиДанных<span style="color: red;">.</span>НастройкиПоУмолчанию<span style="color: red;">,</span> СтруктураПараметров<span style="color: red;">,</span> Расшифровка<span style="color: red;">)</span><span style="color: red;">;</span>
        ФормаОтчета<span style="color: red;">.</span>ОбработчикРасшифровки <span style="color: red;">=</span> <span style="color: red;">Новый</span> ОбработкаРасшифровкиКомпоновкиДанных<span style="color: red;">(</span>Расшифровка<span style="color: red;">,</span> <span style="color: red;">Новый</span> ИсточникДоступныхНастроекКомпоновкиДанных<span style="color: red;">(</span>СхемаКомпоновкиДанных<span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
        ФормаОтчета<span style="color: red;">.</span>Открыть<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
    <span style="color: red;">КонецЕсли</span><span style="color: red;">;</span>
<span style="color: red;">КонецПроцедуры</span></code></pre>
которая реализует почти все кроме пункта 2.3. Остался последний штрих, добавить в открываюмую форму обработку расшифровки. Для этого используем событие `ОбработкаРасшифровки` где укажем следующий код:
<pre style="color: blue;"><code class="_1c8">ОбработчикРасшифровки<span style="color: red;">.</span><span style="color: red;">Выполнить</span><span style="color: red;">(</span>Расшифровка<span style="color: red;">)</span><span style="color: red;">;</span>
СтандартнаяОбработка <span style="color: red;">=</span> <span style="color: red;">Ложь</span><span style="color: red;">;</span>
</code></pre>
Теперь расшифровка должна работать как и собственно сама обработка.

###Заключение
как обычно почти весь код приведен и снабжен комментариями, но если у вас не получается собрать аленький цветочек [можно скачать обработку на инфостарте](http://infostart.ru/public/171476/)
