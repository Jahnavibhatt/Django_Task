$(document).ready(function(){
   console.log("admin.js");


   $(".view").click(function(){
        var h = $(this).parent().siblings().removeClass("#bt");
        console.log(h)
        var k = $(this).parent().siblings().find("#id")
        console.log(k)
        console.log($(this).parent().siblings().find("#id").val())

      })

})

