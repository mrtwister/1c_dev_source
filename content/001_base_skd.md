---
Title: "Основные моменты при работе с СКД"
date: 2012-09-05 21:09
Category: "СКД"
Tags: СКД, Параметры СКД
---
 В данном топике я хотел бы затронуть, некоторые моменты работы с СКД: работа с формой отчета, использование нескольких схем компоновки данных, работа с параметрами и так по мелочи, что накопилось за время использования СКД.
<span>continue</span>

##Как использовать параметры в СКД?
При написании отчета для СКД иногда возникает потребность в использовании параметров, какие есть варианты? Для начала надо определиться что для того что бы параметры стали доступными, необходимо поставить галочку в схеме вот здесь:
![Доступность параметра](http://i.imgur.com/zJHEInG.png)

1. Тыкнуть по кнопочке настройки, и задать настройки на стандартной форме. Мы этот вариант даже рассматривать не будем, по той простой причине, что их видно на стандартной форме невооруженным глазом, достаточно тыкнуть на кнопку... Настройки конечно же.
2. Сделать таблицу на форме и указать у нее источник.
3. Добавить на форму отчета поля ввода и прописать изменение параметров СКД при их изменении

Рассмотрим  все варианты по подробнее.
###2. Вывод всех прописанных настроек в одной таблице
Это делается очень просто, добавляется таблица значений на форму а источником данных нужно указать: ОтчетОбъект -> КомпоновщикНастроек -> Настройки -> Параметры данных.
###3. Вынесение параметров отчета на форму, как правило самый нужный и удобный метод установки параметров.
Для этого создадим форму отчета, если вы ее еще не создали (куда то, нам надо вынести параметры которые мы будем передавать в СКД) и добавим поле ввода нужного нам типа. И в событии "ПриИзменении" укажем следующий код:
<pre style="color: blue;"><code class="_1c8">Параметры <span style="color: red;">=</span> КомпоновщикНастроек<span style="color: red;">.</span>Настройки<span style="color: red;">.</span>ПараметрыДанных<span style="color: red;">;</span><br>
Параметр <span style="color: red;">=</span> Параметры<span style="color: red;">.</span>НайтиЗначениеПараметра<span style="color: red;">(</span><span style="color: red;">Новый</span> ПараметрКомпоновкиДанных<span style="color: red;">(</span><span style="color: black;">"ПараметрУказанныйВЗапросе"</span><span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
<span style="color: red;">Если</span> Параметр <span style="color: red;">&lt;</span><span style="color: red;">&gt;</span> <span style="color: red;">Неопределено</span> <span style="color: red;">Тогда</span>
    Параметр<span style="color: red;">.</span>Значение <span style="color: red;">=</span> ЗначениеКотороеМыХотимУстановить<span style="color: red;">;</span>
    Параметр<span style="color: red;">.</span>Использование <span style="color: red;">=</span> <span style="color: red;">Истина</span><span style="color: red;">;</span>
<span style="color: red;">КонецЕсли</span><span style="color: red;">;</span></code></pre>
Готово! Теперь при изменении элемента на форме параметр будет автоматически загружаться в СКД.
##Использование нескольких схем
Периодически бывает что один отчет должен показывать вроде бы одну и ту же информацию но в разрезе разных показателей. И вроде отчет тот же, только сменился тип аналитики, или убрали колонку, которая участвовала в расчетах, но "почти" это для пользователя, для разработчика это уже другой набор полей и уже скорее всего структура другая, вообщем необходимо делать другой отчет, но можно просто использовать несколько схем и переключаться между ними по мере надобности. Переключаться между схемами несложно, достаточно сделать кнопочку повешать на нее следующую процедуру:
<pre style="color: blue;"><code class="_1c8"><span style="color: red;">Процедура</span> СменитьСхему<span style="color: red;">(</span><span style="color: red;">)</span>
    СхемаКомпоновкиДанных <span style="color: red;">=</span> ПолучитьМакет<span style="color: red;">(</span><span style="color: black;">"ЗдесьНадоУказатьИмяСхемы"</span><span style="color: red;">)</span><span style="color: red;">;</span>
    Настройки <span style="color: red;">=</span> СхемаКомпоновкиДанных<span style="color: red;">.</span>НастройкиПоУмолчанию<span style="color: red;">;</span>
    КомпоновщикНастроек<span style="color: red;">.</span>ЗагрузитьНастройки<span style="color: red;">(</span>Настройки<span style="color: red;">)</span><span style="color: red;">;</span>
<span style="color: red;">КонецПроцедуры</span></code></pre>
Как видите, все просто, при желании можно сократить до двух строк или даже одной, но не уверен, что это пойдет на пользу читаемости кода. Но тут есть свой нюанс, при загрузке новых настроек старые параметры сотрутся, что на самом деле логично, но нас такое положение дел совершенно не устраивает. Какой из этого есть выход? Я думаю надо перед сменой компоновки параметры, надо сохранить в какой то буфер, а потом их восстановить. Как получить\записать параметр я уже говорил выше и не буду на это останавливаться. Так как параметров как правило больше чем два, особенно если это сложный отчет, то неправильно будет, писать

<pre style="color: blue;"><code class="_1c8">Параметр1 <span style="color: red;">=</span> Параметры<span style="color: red;">.</span>НайтиЗначениеПараметра<span style="color: red;">(</span><span style="color: red;">Новый</span> ПараметрКомпоновкиДанных<span style="color: red;">(</span><span style="color: black;">"ПараметрИзЗапроса"</span><span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
СохраненноеЗначение1 <span style="color: red;">=</span> Параметр1<span style="color: red;">.</span>Значение<span style="color: red;">;</span></br>
Параметр2 <span style="color: red;">=</span> Параметры<span style="color: red;">.</span>НайтиЗначениеПараметра<span style="color: red;">(</span><span style="color: red;">Новый</span> ПараметрКомпоновкиДанных<span style="color: red;">(</span><span style="color: black;">"ПараметрИзЗапроса2"</span><span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
СохраненноеЗначение2 <span style="color: red;">=</span> Параметр2<span style="color: red;">.</span>Значение<span style="color: red;">;</span></br>
<span style="color: green;">//смена схемы компоновки</span>
Параметр1 <span style="color: red;">=</span> Параметры<span style="color: red;">.</span>НайтиЗначениеПараметра<span style="color: red;">(</span><span style="color: red;">Новый</span> ПараметрКомпоновкиДанных<span style="color: red;">(</span><span style="color: black;">"ПараметрИзЗапроса"</span><span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
Параметр1<span style="color: red;">.</span>Значение <span style="color: red;">=</span> СохраненноеЗначение1<span style="color: red;">;</span>
Параметр1<span style="color: red;">.</span>Использование <span style="color: red;">=</span> <span style="color: red;">Истина</span><span style="color: red;">;</span></br>
Параметр2 <span style="color: red;">=</span> Параметры<span style="color: red;">.</span>НайтиЗначениеПараметра<span style="color: red;">(</span><span style="color: red;">Новый</span> ПараметрКомпоновкиДанных<span style="color: red;">(</span><span style="color: black;">"ПараметрИзЗапроса2"</span><span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
Параметр2<span style="color: red;">.</span>Значение <span style="color: red;">=</span> СохраненноеЗначение2<span style="color: red;">;</span>
Параметр2<span style="color: red;">.</span>Использование <span style="color: red;">=</span> <span style="color: red;">Истина</span><span style="color: red;">;</span></br>
<span style="color: green;">//и тд</span></code></pre>
*Я надеюсь, что вы понимаете, что этот код написан для примера и не стоит использовать перемнные с именами "СохраненноеЗначение1","СохраненноеЗначение2", но даже если не понимаете, все равно не используйте.*
Хочется оптимизировать вышеприведенный код, что бы просто указать: `СохраниСписокПараметров("ЗдесьСписокПараметров");` потом сменить схему и сделать `ВосстановиСписокПараметров("ЗдесьСписокПараметров");` Написанием этих процедур мы и займемся, для этого далее я напишу эти две процедуры, одна будет сохранять параметры в спецально для этого отведнную структуру, другая будет из нее восстанавливать параметры. Вот они обе:
<pre style="color: blue;"><code class="_1c8"><span style="color: red;">Функция</span> СохранитьПараметры<span style="color: red;">(</span>ИменаПараметров<span style="color: red;">)</span>
    Параметры <span style="color: red;">=</span> КомпоновщикНастроек<span style="color: red;">.</span>Настройки<span style="color: red;">.</span>ПараметрыДанных<span style="color: red;">;</span>
    МассивСИменами <span style="color: red;">=</span> ОбщегоНазначения<span style="color: red;">.</span>РазложитьСтрокуВМассивПодстрок<span style="color: red;">(</span>ИменаПараметров<span style="color: red;">,</span><span style="color: black;">","</span><span style="color: red;">)</span><span style="color: red;">;</span></br>
    СтруктураДляПараметров <span style="color: red;">=</span> <span style="color: red;">Новый</span> Структура<span style="color: red;">;</span></br>
    <span style="color: red;">Для</span> <span style="color: red;">Каждого</span> ИмяПараметра <span style="color: red;">Из</span> МассивСИменами <span style="color: red;">Цикл</span>
        Параметр <span style="color: red;">=</span> Параметры<span style="color: red;">.</span>НайтиЗначениеПараметра<span style="color: red;">(</span><span style="color: red;">Новый</span> ПараметрКомпоновкиДанных<span style="color: red;">(</span>ИмяПараметра<span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
        <span style="color: red;">Если</span> Параметр <span style="color: red;">&lt;</span><span style="color: red;">&gt;</span> <span style="color: red;">Неопределено</span> <span style="color: red;">Тогда</span>
            СтруктураДляПараметров<span style="color: red;">.</span>Вставить<span style="color: red;">(</span>ИмяПараметра<span style="color: red;">,</span> Параметр<span style="color: red;">.</span>Значение<span style="color: red;">)</span><span style="color: red;">;</span>
        <span style="color: red;">КонецЕсли</span><span style="color: red;">;</span>
    <span style="color: red;">КонецЦикла</span><span style="color: red;">;</span></br>
    <span style="color: red;">Возврат</span> СтруктураДляПараметров<span style="color: red;">;</span></br>
<span style="color: red;">КонецФункции</span></br>
<span style="color: red;">Процедура</span> ЗагрузитьПараметры<span style="color: red;">(</span>СтруктураСПараметрами<span style="color: red;">)</span>
    Параметры <span style="color: red;">=</span> КомпоновщикНастроек<span style="color: red;">.</span>Настройки<span style="color: red;">.</span>ПараметрыДанных<span style="color: red;">;</span></br>
    <span style="color: red;">Для</span> <span style="color: red;">Каждого</span> ТекущийПараметр <span style="color: red;">Из</span> СтруктураСПараметрами <span style="color: red;">Цикл</span>
        Параметр <span style="color: red;">=</span> Параметры<span style="color: red;">.</span>НайтиЗначениеПараметра<span style="color: red;">(</span><span style="color: red;">Новый</span> ПараметрКомпоновкиДанных<span style="color: red;">(</span>ТекущийПараметр<span style="color: red;">.</span>Ключ<span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
        <span style="color: red;">Если</span> Параметр <span style="color: red;">&lt;</span><span style="color: red;">&gt;</span> <span style="color: red;">Неопределено</span> <span style="color: red;">Тогда</span>
            Параметр<span style="color: red;">.</span>Значение <span style="color: red;">=</span> ТекущийПараметр<span style="color: red;">.</span>Значение<span style="color: red;">;</span>
            Параметр<span style="color: red;">.</span>Использование <span style="color: red;">=</span> <span style="color: red;">Истина</span><span style="color: red;">;</span>
        <span style="color: red;">КонецЕсли</span><span style="color: red;">;</span>
    <span style="color: red;">КонецЦикла</span><span style="color: red;">;</span>
<span style="color: red;">КонецПроцедуры</span></code></pre>
Остановлюсь, что бы более подробно объяснить, что происходит. Функция СохранитьПараметры принимает на входе строку с именами тех параметров которые надо сохранить. Затем она находит по имени нужный параметр и сохраняет в структуру, которую возвращает по окончании перебора всех параметров полученых из строки. То же самое, только наоборот делает процедура загрузить, она принимает структуру и загружает из нее в СКД параметры. Далее надо собрать все вместе, выглядеть это будет примерно так:
<pre style="color: blue;"><code class="_1c8"><span style="color: red;">Функция</span> СохранитьПараметры<span style="color: red;">(</span>ИменаПараметров<span style="color: red;">)</span>
    Параметры <span style="color: red;">=</span> КомпоновщикНастроек<span style="color: red;">.</span>Настройки<span style="color: red;">.</span>ПараметрыДанных<span style="color: red;">;</span></br>
    МассивСИменами <span style="color: red;">=</span> ОбщегоНазначения<span style="color: red;">.</span>РазложитьСтрокуВМассивПодстрок<span style="color: red;">(</span>ИменаПараметров<span style="color: red;">,</span><span style="color: black;">","</span><span style="color: red;">)</span><span style="color: red;">;</span>
    СтруктураДляПараметров <span style="color: red;">=</span> <span style="color: red;">Новый</span> Структура<span style="color: red;">;</span>
    <span style="color: red;">Для</span> <span style="color: red;">Каждого</span> ИмяПараметра <span style="color: red;">Из</span> МассивСИменами <span style="color: red;">Цикл</span>
        Параметр <span style="color: red;">=</span> Параметры<span style="color: red;">.</span>НайтиЗначениеПараметра<span style="color: red;">(</span><span style="color: red;">Новый</span> ПараметрКомпоновкиДанных<span style="color: red;">(</span>ИмяПараметра<span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
        <span style="color: red;">Если</span> Параметр <span style="color: red;">&lt;</span><span style="color: red;">&gt;</span> <span style="color: red;">Неопределено</span> <span style="color: red;">Тогда</span>
            СтруктураДляПараметров<span style="color: red;">.</span>Вставить<span style="color: red;">(</span>ИмяПараметра<span style="color: red;">,</span> Параметр<span style="color: red;">.</span>Значение<span style="color: red;">)</span><span style="color: red;">;</span>
        <span style="color: red;">КонецЕсли</span><span style="color: red;">;</span>
    <span style="color: red;">КонецЦикла</span><span style="color: red;">;</span></br>
    <span style="color: red;">Возврат</span> СтруктураДляПараметров<span style="color: red;">;</span>
<span style="color: red;">КонецФункции</span></br>
<span style="color: red;">Процедура</span> ЗагрузитьПараметры<span style="color: red;">(</span>СтруктураСПараметрами<span style="color: red;">)</span>
    Параметры <span style="color: red;">=</span> КомпоновщикНастроек<span style="color: red;">.</span>Настройки<span style="color: red;">.</span>ПараметрыДанных<span style="color: red;">;</span></br>
    <span style="color: red;">Для</span> <span style="color: red;">Каждого</span> ТекущийПараметр <span style="color: red;">Из</span> СтруктураСПараметрами <span style="color: red;">Цикл</span>
        Параметр <span style="color: red;">=</span> Параметры<span style="color: red;">.</span>НайтиЗначениеПараметра<span style="color: red;">(</span><span style="color: red;">Новый</span> ПараметрКомпоновкиДанных<span style="color: red;">(</span>ТекущийПараметр<span style="color: red;">.</span>Ключ<span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
        <span style="color: red;">Если</span> Параметр <span style="color: red;">&lt;</span><span style="color: red;">&gt;</span> <span style="color: red;">Неопределено</span> <span style="color: red;">Тогда</span>
            Параметр<span style="color: red;">.</span>Значение <span style="color: red;">=</span> ТекущийПараметр<span style="color: red;">.</span>Значение<span style="color: red;">;</span>
            Параметр<span style="color: red;">.</span>Использование <span style="color: red;">=</span> <span style="color: red;">Истина</span><span style="color: red;">;</span>
        <span style="color: red;">КонецЕсли</span><span style="color: red;">;</span>
    <span style="color: red;">КонецЦикла</span><span style="color: red;">;</span>
<span style="color: red;">КонецПроцедуры</span></br>
<span style="color: red;">Процедура</span> СменитьСхему<span style="color: red;">(</span><span style="color: red;">)</span>
    СтруктураСНастройками <span style="color: red;">=</span> СохранитьПараметры<span style="color: red;">(</span><span style="color: black;">"Параметр1,Параметр2,Параметр3"</span><span style="color: red;">)</span><span style="color: red;">;</span>
    СхемаКомпоновкиДанных <span style="color: red;">=</span> ПолучитьМакет<span style="color: red;">(</span><span style="color: black;">"ЗдесьИмяНужнойВамСхемы"</span><span style="color: red;">)</span><span style="color: red;">;</span></br>
    Настройки <span style="color: red;">=</span> СхемаКомпоновкиДанных<span style="color: red;">.</span>НастройкиПоУмолчанию<span style="color: red;">;</span>
    КомпоновщикНастроек<span style="color: red;">.</span>ЗагрузитьНастройки<span style="color: red;">(</span>Настройки<span style="color: red;">)</span><span style="color: red;">;</span>
    ЗагрузитьПараметры<span style="color: red;">(</span>СтруктураСНастройками<span style="color: red;">)</span><span style="color: red;">;</span>
<span style="color: red;">КонецПроцедуры</span></code></pre>

##Вывод СКД в отчет
Если вы создали форму отчета у СКД(то есть если у вас отчет и есть схема компоновки данных), то по умолчанию на кнопке "Сформировать" висит предустанновленная команда "Сфрмировать", которая запустит текущую схему, но можно туда повесить свой обработчик, если нужно перед формированием сделать какие нибудь манипуляции, вот код который можно туда повесить:
<pre style="color: blue;"><code class="_1c8">КомпоновщикМакета<span style="color: red;">=</span><span style="color: red;">Новый</span> КомпоновщикМакетаКомпоновкиДанных<span style="color: red;">;</span>
МакетКомпоновкиДанных<span style="color: red;">=</span>КомпоновщикМакета<span style="color: red;">.</span><span style="color: red;">Выполнить</span><span style="color: red;">(</span>СхемаКомпоновкиДанных<span style="color: red;">,</span>КомпоновщикНастроек<span style="color: red;">.</span>Настройки<span style="color: red;">,</span>ДанныеРасшифровки<span style="color: red;">)</span><span style="color: red;">;</span>
ПроцессорКомпоновкиДанных<span style="color: red;">=</span><span style="color: red;">Новый</span> ПроцессорКомпоновкиДанных<span style="color: red;">;</span>
ПроцессорКомпоновкиДанных<span style="color: red;">.</span>Инициализировать<span style="color: red;">(</span>МакетКомпоновкиДанных<span style="color: red;">,</span><span style="color: red;">,</span>ДанныеРасшифровки<span style="color: red;">,</span><span style="color: red;">Истина</span><span style="color: red;">)</span><span style="color: red;">;</span>
ПроцессорВывода<span style="color: red;">=</span><span style="color: red;">Новый</span> ПроцессорВыводаРезультатаКомпоновкиДанныхВТабличныйДокумент<span style="color: red;">;</span>
ПроцессорВывода<span style="color: red;">.</span>УстановитьДокумент<span style="color: red;">(</span>ЭлементыФормы<span style="color: red;">.</span>Результат<span style="color: red;">)</span><span style="color: red;">;</span>
ПроцессорВывода<span style="color: red;">.</span>Вывести<span style="color: red;">(</span>ПроцессорКомпоновкиДанных<span style="color: red;">)</span><span style="color: red;">;</span></code></pre>
</font>ПроцессорВывода<font color=red>.</font>Вывести<font color=red>(</font>ПроцессорКомпоновкиДанных<font color=red>);</font></p></pre>
Если вы не понимаете, что вообще происходит, просто сделайте кнопку на форме, и засуньте в обработчик этот код, сразу станет понятно, что все просто и что в целом то даже процессом вывода можно управлять, например перед формированием отчета, можно установить заголовок, в зависимости от установленных параметров или свернуть группировки после формирования, или время там формирования засечь, всякое бывает. Также можно вывести разом, а можно построчно, посмотреть детали можно в синтаксис помощнике по адресу Общие объекты -> Система компоновки данных -> Работа с механизмом -> ПроцессорВыводаРезультатаКомпоновкиДанных
###Установка в качестве параметра списка значений.
Когда нужно использовать список значений, для параметра необходимо установить галочку "Доступен список значений" иначе, даже если на входе будет список, СКД все равно будет брать только первое значение, галочка вот здесь:
![Параметр в списке](http://i.imgur.com/1ENucxo.png)
С этой галочкой в штатном списке параметров СКД, вы бонусом получаете красивый и удобный список для подбора ваших значений.

###Вывод СКД в таблицу.
Бывает нужен, если нужно проанализировать или что то сделать с результатами работы, что бы получить результат работы  СКД в таблицу значений или в дерево значений, вам поможет следующий код:
<pre style="color: blue;"><code class="_1c8">КомпоновщикМакета<span style="color: red;">=</span><span style="color: red;">Новый</span> КомпоновщикМакетаКомпоновкиДанных<span style="color: red;">;</span>
МакетКомпоновкиДанных<span style="color: red;">=</span>КомпоновщикМакета<span style="color: red;">.</span><span style="color: red;">Выполнить</span><span style="color: red;">(</span>СхемаКомпоновкиДанных<span style="color: red;">,</span>КомпоновщикНастроек<span style="color: red;">.</span>Настройки<span style="color: red;">,</span><span style="color: red;">,</span><span style="color: red;">,</span>Тип<span style="color: red;">(</span><span style="color: black;">"ГенераторМакетаКомпоновкиДанныхДляКоллекцииЗначений"</span><span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
ПроцессорКомпоновкиДанных<span style="color: red;">=</span><span style="color: red;">Новый</span> ПроцессорКомпоновкиДанных<span style="color: red;">;</span>
ПроцессорКомпоновкиДанных<span style="color: red;">.</span>Инициализировать<span style="color: red;">(</span>МакетКомпоновкиДанных<span style="color: red;">)</span><span style="color: red;">;</span>
ТЗДляВывода <span style="color: red;">=</span> <span style="color: red;">Новый</span> ТаблицаЗначений<span style="color: red;">;</span><span style="color: green;">//здесь может быть и дерево значений</span>
ПроцессорВывода <span style="color: red;">=</span> <span style="color: red;">Новый</span> ПроцессорВыводаРезультатаКомпоновкиДанныхВКоллекциюЗначений<span style="color: red;">;</span>
ПроцессорВывода<span style="color: red;">.</span>УстановитьОбъект<span style="color: red;">(</span>ТЗДляВывода<span style="color: red;">)</span><span style="color: red;">;</span>
ПроцессорВывода<span style="color: red;">.</span>Вывести<span style="color: red;">(</span>ПроцессорКомпоновкиДанных<span style="color: red;">)</span><span style="color: red;">;</span></code></pre>собственно здесь в ТЗДляВывода мы получаем результат формирования отчета. Собственно если не касаться непосредствнно самого СКД, то здесь описаны практически все моменты работы с формой отчета построенного на СКД.
###Бонусы
Тому кто домучал до конца эту длинную повесть, пригодятся бонусы:
Курс от гилева про СКД, что бы не искать информацию про СКД, можно скачать [бесплатный курс по СКД](http://www.spec8.ru/kurs-po-skd-besplatno)
Можно взять [шаблон, в котором есть все нужные для оформления фичи](https://googledrive.com/host/0BxFnXEinPWUJckpLWkVCVjc0dUU/%D0%A8%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD.erf)
