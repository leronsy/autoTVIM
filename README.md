# autoTVIM
<p>Запускать через main.py</p>
<p>Параметры по умолчанию означают выполнение всех функций, выбор файла списка статей по умолчанию и отладку (запись изменений в новые файлы).</p>
<p>В "production" нужно только отключить debug main(debug=False)</p>
<p>Параметр c=True - исправление грамматики, синтаксиса и других мелких ошибок. Шаблоны исправления хранятся в dictionaries.py в correction_dict.</p>
<p>Параметр s=True - проверка и коррекция структуры файла, удаление лишнего и добавление блоков необходимых данных.</p>
<p>Параметр a=True - сборка файлов authors и referats исходя из данных в списке статей.</p>