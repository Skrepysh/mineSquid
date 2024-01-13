# mineSquid
<p align="center">
  <img src="https://github.com/Skrepysh/mineSquid/blob/master/icon.jpg" width="350" title="mineSquid - modpack switcher for minecraft">
</p>
<p align="left">
  <img src="https://forthebadge.com/images/badges/made-with-python.svg" width="150" title="Python">
<img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FSkrepysh%2FmineSquid&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=HITS&edge_flat=false" width="120" title="Hits since 08.09.2023">
<img src="https://img.shields.io/badge/License-MIT-yellow.svg" width="95" title="MIT">
</p>
Проект, который поможет вам переключаться между модпаками в майнкрафте. Для этого закиньте все ваши модпаки в папку %appdata%/mineSquid/modpacks* (папка доступна с рабочего стола, ярлык - squidModpacks).<br />
\* - каждый модпак должен находиться в своей собственной папке (например:<br /> /../../minesquid/modpacks/modpack1,<br /> /../../minesquid/modpacks/modpack228,<br /> или /../../minesquid/modpacks/super-puper-modpack)<br />
------------------------------------------<br />
Начиная с версии 2.9 добавлены аргументы командной строки:<br />
<s>--mp [номер модпака] - этот аргумент позволит создавать ярлыки быстрой активации самых частых модпаков (узнать номер нужного пака можно запустив программу) (/.../.../mineSquid.exe --mp [номер модпака])</s>s> Не актуально!<br />
--mpname [ИМЯ модпака] - этот аргумент позволит создавать ярлыки быстрой активации самых частых модпаков ПО ИМЕНИ(узнать ИМЯ нужного пака можно запустив программу) (/.../.../mineSquid.exe --mpname "[ИМЯ модпака]")<br />
⚠️⚠️⚠️При использовании --mpname имя модпака должно быть в кавычках⚠️⚠️⚠️<br />
--mpnum [НОМЕР модпака] - этот аргумент позволит создавать ярлыки быстрой активации самых частых модпаков ПО НОМЕРУ(узнать НОМЕР нужного пака можно запустив программу) (/.../.../mineSquid.exe --mpnum[НОМЕР модпака])<br />
--restore - этот аргумент позволит быстро восстановить бэкап своих модов (/.../.../mineSquid.exe --restore)<br />
--h - получение помощи по всем аргументам командной строки (/.../.../mineSquid.exe --h)<br />
------------------------------------------<br />
<h3>Инструкция по установке:</h3>
<h4>Метод первый:</h4>
1. Установите программу с помощью winget:<br />
&nbsp;&nbsp;&nbsp;&nbsp;<code>winget install mineSquid</code><br />
2.ПРОФИТ!<br />

<h4>Метод второй:</h4>
1.Скачайте установщик<br />
2.Установите программу<br />
3.Запустите программу. Она автоматически создаст все необходимые для работы папки и откроет папку modpacks, если она пуста.<br />
4.ПРОФИТ<br />

⚠️⚠️⚠️ ВАЖНО! Если вы пользовались mineSquid, а потом установили старую версию до 2.12(pySelector), то при повторной установке новой версии модпаки перенесены не будут!!! Необходимо будет сделать это вручную\*!⚠️⚠️⚠️<br />
\* - старое место хранения данных - "%appdata%/pySelector", а новое - "%appdata%/mineSquid"
