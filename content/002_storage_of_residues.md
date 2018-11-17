---
Title: Хранение остатков поставщика у себя в базе
date: 2012-09-05 21:09
Category: "Программирование"
Tags: Практика программирования 1С, Таблица значений, Запрос
---
 <!--more-->
В этой статье, я хотел бы рассказать об опыте настройки хранения остатков по складу поставщика. Почему именно об этом? Потому что, заодно мы рассмотрим:<ul><li>Механизм обработки в запросе таблицы значений. Что в целом может пригодиться.</li><li>Механизм формирования таблицы движений сразу в запросе.</li></ul>

Заказчиком было поставлено условие: изменение конфигурации, должно быть обоснованным и не происходить без надобности. Были найдены и рассмотрены следующие варианты:

 1. Добавление регистра в базу. Загрузка туда остатков, да и вообще всего что можно загрузить.
 2. Загрузка данных из экселя (Именно в этом формате поставщик хранит свои данные) каждый раз при открытии подбора в документ отгрузки.
 3. Создание нового склада, и загрузка данных туда корректирующим документом.

Первые два способа подразумевают модификацию обработки подбора в документ реализации  а один из них еще и добавление регистра, что само по себе не страшно конечно, но для заказчика не желательно. А во втором случае, надо каждый раз читать эксель, что тоже не очень хорошо. После [консультаций с комьюнити](http://www.forum.mista.ru/topic.php?id=619127), было выяснено, что вроде как все считают, что хранить  остатки у себя в базе нельзя, но почему, никто сказать не может. Решили остановиться на третьем варианте.

И так что мы будем делать:
1. Загрузим из подсунутого экселя остатки поставщика
2. Подсчитаем дельту, на которую надо скорректировать остатки.
3. Создадим документ «КоорректировкаЗаписейРегистраНакопления» и в него зальем движения.

Начинаем. Читаем эксель в таблицу значений.
<pre style="color: blue;"><code class="_1c8"><span style="color: red;">Функция</span> ПрочитатьЭксель<span style="color: red;">(</span><span style="color: red;">)</span>
    КСАртикул <span style="color: red;">=</span> <span style="color: red;">Новый</span> КвалификаторыСтроки<span style="color: red;">(<span style="color: black;">25</span></span><span style="color: red;">)</span><span style="color: red;">;</span>
    Массив <span style="color: red;">=</span> <span style="color: red;">Новый</span> Массив<span style="color: red;">;</span>
    Массив<span style="color: red;">.</span>Добавить<span style="color: red;">(</span>Тип<span style="color: red;">(</span><span style="color: black;">"Строка"</span><span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
    ОписаниеТиповАртикул <span style="color: red;">=</span> <span style="color: red;">Новый</span> ОписаниеТипов<span style="color: red;">(</span>Массив<span style="color: red;">,</span> <span style="color: red;">,</span> КСАртикул<span style="color: red;">)</span><span style="color: red;">;</span></br>
    Массив<span style="color: red;">.</span>Очистить<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
    КЧ <span style="color: red;">=</span> <span style="color: red;">Новый</span> КвалификаторыЧисла<span style="color: red;">(<span style="color: black;">10</span></span><span style="color: red;">)</span><span style="color: red;">;</span>
    Массив<span style="color: red;">.</span>Добавить<span style="color: red;">(</span>Тип<span style="color: red;">(</span><span style="color: black;">"Число"</span><span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
    ОписаниеТиповЧ <span style="color: red;">=</span> <span style="color: red;">Новый</span> ОписаниеТипов<span style="color: red;">(</span>Массив<span style="color: red;">,</span> <span style="color: red;">,</span> <span style="color: red;">,</span>КЧ<span style="color: red;">)</span><span style="color: red;">;</span></br>
    ТЗ <span style="color: red;">=</span> <span style="color: red;">Новый</span> ТаблицаЗначений<span style="color: red;">;</span>
    ТЗ<span style="color: red;">.</span>Колонки<span style="color: red;">.</span>Добавить<span style="color: red;">(</span><span style="color: black;">"Артикул"</span><span style="color: red;">,</span> ОписаниеТиповАртикул<span style="color: red;">)</span><span style="color: red;">;</span>
    ТЗ<span style="color: red;">.</span>Колонки<span style="color: red;">.</span>Добавить<span style="color: red;">(</span><span style="color: black;">"Количество"</span><span style="color: red;">,</span> ОписаниеТиповЧ<span style="color: red;">)</span><span style="color: red;">;</span></br>
    <span style="color: red;">Попытка</span>
        Excel <span style="color: red;">=</span> <span style="color: red;">Новый</span> COMОбъект<span style="color: red;">(</span><span style="color: black;">"Excel.Application"</span><span style="color: red;">)</span><span style="color: red;">;</span>
        Excel<span style="color: red;">.</span>WorkBooks<span style="color: red;">.</span>Open<span style="color: red;">(</span>ИмяФайла<span style="color: red;">)</span><span style="color: red;">;</span>
        Состояние<span style="color: red;">(</span><span style="color: black;">"Обработка файла Microsoft Excel"</span><span style="color: red;">)</span><span style="color: red;">;</span>
        ExcelЛист <span style="color: red;">=</span> Excel<span style="color: red;">.</span>Sheets<span style="color: red;">(<span style="color: black;">1</span></span><span style="color: red;">)</span><span style="color: red;">;</span>
    <span style="color: red;">Исключение</span>
        Сообщить<span style="color: red;">(</span><span style="color: black;">"Не удалось обработать файл!"</span><span style="color: red;">)</span><span style="color: red;">;</span>
        <span style="color: red;">Возврат</span> <span style="color: black;">""</span><span style="color: red;">;</span>
    <span style="color: red;">КонецПопытки</span><span style="color: red;">;</span></br>
    <span style="color: red;">Для</span> СтрокаЭксель <span style="color: red;">=</span> СтрокаНачало <span style="color: red;">По</span> СтрокаОкончание <span style="color: red;">Цикл</span>
        Прогресс <span style="color: red;">=</span> <span style="color: red;">(</span>СтрокаЭксель <span style="color: red;">/</span> СтрокаОкончание<span style="color: red;">)</span> <span style="color: red;">*</span> <span style="color: black;">100</span><span style="color: red;">;</span>
        ЭлементыФормы<span style="color: red;">.</span>СтрокаСтатуса<span style="color: red;">.</span>Заголовок <span style="color: red;">=</span> <span style="color: black;">"Считывается эксель в память "</span> <span style="color: red;">+</span> СтрокаЭксель <span style="color: red;">+</span> <span style="color: black;">" из "</span> <span style="color: red;">+</span> СтрокаОкончание<span style="color: red;">;</span></br>
        Зн <span style="color: red;">=</span> ExcelЛист<span style="color: red;">.</span>Cells<span style="color: red;">(</span>СтрокаЭксель<span style="color: red;">,</span> КолонкаАртикул<span style="color: red;">)</span><span style="color: red;">.</span>Text<span style="color: red;">;</span>
        АртикулВДокумент <span style="color: red;">=</span> СокрЛ<span style="color: red;">(</span>ExcelЛист<span style="color: red;">.</span>Cells<span style="color: red;">(</span>СтрокаЭксель<span style="color: red;">,</span> КолонкаАртикул<span style="color: red;">)</span><span style="color: red;">.</span>Text<span style="color: red;">)</span><span style="color: red;">;</span>
        КолвоВДокумент <span style="color: red;">=</span> СокрЛ<span style="color: red;">(</span>ExcelЛист<span style="color: red;">.</span>Cells<span style="color: red;">(</span>СтрокаЭксель<span style="color: red;">,</span> КолонкаКоличество<span style="color: red;">)</span><span style="color: red;">.</span>Text<span style="color: red;">)</span><span style="color: red;">;</span>
        КолвоВДокумент <span style="color: red;">=</span> <span style="color: red;">?</span><span style="color: red;">(</span>КолвоВДокумент <span style="color: red;">=</span> <span style="color: black;">""</span><span style="color: red;">,</span> <span style="color: black;">0</span><span style="color: red;">,</span> Число<span style="color: red;">(</span>КолвоВДокумент<span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span></br>
        НоваяСтрокаТЗ <span style="color: red;">=</span> ТЗ<span style="color: red;">.</span>Добавить<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
        НоваяСтрокаТЗ<span style="color: red;">.</span>Артикул <span style="color: red;">=</span> АртикулВДокумент<span style="color: red;">;</span>
        НоваяСтрокаТЗ<span style="color: red;">.</span>Количество <span style="color: red;">=</span> КолвоВДокумент<span style="color: red;">;</span>
    <span style="color: red;">КонецЦикла</span><span style="color: red;">;</span></br>
    Excel<span style="color: red;">.</span>WorkBooks<span style="color: red;">.</span>Close<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
    Excel <span style="color: red;">=</span> <span style="color: black;">0</span><span style="color: red;">;</span>
    <span style="color: red;">Возврат</span> ТЗ<span style="color: red;">;</span>
<span style="color: red;">КонецФункции</span> <span style="color: green;">// ПрочитатьЭксель()</span></code></pre>

Я читаю эксель в типизизрованную таблицу значений, потому что для обработки таблицы запросом она должна быть типизирована. На форме есть надпись с названием "СтрокаСтатуса" которая рассказывает про текущий ход загрузки данных из экселя. Так же есть поля ввода в которых лежат номера колонок где артикул номенклатуры а где количество. Здесь вроде все настолько просто, что даже не знаю что тут прокомментировать. Ну раз с первым моментом нам все ясно, перейдем к вычислению дельты которую надо грузить в регистр. Для начала, что бы обращаться к этой таблице в запросе, надо ее поместить во временную таблицу, это не очень сложно и делается с помощью вот такого кода:
<pre style="color: blue;"><code class="_1c8">ТЗЭксель <span style="color: red;">=</span> ПрочитатьЭксель<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
МВТ <span style="color: red;">=</span> <span style="color: red;">Новый</span> МенеджерВременныхТаблиц<span style="color: red;">;</span>
ТаблицаЭксель <span style="color: red;">=</span> <span style="color: red;">Новый</span> Запрос<span style="color: red;">;</span>
ТаблицаЭксель<span style="color: red;">.</span>МенеджерВременныхТаблиц <span style="color: red;">=</span> МВТ<span style="color: red;">;</span>
ТаблицаЭксель<span style="color: red;">.</span>Текст <span style="color: red;">=</span>
    <span style="color: black;">"Выбрать</span>
    <span style="color: black;">|   </span>
    <span style="color: black;">|ПОМЕСТИТЬ ДокЭксель</span>
    <span style="color: black;">|ИЗ</span>
    <span style="color: black;">|&amp;ТаблицаСДанными КАК Таблица"</span><span style="color: red;">;</span>
ТаблицаЭксель<span style="color: red;">.</span>УстановитьПараметр<span style="color: red;">(</span><span style="color: black;">"ТаблицаСДанными"</span><span style="color: red;">,</span> ТЗЭксель<span style="color: red;">)</span><span style="color: red;">;</span>
ТаблицаЭксель<span style="color: red;">.</span><span style="color: red;">Выполнить</span><span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span></code></pre>

Таблица есть, теперь перейдем к загрузке. Так как в экселе могут быть уже существующие записи или не быть тех которые есть в регистре, мы будем привязываться к справочнику номенклатура. Собственно вот он запрос:
<pre style="text-align: left; font-family: courier new,courier; color: black">
<font color=blue>ВЫБРАТЬ
    </font><font color=brown>ЕСТЬNULL</font><font color=blue>(</font>ТоварыНаСкладахОстатки.КоличествоОстаток<font color=blue>, </font><font color=#ff00ff>0</font><font color=blue>) КАК </font>ОстатокНаСкладе<font color=blue>,
    </font><font color=brown>ЕСТЬNULL</font><font color=blue>(</font>ДокЭксель.Количество<font color=blue>, </font><font color=#ff00ff>0</font><font color=blue>) КАК </font>КоличествоЭксель<font color=blue>,
    </font><font color=brown>ВЫБОР
        КОГДА ЕСТЬNULL</font><font color=blue>(</font>ДокЭксель.Количество<font color=blue>, </font><font color=#ff00ff>0</font><font color=blue>) - </font><font color=brown>ЕСТЬNULL</font><font color=blue>(</font>ТоварыНаСкладахОстатки.КоличествоОстаток<font color=blue>, </font><font color=#ff00ff>0</font><font color=blue>) < </font><font color=#ff00ff>0
            </font><font color=brown>ТОГДА </font><font color=#ff00ff>0 </font><font color=blue>- (</font><font color=brown>ЕСТЬNULL</font><font color=blue>(</font>ДокЭксель.Количество<font color=blue>, </font><font color=#ff00ff>0</font><font color=blue>) - </font><font color=brown>ЕСТЬNULL</font><font color=blue>(</font>ТоварыНаСкладахОстатки.КоличествоОстаток<font color=blue>, </font><font color=#ff00ff>0</font><font color=blue>))
        </font><font color=brown>ИНАЧЕ ЕСТЬNULL</font><font color=blue>(</font>ДокЭксель.Количество<font color=blue>, </font><font color=#ff00ff>0</font><font color=blue>) - </font><font color=brown>ЕСТЬNULL</font><font color=blue>(</font>ТоварыНаСкладахОстатки.КоличествоОстаток<font color=blue>, </font><font color=#ff00ff>0</font><font color=blue>)
    </font><font color=brown>КОНЕЦ </font><font color=blue>КАК </font><font color=brown>Количество</font><font color=blue>,
    </font><font color=#008b8b>&Склад</font><font color=blue>,
    </font>Товар.<font color=brown>Ссылка </font><font color=blue>КАК </font>Номенклатура<font color=blue>,
    </font><font color=brown>ЗНАЧЕНИЕ</font><font color=blue>(</font>Справочник.Качество.Новый<font color=blue>) КАК </font>Качество<font color=blue>,
    </font><font color=brown>ВЫБОР
        КОГДА ЕСТЬNULL</font><font color=blue>(</font>ДокЭксель.Количество<font color=blue>, </font><font color=#ff00ff>0</font><font color=blue>) - </font><font color=brown>ЕСТЬNULL</font><font color=blue>(</font>ТоварыНаСкладахОстатки.КоличествоОстаток<font color=blue>, </font><font color=#ff00ff>0</font><font color=blue>) > </font><font color=#ff00ff>0
            </font><font color=brown>ТОГДА ЗНАЧЕНИЕ</font><font color=blue>(</font>ВидДвиженияНакопления.Приход<font color=blue>)
        </font><font color=brown>ИНАЧЕ ЗНАЧЕНИЕ</font><font color=blue>(</font>ВидДвиженияНакопления.Расход<font color=blue>)
    </font><font color=brown>КОНЕЦ </font><font color=blue>КАК </font>ВидДвижения<font color=blue>,
    </font><font color=brown>ИСТИНА </font><font color=blue>КАК </font>Активность<font color=blue>,
    </font><font color=#008b8b>&Период</font><font color=blue>,
    </font><font color=#008b8b>&Док </font><font color=blue>КАК </font>Регистратор
<font color=blue>ИЗ
    </font>Справочник.Номенклатура <font color=blue>КАК </font>Товар
        <font color=blue>ЛЕВОЕ СОЕДИНЕНИЕ </font>РегистрНакопления.ТоварыНаСкладах.Остатки<font color=blue>(, </font>Склад <font color=blue>= </font><font color=#008b8b>&Склад</font><font color=blue>) КАК </font>ТоварыНаСкладахОстатки
        <font color=blue>ПО </font>Товар.<font color=brown>Ссылка </font><font color=blue>= </font>ТоварыНаСкладахОстатки.Номенклатура
        <font color=blue>ЛЕВОЕ СОЕДИНЕНИЕ </font>ДокЭксель <font color=blue>КАК </font>ДокЭксель
        <font color=blue>ПО </font>Товар.Артикул <font color=blue>= </font>ДокЭксель.Артикул
<font color=blue>ГДЕ
    </font>Товар.Артикул <font color=blue><> </font><font color=red>""</font></pre>
Не забываем, что для того что бы обратиться к временной таблице, нам надо указать менеджер временных таблиц:
<pre><p>Запрос<font color=red>.</font>МенеджерВременныхТаблиц <font color=red>= </font>МВТ<font color=red>;</font></p></pre>

`ЕСТЬNULL` нам гарантирует возврат числа в случае работы соединений, разницу мы получаем в строках с 4 по 8, строки с 9й по 19ю формируют значения для загрузки данных в регистр, собственно все почти готово. Осталось выгрузить результат в таблицу и удалить те значения которые грузить не надо(количество = 0) :
<pre style="color: blue;"><code class="_1c8">ДвиженияВДокумент <span style="color: red;">=</span> Запрос<span style="color: red;">.</span><span style="color: red;">Выполнить</span><span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">.</span>Выгрузить<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span><span style="color: green;">//"Склад,Номенклатура,Качество,Количество"</span>
НулевыеДвижения <span style="color: red;">=</span> ДвиженияВДокумент<span style="color: red;">.</span>НайтиСтроки<span style="color: red;">(</span><span style="color: red;">Новый</span> Структура<span style="color: red;">(</span><span style="color: black;">"Количество"</span><span style="color: red;">,<span style="color: black;">0</span></span><span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
<span style="color: red;">Для</span> <span style="color: red;">Каждого</span> СтрокаТаблицы <span style="color: red;">Из</span> НулевыеДвижения <span style="color: red;">Цикл</span>
    ДвиженияВДокумент<span style="color: red;">.</span>Удалить<span style="color: red;">(</span>СтрокаТаблицы<span style="color: red;">)</span><span style="color: red;">;</span>
<span style="color: red;">КонецЦикла</span><span style="color: red;">;</span></code></pre>
Создать документ корректировки и добавить строку в ТЧ которая укажет на регистр, это нужно для отображения документа и обеспечения возможности его редактировать.
<pre style="color: blue;"><code class="_1c8">НовыйДок <span style="color: red;">=</span> Документы<span style="color: red;">.</span>КорректировкаЗаписейРегистров<span style="color: red;">.</span>СоздатьДокумент<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
НовыйДок<span style="color: red;">.</span>Дата <span style="color: red;">=</span> ТекущаяДата<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
СтрокаТЧ <span style="color: red;">=</span> НовыйДок<span style="color: red;">.</span>ТаблицаРегистровНакопления<span style="color: red;">.</span>Добавить<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
СтрокаТЧ<span style="color: red;">.</span>Имя <span style="color: red;">=</span> <span style="color: black;">"ТоварыНаСкладах"</span><span style="color: red;">;</span>
СтрокаТЧ<span style="color: red;">.</span>Представление <span style="color: red;">=</span> <span style="color: black;">"Товары на складах"</span><span style="color: red;">;</span>
НовыйДок<span style="color: red;">.</span>Записать<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
НовыйДок <span style="color: red;">=</span> НовыйДок<span style="color: red;">.</span>Ссылка<span style="color: red;">;</span></code></pre>
И собственно загрузить данные в регистр
<pre style="color: blue;"><code class="_1c8">НаборВРегистр <span style="color: red;">=</span> РегистрыНакопления<span style="color: red;">.</span>ТоварыНаСкладах<span style="color: red;">.</span>СоздатьНаборЗаписей<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span>
НаборВРегистр<span style="color: red;">.</span>Отбор<span style="color: red;">.</span>Регистратор<span style="color: red;">.</span>Значение <span style="color: red;">=</span> НовыйДок<span style="color: red;">;</span>
НаборВРегистр<span style="color: red;">.</span>Загрузить<span style="color: red;">(</span>ДвиженияВДокумент<span style="color: red;">.</span>Скопировать<span style="color: red;">(</span><span style="color: red;">,</span><span style="color: black;">"Период,Регистратор,Активность,ВидДвижения,Склад,Номенклатура,Качество,Количество"</span><span style="color: red;">)</span><span style="color: red;">)</span><span style="color: red;">;</span>
НаборВРегистр<span style="color: red;">.</span>Записать<span style="color: red;">(</span><span style="color: red;">)</span><span style="color: red;">;</span></code></pre>
Как вы могли заметить документ мы уже не трогаем, его не надо, не записывать, не проводить, он просто является основанием для записи в регистр.
Собственно на этом все, внимательный читатель наверняка уже нашел ошибку а вы? ;)
Как обычно для тех кто дочитал или прокрутил до конца как обычно бонус: [Обработка про которую я рассказывал в этом посте.](https://googledrive.com/host/0BxFnXEinPWUJckpLWkVCVjc0dUU/ЗагрузкаВНовыйСклад.epf)
