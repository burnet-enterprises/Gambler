$(function  () {
  $("ol.example").sortable();
}
$("ol.simple_with_no_drop").sortable({
  group: 'no-drop',
  drop: false
});
$("ol.simple_with_no_drag").sortable({
  group: 'no-drop',
  drag: false
}); 
