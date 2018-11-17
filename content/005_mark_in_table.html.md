---
title: "Печать этикеток из поступления только отмеченной номенклатуры"
date: 2012-09-23 20:53
categories: "Программирование"
Tags: Практика программирования 1С, Табличная часть, МВТ, Запрос
---
###В чем соль?
Реквизит в табличную часть документа добавлять нельзя, так как установка флажка изменяет табличную часть, то форма получает признак модифицированности и постоянные вопросы о необходимости сохранять документ, немного нервируют пользователя(а если документ большой и проведенный, то процедура сохранения, еще и какое то время занимает) в целом это можно было бы и пережить(можно и признак модифицированности скидывать), но клиент мириться с этим не захотел, а так как если при печати все равно придется анализировать табличное поле, было решено сделать колонку не связанную с данными табличной части. В результате анализа ситуации стало ясно следующее:

1. Если данные не хранятся в табличной части, то придется самому позаботится о том где мы будеи держать информацию об отмеченных строках.
2. Механизм отрисовки флажка тоже придется взять на себя.

Как обычно прежде чем начинать городить велосипед, был сделан запрос к [базе знаний](http://www.forum.mista.ru "миста") и выяснено следующее: для моего случая уже есть описанный случай на ИТС и называется он `Реализация отметки строк флажками в табличном поле`. Раз есть готовый код, то берем его, модифицируем, используем. Итак поехали:

###Реализация отметок в табличном поле
Для начала, надо добавить колонку в табличное поле и нужно указать, что элемент управления - флажок, ну и название придумать какое нибудь. Теперь надо позаботится об объекте где будут храниться данные об наших отметках. Это будет переменная и называться она будет `СписокОтметок`, так и объявим в начале модуля:
`Перем СписокОтметок;`
в конце где выполняется код при открытии модуля (если не понимаете о чем я просто поставьте самой последней строкой) укажем тип нашей переменной: `СписокОтметок = Новый Соответствие.`

Теперь надо организовать изменение этого списка, когда пользователь щелкает по флажку в табличной части, для этого подойдет событие табличного поля `ПриИзмененииФлажка`, в нем нам надо указать следующее:

<pre style="color: blue;"><code class="_1c8"><span style="color: red;">Процедура</span> ТоварыПриИзмененииФлажка<span style="color: red;">(</span>Элемент<span style="color: red;">,</span> Колонка<span style="color: red;">)</span>
    <span style="color: red;">Если</span> Колонка<span style="color: red;">.</span>Имя <span style="color: red;">=</span> <span style="color: black;">"Отметка"</span> <span style="color: red;">Тогда</span>
        <span style="color: red;">Если</span> СписокОтметок<span style="color: red;">[</span>Элемент<span style="color: red;">.</span>ТекущаяСтрока<span style="color: red;">]</span> <span style="color: red;">=</span> <span style="color: red;">Неопределено</span> <span style="color: red;">Тогда</span>
            СписокОтметок<span style="color: red;">[</span>Элемент<span style="color: red;">.</span>ТекущаяСтрока<span style="color: red;">]</span> <span style="color: red;">=</span> <span style="color: red;">Истина</span><span style="color: red;">;</span>
        <span style="color: red;">Иначе</span>
            СписокОтметок<span style="color: red;">.</span>Удалить<span style="color: red;">(</span>Элемент<span style="color: red;">.</span>ТекущаяСтрока<span style="color: red;">)</span><span style="color: red;">;</span>
        <span style="color: red;">КонецЕсли</span><span style="color: red;">;</span>
    <span style="color: red;">КонецЕсли</span><span style="color: red;">;</span>
<span style="color: red;">КонецПроцедуры</span></code></pre>

Что здесь происходит: когда пользователь щелкает по флажку, процедура ищет нужную строку табличной части и если ее нет, то добавляет, если есть удалет, таким образом, осуществляя изменение состояния флажка.

Теперь нужно организовать вывод флажков в табличное поле, на текущий момент юзер не видит установленных флажков в табличном поле. Для работы с выводом, нужно использовать событие `ПриВыводеСтроки` вот такой код используется для вывода флажка:

<pre style="color: blue;"><code class="_1c8">ОформлениеСтроки<span style="color: red;">.</span>Ячейки<span style="color: red;">.</span>Отметка<span style="color: red;">.</span>ОтображатьФлажок <span style="color: red;">=</span> <span style="color: red;">Истина</span><span style="color: red;">;</span>
<span style="color: red;">Если</span> СписокОтметок<span style="color: red;">[</span>ДанныеСтроки<span style="color: red;">]</span> <span style="color: red;">=</span> <span style="color: red;">Неопределено</span> <span style="color: red;">Тогда</span>
    ОформлениеСтроки<span style="color: red;">.</span>Ячейки<span style="color: red;">.</span>Отметка<span style="color: red;">.</span>Флажок <span style="color: red;">=</span> <span style="color: red;">Ложь</span><span style="color: red;">;</span>
<span style="color: red;">Иначе</span>
    ОформлениеСтроки<span style="color: red;">.</span>Ячейки<span style="color: red;">.</span>Отметка<span style="color: red;">.</span>Флажок <span style="color: red;">=</span> <span style="color: red;">Истина</span><span style="color: red;">;</span>
<span style="color: red;">КонецЕсли</span><span style="color: red;">;</span></code></pre>

Тут все тоже очень просто: если текущая строка есть в списке отметок мы ее отметим если нету, не будем. Таким образом у нас есть список тех строк табличной части документов, которые были отмечены.
###Передача отмеченных строк в обработку печати этикеток.
Для того, что бы передать список номенклатуры, в обработку печати этикеток, я нашел два варианта, это передать ссылку на группу или ссылку на номенклатуру. Или что бы со списком было бы еще количество, можно передать ссылку на документ. Нам не подходит не первое, не второе. Так как нам нужно и количество и определенный список. Поэтому я немного переделал процедуру печати этикеток `НапечататьЭтикеткиИзДокумента`, которая формирует из ссылки на табличную часть документа, таблицу товары, которую принимает обработка печати этикеток. Для начала я выгрузил в таблицу значений отмеченные значения, загрузил ее во временную таблицу в запросе.
<pre style="color: blue;"><code class="_1c8">МВТ <span style="color: red;">=</span> <span style="color: red;">Новый</span> МенеджерВременныхТаблиц<span style="color: red;">;</span>
ТаблицаИзДока <span style="color: red;">=</span> <span style="color: red;">Новый</span> Запрос<span style="color: red;">;</span>
ТаблицаИзДока<span style="color: red;">.</span>МенеджерВременныхТаблиц <span style="color: red;">=</span> МВТ<span style="color: red;">;</span>
ТаблицаИзДока<span style="color: red;">.</span>Текст <span style="color: red;">=</span>
    <span style="color: black;">"Выбрать</span>
    <span style="color: black;">|Таблица.Номенклатура,</span>
    <span style="color: black;">|Таблица.Количество,</span>
    <span style="color: black;">|Таблица.ЕдиницаИзмерения,</span>
    <span style="color: black;">|ЗНАЧЕНИЕ(Справочник.ХарактеристикиНоменклатуры.ПустаяСсылка) КАК Характеристика,</span>
    <span style="color: black;">|ЗНАЧЕНИЕ(Справочник.СерииНоменклатуры.ПустаяСсылка) КАК Серия,</span>
    <span style="color: black;">|ЗНАЧЕНИЕ(Справочник.Качество.Новый) КАК Качество,</span>
    <span style="color: black;">|0 КАК Цена</span>
    <span style="color: black;">|ПОМЕСТИТЬ ТаблицаИЗДока</span>
    <span style="color: black;">|ИЗ</span>
    <span style="color: black;">|&amp;ТаблицаСДанными КАК Таблица"</span><span style="color: red;">;</span>
ТаблицаИзДока<span style="color: red;">.</span>УстановитьПараметр<span style="color: red;">(</span><span style="color: black;">"ТаблицаСДанными"</span><span style="color: red;">,</span> ТабличкаИЗДокумента<span style="color: red;">)</span><span style="color: red;">;</span>
ТаблицаИзДока<span style="color: red;">.</span><span style="color: red;">Выполнить</span><span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span></code></pre>

Полученную временную таблицу я передал в запрос, выбирающий данные из регистра штрихкодов:
<pre style="color: blue;"><code class="_1c8">Запрос <span style="color: red;">=</span> <span style="color: red;">Новый</span> Запрос<span style="color: red;">;</span>
Запрос<span style="color: red;">.</span>МенеджерВременныхТаблиц <span style="color: red;">=</span> МВТ<span style="color: red;">;</span>
Запрос<span style="color: red;">.</span>Текст <span style="color: red;">=</span>
    <span style="color: black;">"ВЫБРАТЬ</span>
    <span style="color: black;">|   Док.Номенклатура КАК Номенклатура,</span>
    <span style="color: black;">|   Док.Количество КАК Количество,</span>
    <span style="color: black;">|   Док.Характеристика КАК Характеристика,</span>
    <span style="color: black;">|   Док.Серия КАК Серия,</span>
    <span style="color: black;">|   Док.Качество КАК Качество,</span>
    <span style="color: black;">|   Док.ЕдиницаИзмерения КАК ЕдиницаИзмерения,</span>
    <span style="color: black;">|   Док.Цена КАК Цена,</span>
    <span style="color: black;">|   РегШК.ТипШтрихкода КАК ТипШтрихкода,</span>
    <span style="color: black;">|   РегШК.Штрихкод КАК Штрихкод</span>
    <span style="color: black;">|ИЗ</span>
    <span style="color: black;">|   ТаблицаИЗДока КАК Док</span>
    <span style="color: black;">|       ВНУТРЕННЕЕ СОЕДИНЕНИЕ РегистрСведений.Штрихкоды КАК РегШК</span>
    <span style="color: black;">|       ПО (РегШК.Владелец = Док.Номенклатура)</span>
    <span style="color: black;">|           И (РегШК.ЕдиницаИзмерения = Док.ЕдиницаИзмерения)</span>
    <span style="color: black;">|           И (РегШК.ХарактеристикаНоменклатуры = Док.Характеристика)</span>
    <span style="color: black;">|           И (РегШК.СерияНоменклатуры = Док.Серия)</span>
    <span style="color: black;">|           И (РегШК.Качество = Док.Качество)"</span><span style="color: red;">;</span></code></pre>
    
    после этого остается только напечатать этикетки
<pre style="color: blue;"><code class="_1c8">ЗаполнениеДокументов<span style="color: red;">.</span>ПечатьЭтикеток<span style="color: red;">(</span>Запрос<span style="color: red;">.</span><span style="color: red;">Выполнить</span><span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">.</span>Выгрузить<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span></code></pre>