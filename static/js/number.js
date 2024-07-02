function onlyNumberInput()
{
		var key = event.which || event.keyCode;
		if (key && (key <= 47 || key >= 58) && key != 8) {
			event.preventDefault();
		}
}

$(function(){
  $("[name=number]").keypress( onlyNumberInput );
  $("[name=number]").focus();
})