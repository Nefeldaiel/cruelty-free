<html>
Brand List: 
<div id="div1">Loading...</div>
</html>
<script>
var source = "https://hidden-cosmos-182403.appspot.com/getsafeshopper"

function callback() {
    console.log('callback')
} 

$.ajax({
    url: source, 
    dataType: 'jsonp',
    // jsonp: 'callback',
    data: {
        message: 'Hello World in js'
    },
    success: function(result){
        $("#div1").html(result.message);
    },
    error: function(xhr) {
      alert('Error!!');
    }
});
</script>
