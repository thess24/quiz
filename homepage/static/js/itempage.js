$(function() {


    $('.reply').click(function() {
        $('.reply-form').hide();
        $(this).next('.reply-form').toggle();
    });


function pieChartMaker(titles, counts){
        var r = Raphael($('#chart').get(0), 500, 400);
        pie = r.piechart(140, 200, 90, counts,{legend:titles});

        pie.hover(function () {
                this.sector.stop();
                this.sector.scale(1.1, 1.1, this.cx, this.cy);

                if (this.label) {
                    this.label[0].stop();
                    this.label[0].attr({ r: 7.5 });
                    this.label[1].attr({ "font-weight": 800 });
                }
            }, function () {
                this.sector.animate({ transform: 's1 1 ' + this.cx + ' ' + this.cy }, 500, "bounce");

                if (this.label) {
                    this.label[0].animate({ r: 5 }, 500, "bounce");
                    this.label[1].attr({ "font-weight": 400 });
                }
            });
    }


$('.input_id_name').hide();
$('.input_id_email').hide();
$('.input_id_url').hide();



    $('.favform').submit(function() { // catch the form's submit event
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: "POST", // GET or POST
            url: "/ajaxsave/", // the file to call
            context: this,  // so we can use this is success--its not auto passed on
            success: function(response) { // on success..
                $(this).find('span').toggleClass('makered');
            }
        });
        return false;
    });

    $('.ansform').submit(function() { 
        $.ajax({ 
            data: $(this).serialize(), 
            type: "POST", 
            url: "/ajaxanswer/", 
            context: this,  
            success: function(json) { 
              $(this).find('span').toggleClass('makered');
              console.log(json);
            }
        });
        return false;
    });


//Turns response into data
function jsontodicts(json_data){

    count=[]
    titles=[]

    for (var i in json_data) {
      count.push(json_data[i]);
      titles.push(i + '- %%.%');
    }

    return [count,titles];  
}

  var obj = jQuery.parseJSON('{{response|safe}}');
  var dicts = jsontodicts(obj);
  var titles = dicts[1];
  var counts = dicts[0];

  
pieChartMaker(titles,counts);



});