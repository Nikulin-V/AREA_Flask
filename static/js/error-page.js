//При движении мышью вызываем функцию, которая меняет положение фона
document.addEventListener("mousemove", function (e) { MoveBackground(e); });
 
function MoveBackground(e)
{
   //Рассчитываем, насколько далеко от начала оси находится курсор: 0 - 0, 0.5 - середина экрана,
   // 1 - ширина экрана (например, 1920)
   //Затем умножаем получившееся число на 30 - настолько будет сдвигаться фон
   //Например, если курсор находится посередине страницы (0.5), то при умножении получится 15
   //Далее отнимаем половину от 30, чтобы фон мог двигаться как влево, так и вправо
   let offsetX = (e.clientX / window.innerWidth * 30) - 15;
   let offsetY = (e.clientY / window.innerHeight * 10) + 5;
   const logo = document.getElementById("logo-background");
   const bg = document.getElementById("office-background");

   //Меняем положение фона
   logo.setAttribute("style", "background-position: " + offsetX + "px " + offsetY + "px;");
   bg.setAttribute("style", "background-position: " + -offsetX + "px " + -offsetY + "px;");
}
