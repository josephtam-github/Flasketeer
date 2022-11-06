$(function() {
    $(".navbar-toggler").on("click", function(e) {
        $(".edit-header").toggleClass("show");
        e.stopPropagation();
      });
    
      $("html").click(function(e) {
        var header = document.getElementById("edit-header");
    
        if (!header.contains(e.target)) {
          $(".edit-header").removeClass("show");
        }
      });
    
      $("#edit-nav .nav-link").click(function(e) {
        $(".edit-header").removeClass("show");
      });
});

function onButtonPress() {
    $('.alert').alert('close')
}

$(document).ready(function(){
    load_data();
    function load_data(query)
    {
        $.ajax({
            url:"/ajaxlivesearch",
            method:"POST",
            data:{query:query},
            success:function(data)
            {
                $('#result').html(data);
                $("#result").append(data.htmlresponse);
            }
        });
    }
    $('#search_text').keyup(function(){
        var search = $(this).val();
        if(search != ''){
            load_data(search);
        }else{
            load_data();
        }
    });
});