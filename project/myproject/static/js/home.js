window.history.forward();

$(document).ready(function(){
    console.log('home.js')
     var arr = []
    $(".quan").change(function(){
//        console.log("getsvalue")
        var totalQuan = $('.quan').length
//        console.log("total quan --", totalQuan)
        var itemQuantity = this.value
         console.log("q -",this.value)
         arr.push(itemQuantity = this.value)
         console.log("the array",arr)
          var q_id = $(this).attr("id").split('_')
          $("#qun"+ q_id[1]).html(itemQuantity);

        console.log("----",$(this).attr("id"))
        var hello = $("quan").siblings()
        console.log("hello",hello)
        var splitQuanId = $(this).attr("id").split('_')
//        console.log("splitQuanId----",splitQuanId)
        var price = $("#price"+splitQuanId[1]).text()
//        console.log("p--",price,)
        var total = $("#total"+splitQuanId[1]).text()
           console.log("total---",total)
        temp = parseInt(price)*parseInt(itemQuantity);
//        console.log("temp---",temp)
        $("#total"+splitQuanId[1]).text(temp)
        var finalTotal = 0
        for(var i = 1; i <= parseInt(totalQuan); i++){
            total1 = $("#total"+i).text()
            console.log("total--"+i+"---",total1, typeof(total1))
            finalTotal = finalTotal + parseInt(total1)
//            console.log("finalTotal--",finalTotal, typeof(finalTotal))
        }
        var FTot = document.getElementById("finaltot");
        FTot.innerHTML = finalTotal;
//    $(".qulity").html(itemQuantity);
    })


    $(".order").click(function(e){
//        console.log("The paragraph was clicked.");
        var url = $(".order").attr("data-url")
        var id = $(".order").attr('id')
//        console.log('id--',id,url)
        var item_id = []
        console.log("item_id",item_id)
        var quntity_item = arr
        console.log("qun---",quntity_item)
//        var itemQuantity = []
        var finaltotal = $('#finaltot').text()
        for(var j=0; j< $(".item_id").length; j++){
//              item_id.push($(".item_id").attr("id"))
//              console.log(j,'---',$("#total"+(j+1)).text())
//             console.log('--id',$(".item_id")[j].id)
              if($("#total"+(j+1)).text() != '0'){
                console.log(item_id.push($(".item_id")[j].id))
//                console.log(item_id.push($(".item_id")[j].id))
              }

        }

         var total2 = 0
       $.ajax({

               url: url,
               type: "GET",
               data:{
                  'user_id': id,
                  'item_id': item_id,
                  'quntity_item': quntity_item,
                  'total': finaltotal
               },
              success: function (data) {
               $('#hello').html(data)
               $( "#home" ).remove()
               $('#pdf').remove()
               $('.total').remove()
               $( ".order" ).remove();
               $("#finaltot").remove();
               alert("Success");

              },
              error: function () {
                alert("Error")

            }
           });

      });

})

