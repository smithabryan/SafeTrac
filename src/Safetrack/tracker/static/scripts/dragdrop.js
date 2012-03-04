$(function() {
    var viewBlk = $('#viewBlk');
    var groupBlk = $('#groupBlk');
    
    $('li',$('#groupBlk')).draggable();
    
    groupBlk.droppable({
        accept: "#group li",
        activeClass: "highlightSelection",
        drop: function(event,ui) {
            //remove from ajax calls
        }
    viewBlk.droppable({
        accept: "#group li",
        activeClass: "highlightSelection",
        drop: function(event,ui) {
            //add to ajax calls
        }
    });
});